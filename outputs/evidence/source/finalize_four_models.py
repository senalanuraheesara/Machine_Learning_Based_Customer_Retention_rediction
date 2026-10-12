"""Package one validation-selected optimized variant per requested model family."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import nbformat
from model_workflow import paths, load_features, matrix, TARGET, metrics

root=Path(__file__).resolve().parents[1]
source=root/'outputs/clean_optimization'
if not source.exists(): source=root/'outputs/archive/clean_optimization'
out=root/'outputs/final_four'
out.mkdir(exist_ok=True)
validation=pd.read_csv(source/'validation_comparison.csv')
audit=pd.read_csv(source/'fitting_audit.csv').set_index('Model')
families={
    'logistic_regression':['logistic_regression','optimized_logistic_regression','updated_optimized_logistic_regression'],
    'decision_tree':['decision_tree','optimized_decision_tree','updated_optimized_decision_tree'],
    'random_forest':['random_forest','optimized_random_forest','updated_optimized_random_forest'],
    'gradient_boosting':['gradient_boosting','updated_optimized_gradient_boosting']}
data,fingerprint=load_features(paths(root)['processed'])
chosen=[]
for family,names in families.items():
    candidates=validation[validation.Model.isin(names)&validation.Eligible].copy()
    candidates=candidates[candidates.Model.map(audit['Pass'])]
    if candidates.empty: raise ValueError('No eligible candidate for '+family)
    row=candidates.sort_values(['Validation accuracy','CV accuracy','Model'],ascending=[False,False,True]).iloc[0]
    chosen.append(dict(Model=family,Source=row.Model,Threshold=float(row.Threshold),
        **{'Validation accuracy':row['Validation accuracy'],'CV accuracy':row['CV accuracy'],
           'Threshold-matched CV gap':audit.loc[row.Model,'Threshold-matched CV gap']}))
winner=sorted(chosen,key=lambda r:(-r['Validation accuracy'],-r['CV accuracy'],r['Model']))[0]['Model']
selection=dict(model=winner,fingerprint=fingerprint,
    rule='Highest validation accuracy among fitting-eligible variants within each family, then across the four families; exact ties use CV accuracy and name.',
    limitations='Validation and test were previously inspected. Scores are reused-holdout results; no guarantee of zero fitting risk.',
    variants=chosen)
(out/'selection.json').write_text(json.dumps(selection,indent=2))
rows=[]
for record in chosen:
    model=joblib.load(source/f"{record['Source']}.joblib")
    metadata=dict(record,fingerprint=fingerprint,selected=record['Model']==winner)
    # Exactly four model files; each bundles the pipeline and its prediction threshold.
    joblib.dump(dict(pipeline=model,metadata=metadata),out/f"{record['Model']}.joblib")
    row=dict(record)
    for split,label in [('train','Training accuracy'),('validation','Validation accuracy'),('test','Test accuracy')]:
        part=data[data.split.eq(split)]
        measured=metrics(record['Model'],part[TARGET],model.predict_proba(matrix(part))[:,1],record['Threshold'])
        if split=='validation': assert np.isclose(measured['Accuracy'],record[label])
        row[label]=measured['Accuracy']
    row['Train-test gap']=row['Training accuracy']-row['Test accuracy']
    row['Selected']=record['Model']==winner
    row['Fit assessment']='Passes current screens; not proof of zero fitting risk'
    rows.append(row)
summary=pd.DataFrame(rows)
summary.to_csv(out/'accuracy_summary.csv',index=False)
display=summary[['Model','Training accuracy','Validation accuracy','Test accuracy','Threshold-matched CV gap','Selected']].copy()
for c in display.columns:
    if 'accuracy' in c or 'gap' in c: display[c]=display[c].map(lambda x:f'{100*x:.2f}%')
(out/'README.md').write_text('# Final four optimized models\n\nSelected: **'+winner+'**.\n\n'+display.to_markdown(index=False)+'\n\nEach of the four joblib files contains `pipeline` and `metadata`, including the frozen threshold. Predict with `pipeline.predict_proba(X)[:, 1] >= metadata["Threshold"]`; `pipeline.predict()` uses a different default threshold. Features must follow `src/model_workflow.py`. Keep `src` importable when loading. Only load trusted model files.\n\nThese models already include optimization and regularization. Variants were chosen using validation scores and fitting checks, not test ranking. The standard GradientBoostingClassifier family is retained; histogram boosting, spline/kernel variants and ensembles are excluded from this final deliverable.\n\n'+selection['limitations']+'\n',encoding='utf-8')
nb=nbformat.v4.new_notebook(cells=[
    nbformat.v4.new_markdown_cell('# Final four optimized models\n\nLogistic Regression, Decision Tree, Random Forest and Gradient Boosting. Each family retains its strongest eligible validation variant. Training/test accuracy is reported at its frozen threshold. All models pass the current fitting screens; this does not guarantee absence of overfitting or underfitting.'),
    nbformat.v4.new_code_cell("from pathlib import Path\nimport sys, json\nimport pandas as pd\nimport joblib\nroot=Path.cwd()\nif root.name=='notebooks': root=root.parent\nsys.path.insert(0,str(root/'src'))\nfolder=root/'outputs/final_four'\nselection=json.loads((folder/'selection.json').read_text())\nprint('Selected model:',selection['model'])\nsummary=pd.read_csv(folder/'accuracy_summary.csv')\ndisplay(summary.style.format({c:'{:.2%}' for c in summary.columns if 'accuracy' in c or 'gap' in c}))"),
    nbformat.v4.new_code_cell("from model_workflow import paths,load_features,matrix,TARGET,metrics\nimport numpy as np\ndata,fingerprint=load_features(paths(root)['processed'])\nassert fingerprint==selection['fingerprint']\nfor _,row in summary.iterrows():\n    bundle=joblib.load(folder/f'{row.Model}.joblib')\n    for split,column in [('train','Training accuracy'),('validation','Validation accuracy'),('test','Test accuracy')]:\n        part=data[data.split.eq(split)]\n        probabilities=bundle['pipeline'].predict_proba(matrix(part))[:,1]\n        accuracy=metrics(row.Model,part[TARGET],probabilities,bundle['metadata']['Threshold'])['Accuracy']\n        assert np.isclose(accuracy,row[column])\nprint('Verified all four saved models against reported train, validation and test accuracy.')"),
    nbformat.v4.new_code_cell("selected=joblib.load(folder/f\"{selection['model']}.joblib\")\nprint('Prediction threshold:',selected['metadata']['Threshold'])\nprint(selection['limitations'])"),
    nbformat.v4.new_markdown_cell('Optimization uses fold-fitted preprocessing, regularization and customer-disjoint cross-validation. Fitting screens limit mean training–CV and training–validation gaps to 5 percentage points and require CV improvement over the majority baseline. Older experiments are historical; use only this notebook and `outputs/final_four` for the final four-model comparison.')])
nb.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
nbformat.write(nb,root/'notebooks/FINAL_Four_Optimized_Models.ipynb')
print(display.to_string(index=False))
