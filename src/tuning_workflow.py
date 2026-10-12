"""Reproducible training-only CV and optional tuning for the four final models.

Uses only supplied snapshots and final pipeline templates. Published models are
never overwritten. This explicit rerun protocol is not a reconstruction of every
historical experiment.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.model_selection import ParameterGrid, RandomizedSearchCV, StratifiedGroupKFold
from sklearn.metrics import accuracy_score
from threadpoolctl import threadpool_limits
from model_workflow import load_features, matrix, TARGET, MODEL_NAMES, regularized_refit
from accuracy_experiments import select_threshold

ROOT = Path(__file__).resolve().parents[1]
GRIDS = {
    'logistic_regression': {'model__C': [.001, .01, .1, 1, 10], 'model__class_weight': [None, 'balanced']},
    'decision_tree': {'model__max_depth': [2, 3, 4, 6], 'model__min_samples_leaf': [25, 30, 50, 100], 'model__ccp_alpha': [.001, .005, .01]},
    'random_forest': {'model__n_estimators': [200, 350], 'model__max_depth': [3, 4, 6, 8], 'model__min_samples_leaf': [20, 40, 60, 80], 'model__max_features': ['sqrt', .7, 1.]},
    'gradient_boosting': {'model__n_estimators': [60, 80, 120, 240], 'model__learning_rate': [.025, .05, .1], 'model__max_depth': [1, 2, 3], 'model__min_samples_leaf': [40, 60, 80, 120], 'model__subsample': [.7, 1.]},
}

def inputs(model, root=ROOT):
    data, fingerprint = load_features(root/'data/processed')
    bundle_path = root/'outputs/final_four'/f'{model}.joblib'
    bundle = joblib.load(bundle_path)
    if fingerprint != bundle['metadata']['fingerprint']:
        raise ValueError('Snapshot fingerprint differs from the final template; review data provenance first.')
    train = data[data.split.eq('train')].reset_index(drop=True)
    X, y = matrix(train), train[TARGET]
    folds = list(StratifiedGroupKFold(3, shuffle=True, random_state=42).split(X, y, train.CustomerID))
    for a, b in folds:
        assert not set(train.iloc[a].CustomerID) & set(train.iloc[b].CustomerID)
    provenance = dict(model=model, fingerprint=fingerprint, bundle_sha256=hashlib.sha256(bundle_path.read_bytes()).hexdigest(),
                      python=platform.python_version(), sklearn=sklearn.__version__, folds=3, fold_seed=42,
                      status='Newly computed diagnostic; clones fitted only on training folds',
                      limitation='Not nested CV or independent temporal validation; holdouts were reused during development.')
    return data, bundle, train, X, y, folds, provenance

def frozen_cv(model, root=ROOT, output=None):
    data, bundle, train, X, y, folds, provenance = inputs(model, root)
    rows=[]
    for fold, (a,b) in enumerate(folds,1):
        fitted=clone(bundle['pipeline']).fit(X.iloc[a], y.iloc[a])
        for threshold in sorted({.5,float(bundle['metadata']['Threshold'])}):
            rows.append(dict(fold=fold, threshold=threshold, training_rows=len(a), heldout_rows=len(b),
                training_customers=train.iloc[a].CustomerID.nunique(), heldout_customers=train.iloc[b].CustomerID.nunique(),
                train_accuracy=accuracy_score(y.iloc[a],fitted.predict_proba(X.iloc[a])[:,1]>=threshold),
                cv_accuracy=accuracy_score(y.iloc[b],fitted.predict_proba(X.iloc[b])[:,1]>=threshold)))
    result=pd.DataFrame(rows)
    destination=Path(output) if output else root/'outputs/evidence/cross_validation'
    destination.mkdir(parents=True,exist_ok=True)
    result.to_csv(destination/f'{model}_folds.csv',index=False)
    (destination/f'{model}_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    return result

def load_cv(model, root=ROOT):
    folder=root/'outputs/evidence/cross_validation'
    provenance=json.loads((folder/f'{model}_provenance.json').read_text())
    _, fingerprint=load_features(root/'data/processed')
    assert provenance['fingerprint']==fingerprint, 'CV evidence uses different data'
    assert provenance['bundle_sha256']==hashlib.sha256((root/'outputs/final_four'/f'{model}.joblib').read_bytes()).hexdigest(), 'CV evidence uses different model'
    return pd.read_csv(folder/f'{model}_folds.csv'),provenance

def tune(model, root=ROOT, n_iter=32, output=None):
    if n_iter < 1: raise ValueError('n_iter must be positive')
    data,bundle,train,X,y,folds,provenance=inputs(model,root)
    destination=Path(output) if output else root/'outputs/reproduction'/model
    destination=destination.resolve()
    published=(root/'outputs/final_four').resolve()
    if destination==published or published in destination.parents:
        raise ValueError('Reruns must not write into the published model directory')
    destination.mkdir(parents=True,exist_ok=True)
    # clone removes all fitted state, including imputation/scaling statistics.
    search=RandomizedSearchCV(clone(bundle['pipeline']), GRIDS[model],
        n_iter=min(n_iter,len(ParameterGrid(GRIDS[model]))), random_state=73,
        scoring={'accuracy':'accuracy'}, cv=folds, refit=False,
        return_train_score=True,n_jobs=1,error_score='raise')
    search.fit(X,y)
    results=pd.DataFrame(search.cv_results_)
    results.to_csv(destination/'search_results.csv',index=False)
    provenance.update(status='Newly computed tuning run; published models unchanged',search_seed=73,
                      n_iter=search.n_iter,parameter_grid=GRIDS[model],best_cv_accuracy=float(results.mean_test_accuracy.max()))
    baseline=max(y.mean(),1-y.mean())
    try:
        index=regularized_refit(search.cv_results_,baseline)
    except ValueError as error:
        provenance.update(eligible=False,reason=str(error))
        (destination/'run.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
        return results,provenance
    candidate=clone(bundle['pipeline']).set_params(**search.cv_results_['params'][index]).fit(X,y)
    validation=data[data.split.eq('validation')]
    probability=candidate.predict_proba(matrix(validation))[:,1]
    threshold,thresholds=select_threshold(validation[TARGET],probability)
    thresholds.to_csv(destination/'validation_thresholds.csv',index=False)
    validation_accuracy=accuracy_score(validation[TARGET],probability>=threshold)
    train_accuracy=accuracy_score(y,candidate.predict_proba(X)[:,1]>=threshold)
    provenance.update(selected_index=int(index),chosen_params=search.cv_results_['params'][index],
        selected_cv_accuracy=float(results.iloc[index].mean_test_accuracy),threshold=threshold,
        validation_accuracy=validation_accuracy,train_validation_gap=train_accuracy-validation_accuracy,
        eligible=bool(train_accuracy-validation_accuracy<=.05),
        note='Training-CV candidate with validation threshold only. No test scoring, automatic promotion or cross-family selection; repeat/threshold-matched audit required before promotion.')
    joblib.dump(dict(pipeline=candidate,metadata=provenance),destination/'candidate.joblib')
    (destination/'run.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    return results,provenance

def historical_search(model,root=ROOT):
    path=root/'outputs/evidence/optimization'/f'updated_optimized_{model}_search.csv'
    results=pd.read_csv(path)
    data,_=load_features(root/'data/processed')
    y=data.loc[data.split.eq('train'),TARGET]
    index=regularized_refit(results,max(y.mean(),1-y.mean()))
    return results,index

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',choices=MODEL_NAMES+['all'],default='all')
    parser.add_argument('--mode',choices=['cv','tune'],default='cv')
    parser.add_argument('--n-iter',type=int,default=32)
    args=parser.parse_args()
    with threadpool_limits(limits=2):
        for name in MODEL_NAMES if args.model=='all' else [args.model]:
            if args.mode=='cv':
                scores=frozen_cv(name)
                print(name,scores.groupby('threshold').cv_accuracy.mean().to_dict(),flush=True)
            else:
                _,record=tune(name,n_iter=args.n_iter)
                print(name,json.dumps(record,indent=2),flush=True)
