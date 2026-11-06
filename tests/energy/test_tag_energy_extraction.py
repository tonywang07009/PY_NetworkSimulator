"""Preserve independently captured Notebook behavior through the source API."""
import dataclasses
import importlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))


def test_source_api_preserves_the_accepted_notebook_baseline():
    api = importlib.import_module('energy.tag_energy')
    baseline = json.loads((Path(__file__).parent / 'fixtures/energy-before-extraction.json').read_text())
    for case in baseline['cases']:
        snapshot = api.TagSnapshot('A', 0, case['initial_j'], api.TagMode(case['mode']))
        function = api.trace_tag_operation if case['kind'] == 'operation' else api.advance_tag_interval
        trace = function(snapshot, **case['kwargs'])
        actual = json.loads(json.dumps(dataclasses.asdict(trace)))
        assert actual == case['trace']


def test_completed_tag_harvests_only_until_supplied_batch_cw_off():
    from energy import tag_energy as api
    snapshot = api.TagSnapshot('A', 0, 0.8e-6, api.TagMode.SLEEP)
    trace = api.trace_tag_operation(snapshot, tbs_bytes=16, paging_ns=2_000_000,
                                    wait_ns=1_000_000, window_end_ns=600_000_000,
                                    deadline_ns=1_000_000_000, cw_off_ns=121_000_000,
                                    cw_power_dbm=10, distance_m=10)
    assert [row.phase for row in trace.rows] == ['ACTIVATION','PAGING','WAIT_D2R','D2R','POST_TBS_CW','GUARD']
    tail = trace.rows[4]
    assert (tail.start_ns, tail.end_ns) == (66_000_000,121_000_000)
    # Independent Decimal worked reference: 6.797973850689421e-8 W RF.
    assert tail.harvested_j == pytest.approx(8.959972233598904e-10, rel=1e-12)
    assert tail.consumed_j == pytest.approx(0.55e-9, rel=1e-12)
    assert trace.rows[5].start_ns == 121_000_000
    assert trace.rows[5].harvested_j == 0
    assert trace.snapshot.energy_j == pytest.approx(0.7343339972233599e-6, rel=1e-12)


def batch_operation(api, initial_j=0.8e-6, **changes):
    kwargs = dict(tbs_bytes=16, paging_ns=2_000_000, wait_ns=1_000_000,
                  window_end_ns=600_000_000, deadline_ns=1_000_000_000,
                  cw_off_ns=121_000_000, cw_power_dbm=10, distance_m=10)
    kwargs.update(changes)
    snapshot = api.TagSnapshot('A', 0, initial_j, api.TagMode.SLEEP)
    return snapshot, api.trace_tag_operation(snapshot, **kwargs)


def test_last_member_has_zero_tail_and_guard_starts_at_common_cw_off():
    from energy import tag_energy as api
    _, trace = batch_operation(api, tbs_bytes=32)
    assert [row.phase for row in trace.rows] == ['ACTIVATION','PAGING','WAIT_D2R','D2R','GUARD']
    assert trace.rows[-1].start_ns == 121_000_000
    assert sum(row.harvested_j for row in trace.rows) == 0
    assert trace.snapshot.energy_j == pytest.approx(0.678988e-6, rel=1e-12)


def test_failed_reception_does_not_remove_completed_tag_cw_eligibility():
    from energy import tag_energy as api
    _, success = batch_operation(api)
    _, failure = batch_operation(api, receive_success=False)
    assert success.snapshot == failure.snapshot
    assert success.rows[4] == failure.rows[4]
    assert failure.receive_success is False


def test_future_cw_energy_cannot_fund_admission():
    from energy import tag_energy as api
    with pytest.raises(ValueError, match='stored energy'):
        batch_operation(api, initial_j=66.012e-9-1e-18, cw_power_dbm=22, distance_m=1)
    _, trace = batch_operation(api, initial_j=66.012e-9, cw_power_dbm=22, distance_m=1)
    assert trace.snapshot.energy_j > 0


