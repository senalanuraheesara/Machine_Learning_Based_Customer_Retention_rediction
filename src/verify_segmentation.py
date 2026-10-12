"""Check final segmentation exports against their source and saved notebook."""
from pathlib import Path
import json
import re
import pandas as pd
import numpy as np
import sklearn

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    source = pd.read_csv(ROOT / 'data/processed/customer_features.csv')
    folder = ROOT / 'outputs/segmentation'
    labels = pd.read_csv(folder / 'customer_segments_kmeans_k2.csv')
    assert labels.CustomerID.is_unique and labels.CustomerID.notna().all()
    assert set(labels.CustomerID) == set(source.CustomerID)
    assert labels.Cluster.isin([0, 1]).all()
    pd.testing.assert_frame_equal(labels, pd.read_csv(ROOT / 'data/processed/customer_segments.csv'))
    pd.testing.assert_frame_equal(labels[['CustomerID', 'inactive_in_outcome_window']], source[['CustomerID', 'inactive_in_outcome_window']])
    sizes = pd.read_csv(folder / 'cluster_sizes_k2.csv').set_index('Cluster')
    assert labels.groupby('Cluster').size().to_dict() == sizes.CustomerCount.to_dict() == {0: 1577, 1: 119}
    summary = pd.read_csv(folder / 'cluster_inactivity_summary_k2.csv').set_index('Cluster')
    observed = labels.groupby('Cluster').inactive_in_outcome_window
    assert observed.sum().to_dict() == summary.InactiveCount.to_dict()
    assert np.allclose(observed.mean(), summary.InactivityRate)
    metrics = pd.read_csv(folder / 'kmeans_cluster_comparison_v3.csv')
    assert metrics.loc[metrics.silhouette.idxmax(), 'k'] == 2
    assert np.isclose(metrics.iloc[0].silhouette, 0.6895172557757041)
    notebook = json.loads((ROOT / 'notebooks/04_segmentation.ipynb').read_text(encoding='utf-8'))
    for cell in notebook['cells']:
        assert '%pip' not in ''.join(cell['source'])
        if cell['cell_type'] == 'code':
            assert cell['execution_count'] is not None
            assert not any(o['output_type'] == 'error' for o in cell['outputs'])
    for path in [ROOT / 'START_HERE.md', *ROOT.glob('docs/*.md'), *ROOT.glob('outputs/**/*.md')]:
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' not in link and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).exists(), (path, link)
    result = {'status': 'passed', 'customers': len(labels), 'cluster_sizes': sizes.CustomerCount.to_dict(),
              'silhouette': float(metrics.iloc[0].silhouette), 'scikit_learn': sklearn.__version__,
              'numpy': np.__version__, 'pandas': pd.__version__,
              'checks': 'Executed notebook, assignment identity, source alignment, counts, outcomes, metrics and Markdown links'}
    (ROOT / 'outputs/evidence/segmentation_verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
