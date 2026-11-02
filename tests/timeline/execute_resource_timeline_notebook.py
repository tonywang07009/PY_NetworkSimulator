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
    project_root = Path(__file__).resolve().parents[2]
    notebook_path = project_root / 'notebooks/03_resource_timeline.ipynb'
    notebook = nbformat.read(notebook_path, as_version=4)
    nbformat.validate(notebook)
    with tempfile.TemporaryDirectory(prefix='pynet-kernel-') as directory:
        scratch_directory = Path(directory)
        kernel_root = scratch_directory / 'kernels'
        kernel_directory = kernel_root / 'pynet-resource'
        kernel_directory.mkdir(parents=True)
        kernel_spec = {'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                'display_name': 'Python (resource timeline prototype)', 'language': 'python',
                'env': {'MPLBACKEND': 'Agg', 'MPLCONFIGDIR': str(scratch_directory / 'mpl'),
                        'IPYTHONDIR': str(scratch_directory / 'ipython')}}
        (kernel_directory / 'kernel.json').write_text(json.dumps(kernel_spec), encoding='utf-8')
        kernel_manager = KernelManager(
            kernel_name='pynet-resource', connection_file=str(scratch_directory / 'connection.json'),
            kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel_root)]),
        )
        try:
            NotebookClient(notebook, km=kernel_manager, timeout=120,
                           resources={'metadata': {'path': str(project_root)}}, record_timing=False).execute(cleanup_kc=True)
        finally:
            if kernel_manager.has_kernel:
                kernel_manager.shutdown_kernel(now=True)
        if kernel_manager.has_kernel:
            raise RuntimeError('Notebook kernel未關閉')
    nbformat.validate(notebook)
    code_cells = [notebook_cell for notebook_cell in notebook.cells if notebook_cell.cell_type == 'code']
    if any(notebook_cell.execution_count is None for notebook_cell in code_cells):
        raise RuntimeError('Notebook包含未執行的程式cell')
    if any(cell_output.output_type == 'error' for notebook_cell in code_cells for cell_output in notebook_cell.outputs):
        raise RuntimeError('Notebook包含執行錯誤')
    # 只有完整執行成功，才更新供人工閱讀的Notebook。
    nbformat.write(notebook, notebook_path)
    report = {'python': sys.executable, 'version': sys.version, 'code_cells': len(code_cells),
              'execution_counts': [notebook_cell.execution_count for notebook_cell in code_cells], 'errors': 0, 'kernel_shutdown': True,
              'packages': {package_name: importlib.metadata.version(package_name)
                           for package_name in ('nbformat', 'nbclient', 'ipykernel', 'matplotlib', 'numpy', 'scipy')},
              'notebook': str(notebook_path.relative_to(project_root))}
    receipt = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/pynet-resource-execution.json')
    receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
