"""Behavior at the Notebook event queue and environment seam."""
import json
from pathlib import Path
import sys
import types

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebooks/05_event_engine.ipynb'

@pytest.fixture(scope='module')
def api():
    module = types.ModuleType('event_engine_under_test')
    sys.modules[module.__name__] = module
    module.__dict__['__file__'] = str(NOTEBOOK)
    prior_path = list(sys.path)
    prior_energy = sys.modules.get('event_engine_energy')
    try:
        for cell in json.loads(NOTEBOOK.read_text())['cells']:
            if 'definitions' in cell['metadata'].get('tags', []):
                exec(compile(''.join(cell['source']), str(NOTEBOOK), 'exec'), module.__dict__)
        yield module
    finally:
        sys.path[:] = prior_path
        sys.modules.pop(module.__name__, None)
        if prior_energy is None:
            sys.modules.pop('event_engine_energy', None)
        else:
            sys.modules['event_engine_energy'] = prior_energy


def test_queue_returns_same_time_payloads_together_and_rejects_past_time(api):
    queue = api.EventQueue()
    queue.schedule(10, 'B', {'tag': 'B'})
    queue.schedule(10, 'A', {'tag': 'A'})
    queue.schedule(20, 'C', {})
    assert queue.check_time() == 10
    assert queue.now_ns == 0
    now, events = queue.pop_batch()
    assert now == 10
    assert {event.kind for event in events} == {'A','B'}
    with pytest.raises(ValueError, match='past'):
        queue.schedule(9, 'PAST', {})
    assert queue.pop_batch()[0] == 20
    assert queue.pop_batch() is None
    assert queue.check_time() is None


@pytest.mark.parametrize('time', [True, -1, 0.5, float('nan'), None])
def test_queue_rejects_invalid_ns_without_inserting(api,time):
    queue = api.EventQueue()
    with pytest.raises(ValueError):
        queue.schedule(time, 'BAD')
    assert queue.pop_batch() is None


def new_engine(api, windows, snapshots, tag_nodes, rf_inputs_w, requests=(), *, batches=()):
    scenario = api.prepare_scenario(windows,tag_nodes,rf_inputs_w,requests,batches=batches)
    return api.TagEventEngine(scenario,api.EngineState(snapshots=dict(snapshots)))


def make_engine(api, requests=(), *, initial_energies=None):
    windows = api.build_timeline(api.ResourceConfig('engine-test',42,('N1',),(0,1_000_000_000)))
    snapshots = {tag:api.energy.TagSnapshot(tag,0,0.8e-6,api.energy.TagMode.SLEEP) for tag in ('A','B')}
    for tag,stored in (initial_energies or {}).items():
        snapshots[tag]=api.energy.TagSnapshot(tag,0,stored,api.energy.TagMode.ENERGY_RECOVERY if stored==0 else api.energy.TagMode.SLEEP)
    rf = {(w.window_id,tag):1e-6 for w in windows for tag in snapshots}
    return new_engine(api,windows,snapshots,{'A':'N1','B':'N1'},rf,requests), windows


def test_resources_use_03_direction_switch_and_gap_without_reset(api):
    engine, windows = make_engine(api)
    first = windows[0].nodes[0]
    engine.run_until(first.ue_end_ns)
    expected = 0.8e-6+(0.2571323570959774e-6-10e-9)*first.ue_end_ns/1e9
    assert engine.state.snapshots['A'].energy_j == pytest.approx(expected,abs=1e-18)
    assert engine.state.phases['N1']=='RF_SWITCH'
    engine.run_until(1_000_000_000)
    assert engine.state.snapshots['A'].energy_j == pytest.approx(expected-10e-9*(1-first.ue_end_ns/1e9),abs=1e-18)
    assert engine.state.phases['N1'] in ('UE_UL','UE_DL')
    assert any(row['window_id']==0 and row['end_ns']==600_000_000 for row in engine.records.window_summaries)


def requests_at_switch(api):
    _, windows = make_engine(api)
    start = windows[0].nodes[0].ue_end_ns+1_000_000
    return tuple(api.OperationRequest(start,tag,0,16,2_000_000,1_000_000,20_000_000_000,tag=='A') for tag in ('A','B'))


