"""Check documentation evidence without retraining or modifying model artifacts."""
from pathlib import Path
import csv
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))

def main():
    import joblib
    import numpy as np
    import pandas as pd
    from model_workflow import load_features, matrix, TARGET
    from sklearn.metrics import accuracy_score
    data, fingerprint = load_features(ROOT/'data/processed')
    folder = ROOT/'outputs/final_four'
    selection = json.loads((folder/'selection.json').read_text())
    assert fingerprint == selection['fingerprint']
    summary = pd.read_csv(folder/'accuracy_summary.csv')
    checked = []
    for _, row in summary.iterrows():
        bundle = joblib.load(folder/f'{row.Model}.joblib')
        assert bundle['metadata']['fingerprint'] == fingerprint
        assert bundle['metadata']['Threshold'] == row.Threshold
        for split, column in [('train','Training accuracy'),('validation','Validation accuracy'),('test','Test accuracy')]:
            part = data[data.split.eq(split)]
            measured = accuracy_score(part[TARGET],bundle['pipeline'].predict_proba(matrix(part))[:,1] >= row.Threshold)
            assert np.isclose(measured,row[column]), (row.Model,split,measured,row[column])
            checked.append({'Model':row.Model,'Split':split,'Accuracy':measured})
    comparison = pd.read_csv(folder/'model_comparison.csv')
    winner = comparison[comparison['Fit eligible']].sort_values(['Validation accuracy','CV accuracy','Model'],ascending=[False,False,True]).iloc[0].Model
    assert winner == selection['model']
    for split in ['train','validation','test']:
        part = data[data.split.eq(split)]
        print(split,len(part),'majority accuracy',max(part[TARGET].mean(),1-part[TARGET].mean()))
    docs = [ROOT/'START_HERE.md',*ROOT.glob('docs/*.md'),*ROOT.glob('outputs/**/*.md')]
    broken=[]
    for doc in docs:
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#'): continue
            dest = link.split('#')[0]
            if not (doc.parent/dest).exists(): broken.append((str(doc.relative_to(ROOT)),link))
    assert not broken, broken
    notebooks = list(ROOT.glob('notebooks/*.ipynb'))
    for path in notebooks:
        nb=json.loads(path.read_text(encoding='utf-8'))
        assert not any(o.get('output_type')=='error' for c in nb['cells'] for o in c.get('outputs',[])),path
    print('PASS: 12 model/split accuracy checks; final selection; fingerprints; Markdown links; nine active notebook error scans.')
    (ROOT/'outputs/evidence/documentation_verification.json').write_text(json.dumps({'fingerprint':fingerprint,'selected':winner,'accuracy_checks':checked,'markdown_files_checked':len(docs),'notebooks_scanned':len(notebooks),'note':'Saved pipelines rescored only; no fitting, CV rerun, or notebook execution.'},indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
