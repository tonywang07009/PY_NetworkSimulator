# Tag charging Notebook code trace

Capture: 2026-11-04. Root: /home/tonywang/Net_simluation/PY_NetworkSimulator.
Change: add-tag-charging-trace-notebook. Physical OpenSpec root: /home/tonywang/Net_simluation/PY_NetworkSimulator-agent-work/AgentDoc/openspec/changes/add-tag-charging-trace-notebook.
HEAD: c5fd4be80404e3765dffdbb5f94c61afdedfda52. This is an uncommitted working-tree prototype, not committed runtime evidence.
Human acceptance, extraction and remote delivery remain pending. No archive path exists.

## Actual scoped tree

```text
/home/tonywang/Net_simluation/PY_NetworkSimulator/
├── agent.md                              # Existing project rules
├── README.md                             # Added Notebook link
├── README.zh-TW.md                        # Matching Chinese link
├── notebooks/
│   └── 04_tag_energy.ipynb                # Charging and scheduled state traces; core retained here
├── tests/energy/
│   ├── test_tag_energy_notebook.py        # New public-definition/output checks
│   └── execute_tag_energy_notebook.py     # New isolated-kernel runner
└── docs/architecture/tag-energy-trace/
    ├── README.md                         # English guide and Notebook link
    ├── README.zh-TW.md                    # Chinese guide and Notebook link
    ├── code-trace.md                      # This source/status map
    ├── worked-example.py                  # Existing independent Decimal diagnostic
    └── worked-example.json                # Existing independent expected values
```

The product AgentDoc/.agents/.archify links navigate to the agent worktree.
The change owns proposal.md, design.md, specs/tag-charging-trace/spec.md, tasks.md, validation.md, kernel-execution.json and this trace copy.
Planned general runtime paths src/energy and the full Energy/Engine remain absent. No core extraction is claimed.

## Files and ownership

| Actual path | Responsibility/status |
|---|---|
| [notebooks/04_tag_energy.ipynb](/home/tonywang/Net_simluation/PY_NetworkSimulator/notebooks/04_tag_energy.ipynb) | New; sections 2-4 own accepted settings and harvested_power_w. Sections 5-10 own phase table, explicit energy examples, plot and assertions. |
| [tests/energy/test_tag_energy_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/test_tag_energy_notebook.py) | New; loads tagged definitions, tests reference DC, input bounds, passive behavior, extreme integer rejection, compilation and saved PNG output. |
| [tests/energy/execute_tag_energy_notebook.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/tests/energy/execute_tag_energy_notebook.py) | New; temporary RL kernel, complete execution, error/image checks, shutdown and write-on-success. |
| [docs/architecture/tag-energy-trace/worked-example.json](/home/tonywang/Net_simluation/PY_NetworkSimulator/docs/architecture/tag-energy-trace/worked-example.json) | Unchanged independent scalar reference predating the Notebook; not regenerated from new code. |
| [README.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/README.md) and [README.zh-TW.md](/home/tonywang/Net_simluation/PY_NetworkSimulator/README.zh-TW.md) | Modified; matching entry links and pending-acceptance labels. |
| [src/timeline/resource_timeline.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/timeline/resource_timeline.py:65) | Unchanged supporting context; current projection omits direction/source power. No new energy calls. |
| [src/channel/channel_model.py](/home/tonywang/Net_simluation/PY_NetworkSimulator/src/channel/channel_model.py:71) | Unchanged supporting context; two-way Reader receive budget is not reused as harvesting RF. |

## Requirement to behavior

1. Notebook section 3 converts 20-dBm UE power and -50-dB one-way gain to 1-uW RF, using explicit local inputs.
2. Section 4 validates finite SI inputs, passive shape bounds and stable zero-corrected conversion. Tests call this tagged public definition.
3. Sections 5-7 apply explicit phase gates and named interval calculations, comparing normal, saturated, recovery and gap cases.
4. Section 8 splits the exact depletion example. It does not introduce a general event scheduler or fractional-ns runtime policy.
5. Section 9 embeds a real PNG; section 10 checks prior JSON, literal values and energy balance.

The general Engine, full source adapter and Baseline remain later work.
The authorized extension below adds immutable snapshots, operation admission and selected activation locally in the Notebook.
The Notebook contains a scalar conversion implementation; its explicit interval arithmetic is not a general mutable energy engine.

## Verification

24 focused tests passed. A clean RL kernel executed all 13 code cells with zero errors, saved one PNG and shut down.
See the change validation.md and kernel-execution.json for exact commands and environment.
The two-panel PNG was inspected. Notebook local links and paired guide links were checked.
Human acceptance and hardware calibration are not established by these checks.

## Current state extension

The earlier 24-test/13-cell result records the original scalar delivery. Current evidence is 62 tests and 21 executed code cells.
The current kernel shuts down with zero errors and saves two embedded PNGs. The state/energy plot was inspected.

| File / section | Requirements and tests |
|---|---|
| notebooks/04_tag_energy.ipynb sections 11-13 | TagMode, frozen snapshots/results, trace_tag_operation and advance_tag_interval own state accounting. |
| Same Notebook sections 14-16 | Success, full-cost failure, atomic refusal, recovery and reselection; tables, state/energy PNG and literal assertions. |
| tests/energy/test_tag_energy_notebook.py | Energy/time admission, legal TBS occupancy, deadline/Guard, no mutation, phase gates, capacity, depletion and numeric range. |
| tests/energy/execute_tag_energy_notebook.py | Unchanged isolated-kernel runner executes all 21 code cells and saves outputs on success. |
| docs/architecture/tag-state-design.md | Accepted state/energy meaning; complete Engine remains outside this trace. |

All paths above are relative to the absolute product root in the tree. Notebook and test absolute links are in the ownership table.
Snapshots are values; callers own their replacement. Invalid operations return no partial trace and mutate no supplied Tag.
The operation checks CW availability, stored cost, full Window occupancy and exclusive D2R deadline before WAKING.
Background rows label their starting mode. Depletion offsets describe the internal split; a whole interval must not be read as one state.
No automatic wake-up follows charging. Recovery can re-enter WAKING only through explicit valid selection.
The [current dataflow](../../../.archify/dataflow-tag-state-notebook-20261104-170000/tag-state-notebook.html) is a local contract view, not committed repository evidence.