def test_parallel_operations_expose_current_energy_then_batch_completions(api):
    requests = requests_at_switch(api)
    engine, _ = make_engine(api, requests)
    start = requests[0].start_ns
    engine.run_until(start)
    before = engine.state.snapshots['A'].energy_j
    engine.run_until(start+13_000_000)
    assert engine.state.snapshots['A'].mode is api.energy.TagMode.BACKSCATTER
    assert engine.state.snapshots['A'].energy_j == pytest.approx(before-12.01e-9,abs=1e-18)
    assert not engine.records.completion_batches
    engine.run_until(start+66_200_000)
    assert engine.state.snapshots['A'].energy_j == pytest.approx(before-65.012e-9,abs=1e-18)
    assert engine.state.snapshots['A'].mode is api.energy.TagMode.SLEEP
    batch = engine.records.completion_batches[0]
    assert batch[0] == start+66_000_000
    assert [row['eligible'] for row in batch[1]] == [True,False]
    assert engine.state.snapshots['A'].energy_j == engine.state.snapshots['B'].energy_j
    reversed_engine, _ = make_engine(api, tuple(reversed(requests)))
    reversed_engine.run_until(start+66_200_000)
    assert reversed_engine.records.completion_batches == engine.records.completion_batches
    assert reversed_engine.state.snapshots == engine.state.snapshots


def test_request_refusal_has_no_activation_or_scheduled_completions(api):
    _, windows = make_engine(api)
    start=windows[0].nodes[0].ue_end_ns+1_000_000
    request=api.OperationRequest(start,'A',0,16,2_000_000,1_000_000,start+66_000_000)
    engine,_=make_engine(api,(request,))
    baseline,_=make_engine(api)
    engine.run_until(start+70_000_000)
    baseline.run_until(start+70_000_000)
    assert engine.state.snapshots == baseline.state.snapshots
    assert not engine.records.completion_batches
    assert any(row['kind']=='REJECTED' and 'deadline' in row['outcome'] for row in engine.records.trace)


def test_segmented_run_and_unrelated_events_do_not_double_charge(api):
    requests=requests_at_switch(api)
    end=requests[0].start_ns+66_200_000
    engine,_=make_engine(api,requests)
    reference,_=make_engine(api,requests)
    for offset in (0,1,2_000_000,3_000_000,10_000_000,66_000_000,66_200_000):
        engine.run_until(requests[0].start_ns+offset)
    reference.run_until(end)
    assert engine.state.snapshots == reference.state.snapshots
    assert engine.records.completion_batches == reference.records.completion_batches
    with pytest.raises(ValueError,match='past'):
        engine.queue.schedule(end-1,'OBSERVE')


def test_depleted_tag_recovers_without_automatic_activation(api):
    engine,windows=make_engine(api, initial_energies={'A':0})
    engine.run_until(windows[0].nodes[0].ue_end_ns)
    assert engine.state.snapshots['A'].energy_j>0
    assert engine.state.snapshots['A'].mode is api.energy.TagMode.ENERGY_RECOVERY
    assert not engine.state.active


def test_overlapping_requests_reject_before_second_activation(api):
    requests=requests_at_switch(api)[:1]
    late=api.OperationRequest(requests[0].start_ns+1,'A',0,16,2_000_000,1_000_000,20_000_000_000)
    engine,_=make_engine(api,requests+(late,))
    reference,_=make_engine(api,requests)
    end=requests[0].start_ns+66_200_000
    engine.run_until(end)
    reference.run_until(end)
    assert engine.state.snapshots == reference.state.snapshots
    assert len(engine.records.completion_batches)==1
    assert any(row['kind']=='REJECTED' for row in engine.records.trace)


@pytest.mark.parametrize('until',[True,-1,0.1,None])
def test_invalid_run_time_does_not_advance(api,until):
    engine,_=make_engine(api)
    before=dict(engine.state.snapshots)
    with pytest.raises(ValueError):
        engine.run_until(until)
    assert engine.state.now_ns==0
    assert engine.state.snapshots==before


