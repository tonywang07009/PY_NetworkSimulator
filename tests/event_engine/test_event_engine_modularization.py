"""Behavior of the agreed preparation/state/record boundary."""
import dataclasses
import json
from pathlib import Path

import pytest
from test_event_engine_notebook import api


def setup_engine(api, requests=(), snapshots=None):
    windows=api.build_timeline(api.ResourceConfig('engine-test',42,('N1',),(0,1_000_000_000)))
    snapshots = snapshots or {tag:api.energy.TagSnapshot(tag,0,0.8e-6,api.energy.TagMode.SLEEP) for tag in ('A','B','C')}
    scenario=api.prepare_scenario(windows,{tag:'N1' for tag in snapshots},
                                  {(w.window_id,tag):1e-6 for w in windows for tag in snapshots},requests)
    return api.TagEventEngine(scenario,api.EngineState(snapshots=dict(snapshots)))


def test_observations_are_fixed_and_window_summaries_do_not_grow_per_call(api):
    engine=setup_engine(api)
    first=engine.run_until(0)
    for time in (1,2,3,1000):engine.run_until(time)
    assert first['A'].now_ns==0 and first['A'].energy_j==0.8e-6
    assert engine.records.window_summaries==[]
    engine.run_until(600_000_000)
    assert len(engine.records.window_summaries)==3
    engine.run_until(600_000_001)
    assert len(engine.records.window_summaries)==3
    assert engine.records.window_summaries[0]['start_ns']==0
    assert engine.records.window_summaries[0]['end_ns']==600_000_000


def test_successful_round_consumption_clears_only_used_records_and_never_redelivers(api):
    engine=setup_engine(api)
    engine.run_until(1_600_000_000)
    previous=dict(engine.state.snapshots)
    received=[]
    engine.finish_round(received.append)
    assert len(received)==1 and len(received[0]['window_summaries'])==6
    assert engine.records.window_summaries==[] and engine.records.trace==[]
    assert engine.state.snapshots==previous
    engine.finish_round(received.append)
    assert len(received)==1


def test_failed_round_consumer_preserves_results_for_retry(api):
    engine=setup_engine(api)
    engine.run_until(600_000_000)
    before=list(engine.records.window_summaries)
    def fail(result):
        result['window_summaries'][0]['after_j']=0
        raise RuntimeError('plot failed')
    with pytest.raises(RuntimeError,match='plot failed'):engine.finish_round(fail)
    assert engine.records.window_summaries==before


def test_refactor_preserves_the_independent_valid_snapshot_and_completion_baseline(api):
    fixture=json.loads((Path(__file__).parent/'fixtures/engine-before-modularization.json').read_text())
    windows=api.build_timeline(api.ResourceConfig('engine-test',42,('N1',),(0,1_000_000_000)))
    start=windows[0].nodes[0].ue_end_ns+1_000_000
    for case in fixture['cases']:
        explicit=case['explicit']
        snapshots={tag:api.energy.TagSnapshot(tag,0,0.8e-6,api.energy.TagMode.SLEEP) for tag in ('A','B','C')}
        requests=tuple(api.OperationRequest(start,tag,0,size,2_000_000,1_000_000,20_000_000_000,
                                            tag=='B',batch_id='batch' if explicit else None)
                       for tag,size in (('A',16),('B',32)))
        batches=(api.BatchCW('batch','N1',0,start+121_000_000,10,(('A',10),('B',10))),) if explicit else ()
        scenario=api.prepare_scenario(windows,{tag:'N1' for tag in snapshots},
            {(window.window_id,tag):1e-6 for window in windows for tag in snapshots},requests,batches=batches)
        engine=api.TagEventEngine(scenario,api.EngineState(snapshots=snapshots))
        for expected in case['observations']:
            actual=engine.run_until(expected['time_ns'])
            assert json.loads(json.dumps({tag:dataclasses.asdict(v) for tag,v in actual.items()}))==expected['snapshots']
            assert json.loads(json.dumps(engine.records.completion_batches))==expected['completions']


def test_helpers_do_not_change_input_state_and_initialized_engines_are_independent(api):
    first=setup_engine(api)
    second=api.TagEventEngine(first.scenario,api.EngineState(snapshots=dict(first.state.snapshots)))
    original=dict(second.state.snapshots)
    first.run_until(100_000_000)
    assert second.state.snapshots==original
    assert not second.records.window_starts
    with pytest.raises(TypeError):first.scenario.tag_nodes['A']='changed'


def test_round_cleanup_preserves_an_open_window_active_plan_and_queue(api):
    windows=api.build_timeline(api.ResourceConfig('engine-test',42,('N1',),(0,1_000_000_000)))
    start=windows[0].nodes[0].ue_end_ns+1_000_000
    request=api.OperationRequest(start,'A',0,16,2_000_000,1_000_000,20_000_000_000)
    engine=setup_engine(api,(request,))
    engine.run_until(start+66_000_000)
    before=dict(engine.state.snapshots)
    next_event=engine.queue.peek_time()
    assert engine.state.active and engine.records.completion_batches
    received=[]
    engine.finish_round(received.append)
    assert len(received[0]['completion_batches'])==1
    assert engine.state.snapshots==before and engine.state.active
    assert engine.records.window_starts
    assert engine.queue.peek_time()==next_event
    engine.run_until(600_000_000)
    assert len(engine.records.window_summaries)==3


def test_window_summary_carries_previous_end_through_gap(api):
    engine=setup_engine(api)
    engine.run_until(600_000_000)
    end=engine.records.window_summaries[0]['after_j']
    engine.run_until(1_000_000_000)
    beginning=engine.records.window_starts[(1,'A')]
    assert beginning.energy_j==pytest.approx(end-4e-9,abs=1e-20)
    engine.run_until(1_600_000_000)
    assert engine.records.window_summaries[3]['before_j']==beginning.energy_j


def test_render_replaces_the_supplied_display_and_releases_figures(api):
    plt=pytest.importorskip('matplotlib.pyplot')
    pytest.importorskip('IPython')
    class Display:
        latest=None
        def update(self,image):self.latest=image
    display=Display()
    before=plt.get_fignums()
    result={'window_summaries':({'tag_id':'A','start_ns':0,'end_ns':600_000_000,
                                'before_j':0.8e-6,'after_j':0.7e-6},), 'completion_batches':()}
    api.render_round(result,display)
    assert display.latest.data.startswith(b'\x89PNG')
    api.render_round({'window_summaries':(), 'completion_batches':()},display)
    assert plt.get_fignums()==before


def test_render_failure_closes_the_figure_and_engine_preserves_round_records(api):
    plt=pytest.importorskip('matplotlib.pyplot')
    pytest.importorskip('IPython')
    class FailedDisplay:
        def update(self,image):raise RuntimeError('display unavailable')
    engine=setup_engine(api)
    engine.run_until(600_000_000)
    before=plt.get_fignums()
    with pytest.raises(RuntimeError,match='display unavailable'):
        engine.finish_round(lambda result:api.render_round(result,FailedDisplay()))
    assert len(engine.records.window_summaries)==3
    assert plt.get_fignums()==before
