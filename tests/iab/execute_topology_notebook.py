"""用當前Python啟動獨立kernel；不安裝或註冊使用者層級kernel。"""
from pathlib import Path
import importlib.metadata
import json
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager


def main():
    root = Path(__file__).resolve().parents[2]
    path = root / 'notebooks/01_iab_topology.ipynb'
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    with tempfile.TemporaryDirectory(prefix='pynet-kernel-') as directory:
        scratch = Path(directory)
        kernel_root = scratch / 'kernels'
        kernel = kernel_root / 'pynet-topology'
        kernel.mkdir(parents=True)
        spec = {'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                'display_name': 'Python (IAB topology)', 'language': 'python',
                'env': {'MPLBACKEND': 'Agg', 'MPLCONFIGDIR': str(scratch / 'mpl'),
                        'IPYTHONDIR': str(scratch / 'ipython')}}
        (kernel / 'kernel.json').write_text(json.dumps(spec), encoding='utf-8')
        manager = KernelManager(
            kernel_name='pynet-topology', connection_file=str(scratch / 'connection.json'),
            kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel_root)]),
        )
        try:
            NotebookClient(notebook, km=manager, timeout=120,
                           resources={'metadata': {'path': str(root)}}, record_timing=False).execute(cleanup_kc=True)
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        if manager.has_kernel:
            raise RuntimeError('Notebook kernel未關閉')
    nbformat.validate(notebook)
    code = [cell for cell in notebook.cells if cell.cell_type == 'code']
    if any(cell.execution_count is None for cell in code):
        raise RuntimeError('Notebook包含未執行的程式cell')
    if any(output.output_type == 'error' for cell in code for output in cell.outputs):
        raise RuntimeError('Notebook包含執行錯誤')
    # 只有完整執行成功，才更新供人工閱讀的Notebook。
    nbformat.write(notebook, path)
    report = {'python': sys.executable, 'version': sys.version, 'code_cells': len(code),
              'execution_counts': [cell.execution_count for cell in code], 'errors': 0, 'kernel_shutdown': True,
              'packages': {name: importlib.metadata.version(name)
                           for name in ('nbformat', 'nbclient', 'ipykernel', 'matplotlib')},
              'notebook': str(path.relative_to(root))}
    receipt = root / 'AgentDoc/openspec/changes/add-iab-topology-notebook/notebook-execution.json'
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