def test_post_completion_depletion_remains_recovery_and_preserves_the_ledger():
    from energy import tag_energy as api
    original, trace = batch_operation(api, initial_j=66.012e-9, cw_power_dbm=-2, distance_m=50)
    assert original.energy_j == 66.012e-9
    assert trace.snapshot.mode is api.TagMode.ENERGY_RECOVERY
    assert trace.snapshot.energy_j > 0
    assert trace.rows[-1].consumed_j == 0
    assert 'depletion split' in trace.rows[-2].note
    for row in trace.rows:
        assert row.after_j == pytest.approx(row.before_j+row.harvested_j-row.consumed_j-row.spilled_j,abs=1e-21)
        assert 0 <= row.after_j <= 1e-6


def test_cw_saturation_reports_spill_before_unpowered_guard_draw():
    from energy import tag_energy as api
    _, trace = batch_operation(api, initial_j=1e-6, cw_power_dbm=22, distance_m=1)
    tail, guard = trace.rows[-2:]
    assert tail.after_j == 1e-6
    assert tail.spilled_j > 0
    assert guard.before_j == 1e-6 and guard.harvested_j == 0
    assert trace.snapshot.energy_j == pytest.approx(0.999998e-6, rel=1e-12)


@pytest.mark.parametrize('changes', [dict(cw_off_ns=True),dict(cw_off_ns=-1),dict(cw_off_ns=65_999_999),
                                    dict(cw_power_dbm=18),dict(cw_power_dbm=True),dict(cw_power_dbm=None),
                                    dict(distance_m=0.999999),dict(distance_m=50.000001),dict(distance_m=True),
                                    dict(distance_m=float('nan')),dict(distance_m=10**1000),
                                    dict(window_end_ns=121_199_999),dict(deadline_ns=66_000_000)])
def test_invalid_batch_context_refuses_before_any_snapshot_change(changes):
    from energy import tag_energy as api
    with pytest.raises(ValueError):
        batch_operation(api, **changes)


@pytest.mark.parametrize('power', [-2,10,22])
@pytest.mark.parametrize('distance', [1,50])
def test_cw_one_way_input_uses_the_declared_power_and_distance_limits(power,distance):
    from energy import tag_energy as api
    # Independent one-way gain references, not the reflected Reader link.
    gains = {1:0.0006797973850689421,50:2.7191895402757684e-7}
    watts = {-2:0.000630957344480193,10:0.01,22:0.15848931924611134}
    assert api.cw_rf_input_w(cw_power_dbm=power,distance_m=distance) == pytest.approx(watts[power]*gains[distance],rel=1e-12)


def test_cw_off_window_boundary_and_complete_d2r_deadline_stay_distinct():
    from energy import tag_energy as api
    _, trace = batch_operation(api, window_end_ns=121_200_000, deadline_ns=66_000_001)
    assert trace.snapshot.now_ns == 121_200_000


def test_partial_cw_source_context_is_rejected():
    from energy import tag_energy as api
    with pytest.raises(ValueError,match='explicit batch'):
        batch_operation(api,cw_off_ns=None)


def test_bulk_energy_validation_reuses_rules_and_returns_isolated_inputs():
    from energy import tag_energy as api
    snapshots = {'A':api.TagSnapshot('A',0,0.8e-6,api.TagMode.SLEEP)}
    rf = {(0,'A'):1e-6}
    checked = api.validate_energy_inputs(snapshots=snapshots,rf_inputs_w=rf)
    assert checked['snapshots'] == snapshots
    assert checked['snapshots'] is not snapshots
    assert checked['rf_inputs_w'] == rf and checked['rf_inputs_w'] is not rf
    with pytest.raises(ValueError,match='rf_input_w'):
        api.validate_energy_inputs(snapshots=snapshots,rf_inputs_w={(0,'A'):float('nan')})
    assert snapshots['A'].energy_j == 0.8e-6


def test_operation_projection_returns_current_energy_without_changing_the_plan():
    from energy import tag_energy as api
    _, plan = batch_operation(api)
    current = api.project_tag_operation(plan,now_ns=13_000_000,cw_rf_input_w=6.797973850689421e-8)
    assert current.energy_j == pytest.approx(0.78699e-6,rel=1e-12)
    assert current.mode is api.TagMode.BACKSCATTER
    assert plan.snapshot.now_ns == 121_200_000
    with pytest.raises(ValueError,match='plan interval'):
        api.project_tag_operation(plan,now_ns=121_200_001)
