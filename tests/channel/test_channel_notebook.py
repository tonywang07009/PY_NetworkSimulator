"""通道 Notebook 的公開行為測試。數值來自獨立參考表。"""
import json
from pathlib import Path
import sys
import types

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebooks/02_channel_model.ipynb'


@pytest.fixture(scope='module', params=['notebook', 'python-module'])
def api(request):
    sys.path.insert(0, str(ROOT / 'src'))
    module = types.ModuleType('channel_notebook_under_test')
    sys.modules[module.__name__] = module
    try:
        if request.param == 'python-module':
            from channel import channel_model
            from iab.topology import build_topology, example_config
            yield types.SimpleNamespace(**vars(channel_model),
                                        build_topology=build_topology, example_config=example_config)
            return
        notebook = json.loads(NOTEBOOK.read_text())
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code' and 'definitions' in cell['metadata'].get('tags', []):
                exec(compile(''.join(cell['source']), str(NOTEBOOK) + '#' + cell['id'], 'exec'), module.__dict__)
        yield module
    finally:
        sys.modules.pop(module.__name__, None)
        sys.path.remove(str(ROOT / 'src'))


def test_entry_profile_is_immutable_and_binds_real_power(api):
    from dataclasses import FrozenInstanceError, replace
    config = api.ChannelConfig()
    assert config.cw_power_dbm == (-2.0, 10.0, 22.0)
    with pytest.raises(FrozenInstanceError):
        config.noise_power_dbm = 0
    with pytest.raises(ValueError, match='tuple'):
        api.validate_channel_config(replace(config, cw_power_dbm=[-2, 10, 22]))
    with pytest.raises(ValueError, match='profile'):
        api.validate_channel_config(replace(config, cw_power_dbm=(0, 10, 22)))


def test_link_budget_matches_twenty_metre_worked_example(api):
    link = api.link_budget(api.ChannelConfig(), 20, api.PowerLevel.LOW, 0, 0)
    assert link.received_dbm == pytest.approx(-127.39361003298393)
    assert link.sinr_db == pytest.approx(-2.4039099896237377)
    assert link.rho == pytest.approx(1.1498441941621902)
    assert link.cw_power_w == pytest.approx(0.000630957344480193)
    assert link.residual_self_interference_w == 0


@pytest.mark.parametrize('distance', [0, -1, .999, 50.001, float('inf'), float('nan'), True, None])
def test_rejects_out_of_range_distance(api, distance):
    with pytest.raises(ValueError, match='distance'):
        api.link_budget(api.ChannelConfig(), distance, api.PowerLevel.LOW, 0, 0)


@pytest.mark.parametrize('distance', [1, 10, 30, 50])
def test_accepts_inclusive_distance_boundaries(api, distance):
    assert api.link_budget(api.ChannelConfig(), distance, api.PowerLevel.LOW, 0, 0).distance_m == distance


def test_fbl_matches_independent_reference_table(api):
    import csv
    with (ROOT / 'Plan/channel-fbl-reference.csv').open(encoding='utf-8-sig') as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        result = api.fbl_reference(float(row['rho_real_bpsk']), int(row['k']), int(row['n']))
        assert result.capacity_bits == pytest.approx(float(row['C_bits']), abs=3e-10)
        assert result.dispersion_bits2 == pytest.approx(float(row['V_bits2']), abs=3e-10)
        assert result.log_error == pytest.approx(float(row['log_error']), abs=3e-8)
        assert result.log_success == pytest.approx(float(row['log_success']), abs=3e-8)


def test_fbl_preserves_log_tail_and_diagnoses_precision_limit(api):
    tail = api.fbl_reference(16, 64, 128)
    assert tail.status == 'FLOAT_TAIL'
    assert tail.epsilon == 0
    assert tail.log_error < -1000
    unavailable = api.fbl_reference(300, 64, 128)
    assert unavailable.status == 'QUADRATURE_PRECISION_LIMIT'
    assert unavailable.epsilon is None


def test_fbl_diagnoses_overflow_of_log_probability(api):
    result = api.fbl_reference(16, 64, 10 ** 308)
    assert result.status == 'NORMAL_APPROXIMATION_NUMERIC_LIMIT'
    assert result.epsilon is None
    assert result.log_error is None


