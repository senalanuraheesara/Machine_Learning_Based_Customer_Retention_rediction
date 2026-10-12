"""Validate the documented 32-trial rerun and unchanged published bundles."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    before = json.loads((ROOT / 'outputs/evidence/model_hashes_before_rerun.json').read_text())
    rows = []
    for model, count in [('logistic_regression', 10), ('decision_tree', 32),
                         ('random_forest', 32), ('gradient_boosting', 32)]:
        folder = ROOT / 'outputs/reproduction' / model
        record = json.loads((folder / 'run.json').read_text())
        trials = pd.read_csv(folder / 'search_results.csv')
        assert len(trials) == record['n_iter'] == count
        assert trials[[f'split{i}_test_accuracy' for i in range(3)]].notna().all().all()
        path = ROOT / 'outputs/final_four' / f'{model}.joblib'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == before[path.name] == record['bundle_sha256']
        if 'selected_index' in record:
            assert (folder / 'candidate.joblib').exists()
            assert (folder / 'validation_thresholds.csv').exists()
        rows.append({key: record.get(key) for key in ['model', 'n_iter', 'best_cv_accuracy',
                    'selected_cv_accuracy', 'validation_accuracy', 'threshold', 'eligible']})
    report = {'status': 'passed', 'total_configurations': 106, 'cv_fits': 318,
              'published_models_unchanged': True, 'results': rows,
              'scope': 'Complete documented randomized rerun, not exhaustive grid or exact historical replay; no test scoring'}
    (ROOT / 'outputs/evidence/full_tuning_verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
