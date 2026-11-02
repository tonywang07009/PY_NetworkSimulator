"""Behavior checks at the resource Notebook's public boundary."""
from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import random
import sys
import types

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebooks/03_resource_timeline.ipynb'


@pytest.fixture(scope='module', params=['notebook', 'python-module'])
def api(request):
    original_path = sys.path.copy()
    if request.param == 'python-module':
        sys.path.insert(0, str(ROOT / 'src'))
        try:
            from timeline import contracts, resource_timeline, plotting
            yield types.SimpleNamespace(**(vars(contracts) | vars(resource_timeline) | vars(plotting)))
        finally:
            sys.path[:] = original_path
        return

    module = types.ModuleType('resource_notebook_under_test')
    sys.modules[module.__name__] = module
    try:
        for cell in json.loads(NOTEBOOK.read_text())['cells']:
            if cell['cell_type'] == 'code' and 'definitions' in cell['metadata'].get('tags', []):
                exec(compile(''.join(cell['source']), str(NOTEBOOK), 'exec'), module.__dict__)
        yield module
    finally:
        sys.modules.pop(module.__name__, None)
        sys.path[:] = original_path


def config(api):
    return api.ResourceConfig('demo', 42, ('Node-1', 'Node-2'), (0, 800_000_000))


def test_windows_include_ue_then_tag_and_preserve_explicit_gap(api):
    snapshots = api.build_timeline(config(api))
    assert [(window.start_ns, window.end_ns) for window in snapshots] == [(0, 600_000_000), (800_000_000, 1_400_000_000)]
    for window in snapshots:
        for node_resource in window.nodes:
            assert node_resource.start_ns == window.start_ns and node_resource.end_ns == window.end_ns
            assert 360_000_000 <= node_resource.ue_end_ns - node_resource.start_ns <= 450_000_000
            assert (node_resource.ue_end_ns - node_resource.start_ns) % 1_000_000 == 0
            assert node_resource.direction.value in ('UL', 'DL')


@pytest.mark.parametrize('value,expected', [(360,360), (450,450), (398.2,399), (398,398), (397.999999,398), (398.000001,399)])
def test_duration_rounds_up_to_ms(api, value, expected):
    assert api.round_ue_duration_ns(value) == expected * 1_000_000


@pytest.mark.parametrize('value', [True, None, float('nan'), float('inf'), 10**1000, -1, 359.9, 450.1])
def test_rejects_invalid_duration(api, value):
    with pytest.raises(ValueError):
        api.round_ue_duration_ns(value)


@pytest.mark.parametrize('field,value', [('seed',True),('seed',-1),('node_ids',[]),('node_ids',()),('node_ids',('N','N')),('node_ids',(' ',)),('window_starts_ns',()),('window_starts_ns',[0]),('window_starts_ns',(1,)),('window_starts_ns',(False,)),('window_starts_ns',(0,0)),('window_starts_ns',(0,599_999_999)),('window_starts_ns',(0,800.0)),('scenario_id','')])
def test_invalid_input_rejected_before_trace(api, field, value):
    with pytest.raises(ValueError):
        api.build_timeline(replace(config(api), **{field:value}))


def test_seed_query_order_and_global_rng_isolation(api):
    global_rng_before = random.getstate()
    original_windows = api.build_timeline(config(api))
    assert original_windows == api.build_timeline(config(api))
    reordered_windows = api.build_timeline(replace(config(api), node_ids=('Node-2','Node-1')))
    def index_resources_by_window_and_node(resource_windows):
        return {(window.window_id, node_resource.node_id): node_resource
                for window in resource_windows for node_resource in window.nodes}
    assert index_resources_by_window_and_node(original_windows) == index_resources_by_window_and_node(reordered_windows)
    assert random.getstate() == global_rng_before
    with pytest.raises(FrozenInstanceError):
        original_windows[0].start_ns = 1


def test_current_projection_respects_half_open_boundaries_and_gaps(api):
    timeline = api.build_timeline(config(api))
    ue_end_ns = timeline[0].nodes[0].ue_end_ns
    assert api.current_resource(timeline, 'Node-1', ue_end_ns-1).status == 'UE_OCCUPIED'
    current_projection = api.current_resource(timeline, 'Node-1', ue_end_ns)
    assert current_projection.status == 'TAG_AVAILABLE'
    assert current_projection.window_end_ns == 600_000_000
    assert not hasattr(current_projection, 'windows') and not hasattr(current_projection, 'seed')
    assert api.current_resource(timeline, 'Node-1', 600_000_000).status == 'NO_WINDOW'
    assert api.current_resource(timeline, 'Node-1', 800_000_000).status == 'UE_OCCUPIED'
    with pytest.raises(ValueError):
        api.current_resource(timeline, 'unknown', 0)
    with pytest.raises(ValueError):
        api.current_resource(timeline, 'Node-1', True)


def test_table_plot_and_export_share_snapshot(api, tmp_path):
    import matplotlib.pyplot as plt
    timeline = api.build_timeline(config(api))
    rows = api.resource_rows(timeline)
    assert len(rows) == 4
    figure = api.plot_resources(timeline)
    assert len(figure.axes[0].patches) == 8
    plt.close(figure)
    api.export_resources(timeline, tmp_path)
    payload = json.loads((tmp_path/'snapshot.json').read_text())
    assert payload['seed'] == 42 and payload['scenario_id'] == 'demo'
    assert payload['window_starts_ns'] == [0, 800_000_000]
    assert payload['windows'][0]['nodes'][0]['ue_end_ns'] == rows[0]['ue_end_ns']
    assert {exported_path.name for exported_path in tmp_path.iterdir()} == {'snapshot.json','resources.csv','timeline.png','timeline.svg'}


def test_equal_random_outcomes_are_legal(api):
    timeline = api.build_timeline(replace(config(api), window_starts_ns=tuple(window_index*600_000_000 for window_index in range(100))))
    directions = [node_resource.direction for window in timeline for node_resource in window.nodes]
    assert len(directions) == 200
    assert len(set(directions)) == 2


def test_invalid_projection_identity_and_empty_export_have_clear_failure(api, tmp_path):
    timeline = api.build_timeline(config(api))
    for invalid_node_id in (None, [], '', True):
        with pytest.raises(ValueError):
            api.current_resource(timeline, invalid_node_id, 0)
    destination = tmp_path / 'empty'
    with pytest.raises(ValueError):
        api.export_resources((), destination)
    assert not destination.exists()