def test_same_tag_simultaneous_conflicts_reject_whole_conflict_group(api):
    first=requests_at_switch(api)[0]
    second=api.OperationRequest(first.start_ns,'A',0,8,2_000_000,1_000_000,20_000_000_000)
    engine,_=make_engine(api,(first,second))
    baseline,_=make_engine(api)
    end=first.start_ns+70_000_000
    engine.run_until(end)
    baseline.run_until(end)
    assert engine.state.snapshots==baseline.state.snapshots
    assert not engine.records.completion_batches


def test_missing_cw_refuses_without_activation(api):
    first=requests_at_switch(api)[0]
    request=api.OperationRequest(first.start_ns,'A',0,16,2_000_000,1_000_000,20_000_000_000,cw_available=False)
    engine,_=make_engine(api,(request,))
    baseline,_=make_engine(api)
    engine.run_until(first.start_ns)
    baseline.run_until(first.start_ns)
    assert engine.state.snapshots==baseline.state.snapshots
    assert not engine.state.active


@pytest.mark.parametrize('tag_id,window_id', [([],0),('',0),('A',False),('A',-1),('A',0.5)])
def test_request_identity_rejects_ambiguous_values(api,tag_id,window_id):
    with pytest.raises(ValueError):
        api.OperationRequest(1,tag_id,window_id,16,2_000_000,1_000_000,1_000_000_000)


def test_explicit_batch_cw_recharges_completed_member_but_not_active_or_unselected_tags(api):
    windows = api.build_timeline(api.ResourceConfig('cw-test',42,('N1',),(0,)))
    start = windows[0].nodes[0].ue_end_ns + 1_000_000
    requests = (api.OperationRequest(start,'A',0,16,2_000_000,1_000_000,20_000_000_000,
                                     receive_success=False,batch_id='batch-1'),
                api.OperationRequest(start,'B',0,32,2_000_000,1_000_000,20_000_000_000,
                                     batch_id='batch-1'))
    batch = api.BatchCW('batch-1','N1',0,start+121_000_000,10,(('A',10),('B',10)))
    snapshots = {tag:api.energy.TagSnapshot(tag,0,0.8e-6,api.energy.TagMode.SLEEP) for tag in ('A','B','C')}
    rf = {(0,tag):1e-6 for tag in snapshots}
    engine = new_engine(api,windows,snapshots,{tag:'N1' for tag in snapshots},rf,requests,batches=(batch,))
    engine.run_until(start)
    before = engine.state.snapshots['A'].energy_j
    c_before = engine.state.snapshots['C'].energy_j
    engine.run_until(start+76_000_000)
    assert engine.state.snapshots['A'].mode is api.energy.TagMode.SLEEP
    assert engine.state.snapshots['A'].energy_j == pytest.approx(before-65.11e-9+1.6290858606543462e-10,abs=1e-20)
    assert engine.state.snapshots['B'].energy_j == pytest.approx(before-75.01e-9,abs=1e-20)
    assert engine.state.snapshots['C'].energy_j == pytest.approx(c_before-0.76e-9,abs=1e-20)
    engine.run_until(start+121_200_000)
    assert engine.state.snapshots['A'].energy_j == pytest.approx(before-65.562e-9+8.959972233598904e-10,abs=1e-20)
    assert engine.state.snapshots['B'].energy_j == pytest.approx(before-120.012e-9,abs=1e-20)
    assert any(row['kind']=='CW_OFF' for row in engine.records.trace)
    assert len(engine.state.active)==0
    assert engine.records.completion_batches[0][1][0]['receive_success'] is False


def cw_engine(api, *, tbs=(16,32), cw_off_offset=121_000_000, power=10, distance=10,
              energies=(0.8e-6,0.8e-6), success=True, reverse=False):
    windows = api.build_timeline(api.ResourceConfig('cw-test',42,('N1',),(0,)))
    start = windows[0].nodes[0].ue_end_ns+1_000_000
    requests = tuple(api.OperationRequest(start,tag,0,size,2_000_000,1_000_000,20_000_000_000,
                                          receive_success=success,batch_id='explicit')
                     for tag,size in zip(('A','B'),tbs,strict=True))
    batch = api.BatchCW('explicit','N1',0,start+cw_off_offset,power,(('A',distance),('B',distance)))
    snapshots = {tag:api.energy.TagSnapshot(tag,0,stored,api.energy.TagMode.SLEEP)
                 for tag,stored in zip(('A','B'),energies,strict=True)}
    engine = new_engine(api,windows,snapshots,{'A':'N1','B':'N1'},
                               {(0,tag):0 for tag in snapshots},tuple(reversed(requests)) if reverse else requests,
                               batches=(batch,))
    return engine,start


