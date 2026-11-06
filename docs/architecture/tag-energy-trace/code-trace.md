# Tag energy source trace

Date: 2026-11-06. Product root: `/home/tonywang/Net_simluation/PY_NetworkSimulator`.
Authority: `add-tag-charging-trace-notebook`, Q-CW-01 through Q-CW-05, R-01 section 93.
The original Notebook human trace is complete. Extraction is authorized; the changed CW behavior awaits human trace.
This describes the local working tree. No commit, remote delivery or archive is claimed.

## Reading tree

```text
/home/tonywang/Net_simluation/PY_NetworkSimulator/
├── src/energy/
│   ├── contracts.py                    # TagMode, frozen snapshots and ledger DTOs
│   ├── tag_energy.py                   # Conversion, admission, background and CW tail
│   └── __init__.py                     # Public energy exports
├── notebooks/
│   ├── 04_tag_energy.ipynb             # Settings, formulas, tables, plots and checks
│   └── 05_event_engine.ipynb           # Source caller; explicit BatchCW and current state
├── tests/energy/
│   ├── fixtures/energy-before-extraction.json  # 13 original Notebook traces
│   ├── test_tag_energy_extraction.py   # Source baseline and new CW boundaries
│   ├── test_tag_energy_notebook.py     # Original behavior through imported definitions
│   └── execute_tag_energy_notebook.py  # Independent temporary-kernel runner
├── tests/event_engine/test_event_engine_notebook.py
└── docs/architecture/tag-energy-trace/
    ├── worked-example.py / .json       # Original independent scalar reference
    ├── worked-cw-example.py            # Independent Decimal CW reference
    ├── README.md / README.zh-TW.md     # Paired guides
    └── code-trace.md                   # This reading map
```

## Requirements, source and tests

Each source link is absolute. Its label gives the repository-relative path.

| Source | Responsibility / requirement | Evidence |
|---|---|---|
| [src/energy/contracts.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/energy/contracts.py) | Seven modes and immutable isolated snapshot/results. Integer ns and SI energy. | Existing state, no-mutation and source-baseline tests. |
| [src/energy/tag_energy.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/energy/tag_energy.py) | `harvested_power_w`: unchanged passive zero-corrected Sigmoid and validation. | Original conversion tests; independent worked-example.json. |
| Same core, `trace_tag_operation` | Validate full stored energy, strict D2R deadline and complete Window/Guard before debit. Preserve whole TBS and no refund. Optional explicit CW ends at common CW_OFF. | Original admission tests; source baseline; failed reception, future-energy refusal and common-Guard tests. |
| Same core, `advance_tag_interval` | Inactive accounting; normal draw, diagnostic depletion, recovery, capacity and spill. `POST_TBS_CW` requires externally established completed-member eligibility. | Recovery, balance, phase, saturation and source CW tests. |
| Same core, `cw_rf_input_w` | Serving-DU -2/10/22-dBm one-way RF at 1-50 m; no reflected Reader power. | Six power/distance endpoint cases and independent Decimal CW example. |
| [src/energy/__init__.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/energy/__init__.py) | Public contracts and accounting exports. | Source import and preserved-trace checks. |
| [notebooks/04_tag_energy.ipynb](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/04_tag_energy.ipynb) | Sections 4, 11-13 import source; settings, formulas and plots stay local. Section 16.1 adds an explicit two-member example. | 22 clean-kernel code cells; original assertions plus independent CW literals. |
| [notebooks/05_event_engine.ipynb](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/05_event_engine.ipynb) | Import source; external BatchCW identity, members, common CW_OFF and geometry. Prepare all plans before activation; project inactive tail/Guard with the shared integrator. | Event tests: unequal/equal completions, unselected/active/failure, refusal, boundaries, segmented saturation/recovery and insertion order. Seven clean-kernel cells. |
| [tests/energy/test_tag_energy_extraction.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/test_tag_energy_extraction.py) | Preserve independently captured original behavior; check approved CW correction. | Missing-source RED, then baseline and new boundary GREEN. |
| [tests/energy/test_tag_energy_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/test_tag_energy_notebook.py) | Execute tagged source imports through the teaching Notebook. | Existing 62 tests remain. |
| [tests/event_engine/test_event_engine_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/event_engine/test_event_engine_notebook.py) | Exercise actual Engine caller entry. | No source-only substitute for batch/event checks. |
| [tests/energy/execute_tag_energy_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/execute_tag_energy_notebook.py) | Execute 04 or 05 in an isolated temporary kernel; save only on success. | RL receipts under the scoped OpenSpec change. |
| [docs/architecture/tag-energy-trace/worked-cw-example.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/docs/architecture/tag-energy-trace/worked-cw-example.py) | Recompute the new scalar expectation independently of runtime imports. | A final after Guard: 0.7343339972233599 uJ. |

## Call and time flow

```text
Notebook settings + TagSnapshot
  ├─ advance_tag_interval
  │    └─ validate -> RF/DC -> mode draw/depletion -> capacity/spill -> new snapshot
  └─ trace_tag_operation
       ├─ validate full TBS, stored energy, deadline, common CW/Guard Window
       ├─ refuse without changing the input, or debit activation + Paging + wait + full D2R
       ├─ own D2R_END < CW_OFF: inactive POST_TBS_CW using one-way RF
       └─ CW_OFF -> unpowered Guard -> new snapshot + immutable ledger

Notebook 05 explicit BatchCW + member OperationRequest values
  ├─ validate identity, Node/Window, exact membership and final member D2R end
  ├─ one supplied Paging start; prepare all member plans before activation
  ├─ collect each complete D2R result; failed decoding does not cancel CW eligibility
  └─ run_until: project active cost or integrate completed tail/Guard at current time
```

No-batch callers retain their original immediate Guard and no CW tail.
Unselected Tags use ordinary phase accounting. Mere inactivity never grants batch membership.
Future CW energy is excluded from admission. Normal tail draw is 10 nW until depletion; charging alone creates no new state.
Batch Guard starts at the final D2R completion. Outer Window slack is not CW availability.

[Current flow diagram](../../../.archify/dataflow-tag-energy-src-20261106-160000/tag-energy-src.html) describes this local contract.
Its automated artifact/browser checks do not prove hardware accuracy or human readability acceptance.
Full Access scheduling, service accounting, FBL sampling and Baseline remain outside this extraction.
