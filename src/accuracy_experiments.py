"""Bounded classical-ML experiment. No test scoring during fitting/selection."""
from pathlib import Path
import json
import time
import numpy as np
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder, SplineTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, VotingClassifier
from sklearn.kernel_approximation import Nystroem
from sklearn.model_selection import RandomizedSearchCV, StratifiedGroupKFold, cross_validate
from model_workflow import FEATURES, TARGET, MODEL_NAMES, SEED, matrix, load_features, paths, signed_log1p, metrics, regularized_refit

COMPACT = ['positive_recency_days','positive_invoice_count','positive_order_value',
           'days_overdue','orders_30d','orders_60d','orders_90d','order_trend',
           'history_days','purchase_interval_cv','return_rate','product_diversity']
DERIVED = ['recent_order_share','recent_spend_share','order_rate','active_month_fraction',
           'recent_order_change','recent_order_value','spend_per_product']
MAX_CV_GAP = .05
MAX_TEMPORAL_GAP = .08
N_SEARCH = 24

class BehaviorFeatures(BaseEstimator, TransformerMixin):
    """Deterministic past-feature interactions; no fitted or target-derived values."""
    def fit(self,X,y=None): return self
    def transform(self,X):
        out=X.copy()
        out['recent_order_share']=out.orders_30d/(out.orders_90d+1)
        out['recent_spend_share']=out.spend_30d/(out.spend_90d+1)
        out['order_rate']=out.positive_invoice_count/(out.history_days.clip(lower=30)/30)
        out['active_month_fraction']=out.active_months/(out.history_days.clip(lower=30)/30)
        out['recent_order_change']=2*out.orders_30d-out.orders_60d
        out['recent_order_value']=out.spend_30d/(out.orders_30d+1)
        out['spend_per_product']=out.monetary_total/(out.product_diversity+1)
        return out.replace([np.inf,-np.inf],np.nan)

def preparation(compact=False,linear=False):
    numeric=COMPACT if compact else [x for x in FEATURES if x!='country']+DERIVED
    steps=[('impute',SimpleImputer(strategy='median',keep_empty_features=True))]
    if linear:
        steps += [('log',FunctionTransformer(signed_log1p,feature_names_out='one-to-one')),('scale',StandardScaler())]
    return ColumnTransformer([('numeric',Pipeline(steps),numeric),
        ('country',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),
                            ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),['country'])])

def make_pipeline(estimator,linear=False):
    return Pipeline([('features',BehaviorFeatures()),('prepare',preparation(linear=linear)),('model',estimator)])

def guarded_refit(results,baseline_accuracy):
    return regularized_refit(results,baseline_accuracy)

def candidates():
    linear_preps=[preparation(compact=x,linear=True) for x in [True,False]]
    tree_preps=[preparation(compact=x) for x in [True,False]]
    yield 'optimized_logistic_regression',make_pipeline(LogisticRegression(max_iter=3000,random_state=SEED),True),{
        'prepare':linear_preps,'model__C':[.001,.01,.1,1,10], 'model__class_weight':[None,'balanced']}
    spline=make_pipeline(LogisticRegression(max_iter=3000,random_state=SEED),True)
    spline.steps.insert(2,('spline',SplineTransformer(n_knots=3,degree=2,extrapolation='linear')))
    yield 'spline_logistic_regression',spline,{'prepare':[preparation(True,True)],'spline__n_knots':[3,4,5],
        'model__C':[.01,.1,1,10],'model__class_weight':[None,'balanced']}
    kernel=make_pipeline(LogisticRegression(max_iter=3000,random_state=SEED),True)
    kernel.steps.insert(2,('kernel',Nystroem(n_components=100,random_state=SEED)))
    yield 'kernel_logistic_regression',kernel,{'prepare':[preparation(True,True)],'kernel__gamma':[.005,.02,.08,.2],
        'model__C':[.1,1,10,100],'model__class_weight':[None,'balanced']}
    yield 'optimized_decision_tree',make_pipeline(DecisionTreeClassifier(random_state=SEED)),{
        'prepare':tree_preps,'model__max_depth':[2,3,4,6], 'model__min_samples_leaf':[25,50,100],
        'model__ccp_alpha':[.001,.005,.01],'model__class_weight':[None,'balanced']}
    yield 'optimized_random_forest',make_pipeline(RandomForestClassifier(n_estimators=200,n_jobs=1,random_state=SEED)),{
        'prepare':tree_preps,'model__max_depth':[3,4,6,8],'model__min_samples_leaf':[20,40,80],
        'model__max_features':['sqrt',.7,1.0],'model__class_weight':[None,'balanced']}
    yield 'hist_gradient_boosting',make_pipeline(HistGradientBoostingClassifier(early_stopping=False,random_state=SEED)),{
        'prepare':tree_preps,'model__max_iter':[75,150,250],'model__learning_rate':[.025,.05,.1],
        'model__max_leaf_nodes':[3,7,15], 'model__min_samples_leaf':[30,60,100], 'model__l2_regularization':[1,10,50]}

