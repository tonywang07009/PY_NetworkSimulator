# Event Engine source trace

Date: 2026-11-06. Product root: `/home/tonywang/Net_simluation/PY_NetworkSimulator`.
Change: add-event-engine-notebook. All evidence describes the local working tree, not a merged delivery.
The modular Notebook is implemented for human trace. Human acceptance and later Engine extraction remain pending.

## Actual tree

```text
/home/tonywang/Net_simluation/PY_NetworkSimulator/
├── notebooks/05_event_engine.ipynb
│   ├── Event / EventQueue                 # Existing queue owner
│   ├── OperationRequest / BatchCW         # Supplied inputs, integer ns
│   ├── EngineScenario / State / Records   # Explicit typed data owners
│   ├── prepare_resources                 # Window/Node/Tag/RF-key relationships
│   ├── validate_batch / prepare_batches   # Immutable geometry, membership and CW_OFF
│   ├── prepare_scenario                  # Prepared read-only copied indexes
│   ├── collect_completions               # Returned same-time completion values
│   ├── TagEventEngine                    # Explicit runtime/queue/record commits
│   └── render_round                      # One display, figure cleanup, no files
├── src/energy/
│   ├── contracts.py                      # Existing immutable snapshots/plans
│   ├── tag_energy.py                     # Existing accounting + supported bulk validation/projection
│   └── __init__.py                       # Energy exports
├── src/timeline/
│   ├── contracts.py                      # Existing Window/resource contracts
│   └── resource_timeline.py               # Existing build_timeline
├── tests/event_engine/
│   ├── fixtures/engine-before-modularization.json
│   ├── test_event_engine_notebook.py
│   └── test_event_engine_modularization.py
├── tests/energy/
│   ├── test_tag_energy_extraction.py
│   └── execute_tag_energy_notebook.py
└── docs/architecture/event-engine/
    ├── README.md / README.zh-TW.md
    └── code-trace.md
```

## Reading map: relative labels, absolute links

| Actual source | Inputs / output / state owner | Acceptance and evidence |
|---|---|---|
| [notebooks/05_event_engine.ipynb](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/05_event_engine.ipynb) sections 1-2 | Import source; EventQueue schedules/populates integer-ns batches. Queue owns its heap; check_time reads the next timestamp without consuming it. | Queue invalid/past-time and same-time tests. |
| Same Notebook, section 3 inputs | OperationRequest and BatchCW use Tag/Node/Window identities and ns; CW source is explicit. | Invalid identity and immutable/malformed geometry refusals. |
| Same Notebook, section 3.1 data | Scenario holds read-only prepared mappings; State holds current snapshots/plans; Records holds current-Window trace, pending starts and round results. | Independent-run and snapshot-copy tests. Types/key shapes are visible. |
| Same Notebook, sections 3.2-3.4 preparation | Pure preparation returns indexes; no state, queue or activation writes. Bad geometry raises ValueError. | Existing refusal cases and new preparation tests. |
| Same Notebook, section 4 calculation | collect_completions returns sorted same-time results; source energy returns snapshots. No EngineState argument. | Completion ordering; preserved 18-point fixture. |
| Same Notebook, TagEventEngine.__init__ | Prepared scenario and initial state -> bulk energy validation -> own containers -> schedule. | Input isolation and initial refusal tests. |
| Same Notebook, _advance | Read previous snapshot -> project active plan or integrate inactive interval -> assign updated snapshot -> update clock. | Active D2R/current-time, saturation/recovery and segmented progression. |
| Same Notebook, _plan / _request_batch / _admit | Prepare complete plans before Engine writes active/trace/queue. All members must pass. | Atomic batch refusal, CW, deadline and no future-energy admission. |
| Same Notebook, _apply_boundaries | Engine captures real Window start/end after energy advance, updates phases/active and resets latest-Window trace. | One endpoint summary per Tag/Window; GAP carry-forward. |
| Same Notebook, run_until | Advance -> collect completions -> boundaries -> requests. Return copied current snapshot mapping. | Same-time causal tests; earlier observation isolation. |
| Same Notebook, finish_round | Deliver copied round summary/completion collections; consumer succeeds -> delete consumed prefixes. No live-state or pending-start reset. | Success/failure, no redelivery, active-plan and pending queue preservation. |
| Same Notebook, render_round | Endpoint summaries + dedicated display handle -> updated PNG. Figure closes in finally. | Repeated replacement, empty summary and rendering-failure tests; clean kernel. |
| [src/energy/tag_energy.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/energy/tag_energy.py:324) | validate_energy_inputs returns copied checked snapshot/RF dictionaries using existing private rules. No mutation. | Bulk validation/refusal/isolation test. |
| [Same energy core, projection](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/energy/tag_energy.py:338) | project_tag_operation accepts a core-generated plan and current ns; returns current TagSnapshot with finite/underflow guards. CW tail/Guard reuses inactive accounting. | Direct public projection test, original full-plan tests and 18 preserved observations. |
| [src/energy/__init__.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/energy/__init__.py) | Supported public energy exports, without Notebook/plot dependencies. | Source and caller imports. |
| [tests/event_engine/test_event_engine_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/event_engine/test_event_engine_notebook.py) | Actual prepared-scenario constructor and state/records access. Existing expected electrical values remain. | Queue, operation/CW, conflicts, same-time ordering, malformed geometry. |
| [tests/event_engine/test_event_engine_modularization.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/event_engine/test_event_engine_modularization.py) | Public scenario/Engine/run_until/finish_round and display-update boundaries. | Preserved fixture, observation/record isolation, endpoint storage and cleanup/failure behavior. |
| [tests/event_engine/fixtures/engine-before-modularization.json](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/event_engine/fixtures/engine-before-modularization.json) | Independent valid pre-refactor state/completion reference. | 18 retained observations from the saved original Notebook, not generated from the new Engine. |
| [tests/energy/test_tag_energy_extraction.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/test_tag_energy_extraction.py) | Original energy references plus public bulk validation/projection cases. | New entry tests were RED before implementations. |
| [tests/energy/execute_tag_energy_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/execute_tag_energy_notebook.py) | Isolated temporary kernel; saves Notebook only after execution succeeds. | RL Notebook 05 receipt; 04 default unchanged. |

## Flow and lifetime

```text
build_timeline + explicit Tag/RF/request/batch inputs
  -> prepare_resources / prepare_batches -> EngineScenario
initial EngineState + scenario -> validate_energy_inputs -> Engine creates own state/records/queue

run_until
  -> read current TagSnapshot and required context
  -> energy.project_tag_operation OR advance_tag_interval
  -> Engine assigns returned snapshot
  -> collect same-time completions -> Engine records results
  -> Engine applies resource boundaries and Window endpoint summaries
  -> prepare operation plans -> Engine commits admission and events
  -> copied current snapshots returned to caller

outer caller chooses round end -> finish_round(consume_results)
  -> copied summaries/results -> outer result use + render_round
  -> success: remove consumed record prefixes
  -> failure: retain records for retry
```

Do not clear State, active plans, clock, pending Window starts or queued Guard events during round cleanup.
Window summaries preserve start/end energy, not every internal transition. Current/latest-Window trace is replaced on the next start.
Only the latest PNG is held in the reused display; no automatic exports or deletion. Single-round usage still scales with inputs.

[Current implemented contract flow](../../../.archify/dataflow-event-engine-modular-notebook-20261106-173444/event-engine-modular.html).
Earlier design diagrams remain historical. Artifact/browser checks do not prove program behavior or human acceptance.
No ServiceManager, full Access planner, strategy/Baseline, hardware calibration, Engine extraction or remote delivery is claimed.
