"""Behavior checks for the charging trace Notebook's conversion boundary."""
import json
from pathlib import Path
import types
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebooks/04_tag_energy.ipynb'


@pytest.fixture(scope='module')
def api():
    module = types.ModuleType('charging_trace_under_test')
    sys.modules[module.__name__] = module
    try:
        for index, cell in enumerate(json.loads(NOTEBOOK.read_text())['cells']):
            if cell['cell_type'] == 'code' and 'definitions' in cell['metadata'].get('tags', []):
                exec(compile(''.join(cell['source']), f'{NOTEBOOK}:definitions-{index}', 'exec'), module.__dict__)
        yield module
    finally:
        sys.modules.pop(module.__name__, None)


def test_accepted_ul_input_produces_the_independent_dc_reference(api):
    output = api.harvested_power_w(1e-6, maximum_w=10e-6, slope_per_w=2e5, midpoint_w=10e-6)
    assert output == pytest.approx(0.2571323570959774e-6, rel=1e-12)


def conversion(api, value, **changes):
    settings = {'maximum_w': 10e-6, 'slope_per_w': 2e5, 'midpoint_w': 10e-6}
    settings.update(changes)
    return api.harvested_power_w(value, **settings)


def test_zero_weak_and_strong_inputs_are_monotone_and_passive(api):
    inputs = (0.0, 1e-20, 1e-12, 1e-6, 10e-6, 680e-6, 1.0, 1e308)
    outputs = [conversion(api, value) for value in inputs]
    assert outputs[0] == 0.0
    assert outputs[1] > 0
    assert outputs == sorted(outputs)
    for value, output in zip(inputs, outputs, strict=True):
        assert 0 <= output <= min(value, 10e-6)
    assert outputs[-1] == pytest.approx(10e-6)


@pytest.mark.parametrize('value', [None, True, '1e-6', -1e-9, float('nan'), float('inf'), 10**1000])
def test_invalid_rf_input_is_rejected(api, value):
    with pytest.raises(ValueError, match='rf_input_w'):
        conversion(api, value)


@pytest.mark.parametrize('field,value', [
    ('maximum_w', 0), ('maximum_w', -1), ('maximum_w', None),
    ('maximum_w', float('inf')), ('midpoint_w', 0),
    ('midpoint_w', float('nan')), ('slope_per_w', True),
    ('slope_per_w', -1), ('slope_per_w', 0),
])
def test_invalid_conversion_parameters_are_rejected(api, field, value):
    with pytest.raises(ValueError):
        conversion(api, 1e-6, **{field: value})


def test_nonpassive_paper_scale_is_rejected_without_clipping(api):
    with pytest.raises(ValueError, match='passive slope bound'):
        conversion(api, 1e-6, maximum_w=0.24, slope_per_w=150, midpoint_w=0.014)


def test_unrepresentable_shape_is_rejected(api):
    with pytest.raises(ValueError, match='shape'):
        conversion(api, 1e-6, midpoint_w=1e308)


