"""正式模組必須重現人工接受前Notebook的實際輸出。"""
from dataclasses import asdict, replace
import json
from pathlib import Path
import sys

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
