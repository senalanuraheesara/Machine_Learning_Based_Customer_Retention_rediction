"""Verify stored sklearn versions and published scores without refitting models."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import warnings
import joblib
import sklearn
from sklearn.base import BaseEstimator
from sklearn.exceptions import InconsistentVersionWarning
from verify_submission_docs import main as verify_scores

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    subprocess.run([sys.executable, '-m', 'pip', 'check'], check=True)
    expected = next(line.split('==')[1] for line in (ROOT / 'requirements-lock.txt').read_text().splitlines()
                    if line.startswith('scikit-learn=='))
    assert sklearn.__version__ == expected, (sklearn.__version__, expected)
    records = {}
    original = BaseEstimator.__setstate__
    versions = set()

    def capture_version(self, state):
        if '_sklearn_version' in state:
            versions.add(state['_sklearn_version'])
        return original(self, state)

    try:
        BaseEstimator.__setstate__ = capture_version
        with warnings.catch_warnings():
            warnings.simplefilter('error', InconsistentVersionWarning)
            for path in sorted((ROOT / 'outputs/final_four').glob('*.joblib')):
                versions.clear()
                joblib.load(path)
                assert versions == {expected}, (path.name, versions)
                records[path.name] = {'stored_sklearn_versions': sorted(versions),
                                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    finally:
        BaseEstimator.__setstate__ = original
    with warnings.catch_warnings():
        warnings.simplefilter('error', InconsistentVersionWarning)
        verify_scores()
    report = {'status': 'passed', 'python': platform.python_version(), 'platform': platform.platform(),
              'sklearn': sklearn.__version__, 'models': records,
              'checks': 'pip check, serialized estimator versions, 12 saved accuracy scores, fingerprints and selection',
              'scope': 'Fresh local virtual environment; not a separate physical computer or another operating system'}
    (ROOT / 'outputs/evidence/environment_verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
