"""Clean classical-ML selection; test scores are calculated only after freezing selection."""
from pathlib import Path
import json
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedGroupKFold, cross_validate
from sklearn.model_selection import ParameterGrid
from threadpoolctl import threadpool_limits
from model_workflow import paths, load_features, matrix, TARGET, SEED, regularized_refit, metrics, evaluation_model_names
from accuracy_experiments import candidates, make_pipeline, preparation, select_threshold


def run(root):
    root = Path(root)
    p = paths(root)
    out = root / 'outputs/clean_optimization'
    out.mkdir(parents=True, exist_ok=True)
    data, fingerprint = load_features(p['processed'])
    train = data[data.split.eq('train')]
    val = data[data.split.eq('validation')]
    X, y = matrix(train), train[TARGET]
    Xv, yv = matrix(val), val[TARGET]
    baseline = max(y.mean(), 1-y.mean())
    folds = list(StratifiedGroupKFold(3, shuffle=True, random_state=SEED).split(X, y, train.CustomerID))
    repeat = list(StratifiedGroupKFold(3, shuffle=True, random_state=137).split(X, y, train.CustomerID))
    for a, b in folds + repeat:
        assert not set(train.iloc[a].CustomerID) & set(train.iloc[b].CustomerID)
    protocol = dict(fingerprint=fingerprint, seed=SEED, search_iterations=32,
        selection='Highest validation accuracy among eligible models; exact ties use CV accuracy then name',
        controls='Train-CV and train-validation gaps <= 5pp; both CV means >= training majority + 3pp; search capacity loss <= 1pp',
        limitations='Repeated CV is a stability screen, not nested CV. Validation and test have been reused; confirm on fresh future data.')
    (out/'protocol.json').write_text(json.dumps(protocol, indent=2))
    rows, models = [], {}

    def record(name, model, cv_train, cv_acc, best_cv, seconds):
        scores = cross_validate(model, X, y, cv=repeat, scoring='accuracy', return_train_score=True, n_jobs=2, error_score='raise')
        threshold, _ = select_threshold(yv, model.predict_proba(Xv)[:, 1])
        tr = metrics(name, y, model.predict_proba(X)[:, 1], threshold)['Accuracy']
        va = metrics(name, yv, model.predict_proba(Xv)[:, 1], threshold)['Accuracy']
        ra = float(scores['test_score'].mean())
        rg = float((scores['train_score']-scores['test_score']).mean())
        reasons = []
        if cv_train-cv_acc > .05 or rg > .05: reasons.append('Overfitting warning: CV gap')
        if tr-va > .05: reasons.append('Temporal generalization gap')
        if min(cv_acc, ra) < baseline+.03: reasons.append('Possible underfitting or weak signal')
        if best_cv-cv_acc > .0100000001: reasons.append('Excessive regularization warning')
        if not np.isfinite([tr, va, cv_train, cv_acc, ra, rg, best_cv]).all(): reasons.append('Invalid evidence')
        rows.append({'Model':name, 'Training accuracy':tr, 'Validation accuracy':va,
            'CV accuracy':cv_acc, 'CV gap':cv_train-cv_acc, 'Repeated CV accuracy':ra,
            'Repeated CV gap':rg, 'Threshold':threshold, 'Eligible':not reasons,
            'Fit diagnosis':'; '.join(reasons) or 'Passes screening; not proof of zero fitting risk',
            'Training seconds':seconds})
        models[name] = model
        joblib.dump(model, out/f'{name}.joblib')
        print(name, 'validation=', round(va, 4), 'eligible=', not reasons, flush=True)

    # Reassess every existing model under the same threshold grid and stability rules.
    for name in evaluation_model_names(p):
        meta = json.loads((p['models']/f'{name}.json').read_text())
        if meta['fingerprint'] != fingerprint: raise ValueError('Stale model: '+name)
        results = pd.read_csv(p['tables']/f'{name}_cv.csv')
        record(name, joblib.load(p['models']/f'{name}.joblib'), meta['cv_train_accuracy'],
               meta['cv_accuracy'], results.mean_test_accuracy.max(), meta['training_seconds'])

    spaces = list(candidates())
    spaces.append(('optimized_gradient_boosting', make_pipeline(GradientBoostingClassifier(random_state=SEED)), {
        'prepare':[preparation(True), preparation(False)], 'model__n_estimators':[60,120,240],
        'model__learning_rate':[.025,.05,.1], 'model__max_depth':[1,2,3],
        'model__min_samples_leaf':[40,80,120], 'model__subsample':[.7,1.0]}))
    failures = {}
    for family, pipeline, space in spaces:
        name = 'updated_'+family
        print('SEARCH', name, flush=True)
        start = time.perf_counter()
        search = RandomizedSearchCV(pipeline, space, n_iter=min(32,len(ParameterGrid(space))),
            scoring={'accuracy':'accuracy'}, refit=False, cv=folds, n_jobs=2,
            random_state=73, return_train_score=True, error_score='raise')
        search.fit(X,y)
        results = pd.DataFrame(search.cv_results_)
        results.to_csv(out/f'{name}_search.csv', index=False)
        try:
            i = regularized_refit(search.cv_results_, baseline)
        except ValueError as error:
            failures[name] = str(error)
            continue
        model = pipeline.set_params(**search.cv_results_['params'][i]).fit(X,y)
        r = results.iloc[i]
        record(name, model, r.mean_train_accuracy, r.mean_test_accuracy,
               results.mean_test_accuracy.max(), time.perf_counter()-start)
    comparison = pd.DataFrame(rows)
    comparison.to_csv(out/'validation_comparison.csv', index=False)
    (out/'rejected_searches.json').write_text(json.dumps(failures, indent=2))
    eligible = comparison[comparison.Eligible].sort_values(['Validation accuracy','CV accuracy','Model'], ascending=[False,False,True])
    if eligible.empty: raise ValueError('No eligible model; no unsafe fallback published.')
    winner = eligible.iloc[0]
    selection = dict(model=winner.Model, threshold=float(winner.Threshold), protocol=protocol)
    # Persist frozen selection BEFORE any test prediction or label scoring.
    (out/'selection.json').write_text(json.dumps(selection, indent=2))
    joblib.dump({'pipeline':models[winner.Model], 'selection':selection}, out/'best_model_bundle.joblib')
    test = data[data.split.eq('test')]
    for row in rows:
        result = metrics(row['Model'], test[TARGET], models[row['Model']].predict_proba(matrix(test))[:,1], row['Threshold'])
        row['Test accuracy'] = result['Accuracy']
        row['Test F1'] = result['F1']
        row['Train-test gap'] = row['Training accuracy']-result['Accuracy']
        row['Selected'] = row['Model']==winner.Model
    summary = pd.DataFrame(rows).sort_values(['Selected','Validation accuracy'], ascending=[False,False])
    summary.to_csv(out/'all_models_accuracy.csv', index=False)
    display = summary[['Model','Training accuracy','Validation accuracy','Test accuracy','CV gap','Eligible','Selected']].copy()
    for column in ['Training accuracy','Validation accuracy','Test accuracy','CV gap']:
        display[column] = display[column].map(lambda v:f'{100*v:.2f}%')
    report = '# Clean optimization results\n\nSelected model: **'+winner.Model+'**. Selection uses validation accuracy after fitting screens, never test rank.\n\n'
    report += display.to_markdown(index=False)
    report += '\n\nAll existing candidates were reassessed; seven model families were searched with up to 32 configurations each. Every model uses the same validation threshold grid. No model is forced to win.\n\n'
    report += protocol['limitations']+' A small gap does not establish absence of underfitting or overfitting. Training accuracy is in-sample. Test scores are descriptive reused-holdout results. Earlier deployment artifacts remain historical; use the bundle in this folder for this run.\n'
    report += '\nHistorical results use previously chosen thresholds and are not directly identical operating points. This run uses a common coarser threshold grid; do not interpret a changed score as a change in the fitted estimator alone. No guaranteed accuracy improvement is claimed.\n'
    (out/'RESULTS.md').write_text(report, encoding='utf-8')
    print('SELECTED', winner.Model, flush=True)
    print(display.to_string(index=False), flush=True)


if __name__ == '__main__':
    with threadpool_limits(limits=2):
        run(Path(__file__).resolve().parents[1])
    from joblib.externals.loky import get_reusable_executor
    get_reusable_executor().shutdown(wait=True, kill_workers=True)
