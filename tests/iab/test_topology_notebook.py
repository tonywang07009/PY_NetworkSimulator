"""透過Notebook公開入口驗證行為，不複製業務實作。"""
import json
from pathlib import Path
import sys
import types
from collections import Counter

import pytest

NOTEBOOK = Path(__file__).resolve().parents[2] / 'notebooks/01_iab_topology.ipynb'

@pytest.fixture(scope='module', params=['notebook', 'python-module'])
def api(request):
    source_root = str(NOTEBOOK.parents[1] / 'src')
    if source_root not in sys.path:
        sys.path.insert(0, source_root)
    if request.param == 'python-module':
        from iab import topology
        yield topology
        return
    notebook = json.loads(NOTEBOOK.read_text())
    module = types.ModuleType('topology_notebook_under_test')
    sys.modules[module.__name__] = module
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and 'definitions' in cell['metadata'].get('tags', []):
            exec(compile(''.join(cell['source']), str(NOTEBOOK) + '#' + cell['id'], 'exec'), module.__dict__)
    yield module
    sys.modules.pop(module.__name__, None)


def test_builds_exact_global_quotas_and_one_ue_per_node(api):
    config = api.example_config(seed=42)
    result = api.build_topology(config)
    assert len(result.config.iab_nodes) == 5
    assert len(result.ues) == 5
    assert len(result.tags) == 30
    assert Counter(tag.zone.value for tag in result.tags) == {'NEAR': 10, 'MID': 13, 'FAR': 7}
    assert len({tag.tag_id for tag in result.tags}) == 30
    owners = Counter(tag.parent_node_id for tag in result.tags)
    assert set(owners) == {node.node_id for node in config.iab_nodes}
    assert min(owners.values()) >= 2
    assert {ue.parent_node_id for ue in result.ues} == set(owners)
    assert all(not hasattr(ue, 'position') for ue in result.ues)

from dataclasses import replace, FrozenInstanceError
import math
import random


@pytest.mark.parametrize('distance,expected', [
    (0.001, 'NEAR'), (9.999, 'NEAR'), (10, 'NEAR'), (10.001, 'MID'),
    (29.999, 'MID'), (30, 'MID'), (30.001, 'FAR'), (49.999, 'FAR'), (50, 'FAR'),
])
def test_classifies_horizontal_distance_at_exclusive_inner_boundaries(api, distance, expected):
    assert api.classify_distance(distance).value == expected


@pytest.mark.parametrize('distance', [0, -1, 50.001, float('inf'), float('nan'), True, None])
def test_rejects_distance_outside_deployment(api, distance):
    with pytest.raises(ValueError, match='distance'):
        api.classify_distance(distance)


@pytest.mark.parametrize('field,value', [
    ('zone_tag_counts', (9, 0, 0)), ('zone_tag_counts', (0, 0, 0)),
    ('zone_tag_counts', (-1, 20, 11)), ('zone_tag_counts', (10.5, 13, 7)),
    ('zone_tag_counts', (True, 13, 7)), ('zone_tag_counts', (10, 13)),
    ('zone_tag_counts', None), ('zone_outer_radii_m', (0, 30, 50)),
    ('zone_outer_radii_m', (30, 10, 50)), ('zone_outer_radii_m', (10, 10, 50)),
    ('zone_outer_radii_m', (10, 30, float('inf'))), ('zone_outer_radii_m', (True, 30, 50)),
    ('zone_outer_radii_m', (10, 30)), ('seed', True), ('seed', 4.2),
    ('seed', None), ('min_tags_per_node', 1), ('min_tags_per_node', True),
    ('min_tags_per_node', 2.5), ('iab_nodes', ()), ('iab_nodes', None), ('donor', None),
])
def test_refuses_invalid_config_with_reason(api, field, value):
    config = replace(api.example_config(), **{field: value})
    with pytest.raises(ValueError, match='.+'):
        api.build_topology(config)


@pytest.mark.parametrize('config', [None, {}, 'config'])
def test_refuses_wrong_config_type(api, config):
    with pytest.raises(ValueError, match='config'):
        api.build_topology(config)


@pytest.mark.parametrize('node_id,position', [
    ('', (0, 0)), (' ', (0, 0)), (None, (0, 0)), ('Node-2', (0, 0)),
    ('Donor-1', (0, 0)), ('Node-1', (float('nan'), 0)),
    ('Node-1', (0, float('inf'))), ('Node-1', (True, 0)),
])
def test_refuses_duplicate_ids_and_invalid_coordinates(api, node_id, position):
    config = api.example_config()
    bad_node = api.FixedNodeConfig(node_id, api.Position2D(*position))
    with pytest.raises(ValueError, match='.+'):
        api.build_topology(replace(config, iab_nodes=(bad_node,) + config.iab_nodes[1:]))