def select_threshold(y,prob):
    # Coarser grid than the previous .01 search to reduce validation threshold flexibility.
    rows=pd.DataFrame([metrics('candidate',y,prob,t) for t in np.linspace(.25,.65,17)])
    rows['distance']=abs(rows.Threshold-.5)
    chosen=rows.sort_values(['Accuracy','distance','Threshold'],ascending=[False,True,True]).iloc[0]
    return float(chosen.Threshold),rows

def run(root):
    root=Path(root); p=paths(root)
    out=root/'outputs/accuracy_optimization'; out.mkdir(exist_ok=True)
    data,fingerprint=load_features(p['processed'])
    # Test features/labels are never passed to any fit, search, threshold or selection here.
    train=data[data.split.eq('train')]; validation=data[data.split.eq('validation')]
    X,y=matrix(train),train[TARGET]; Xv,yv=matrix(validation),validation[TARGET]
    folds=list(StratifiedGroupKFold(n_splits=3,shuffle=True,random_state=SEED).split(X,y,train.CustomerID))
    for a,b in folds: assert not set(train.iloc[a].CustomerID)&set(train.iloc[b].CustomerID)
    baseline=max(y.mean(),1-y.mean())
    protocol={'seed':SEED,'n_search_per_family':N_SEARCH,'folds':3,'max_cv_gap':MAX_CV_GAP,
        'max_train_validation_gap':MAX_TEMPORAL_GAP,'minimum_cv_gain_over_majority':.03,
        'selection':'highest validation accuracy among eligible candidates; incumbent wins exact ties',
        'test_policy':'do not score test until selection is frozen; reused holdout',
        'fingerprint':fingerprint}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2))
    incumbent=json.loads((p['models']/'selection.json').read_text())
    if incumbent.get('optimization_protocol'):
        incumbent=json.loads((out/'incumbent_selection.json').read_text())
    else:
        (out/'incumbent_selection.json').write_text(json.dumps(incumbent,indent=2))
    rows=[]; fitted={}

    def record_candidate(name,model,cv_train,cv_acc,cv_ap,cv_std,cv_gap_std,seconds,params):
        tp=model.predict_proba(X)[:,1]; vp=model.predict_proba(Xv)[:,1]
        cutoff,thresholds=select_threshold(yv,vp)
        training=metrics(name,y,tp,cutoff); val=metrics(name,yv,vp,cutoff)
        cv_gap=cv_train-cv_acc; temporal_gap=training['Accuracy']-val['Accuracy']
        eligible=cv_gap<=MAX_CV_GAP and temporal_gap<=MAX_TEMPORAL_GAP and cv_acc>=baseline+.03
        metadata=dict(model=name,fingerprint=fingerprint,training_seconds=seconds,cv_accuracy=cv_acc,
            cv_train_accuracy=cv_train,cv_ap=cv_ap,cv_ap_std=cv_std,cv_accuracy_std=cv_gap_std,
            threshold=cutoff,best_params=params,optimization_eligible=bool(eligible),
            diagnosis='No large fitting gap; no clear severe-underfitting signal' if eligible else 'Rejected by predefined fitting/stability screen')
        joblib.dump(model,p['models']/f'{name}.joblib')
        (p['models']/f'{name}.json').write_text(json.dumps(metadata,indent=2,default=str))
        thresholds.to_csv(p['tables']/f'{name}_thresholds.csv',index=False)
        vout=validation[['row_id','CustomerID','prediction_date']].copy()
        vout['actual']=yv.to_numpy(); vout['probability']=vp
        vout.to_csv(p['tables']/f'{name}_validation_predictions.csv',index=False)
        pd.DataFrame([dict(metrics(name,y,tp),Split='train'),dict(metrics(name,yv,vp),Split='validation')]).to_csv(p['tables']/f'{name}_metrics.csv',index=False)
        rows.append({'Model':name,'Training accuracy':training['Accuracy'],'Validation accuracy':val['Accuracy'],
            'CV accuracy':cv_acc,'CV train accuracy':cv_train,'CV gap':cv_gap,'Train-validation gap':temporal_gap,
            'Threshold':cutoff,'Eligible':bool(eligible)})
        print(rows[-1],flush=True)
        fitted[name]=model

    for name,pipeline,space in candidates():
        print('SEARCH',name,flush=True); start=time.perf_counter()
        from sklearn.model_selection import ParameterGrid
        search=RandomizedSearchCV(pipeline,space,n_iter=min(N_SEARCH,len(ParameterGrid(space))),
            scoring={'accuracy':'accuracy','ap':'average_precision'},refit=lambda results: regularized_refit(results,baseline),
            cv=folds,n_jobs=2,random_state=SEED,return_train_score=True,error_score='raise')
        search.fit(X,y)
        results=pd.DataFrame(search.cv_results_); results.to_csv(p['tables']/f'{name}_cv.csv',index=False)
        r=results.iloc[search.best_index_]
        record_candidate(name,search.best_estimator_,float(r.mean_train_accuracy),float(r.mean_test_accuracy),
            float(r.mean_test_ap),float(r.std_test_ap),float(r.std_test_accuracy),time.perf_counter()-start,search.best_params_)

    # Fixed equal weights; member selection uses training CV only, not validation/test.
    shortlist=pd.DataFrame(rows)
    safe=shortlist[(shortlist['CV gap']<=MAX_CV_GAP)&(shortlist['CV accuracy']>=baseline+.03)]
    members=safe.sort_values('CV accuracy',ascending=False).head(3).Model.tolist()
    if len(members)>=2:
        print('FIT equal-weight soft voting:',members,flush=True); start=time.perf_counter()
        vote=VotingClassifier([(name,clone(fitted[name])) for name in members],voting='soft',n_jobs=1)
        scores=cross_validate(vote,X,y,cv=folds,scoring={'accuracy':'accuracy','ap':'average_precision'},
                              return_train_score=True,n_jobs=2,error_score='raise')
        vote.fit(X,y)
        record_candidate('soft_voting',vote,float(scores['train_accuracy'].mean()),float(scores['test_accuracy'].mean()),
            float(scores['test_ap'].mean()),float(scores['test_ap'].std()),float(scores['test_accuracy'].std()),
            time.perf_counter()-start,{'members':members,'weights':'equal'})
        pd.DataFrame([{'mean_test_accuracy':scores['test_accuracy'].mean(),
            'mean_train_accuracy':scores['train_accuracy'].mean()}]).to_csv(p['tables']/'soft_voting_cv.csv',index=False)

    # Include the original four models as benchmarks; their settings are already fixed.
    for name in MODEL_NAMES:
        rec=json.loads((p['models']/f'{name}.json').read_text())
        model=joblib.load(p['models']/f'{name}.joblib')
        train_acc=metrics(name,y,model.predict_proba(X)[:,1],rec['threshold'])['Accuracy']
        val_acc=metrics(name,yv,model.predict_proba(Xv)[:,1],rec['threshold'])['Accuracy']
        cv_gap=rec['cv_train_accuracy']-rec['cv_accuracy']
        rows.append({'Model':name,'Training accuracy':train_acc,'Validation accuracy':val_acc,
            'CV accuracy':rec['cv_accuracy'],'CV train accuracy':rec['cv_train_accuracy'],'CV gap':cv_gap,
            'Train-validation gap':train_acc-val_acc,'Threshold':rec['threshold'],
            'Eligible':bool(cv_gap<=MAX_CV_GAP and train_acc-val_acc<=MAX_TEMPORAL_GAP and rec['cv_accuracy']>=baseline+.03)})
    comparison=pd.DataFrame(rows)
    eligible=comparison[comparison.Eligible].copy()
    eligible['incumbent_priority']=(eligible.Model!=incumbent['model']).astype(int)
    winner=eligible.sort_values(['Validation accuracy','incumbent_priority','CV gap'],ascending=[False,True,True]).iloc[0]
    selected_name=winner.Model
    # Learning curves for every new model, using whole-customer subsamples.
    for name,model in fitted.items():
        records=[]
        for fold,(a,b) in enumerate(folds):
            customers=np.asarray(train.iloc[a].CustomerID.unique(),dtype=object).copy(); np.random.default_rng(SEED+fold).shuffle(customers)
            for fraction in [.35,.65,1.0]:
                chosen=set(customers[:max(2,int(len(customers)*fraction))])
                subset=a[train.iloc[a].CustomerID.isin(chosen).to_numpy()]
                estimator=clone(model).fit(X.iloc[subset],y.iloc[subset])
                records.append({'fraction':fraction,'fold':fold,'rows':len(subset),
                    'train_accuracy':estimator.score(X.iloc[subset],y.iloc[subset]),
                    'cv_accuracy':estimator.score(X.iloc[b],y.iloc[b])})
        pd.DataFrame(records).to_csv(p['tables']/f'{name}_learning_curve.csv',index=False)
    comparison.to_csv(out/'validation_comparison.csv',index=False)
    record=json.loads((p['models']/f'{selected_name}.json').read_text())
    selection=dict(incumbent,model=selected_name,threshold=record['threshold'],
        model_rule=protocol['selection'],refit=False,optimization_protocol=protocol,
        selection_change='Bounded classical ML optimization requested after prior holdout inspection; use fresh future data for confirmation')
    (out/'selection.json').write_text(json.dumps(selection,indent=2))
    (out/'candidate_names.json').write_text(json.dumps(MODEL_NAMES+list(fitted),indent=2))
    print('FROZEN WINNER:',selected_name,flush=True)
    return comparison,selection

if __name__=='__main__':
    from threadpoolctl import threadpool_limits
    # Import by stable module name so serialized custom transformers remain loadable.
    from accuracy_experiments import run as experiment_run
    with threadpool_limits(limits=2): experiment_run(Path(__file__).resolve().parents[1])
    from joblib.externals.loky import get_reusable_executor
    get_reusable_executor().shutdown(wait=True,kill_workers=True)