@pytest.mark.parametrize('rho,k,n', [(0, 64, 128), (-1, 64, 128), (float('nan'), 64, 128), (True, 64, 128), (1, 0, 128), (1, True, 128), (1, 129, 128), (1, 64, 0), (1, 64, 128.0)])
def test_rejects_invalid_fbl_inputs(api, rho, k, n):
    with pytest.raises(ValueError, match='.+'):
        api.fbl_reference(rho, k, n)


def test_window_repeats_freeze_power_and_new_window_changes_quality(api):
    import random
    topology = api.build_topology(api.example_config())
    before = random.getstate()
    model = api.ChannelModel(api.ChannelConfig(), topology)
    first = model.window(0, api.PowerLevel.LOW)
    first_link = model.link(0, topology.tags[0].tag_id)
    assert model.window(0, api.PowerLevel.LOW) == first
    assert model.link(0, topology.tags[0].tag_id) == first_link
    with pytest.raises(ValueError, match='power'):
        model.window(0, api.PowerLevel.HIGH)
    second = model.window(1, api.PowerLevel.LOW)
    assert all(a[1] != b[1] for a, b in zip(first.node_offsets_db, second.node_offsets_db))
    assert model.link(1, topology.tags[0].tag_id).budget.snr_db != first_link.budget.snr_db
    assert random.getstate() == before
    for unavailable in (0, 2):
        with pytest.raises(ValueError, match='current'):
            model.link(unavailable, topology.tags[0].tag_id)


def test_power_table_retains_random_class_under_better_offset(api):
    for power, expected in [
        (api.PowerLevel.LOW, {'NEAR': 'RELIABLE', 'MID': 'RANDOM', 'FAR': 'UNREACHABLE'}),
        (api.PowerLevel.MEDIUM, {'NEAR': 'RELIABLE', 'MID': 'RELIABLE', 'FAR': 'RANDOM'}),
        (api.PowerLevel.HIGH, {'NEAR': 'RELIABLE', 'MID': 'RELIABLE', 'FAR': 'RELIABLE'}),
    ]:
        topology = api.build_topology(api.example_config())
        model = api.ChannelModel(api.ChannelConfig(), topology)
        model.window(0, power)
        for tag in topology.tags:
            result = model.link(0, tag.tag_id)
            assert result.receive_class == expected[tag.zone.value]
            if result.receive_class != 'RANDOM':
                assert result.used_error_probability == (0 if result.receive_class == 'RELIABLE' else 1)
            else:
                assert result.used_error_probability == result.fbl.epsilon
            assert result.budget.profile_id == api.ChannelConfig().profile_id


def test_same_node_shares_offset_and_distance_preserves_quality_order(api):
    topology = api.build_topology(api.example_config())
    model = api.ChannelModel(api.ChannelConfig(), topology)
    model.window(0, api.PowerLevel.LOW)
    for node in topology.config.iab_nodes:
        results = [model.link(0, t.tag_id) for t in topology.tags if t.parent_node_id == node.node_id]
        assert len({r.budget.offset_db for r in results}) == 1
        results.sort(key=lambda r: r.budget.distance_m)
        assert all(a.budget.snr_db > b.budget.snr_db for a, b in zip(results, results[1:]))


def test_packet_replay_rejects_conflicting_parameters(api):
    topology = api.build_topology(api.example_config())
    model = api.ChannelModel(api.ChannelConfig(), topology)
    model.window(0, api.PowerLevel.LOW)
    tag = next(t for t in topology.tags if t.zone == api.TagZone.MID)
    first = model.receive(0, tag.tag_id, 'packet-1')
    assert model.receive(0, tag.tag_id, 'packet-1') == first
    assert model.link(0, tag.tag_id).budget == first.link.budget
    with pytest.raises(ValueError, match='transmission'):
        model.receive(0, tag.tag_id, 'packet-1', k=32, n=128)
    draws = [model.receive(0, tag.tag_id, f'packet-{i}').uniform_draw for i in range(2, 12)]
    assert len(set(draws)) == 10