@pytest.mark.parametrize('separation', [0, 99.999, 100])
def test_refuses_overlapping_or_touching_node_regions(api, separation):
    config = api.example_config()
    node = replace(config.iab_nodes[1], position=api.Position2D(separation, 0))
    with pytest.raises(ValueError, match='overlap|touch'):
        api.build_topology(replace(config, iab_nodes=(config.iab_nodes[0], node) + config.iab_nodes[2:]))


def test_supports_minimum_count_and_empty_zones(api):
    result = api.build_topology(replace(api.example_config(), zone_tag_counts=(10, 0, 0)))
    assert Counter(t.parent_node_id for t in result.tags) == {f'Node-{i}': 2 for i in range(1, 6)}
    assert {t.zone.value for t in result.tags} == {'NEAR'}


def test_all_positions_match_owner_and_assigned_ring(api):
    for seed in (0, 1, 42, -7, 123456):
        config = api.example_config(seed)
        nodes = {n.node_id: n for n in config.iab_nodes}
        result = api.build_topology(config)
        for tag in result.tags:
            centre = nodes[tag.parent_node_id].position
            distance = math.hypot(tag.position.x_m - centre.x_m, tag.position.y_m - centre.y_m)
            assert api.classify_distance(distance, config.zone_outer_radii_m) == tag.zone


def test_reproduces_result_without_reading_or_mutating_global_rng(api):
    config = api.example_config()
    state = random.getstate()
    first = api.build_topology(config)
    assert random.getstate() == state
    external = random.Random(987)
    external.random()
    random.setstate(external.getstate())
    try:
        assert api.build_topology(config) == first
        assert api.build_topology(replace(config, seed=43)) != first
    finally:
        random.setstate(state)


def test_snapshot_is_deeply_immutable_with_tuple_inputs(api):
    config = api.example_config()
    result = api.build_topology(config)
    assert len(result.config.iab_nodes) == 5
    assert result.config.zone_tag_counts == (10, 13, 7)
    with pytest.raises(TypeError):
        result.config.zone_tag_counts[0] = 999
    for obj, field, value in [(result, 'tags', ()), (result.config, 'seed', 8),
                              (result.tags[0].position, 'x_m', 999)]:
        with pytest.raises(FrozenInstanceError):
            setattr(obj, field, value)


def test_samples_annulus_by_area_not_uniform_radius(api, monkeypatch):
    class ControlledRandom:
        def shuffle(self, values):
            pass
        def random(self):
            return 0.25
        def uniform(self, start, end):
            return 0.0
    monkeypatch.setattr(api.random, 'Random', lambda seed: ControlledRandom())
    result = api.build_topology(replace(api.example_config(), zone_tag_counts=(0, 10, 0)))
    # 中環帶的75%面積分位是sqrt(700)，不是線性距離25m。
    assert result.tags[0].position.x_m == pytest.approx(26.457513105737892)
    assert result.tags[0].position.y_m == 0


def test_tables_preserve_snapshot_ids_coordinates_and_link_counts(api):
    result = api.build_topology(api.example_config())
    tables = api.topology_tables(result)
    assert len(tables['nodes']) == 5
    assert sum(row['near'] for row in tables['nodes']) == 10
    assert sum(row['mid'] for row in tables['nodes']) == 13
    assert sum(row['far'] for row in tables['nodes']) == 7
    assert min(row['total'] for row in tables['nodes']) >= 2
    assert [row['tag_id'] for row in tables['tags']] == [t.tag_id for t in result.tags]
    assert [row['x_m'] for row in tables['tags']] == [t.position.x_m for t in result.tags]
    assert Counter(row['kind'] for row in tables['links']) == {'BACKHAUL': 5, 'UE_ASSOCIATION': 5, 'TAG_ACCESS': 30}
    assert tables['settings'][0]['value'] == 42


def test_plot_draws_real_geometry_without_invented_ue_positions(api):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib.patches import Circle
    from matplotlib import pyplot as plt
    result = api.build_topology(api.example_config())
    fig, ax = api.plot_topology(result)
    try:
        assert len([p for p in ax.patches if isinstance(p, Circle)]) == 15
        circles = [p for p in ax.patches if isinstance(p, Circle)]
        assert Counter(p.radius for p in circles) == {10: 5, 30: 5, 50: 5}
        scatter_points = sum(len(collection.get_offsets()) for collection in ax.collections)
        assert scatter_points == 36  # Donor + 5 Nodes + 30 Tags，沒有UE假座標。
        assert ax.get_aspect() == 1.0
        assert ax.get_xlabel() == 'x (m)'
        assert len(ax.lines) == 5
    finally:
        plt.close(fig)


