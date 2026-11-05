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
    now, events = queue.pop_batch()
    assert now == 10
    assert {event.kind for event in events} == {'A','B'}
    with pytest.raises(ValueError, match='past'):
        queue.schedule(9, 'PAST', {})
    assert queue.pop_batch()[0] == 20
    assert queue.pop_batch() is None


@pytest.mark.parametrize('time', [True, -1, 0.5, float('nan'), None])
def test_queue_rejects_invalid_ns_without_inserting(api,time):
    queue = api.EventQueue()
    with pytest.raises(ValueError):
        queue.schedule(time, 'BAD')
    assert queue.pop_batch() is None


def make_engine(api, requests=()):
    windows = api.build_timeline(api.ResourceConfig('engine-test',42,('N1',),(0,1_000_000_000)))
    snapshots = {tag:api.energy.TagSnapshot(tag,0,0.8e-6,api.energy.TagMode.SLEEP) for tag in ('A','B')}
    rf = {(w.window_id,tag):1e-6 for w in windows for tag in snapshots}
    return api.TagEventEngine(windows,snapshots,{'A':'N1','B':'N1'},rf,requests), windows


def test_resources_use_03_direction_switch_and_gap_without_reset(api):
    engine, windows = make_engine(api)
    first = windows[0].nodes[0]
    engine.run_until(first.ue_end_ns)
    expected = 0.8e-6+(0.2571323570959774e-6-10e-9)*first.ue_end_ns/1e9
    assert engine.snapshots['A'].energy_j == pytest.approx(expected,abs=1e-18)
    assert engine.phases['N1']=='RF_SWITCH'
    engine.run_until(1_000_000_000)
    assert engine.snapshots['A'].energy_j == pytest.approx(expected-10e-9*(1-first.ue_end_ns/1e9),abs=1e-18)
    assert engine.phases['N1'] in ('UE_UL','UE_DL')
    assert any(row['kind']=='WINDOW_END' for row in engine.trace)


def requests_at_switch(api):
    _, windows = make_engine(api)
    start = windows[0].nodes[0].ue_end_ns+1_000_000
    return tuple(api.OperationRequest(start,tag,0,16,2_000_000,1_000_000,20_000_000_000,tag=='A') for tag in ('A','B'))


def test_parallel_operations_expose_current_energy_then_batch_completions(api):
    requests = requests_at_switch(api)
    engine, _ = make_engine(api, requests)
    start = requests[0].start_ns
    engine.run_until(start)
    before = engine.snapshots['A'].energy_j
    engine.run_until(start+13_000_000)
    assert engine.snapshots['A'].mode is api.energy.TagMode.BACKSCATTER
    assert engine.snapshots['A'].energy_j == pytest.approx(before-12.01e-9,abs=1e-18)
    assert not engine.completion_batches
    engine.run_until(start+66_200_000)
    assert engine.snapshots['A'].energy_j == pytest.approx(before-65.012e-9,abs=1e-18)
    assert engine.snapshots['A'].mode is api.energy.TagMode.SLEEP
    batch = engine.completion_batches[0]
    assert batch[0] == start+66_000_000
    assert [row['eligible'] for row in batch[1]] == [True,False]
    assert engine.snapshots['A'].energy_j == engine.snapshots['B'].energy_j
    reversed_engine, _ = make_engine(api, tuple(reversed(requests)))
    reversed_engine.run_until(start+66_200_000)
    assert reversed_engine.completion_batches == engine.completion_batches
    assert reversed_engine.snapshots == engine.snapshots


def test_request_refusal_has_no_activation_or_scheduled_completions(api):
    _, windows = make_engine(api)
    start=windows[0].nodes[0].ue_end_ns+1_000_000
    request=api.OperationRequest(start,'A',0,16,2_000_000,1_000_000,start+66_000_000)
    engine,_=make_engine(api,(request,))
    baseline,_=make_engine(api)
    engine.run_until(start+70_000_000)
    baseline.run_until(start+70_000_000)
    assert engine.snapshots == baseline.snapshots
    assert not engine.completion_batches
    assert any(row['kind']=='REJECTED' and 'deadline' in row['outcome'] for row in engine.trace)


def test_segmented_run_and_unrelated_events_do_not_double_charge(api):
    requests=requests_at_switch(api)
    end=requests[0].start_ns+66_200_000
    engine,_=make_engine(api,requests)
    reference,_=make_engine(api,requests)
    for offset in (0,1,2_000_000,3_000_000,10_000_000,66_000_000,66_200_000):
        engine.run_until(requests[0].start_ns+offset)
    reference.run_until(end)
    assert engine.snapshots == reference.snapshots
    assert engine.completion_batches == reference.completion_batches
    with pytest.raises(ValueError,match='past'):
        engine.queue.schedule(end-1,'OBSERVE')


def test_depleted_tag_recovers_without_automatic_activation(api):
    engine,windows=make_engine(api)
    engine.snapshots['A']=api.energy.TagSnapshot('A',0,0,api.energy.TagMode.ENERGY_RECOVERY)
    engine.run_until(windows[0].nodes[0].ue_end_ns)
    assert engine.snapshots['A'].energy_j>0
    assert engine.snapshots['A'].mode is api.energy.TagMode.ENERGY_RECOVERY
    assert not engine.active


def test_overlapping_requests_reject_before_second_activation(api):
    requests=requests_at_switch(api)[:1]
    late=api.OperationRequest(requests[0].start_ns+1,'A',0,16,2_000_000,1_000_000,20_000_000_000)
    engine,_=make_engine(api,requests+(late,))
    reference,_=make_engine(api,requests)
    end=requests[0].start_ns+66_200_000
    engine.run_until(end)
    reference.run_until(end)
    assert engine.snapshots == reference.snapshots
    assert len(engine.completion_batches)==1
    assert any(row['kind']=='REJECTED' for row in engine.trace)


@pytest.mark.parametrize('until',[True,-1,0.1,None])
def test_invalid_run_time_does_not_advance(api,until):
    engine,_=make_engine(api)
    before=dict(engine.snapshots)
    with pytest.raises(ValueError):
        engine.run_until(until)
    assert engine.now_ns==0
    assert engine.snapshots==before


def test_same_tag_simultaneous_conflicts_reject_whole_conflict_group(api):
    first=requests_at_switch(api)[0]
    second=api.OperationRequest(first.start_ns,'A',0,8,2_000_000,1_000_000,20_000_000_000)
    engine,_=make_engine(api,(first,second))
    baseline,_=make_engine(api)
    end=first.start_ns+70_000_000
    engine.run_until(end)
    baseline.run_until(end)
    assert engine.snapshots==baseline.snapshots
    assert not engine.completion_batches


def test_missing_cw_refuses_without_activation(api):
    first=requests_at_switch(api)[0]
    request=api.OperationRequest(first.start_ns,'A',0,16,2_000_000,1_000_000,20_000_000_000,cw_available=False)
    engine,_=make_engine(api,(request,))
    baseline,_=make_engine(api)
    engine.run_until(first.start_ns)
    baseline.run_until(first.start_ns)
    assert engine.snapshots==baseline.snapshots
    assert not engine.active


@pytest.mark.parametrize('tag_id,window_id', [([],0),('',0),('A',False),('A',-1),('A',0.5)])
def test_request_identity_rejects_ambiguous_values(api,tag_id,window_id):
    with pytest.raises(ValueError):
        api.OperationRequest(1,tag_id,window_id,16,2_000_000,1_000_000,1_000_000_000)
