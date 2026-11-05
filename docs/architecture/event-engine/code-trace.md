# Event engine source trace

Date: 2026-11-04. Comparison HEAD c5fd4be80404e3765dffdbb5f94c61afdedfda52.
All new implementation is uncommitted local working-tree evidence. No archive or merge is claimed.

## Tree and ownership

```text
/home/tonywang/Net_simluation/PY_NetworkSimulator/
├── notebooks/05_event_engine.ipynb          # New queue and state adapter, retained for human trace
├── notebooks/03_resource_timeline.ipynb     # Existing teaching source, separately rerun in RL when authorized
├── notebooks/04_tag_energy.ipynb            # Existing energy owner, definitions reused without extraction
├── src/timeline/
│   ├── contracts.py                       # Unchanged resource records
│   └── resource_timeline.py                # Unchanged build_timeline
├── tests/event_engine/
│   └── test_event_engine_notebook.py       # New public queue/engine behavior checks
├── tests/energy/
│   └── execute_tag_energy_notebook.py      # Existing runner gains optional Notebook path; default 04 unchanged
└── docs/architecture/event-engine/
    ├── README.md                          # English guide
    ├── README.zh-TW.md                     # Chinese guide
    └── code-trace.md                       # This map
```

| Absolute implementation path | Requirement, callers and evidence |
|---|---|
| [05 Notebook](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/05_event_engine.ipynb) | EventQueue, OperationRequest and TagEventEngine; sections 2-3 own definitions; section 4 calls them. Tests exercise tagged definitions. |
| [Engine tests](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/event_engine/test_event_engine_notebook.py) | Integer-ns batches, current-time energy, gap persistence, simultaneous completion, exact deadline refusal, CW refusal, conflict groups and invalid identities. |
| [Kernel runner](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/execute_tag_energy_notebook.py) | Optional Notebook path selects 05. Isolated kernel lifecycle and 04 default remain shared. |
| [04 energy owner](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/04_tag_energy.ipynb) | Unchanged; imported tagged definitions supply admission, inactive progression and immutable snapshots. |
| [03 resource core](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/timeline/resource_timeline.py) | Unchanged; build_timeline supplies actual per-Node direction and UE/Window boundaries. |

## Flow and test links

ResourceConfig -> build_timeline -> resource boundary events -> EventQueue.pop_batch -> current-time Tag advancement.
Completions -> deterministic result batch -> resource boundary updates -> grouped request checks -> selected-operation admission.
Admission uses 04 full cost and strict deadlines. Private plans schedule future phase boundaries; current snapshots never jump to final energy.
External RF is keyed by window_id and tag_id; Reader reflected receive power is not substituted.
Analytic inactive depletion remains within 04; fractional diagnostic offsets do not enter the integer-ns queue.
Input snapshots are copied into engine ownership and never mutated. Dynamic service allocation and full Access batch validation remain absent.

23 engine tests + 62 energy tests + 72 timeline checks = 157 passing checks in RL.
The clean 05 kernel ran six code cells with zero errors and shutdown. Its PNG was inspected.
Spec and Standards reviewers independently confirmed repairs. No scoped shortcut markers were found.
Human acceptance, source extraction, hardware validation and remote delivery remain pending.