def test_exports_same_snapshot_as_json_csv_png_and_svg(api, tmp_path):
    import csv
    result = api.build_topology(api.example_config())
    paths = api.export_topology(result, tmp_path)
    saved = json.loads(paths['snapshot'].read_text())
    assert saved['config']['seed'] == 42
    assert len(saved['tags']) == 30
    assert saved['tags'][0]['position']['x_m'] == result.tags[0].position.x_m
    with paths['tags'].open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 30
    assert rows[0]['tag_id'] == result.tags[0].tag_id
    assert float(rows[0]['x_m']) == result.tags[0].position.x_m
    assert paths['png'].read_bytes().startswith(b'\x89PNG')
    assert '<svg' in paths['svg'].read_text()


def test_refuses_station_ids_that_collide_with_generated_entities(api):
    config = api.example_config()
    for collision in ('UE-1', 'Tag-001'):
        node = replace(config.iab_nodes[0], node_id=collision)
        with pytest.raises(ValueError, match='ID'):
            api.build_topology(replace(config, iab_nodes=(node,) + config.iab_nodes[1:]))


def test_rejects_geometry_that_loses_tag_distance_to_float_precision(api):
    config = api.example_config()
    nodes = tuple(replace(n, position=api.Position2D(1e18+n.position.x_m, 1e18+n.position.y_m))
                  for n in config.iab_nodes)
    with pytest.raises(ValueError, match='geometry|precision|distance'):
        api.build_topology(replace(config, iab_nodes=nodes))


def test_supports_custom_radii_higher_minimum_and_negative_coordinates(api):
    result = api.build_topology(replace(api.example_config(-1), zone_outer_radii_m=(5, 15, 40),
                                       zone_tag_counts=(5, 5, 5), min_tags_per_node=3))
    assert Counter(t.parent_node_id for t in result.tags) == {f'Node-{i}': 3 for i in range(1, 6)}
    assert result.config.donor.position.y_m == -120
    nodes = {n.node_id: n.position for n in result.config.iab_nodes}
    for tag in result.tags:
        centre = nodes[tag.parent_node_id]
        d = math.hypot(tag.position.x_m-centre.x_m, tag.position.y_m-centre.y_m)
        assert api.classify_distance(d, result.config.zone_outer_radii_m) == tag.zone


def test_accepts_representable_outer_ring_under_rounding_at_rng_endpoint(api, monkeypatch):
    class OuterEndpointRandom:
        def shuffle(self, values):
            pass
        def random(self):
            return 0.0
        def uniform(self, start, end):
            return math.tau / 1000
    monkeypatch.setattr(api.random, 'Random', lambda seed: OuterEndpointRandom())
    result = api.build_topology(replace(api.example_config(), zone_tag_counts=(0, 0, 10)))
    nodes = {n.node_id: n.position for n in result.config.iab_nodes}
    for tag in result.tags:
        centre = nodes[tag.parent_node_id]
        distance = math.hypot(tag.position.x_m-centre.x_m, tag.position.y_m-centre.y_m)
        assert 30 < distance <= 50
        assert distance == pytest.approx(50, abs=1e-10)
        assert tag.zone.value == 'FAR'


def test_refuses_unrepresentable_integer_coordinate_difference_with_valueerror(api):
    config = api.example_config()
    nodes = list(config.iab_nodes)
    nodes[0] = replace(nodes[0], position=api.Position2D(10**308, 0))
    nodes[1] = replace(nodes[1], position=api.Position2D(-(10**308), 0))
    with pytest.raises(ValueError, match='geometry|separation'):
        api.build_topology(replace(config, iab_nodes=tuple(nodes)))


@pytest.mark.parametrize('field,value', [
    ('iab_nodes', 'example_nodes'),
    ('zone_outer_radii_m', [10, 30, 50]),
    ('zone_tag_counts', [10, 13, 7]),
])
def test_accepts_only_tuple_for_collection_config(api, field, value):
    config = api.example_config()
    if field == 'iab_nodes':
        value = list(config.iab_nodes)
    with pytest.raises(ValueError, match=field):
        api.build_topology(replace(config, **{field: value}))
