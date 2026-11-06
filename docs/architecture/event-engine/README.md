# Event engine Notebook

[繁體中文](README.zh-TW.md)

The former Engine constructor mixed validation, indexing, scheduling and runtime state.
Notebook 05 now separates prepared inputs, current state and round records so readers can trace calculations and writes.
The Engine remains a Notebook prototype awaiting human acceptance. It imports the existing timeline and energy cores.

## Quick run

Open [Notebook 05](../../../notebooks/05_event_engine.ipynb) in the existing RL environment from the product root or notebooks directory.
Execute cells in order. The last cell displays one Window-endpoint plot and asserts consumed records are cleared while live state remains.
A clean temporary-kernel run from the product root is:

```bash
python tests/energy/execute_tag_energy_notebook.py /tmp/pynet-event-engine-execution.json notebooks/05_event_engine.ipynb
```

No kernel registration, dependency installation or automatic data export is required.

## Architecture reading path

Read [the current flow](../../../.archify/dataflow-event-engine-modular-notebook-20261106-173444/event-engine-modular.html), then [the complete source trace](code-trace.md).
The flow describes the uncommitted working-tree contract, not committed source evidence.

| Notebook section | Responsibility |
|---|---|
| 1-2 | Import source cores and define the existing integer-ns EventQueue. |
| 3 | Define supplied inputs, EngineScenario/State/Records and preparation functions. |
| 4 | Read previous snapshots, obtain results and explicitly commit event/state changes. |
| Demonstration | Observe active D2R, completion results, GAP and the next Window. |
| 5 | Consume round results, update one plot output and clear only after success. |
| 6 | State acceptance and integration limits. |

Calculation helpers return values. Engine methods own state, queue and record writes.
prepare_scenario checks relationships; the constructor uses validate_energy_inputs before queue creation.
project_tag_operation preserves the existing current-plan projection and numeric guards; inactive segments use advance_tag_interval.
run_until collects all D2R completions before resource changes and new requests. Complete stored-energy admission remains unchanged.

## Data and lifetime

EngineScenario holds copied read-only indexes. EngineState holds current snapshots, phases and active plans.
EngineRecords holds current/latest-Window trace, pending Window starts, round summaries and round completion batches.
Each completed Window adds one endpoint summary per Tag. Repeated observations do not add energy-history samples.
GAP consumption/recovery carries forward; cleanup never refills the battery.

The caller chooses round end and calls finish_round(consume_results).
The consumer receives record copies. A successful call removes consumed prefixes; failure retains records for retry.
Open Window starts, active plans, current time/energy and queued events survive cleanup.
render_round updates the supplied dedicated display and closes its figure in finally. Reuse that display across rounds.
Only the latest plot remains in that display; no files are automatically written or deleted.
The endpoint plot does not reconstruct within-Window charging/depletion transitions. Single-round memory still scales with supplied inputs.

## Evidence and limits

18 independent pre-refactor snapshot/completion observations match. The full existing RL suite passes 463 tests.
Notebook 05 runs 13 code cells in a clean RL kernel with zero errors and shutdown.
Base focused checks pass 134 tests and skip two plotting checks when optional display dependencies are absent.
Detailed commands, review repairs and kernel receipts are in the scoped OpenSpec validation record.
Automated diagram checks and program checks do not establish human readability acceptance.

RF, selected Access timing, receive outcomes and explicit batch CW remain external inputs.
No complete CFA/SFS planner, ServiceManager, Policy/Baseline, FBL sampling or calibrated hardware is provided.
No Engine source extraction, publication or merge is claimed. Full STE dictionary conformance remains [Needs Verification].
