"""Build and verify a submission ZIP without environments or Python caches."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {'.git', '.venv', '.segmentation-venv', '.repro-venv', '.repro-check', 'venv', '__pycache__', '.ipynb_checkpoints', '.pytest_cache'}

if __name__ == '__main__':
    destination = ROOT / 'submission.zip'
    files = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and not (set(p.relative_to(ROOT).parts) & EXCLUDE)
                   and p.suffix.lower() not in {'.pyc', '.pyo', '.zip'}
                   and p.name != 'cleanup_segmentation.py')
    with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    with ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert not any(set(Path(n).parts) & EXCLUDE or n.endswith(('.pyc', '.pyo')) for n in archive.namelist())
    print(f'Created {destination} with {len(files)} files; integrity and exclusions verified.')
