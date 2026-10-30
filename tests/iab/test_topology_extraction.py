"""正式模組必須重現人工接受前Notebook的實際輸出。"""
from dataclasses import asdict, replace
import json
from pathlib import Path
import sys
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
BASELINE = json.loads((ROOT / 'tests/iab/fixtures/topology-before-extraction.json').read_text())


@pytest.mark.parametrize('case', BASELINE['cases'], ids=['default', 'minimum', 'custom', 'different-seed'])
def test_python_module_preserves_accepted_notebook_snapshot_and_tables(case):
    from iab.topology import build_topology, example_config, topology_tables

    config = replace(example_config(case['seed']), zone_tag_counts=tuple(case['counts']),
                     zone_outer_radii_m=tuple(case['radii']), min_tags_per_node=case['minimum'])
    snapshot = build_topology(config)
    # JSON正規化僅用於比較tuple與已保存JSON陣列；沒有重算預期結果。
    assert json.loads(json.dumps(asdict(snapshot))) == case['snapshot']
    assert json.loads(json.dumps(topology_tables(snapshot))) == case['tables']


@pytest.mark.parametrize('working_dir', ['.', 'notebooks', 'tests/iab'])
def test_notebook_imports_src_modules_without_preconfigured_pythonpath(working_dir):
    notebook = json.loads((ROOT / 'notebooks/01_iab_topology.ipynb').read_text())
    imports = next(''.join(cell['source']) for cell in notebook['cells']
                   if cell['cell_type'] == 'code')
    check = "\nassert example_config().seed == 42\nassert Path(sys.modules['iab.topology'].__file__).resolve() == project_root / 'src/iab/topology.py'\n"
    result = subprocess.run([sys.executable, '-I', '-c', imports + check],
                            cwd=ROOT / working_dir, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_notebook_explains_when_started_outside_project(tmp_path):
    notebook = json.loads((ROOT / 'notebooks/01_iab_topology.ipynb').read_text())
    imports = next(''.join(cell['source']) for cell in notebook['cells']
                   if cell['cell_type'] == 'code')
    result = subprocess.run([sys.executable, '-I', '-c', imports],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode != 0
    assert '找不到 src/iab' in result.stderr
    assert 'ModuleNotFoundError' not in result.stderr