def test_equal_completion_batch_has_no_cw_harvest(api):
    engine,start = cw_engine(api,tbs=(16,16),cw_off_offset=66_000_000)
    engine.run_until(start)
    before = engine.state.snapshots['A'].energy_j
    engine.run_until(start+66_200_000)
    assert engine.state.snapshots['A'].energy_j == pytest.approx(before-65.012e-9,abs=1e-20)
    assert engine.state.snapshots['A'].energy_j == engine.state.snapshots['B'].energy_j


@pytest.mark.parametrize('off',[120_999_999,121_000_001])
def test_explicit_cw_off_must_match_the_last_full_member_d2r(api,off):
    with pytest.raises(ValueError,match='final complete D2R'):
        cw_engine(api,cw_off_offset=off)


def test_invalid_member_refuses_the_whole_declared_batch_before_activation(api):
    engine,start = cw_engine(api,energies=(0.8e-6,1e-9))
    engine.run_until(start)
    assert not engine.state.active
    assert not engine.records.completion_batches
    assert all(row['kind']!='WAKING' for row in engine.records.trace)
    assert len([row for row in engine.records.trace if row['kind']=='REJECTED']) == 2
    assert engine.state.snapshots['A'].energy_j == pytest.approx(0.8e-6-10e-9*start/1e9,abs=1e-20)


@pytest.mark.parametrize('power,distance,energies', [(22,1,(1e-6,1e-6)),(-2,50,(70e-9,0.8e-6))])
def test_segmented_cw_progression_matches_full_run_at_saturation_or_depletion(api,power,distance,energies):
    whole,start = cw_engine(api,power=power,distance=distance,energies=energies)
    split,_ = cw_engine(api,power=power,distance=distance,energies=energies,reverse=True)
    for offset in (0,66_000_000,66_000_001,70_000_000,100_000_000,121_000_000,121_200_000):
        split.run_until(start+offset)
    whole.run_until(start+121_200_000)
    assert split.state.snapshots == whole.state.snapshots
    assert split.records.completion_batches == whole.records.completion_batches
    assert [row['time_ns'] for row in whole.records.trace if row['kind']=='CW_OFF'] == [start+121_000_000]


def test_missing_explicit_batch_is_rejected_instead_of_inferring_membership(api):
    _,windows = make_engine(api)
    start = windows[0].nodes[0].ue_end_ns+1_000_000
    request = api.OperationRequest(start,'A',0,16,2_000_000,1_000_000,20_000_000_000,batch_id='missing')
    with pytest.raises(ValueError,match='missing explicit batch'):
        make_engine(api,(request,))


@pytest.mark.parametrize('distances', [[['A',10],['B',10]], (('A',10),['B',10]), (('A',),('B',10)), None])
def test_batch_geometry_rejects_mutable_or_malformed_collections(api,distances):
    windows = api.build_timeline(api.ResourceConfig('cw-test',42,('N1',),(0,)))
    start = windows[0].nodes[0].ue_end_ns+1_000_000
    requests = tuple(api.OperationRequest(start,tag,0,16,2_000_000,1_000_000,20_000_000_000,batch_id='explicit')
                     for tag in ('A','B'))
    snapshots = {tag:api.energy.TagSnapshot(tag,0,0.8e-6,api.energy.TagMode.SLEEP) for tag in ('A','B')}
    batch = api.BatchCW('explicit','N1',0,start+66_000_000,10,distances)
    with pytest.raises(ValueError,match='tuple of Tag/distance pairs'):
        new_engine(api,windows,snapshots,{'A':'N1','B':'N1'},
                           {(0,tag):0 for tag in snapshots},requests,batches=(batch,))
