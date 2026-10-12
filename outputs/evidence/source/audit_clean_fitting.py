"""Audit frozen models at their deployed thresholds; never tune using test scores."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import accuracy_score
from threadpoolctl import threadpool_limits
from model_workflow import paths, load_features, matrix, TARGET


def run():
    root = Path(__file__).resolve().parents[1]
    out = root/'outputs/clean_optimization'
    summary = pd.read_csv(out/'all_models_accuracy.csv')
    selection = json.loads((out/'selection.json').read_text())
    data, fingerprint = load_features(paths(root)['processed'])
    assert fingerprint == selection['protocol']['fingerprint']
    train = data[data.split.eq('train')]
    X, y = matrix(train), train[TARGET]
    baseline = max(y.mean(),1-y.mean())
    folds = list(StratifiedGroupKFold(3, shuffle=True, random_state=137).split(X,y,train.CustomerID))
    rows, curves = [], []
    for _, row in summary.iterrows():
        model = joblib.load(out/f'{row.Model}.joblib')
        scores = []
        for fold,(a,b) in enumerate(folds):
            assert not set(train.iloc[a].CustomerID)&set(train.iloc[b].CustomerID)
            fitted = clone(model).fit(X.iloc[a],y.iloc[a])
            ta = accuracy_score(y.iloc[a],fitted.predict_proba(X.iloc[a])[:,1]>=row.Threshold)
            va = accuracy_score(y.iloc[b],fitted.predict_proba(X.iloc[b])[:,1]>=row.Threshold)
            scores.append((ta,va))
            if row.Model == selection['model']:
                curves.append(dict(Fold=fold,Fraction=1.0,Rows=len(a),Training=ta,CV=va))
                customers = np.asarray(train.iloc[a].CustomerID.unique(), dtype=object).copy()
                np.random.default_rng(137+fold).shuffle(customers)
                for fraction in [.35,.65]:
                    chosen = customers[:max(2,int(len(customers)*fraction))]
                    subset = a[train.iloc[a].CustomerID.isin(chosen).to_numpy()]
                    small = clone(model).fit(X.iloc[subset],y.iloc[subset])
                    curves.append(dict(Fold=fold,Fraction=fraction,Rows=len(subset),
                        Training=accuracy_score(y.iloc[subset],small.predict_proba(X.iloc[subset])[:,1]>=row.Threshold),
                        CV=accuracy_score(y.iloc[b],small.predict_proba(X.iloc[b])[:,1]>=row.Threshold)))
        mean_train,mean_cv = np.mean(scores,axis=0)
        gap = mean_train-mean_cv
        temporal = row['Training accuracy']-row['Validation accuracy']
        warnings = []
        if max(gap,row['CV gap'],row['Repeated CV gap'],temporal)>.05:
            warnings.append('Overfitting/generalization warning: training gap exceeds 5pp')
        if min(mean_cv,row['CV accuracy'],row['Repeated CV accuracy'])<baseline+.03:
            warnings.append('Possible underfitting or weak signal: CV within 3pp of majority baseline')
        rows.append(dict(Model=row.Model,Threshold=row.Threshold,
            **{'Threshold-matched CV train accuracy':mean_train,'Threshold-matched CV accuracy':mean_cv,
               'Threshold-matched CV gap':gap,'Train-validation gap':temporal,
               'Train-test gap (descriptive only)':row['Train-test gap'],
               'Assessment':'; '.join(warnings) or 'No strong fitting warning under current screening rules',
               'Pass':not warnings}))
        print(row.Model, 'matched CV gap:',round(100*gap,2),'pp', 'warnings:',warnings,flush=True)
    audit = pd.DataFrame(rows)
    audit.to_csv(out/'fitting_audit.csv',index=False)
    pd.DataFrame(curves).to_csv(out/'selected_learning_curve.csv',index=False)
    winner = audit.set_index('Model').loc[selection['model']]
    report = '# Frozen-model fitting audit\n\n'
    report += 'Selected model: **'+selection['model']+'**. '+winner.Assessment+'.\n\n'
    display = audit.copy()
    for c in display.columns:
        if 'accuracy' in c or 'gap' in c: display[c] = display[c].map(lambda v:f'{100*v:.2f}%')
    report += display.to_markdown(index=False)
    report += '\n\nThe previous CV scores used the default 0.50 threshold. This additional audit evaluates each frozen deployment threshold on customer-disjoint training folds. Thresholds were selected on validation, so this is a diagnostic, not a nested unbiased performance estimate. No test outcomes affect fitting or selection.\n\n'
    report += 'The 5pp gap and baseline-plus-3pp rules are heuristics, not statistical guarantees. A modest positive gap is expected and does not require automatic retraining. Existing regularization, depth/leaf limits, grouped CV, and pipeline-fitted preprocessing remain active. Repeated use of validation/test can cause selection overfitting that these gaps cannot exclude. Confirm on new future data.\n\n'
    report += 'Selected model learning curve (frozen threshold):\n\n'+pd.DataFrame(curves).groupby('Fraction')[['Training','CV']].mean().to_markdown()+'\n'
    (out/'FITTING_AUDIT.md').write_text(report,encoding='utf-8')
    if not winner['Pass']:
        raise ValueError('Selected model fails diagnostic: review before use. No automatic test-driven replacement.')


if __name__ == '__main__':
    with threadpool_limits(limits=2): run()
