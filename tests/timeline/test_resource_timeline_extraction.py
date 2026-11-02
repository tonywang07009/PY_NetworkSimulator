"""Compare src output with the independently saved, accepted Notebook."""
from dataclasses import asdict
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASELINE = json.loads((ROOT/'tests/timeline/fixtures/resource-before-extraction.json').read_text())


@pytest.mark.parametrize('expected_case', BASELINE['cases'], ids=lambda case: str(case['seed']))
def test_extracted_core_matches_accepted_snapshots_rows_and_observations(expected_case):
    original_path = sys.path.copy()
    sys.path.insert(0, str(ROOT/'src'))
    try:
        from timeline.contracts import ResourceConfig
        from timeline.resource_timeline import build_timeline, current_resource, resource_rows

        config = ResourceConfig(BASELINE['scenario_id'], expected_case['seed'],
                                tuple(BASELINE['node_ids']), tuple(BASELINE['starts']))
        windows = build_timeline(config)
        actual = {'seed': config.seed, 'windows': [asdict(window) for window in windows],
                  'rows': resource_rows(windows),
                  'observations': [asdict(current_resource(windows, 'Node-1', observation['now_ns']))
                                   for observation in expected_case['observations']]}
        assert json.loads(json.dumps(actual, allow_nan=False)) == expected_case
    finally:
        sys.path[:] = original_path
