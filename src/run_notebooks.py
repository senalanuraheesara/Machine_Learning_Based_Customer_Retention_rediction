"""Execute project notebooks with the current Python environment, saving real outputs."""
from pathlib import Path
import argparse
import os
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('notebooks',nargs='*')
    args=parser.parse_args()
    # The final deliverable supersedes historical experiment notebooks.
    names=args.notebooks or ['03_05_model_comparison_selection.ipynb','FINAL_Four_Optimized_Models.ipynb']
    os.environ['MPLBACKEND']='module://matplotlib_inline.backend_inline'
    os.environ['OMP_NUM_THREADS']='2'
    for name in names:
        path=ROOT/'notebooks'/name
        print('RUN',name,flush=True)
        nb=nbformat.read(path,as_version=4)
        nb.cells.append(nbformat.v4.new_code_cell(
            'from joblib.externals.loky import get_reusable_executor\n'
            'get_reusable_executor().shutdown(wait=True, kill_workers=True)'))
        manager=KernelManager(kernel_name='python3')
        manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
        client=NotebookClient(nb,timeout=1800,km=manager,resources={'metadata':{'path':str(ROOT)}})
        try:
            client.execute()
        finally:
            nb.cells.pop()  # Execution-only worker cleanup is not teaching content.
            nbformat.write(nb,path)
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        print('OK',name,flush=True)