def test_notebook_labels_the_runtime_boundary_and_research_assumptions():
    notebook = json.loads(NOTEBOOK.read_text())
    text = '\n'.join(''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
    assert '尚未實作完整 Tag 狀態引擎' in text
    assert '研究基準' in text
    assert '正常待機' in text and '被動恢復' in text


def test_all_notebook_code_cells_compile():
    notebook = json.loads(NOTEBOOK.read_text())
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            compile(''.join(cell['source']), f'{NOTEBOOK}:cell-{index}', 'exec')


def test_finite_integer_extremes_reject_overflowing_derived_bound(api):
    with pytest.raises(ValueError, match='passive slope bound'):
        conversion(api, 1e-6, maximum_w=10**308, slope_per_w=10**308, midpoint_w=1e-308)


def test_delivered_notebook_contains_a_rendered_energy_plot():
    notebook = json.loads(NOTEBOOK.read_text())
    image_outputs = [output for cell in notebook['cells'] if cell['cell_type'] == 'code'
                     for output in cell.get('outputs', []) if 'image/png' in output.get('data', {})]
    assert image_outputs, 'Execute the Notebook and embed the energy plot before delivery'


def test_selected_operation_traces_modes_and_full_cost_without_mutation(api):
    original = api.TagSnapshot('Tag-001', 1_401_000_000, 0.8e-6, api.TagMode.STATIC)
    trace = api.trace_tag_operation(original, tbs_bytes=16, paging_ns=2_000_000,
                                    wait_ns=1_000_000, window_end_ns=1_600_000_000,
                                    deadline_ns=2_000_000_000)
    assert [row.mode for row in trace.rows] == [api.TagMode.WAKING, api.TagMode.PAGING_RX,
                                               api.TagMode.WAIT_D2R, api.TagMode.BACKSCATTER,
                                               api.TagMode.SLEEP]
    assert trace.snapshot.energy_j == pytest.approx(0.733988e-6, rel=1e-12)
    assert trace.snapshot.now_ns == 1_467_200_000
    assert trace.snapshot.mode is api.TagMode.SLEEP
    assert original.energy_j == 0.8e-6 and original.mode is api.TagMode.STATIC


def operation(api, snapshot, **changes):
    kwargs = dict(tbs_bytes=16, paging_ns=2_000_000, wait_ns=1_000_000,
                  window_end_ns=1_600_000_000, deadline_ns=2_000_000_000)
    kwargs.update(changes)
    return api.trace_tag_operation(snapshot, **kwargs)


def test_admission_energy_boundary_and_refusal_are_atomic(api):
    required = 66.012e-9
    for supplied in (required - 1e-18, 0.0):
        original = api.TagSnapshot('Tag-001', 1_401_000_000, supplied, api.TagMode.SLEEP)
        with pytest.raises(ValueError, match='stored energy'):
            operation(api, original)
        assert original.energy_j == supplied
    exact = api.TagSnapshot('Tag-001', 1_401_000_000, required, api.TagMode.SLEEP)
    trace = operation(api, exact)
    assert trace.snapshot.energy_j == 0
    assert trace.snapshot.mode is api.TagMode.ENERGY_RECOVERY


def test_deadline_is_strict_but_guard_may_finish_after_it_within_window(api):
    original = api.TagSnapshot('Tag-001', 1_401_000_000, 1e-6, api.TagMode.STATIC)
    with pytest.raises(ValueError, match='exclusive deadline'):
        operation(api, original, deadline_ns=1_467_000_000)
    trace = operation(api, original, deadline_ns=1_467_000_001, window_end_ns=1_467_200_000)
    assert trace.snapshot.now_ns == 1_467_200_000
    with pytest.raises(ValueError, match='Window'):
        operation(api, original, window_end_ns=1_467_199_999)


def test_failed_reception_consumes_the_same_complete_operation(api):
    original = api.TagSnapshot('Tag-001', 1_401_000_000, 1e-6, api.TagMode.STATIC)
    success = operation(api, original)
    failure = operation(api, original, receive_success=False)
    assert success.snapshot == failure.snapshot
    assert success.receive_success is True and failure.receive_success is False
    assert 'no energy refund' in failure.rows[3].note
    assert sum(row.consumed_j for row in failure.rows) == pytest.approx(66.012e-9)


@pytest.mark.parametrize('field,value', [('tbs_bytes', True), ('tbs_bytes', 5), ('paging_ns', 0),
                                       ('paging_ns', -1), ('wait_ns', 0.5), ('wait_ns', True),
                                       ('wait_ns', -1), ('receive_success', 1)])
def test_operation_rejects_invalid_inputs_without_debit(api, field, value):
    original = api.TagSnapshot('Tag-001', 1_401_000_000, 1e-6, api.TagMode.STATIC)
    with pytest.raises(ValueError):
        operation(api, original, **{field: value})
    assert original.energy_j == 1e-6


def test_active_tag_cannot_start_a_second_operation(api):
    original = api.TagSnapshot('Tag-001', 1_401_000_000, 1e-6, api.TagMode.BACKSCATTER)
    with pytest.raises(ValueError, match='inactive'):
        operation(api, original)


def test_background_depletion_recovery_and_phase_gate_are_explicit(api):
    original = api.TagSnapshot('Tag-001', 600_000_000, 0.002e-6, api.TagMode.SLEEP)
    depleted = api.advance_tag_interval(original, duration_ns=400_000_000, phase='GAP', rf_input_w=1e-6)
    assert depleted.snapshot.now_ns == 1_000_000_000
    assert depleted.snapshot.energy_j == 0
    assert depleted.snapshot.mode is api.TagMode.ENERGY_RECOVERY
    assert depleted.depletion_after_s == pytest.approx(0.2)
    assert depleted.rows[0].harvested_j == 0
    charged = api.advance_tag_interval(depleted.snapshot, duration_ns=400_000_000, phase='UE_UL', rf_input_w=1e-6)
    assert charged.snapshot.energy_j == pytest.approx(0.10285294283839096e-6, rel=1e-12)
    assert charged.snapshot.mode is api.TagMode.ENERGY_RECOVERY
    assert charged.rows[0].consumed_j == 0
    assert original.energy_j == 0.002e-6


@pytest.mark.parametrize('phase', ['RF_SWITCH', 'PAGING', 'WAIT_D2R', 'D2R', 'GUARD', 'GAP'])
def test_inactive_tag_does_not_harvest_in_forbidden_phases(api, phase):
    original = api.TagSnapshot('Tag-001', 0, 0.8e-6, api.TagMode.SLEEP)
    trace = api.advance_tag_interval(original, duration_ns=400_000_000, phase=phase, rf_input_w=1e-6)
    assert trace.snapshot.energy_j == pytest.approx(0.796e-6)
    assert trace.rows[0].harvested_j == 0


def test_normal_charging_saturation_and_split_intervals_preserve_state(api):
    original = api.TagSnapshot('Tag-001', 0, 0.95e-6, api.TagMode.STATIC)
    full = api.advance_tag_interval(original, duration_ns=400_000_000, phase='UE_DL', rf_input_w=1e-6)
    first = api.advance_tag_interval(original, duration_ns=200_000_000, phase='UE_DL', rf_input_w=1e-6)
    split = api.advance_tag_interval(first.snapshot, duration_ns=200_000_000, phase='UE_DL', rf_input_w=1e-6)
    assert full.snapshot == split.snapshot
    assert full.snapshot.energy_j == 1e-6
    assert full.rows[0].spilled_j == pytest.approx(0.04885294283839096e-6, rel=1e-12)
    assert first.rows[0].spilled_j + split.rows[0].spilled_j == pytest.approx(full.rows[0].spilled_j, abs=1e-21)


def test_recovery_is_eligible_but_does_not_wake_until_selected(api):
    recovered = api.TagSnapshot('Tag-001', 1_401_000_000, 0.1e-6, api.TagMode.ENERGY_RECOVERY)
    trace = operation(api, recovered)
    assert trace.rows[0].mode is api.TagMode.WAKING
    assert trace.rows[0].consumed_j == 1e-9
    assert recovered.mode is api.TagMode.ENERGY_RECOVERY
    assert trace.snapshot.energy_j == pytest.approx(0.033988e-6)
    other = api.TagSnapshot('Tag-002', 0, 1e-6, api.TagMode.STATIC)
    assert other.energy_j == 1e-6 and other.now_ns == 0


@pytest.mark.parametrize('tbs,duration', [(8,35_000_000),(16,63_000_000),(32,118_000_000),(64,228_000_000)])
def test_each_selected_tbs_keeps_full_accepted_occupancy(api, tbs, duration):
    original = api.TagSnapshot('Tag-001', 0, 1e-6, api.TagMode.STATIC)
    trace = operation(api, original, tbs_bytes=tbs, window_end_ns=600_000_000, deadline_ns=1_000_000_000)
    row = trace.rows[3]
    assert row.end_ns - row.start_ns == duration
    assert row.consumed_j == pytest.approx({8:35e-9,16:63e-9,32:118e-9,64:228e-9}[tbs])


@pytest.mark.parametrize('duration', [True,-1,0.5,None])
def test_background_rejects_invalid_duration_before_state_change(api, duration):
    original = api.TagSnapshot('Tag-001', 0, 0.8e-6, api.TagMode.STATIC)
    with pytest.raises(ValueError):
        api.advance_tag_interval(original, duration_ns=duration, phase='GAP')
    assert original.now_ns == 0


@pytest.mark.parametrize('energy', [True,-1,float('nan'),float('inf'),1.000001e-6])
def test_invalid_snapshot_energy_is_rejected(api, energy):
    original = api.TagSnapshot('Tag-001', 0, energy, api.TagMode.STATIC)
    with pytest.raises(ValueError):
        api.advance_tag_interval(original, duration_ns=1, phase='GAP')


def test_background_state_and_phase_guards_are_not_bypassable(api):
    active = api.TagSnapshot('Tag-001', 0, 1e-6, api.TagMode.PAGING_RX)
    with pytest.raises(ValueError, match='inactive'):
        api.advance_tag_interval(active, duration_ns=1, phase='PAGING')
    inactive = api.TagSnapshot('Tag-001', 0, 1e-6, api.TagMode.STATIC)
    with pytest.raises(ValueError, match='phase'):
        api.advance_tag_interval(inactive, duration_ns=1, phase='UNKNOWN')


def test_missing_cw_rejects_before_waking(api):
    original = api.TagSnapshot('Tag-001', 1_401_000_000, 1e-6, api.TagMode.SLEEP)
    with pytest.raises(ValueError, match='CW'):
        operation(api, original, cw_available=False)


def test_operation_rejects_nonzero_cost_that_float_cannot_represent(api):
    settings = dict(api.energy_settings)
    for name in ('quiescent_power_w', 'receive_power_w', 'd2r_power_w'):
        settings[name] = 5e-324
    settings['activation_energy_j'] = 0
    snapshot = api.TagSnapshot('Tag-001', 0, 5e-324, api.TagMode.SLEEP)
    with pytest.raises(ValueError, match='floating-point range'):
        api.trace_tag_operation(snapshot, tbs_bytes=8, paging_ns=1, wait_ns=0,
                                window_end_ns=1_000_000_000, deadline_ns=1_000_000_000,
                                settings=settings)
    assert snapshot.energy_j == 5e-324
