"""Compare src output with the independently saved, accepted Notebook."""
from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASELINE = json.loads((ROOT/'tests/timeline/fixtures/resource-before-extraction.json').read_text())


def test_resource_calculation_works_without_plotting_dependency():
    script = '''
import importlib.abc
import sys
sys.path.insert(0, sys.argv[1])

class BlockMatplotlib(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'matplotlib' or fullname.startswith('matplotlib.'):
            raise ModuleNotFoundError('Matplotlib is unavailable')

sys.meta_path.insert(0, BlockMatplotlib())
from timeline.contracts import ResourceConfig
from timeline.resource_timeline import build_timeline, resource_rows, current_resource
from timeline.resource_timeline import plot_resources as exported_plot_resources
from timeline.plotting import plot_resources

assert exported_plot_resources is plot_resources
windows = build_timeline(ResourceConfig('headless', 42, ('Node-1',), (0,)))
assert len(resource_rows(windows)) == 1
assert current_resource(windows, 'Node-1', 0).status == 'UE_OCCUPIED'
assert 'matplotlib' not in sys.modules
try:
    plot_resources(windows)
except ModuleNotFoundError as error:
    assert 'Matplotlib is unavailable' in str(error)
else:
    raise AssertionError('Plotting must require Matplotlib')
'''
    result = subprocess.run([sys.executable, '-I', '-c', script, str(ROOT/'src')],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


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
