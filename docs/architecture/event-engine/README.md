# Event engine Notebook

[繁體中文](README.zh-TW.md)

Notebook 05 connects resource boundaries from 03 with the accepted Tag state/energy definitions from 04.
Open the [Notebook](../../../notebooks/05_event_engine.ipynb), then the [contract diagram](../../../.archify/dataflow-event-engine-20261104-190000/event-engine.html) and [code trace](code-trace.md).
The diagram describes the local working-tree contract, not committed source evidence.

## Read and run

1. Section 1 imports timeline core and loads only tagged energy definitions. It does not execute 04 demonstrations.
2. Section 2 defines the integer-ns batch queue. A sequence number avoids comparing payloads, not deciding physical outcomes.
3. Section 3 owns current snapshots, resource phases, admission and operation progress.
4. Section 4 supplies a two-Window scenario, equal-TBS parallel Tags, opposite receive outcomes, tables and a saved PNG.
5. Section 5 states the remaining integration boundary.

Run from the project root or notebooks directory in the existing RL environment.
The clean runner command from the product root is:

```bash
python tests/energy/execute_tag_energy_notebook.py /tmp/pynet-event-engine-execution.json notebooks/05_event_engine.ipynb
```

The runner keeps 04 as its default. The new optional Notebook path avoids duplicating kernel lifecycle code.

## Causal contract

Advance each Tag with the preceding phase before handling a boundary.
Only UE UL/DL allows harvesting. Add the accepted 1-ms RF switch after the UE prefix.
Use a private admitted operation plan for current-time interpolation; never publish its future final energy as the current snapshot.
Collect simultaneous D2R results before resource changes and new requests. Strict deadlines remain timestamp predicates.
Reject all simultaneous requests that conflict for one Tag before activation; retain independent Tags.
Recovery never triggers automatic selection. Snapshots persist across Window gaps and run segments.

## Evidence and limits

23 event tests and 62 energy tests pass. Combined event, energy and timeline checks pass 157 tests in the RL environment.
The base Python lacks IPython and cannot execute the timeline Notebook test fixture; this is an environment boundary.
A clean kernel executes all six 05 code cells, saves a PNG and shuts down. The energy plot was inspected.
Both review axes have zero remaining findings after conflict-group and identity-boundary repairs.
The scoped marker scan finds no marked shortcut debt. This does not establish zero technical debt.

RF values, receiver timing, legal Access allocation and CW availability are external inputs.
The demonstration uses two equal-TBS Tags on caller-assumed orthogonal resources. The engine does not allocate CFA/SFS or validate a complete heterogeneous batch.
The eligible field is a receive/deadline result, not service credit. Baseline, ServiceManager and FBL sampling remain outside this prototype.
Hardware accuracy and full STE dictionary compliance remain [Needs Verification]. Human acceptance and source extraction remain pending.