def test_same_window_reuses_link_calculation_for_replay_and_distinct_packets(api, monkeypatch):
    from channel import channel_model

    topology = api.build_topology(api.example_config())
    model = api.ChannelModel(api.ChannelConfig(), topology)
    model.window(0, api.PowerLevel.LOW)
    for tag in topology.tags:
        if tag.zone == api.TagZone.MID:
            break
    integration_calls = []
    original_quad = channel_model.quad

    def counted_quad(*args, **kwargs):
        integration_calls.append(1)
        return original_quad(*args, **kwargs)

    monkeypatch.setattr(channel_model, 'quad', counted_quad)
    first = model.receive(0, tag.tag_id, 'packet-1')
    for _ in range(9):
        assert model.receive(0, tag.tag_id, 'packet-1') is first
    second = model.receive(0, tag.tag_id, 'packet-2')
    assert second.link == first.link
    assert second.uniform_draw != first.uniform_draw
    assert model.link(0, tag.tag_id) == first.link
    assert len(integration_calls) == 2


@pytest.mark.parametrize('k,n', [(True, 1), (1, True), (64.0, 128), (64, 128.0),
                                  ([], 128), (64, []), (None, 128), (0, 128),
                                  (-1, 128), (64, 0), (129, 128)])
def test_link_reuse_does_not_bypass_packet_length_validation(api, k, n):
    topology = api.build_topology(api.example_config())
    model = api.ChannelModel(api.ChannelConfig(), topology)
    model.window(0, api.PowerLevel.LOW)
    tag_id = topology.tags[0].tag_id
    model.link(0, tag_id, 1, 1)
    first = model.link(0, tag_id)
    with pytest.raises(ValueError):
        model.link(0, tag_id, k, n)
    assert model.link(0, tag_id) == first


def test_link_reuse_keeps_tags_and_packet_lengths_separate(api):
    topology = api.build_topology(api.example_config())
    model = api.ChannelModel(api.ChannelConfig(), topology)
    model.window(0, api.PowerLevel.LOW)
    first_tag, second_tag = topology.tags[:2]
    first = model.link(0, first_tag.tag_id)
    other_tag = model.link(0, second_tag.tag_id)
    assert other_tag.tag_id == second_tag.tag_id
    assert other_tag != first
    for k, n in ((32, 128), (64, 256)):
        changed = model.link(0, first_tag.tag_id, k, n)
        assert (changed.fbl.k, changed.fbl.n) == (k, n)
        assert changed != first
    assert model.link(0, first_tag.tag_id) == first
    model.receive(0, first_tag.tag_id, 'length-bound', 32, 128)
    with pytest.raises(ValueError, match='transmission'):
        model.receive(0, first_tag.tag_id, 'length-bound', 64, 128)


def test_link_reuse_tracks_successful_windows_and_preserves_failed_windows(api, monkeypatch):
    from channel import channel_model

    topology = api.build_topology(api.example_config())
    model = api.ChannelModel(api.ChannelConfig(), topology)
    first_window = model.window(0, api.PowerLevel.LOW)
    for tag in topology.tags:
        if tag.zone == api.TagZone.MID:
            tag_id = tag.tag_id
            break
    first = model.link(0, tag_id)
    original_quad = channel_model.quad
    integration_calls = []

    def counted_quad(*args, **kwargs):
        integration_calls.append(1)
        return original_quad(*args, **kwargs)

    monkeypatch.setattr(channel_model, 'quad', counted_quad)
    assert model.window(0, api.PowerLevel.LOW) == first_window
    assert model.link(0, tag_id) == first
    with pytest.raises(ValueError, match='power'):
        model.window(0, api.PowerLevel.HIGH)
    old_offsets = dict(first_window.node_offsets_db)

    def colliding_rng(seed, kind, node_id, window_id):
        return types.SimpleNamespace(uniform=lambda low, high: old_offsets[node_id])

    with monkeypatch.context() as collision_patch:
        collision_patch.setattr(channel_model, 'local_rng', colliding_rng)
        with pytest.raises(ValueError, match='collision'):
            model.window(1, api.PowerLevel.LOW)
    assert model.link(0, tag_id) == first
    assert not integration_calls

    model.window(1, api.PowerLevel.LOW)
    second = model.link(1, tag_id)
    assert second.window_id == 1
    assert second.budget != first.budget
    assert len(integration_calls) == 2
    with pytest.raises(ValueError, match='current'):
        model.link(0, tag_id)

    other_model = api.ChannelModel(api.ChannelConfig(), topology)
    other_model.window(0, api.PowerLevel.LOW)
    assert other_model.link(0, tag_id) == first
    assert len(integration_calls) == 4


def test_all_nine_reference_links_keep_physics_and_rule_separate(api):
    import csv
    with (ROOT / 'Plan/channel-link-reference.csv').open(encoding='utf-8-sig') as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        link = api.evaluate_link(api.ChannelConfig(), float(row['distance_m']),
                                 api.PowerLevel(row['level']), 0, 0, window_id=0, node_id='Node-1', tag_id='test-tag', zone=api.TagZone(row['zone']))
        assert link.budget.received_dbm == pytest.approx(float(row['received_dbm']), abs=1e-9)
        assert link.budget.sinr_db == pytest.approx(float(row['sinr_db']), abs=1e-9)
        assert link.receive_class == row['receive_class']
        assert link.used_error_probability == pytest.approx(float(row['used_error_probability']), abs=1e-9)


def test_random_class_survives_float_tail_in_existing_topology_scan(api):
    import csv
    topology = api.build_topology(api.example_config())
    tags = {t.tag_id: t for t in topology.tags}
    with (ROOT / 'Plan/channel-random-region-scan.csv').open(encoding='utf-8-sig') as stream:
        rows = list(csv.DictReader(stream))
    tails = []
    for row in rows:
        tag = tags[row['tag_id']]
        link = api.evaluate_link(api.ChannelConfig(), float(row['distance_m']),
                                 api.PowerLevel(row['level']), float(row['offset_db']), 0,
                                 window_id=0, node_id=tag.parent_node_id, tag_id=tag.tag_id, zone=tag.zone)
        assert link.receive_class == 'RANDOM'
        assert link.fbl.log_error == pytest.approx(float(row['log_error']), abs=1e-6)
        if link.fbl.status == 'FLOAT_TAIL':
            tails.append(link)
            packet = api.draw_reception(api.ChannelConfig(), link, 'tail-packet')
            assert packet.sampling_status == 'FINITE_PRNG_RESOLUTION_LIMIT'
    assert len(tails) == 3


def test_conditional_packet_frequency_matches_moderate_fbl_example(api):
    link = api.evaluate_link(api.ChannelConfig(), 20, api.PowerLevel.LOW, 0, 0,
                             window_id=0, node_id='Node-1', tag_id='test-tag', zone=api.TagZone.MID)
    packets = [api.draw_reception(api.ChannelConfig(), link, f'tx-{i}') for i in range(2000)]
    assert sum(p.failed for p in packets) / len(packets) == pytest.approx(.32707295241502565, abs=.04)
    assert all(p.link.budget == link.budget for p in packets)


@pytest.mark.parametrize('window_id,power', [(True, 'LOW'), (-1, 'LOW'), (1.0, 'LOW'), (0, 'LOW'), (0, None)])
def test_invalid_window_does_not_change_current_window(api, window_id, power):
    model = api.ChannelModel(api.ChannelConfig(), api.build_topology(api.example_config()))
    first = model.window(0, api.PowerLevel.LOW)
    with pytest.raises(ValueError):
        model.window(window_id, power)
    assert model.window(0, api.PowerLevel.LOW) == first


def test_rejected_topology_is_not_moved(api):
    from dataclasses import replace
    from iab.contracts import Position2D
    topology = api.build_topology(api.example_config())
    tag = topology.tags[0]
    owner = next(n for n in topology.config.iab_nodes if n.node_id == tag.parent_node_id)
    bad_tag = replace(tag, position=Position2D(owner.position.x_m + .5, owner.position.y_m))
    bad = replace(topology, tags=(bad_tag,) + topology.tags[1:])
    with pytest.raises(ValueError, match='distance'):
        api.ChannelModel(api.ChannelConfig(), bad)
    assert bad.tags[0].position == bad_tag.position


def test_every_code_cell_has_preceding_markdown_with_source():
    notebook = json.loads(NOTEBOOK.read_text())
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        prior = notebook['cells'][index - 1]
        assert prior['cell_type'] == 'markdown'
        source = ''.join(prior['source'])
        assert '來源' in source or '文獻公式' in source
        assert '](' in source
