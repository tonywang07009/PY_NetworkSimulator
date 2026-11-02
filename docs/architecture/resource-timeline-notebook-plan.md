## Implementation update (2026-10-31)

The Notebook core, demonstrations, tables/plot, explicit export, behavior tests and clean-kernel runner are now implemented. Earlier scaffold-only status below is historical. The user accepted the Notebook on 2026-11-02. Core code now lives in src/timeline; the Notebook imports it.

# Resource timeline Notebook prototype plan

Date: 2026-10-31. Status: Design preparation only; no next-change implementation or specification has started.
Artifact: [notebooks/03_resource_timeline.ipynb](../../notebooks/03_resource_timeline.ipynb). The initial scaffold now exists; core behavior is not implemented.
The user requested starting the Notebook design. Existing accepted resource decisions remain in force.

## Learning goal and scope

The reader can explain how a common 600 ms interval becomes different per-Node UE and Tag intervals.
The reader can change explicit scenario starts and seed, then inspect the resulting tables and plot.
The reader can distinguish full environment truth from a current resource observation.

Use the existing topology for Node identities. Do not create another topology implementation.
The prototype generates resource intervals; it does not implement a global simulation engine or execute Tag packets.
Energy consumption, service credit, CFA scheduling and Baseline/CLM are outside this prototype.
Channel integration demonstrates shared window identity only; it does not claim an end-to-end scheduler.

## Source map

| Source | Use in the Notebook |
|---|---|
| [Original System Model](../../ReferDoc/Plan/main.pdf), pp.10–11 | UE-before-Tag sequence and time containment |
| [Decision record](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md), §34.6–34.11 | Every-window UE, uniform ratio, rounding, direction, shared windows and independent draws |
| [Integrated resource design](resource-timeline-design.md) | Data ownership, reveal boundary and channel lifetime |
| [Resource draft](../../Plan/resource-timeline-draft.md) | Candidate acceptance scenarios and numerical limits |
| [Channel model](../../src/channel/channel_model.py) | Existing current-window API; do not duplicate it |

The local original is /home/tonywang/115-1/system_model_mod/version_1/main.pdf.
The project copy has the same SHA-256, recorded in Plan/design-resumption.md.
The source diagram does not specify the later UL/DL probabilities or UE duration distribution; label those as accepted simulator assumptions.

## Proposed reading and cell sequence

Each numbered unit has a Markdown explanation before its code cell or cells.
Markdown gives purpose, units, source, expected observation and important limits.
Final cell count can change for clarity; these are teaching units, not empty cells to generate mechanically.

| Unit | Planned code responsibility | Reader-visible result |
|---|---|---|
| 0. Purpose and boundary | Markdown only | Source layers and implementation status |
| 1. Load accepted topology | Import existing iab module and obtain Node IDs | Five Node identities |
| 2. Define resource data | Minimal frozen config/snapshot records and direction enum in the prototype definitions section | Units and visibility table |
| 3. Validate scenario input | Reject invalid IDs, seed types and inconsistent outer starts | Reasons without a partial trace |
| 4. Explain independent draws | Stable seed identities by Node/window/kind | Repeatability and legal coincident outcomes |
| 5. Build resource intervals | Uniform duration draw, ceil to ms, conversion to ns, direction draw | Immutable resource snapshots |
| 6. Prepare display tables | Derive rows from snapshots | Window summary and per-Node details |
| 7. Plot timing | Plot UE prefixes and Tag remainders from those same snapshots | Shared boundaries and differing Tag starts |
| 8. Run a small scenario | Explicit starts and seed in the editable settings cell | Tables and timing plot |
| 9. Inspect current visibility | Stateless current-resource projection driven by supplied now_ns | Before UE end, during Tag time and at outer end |
| 10. Compare boundary cases | Controlled boundary inputs and expected values | Rounding and half-open interval checks |
| 11. Compare query order | Generate the same identity set in different traversal orders | Same normalized trace; unchanged global RNG |
| 12. Demonstrate channel handoff | Use one existing ChannelModel window per shared outer ID | Same per-Node link result within a window |
| 13. Export optional results | Explicit export cell with overwrite notice | Snapshot JSON, table CSV and timing PNG/SVG |
| 14. Acceptance recap | Summarize assertions and limits | Human review entry; no automatic human acceptance |

## Editable scenario example

Use an explicitly labelled synthetic fixture with outer starts at 0 and 800000000 ns, and seed 42.
With fixed 600 ms duration, the outer intervals are [0,600) and [800,1400) ms.
The 200 ms gap is an example input, not a default or a research distribution.
Actual sampled directions and durations must come from execution; do not print invented results as observed output.

Use Node IDs from the accepted topology and tuple-valued collections.
Missing starts produce an input error; do not generate a period implicitly.
Treat an empty start sequence as an invalid demonstration scenario in this proposed prototype.
This refusal is a proposed engineering contract, not an existing executed test result.

Do not include a full-run deadline setting in the minimum resource generator.
The engine will later supply the run boundary. The prototype may illustrate batch-fit checks with explicit caller limits.
Do not let this demonstration silently decide unfinished run-end cleanup semantics.

## Proposed data and interface shape

| Data group | Proposed contents |
|---|---|
| Scenario config | scenario_id, schema/profile version, seed, node_ids tuple, window_starts_ns tuple |
| Fixed accepted profile | 600000000 ns window, ratio range 0.60–0.75, 1 ms ceiling grid, equal UL/DL probabilities |
| Per-Node window record | node_id, window_id, start_ns, ue_end_ns, end_ns, direction, raw duration draw, rounded duration |
| Outer snapshot | Shared ID and bounds, immutable tuple of per-Node records |
| Current projection | node_id, window_id, now_ns, current eligible Tag interval and status |

Names are design candidates; do not add field-selection questions when the existing contract suffices.
Keep the accepted numerical profile visible, rather than exposing arbitrary configuration options for every constant.
Separate pure validation, generation, table/plot output and current-resource projection.
The projection receives time from its caller; it does not advance or own a clock.
No future snapshot or complete trace is returned in the policy-facing projection.
Keep full trace access as an environment/evaluation concern, not as a field of that projection.
This is a data/API isolation boundary, not a Python sandbox against hostile code.

## Time arithmetic

For a shared start s and ratio draw r:

- UE duration in ms is ceil(600*r).
- UE duration in ns is that integer multiplied by 1000000.
- UE interval is [s,s+duration_ns).
- Tag interval is [s+duration_ns,s+600000000).

A 398.2 ms pre-rounding value gives 399 ms, then 399000000 ns; the Tag budget is 201 ms.
Use that value as an independent expected arithmetic example, not as an asserted seed-42 draw.
Continuous uniform sampling plus ceiling is not integer-uniform sampling.
Do not redraw equal durations, equal directions or equal outputs across windows.

## Table and plot design

The window summary contains ID, start, end and the gap before each window.
The Node table contains direction, UE duration, Tag start and Tag budget for each Node/window.
Store ns as integers; display ms for reading without feeding display values back into calculations.
Use horizontal bars: one row per Node, separate UE and Tag colours, direction labels and shared boundary markers.
An outer gap stays blank or is explicitly marked unavailable; do not draw it as Tag time.
The plot shows resource availability, not completed payload or measured traffic.
Tables, plots and exports must use the same snapshot.

## Validation and planned tests

Test the prototype's public generation/projection boundary. Do not test only its private helper implementation.
Use the same external behavior tests after eventual extraction.

| Behavior | Boundary or expected result |
|---|---|
| Profile arithmetic | 0.60 → 360 ms; 0.75 → 450 ms; 398.2 ms → 399 ms |
| Start input | First start 0; starts increase; each next start is at least previous end; zero gap permitted as explicit input |
| Invalid input | bool/float timestamps, negative values, duplicate Node IDs, list instead of tuple and missing starts rejected |
| Half-open resource | UE end belongs to Tag resource; outer end is outside that resource |
| Unequal Nodes | Same outer interval can have different UE end times without overlapping UE and Tag on a Node |
| Random identity | Same inputs reproduce results; reordered Nodes or policy RNG calls do not change normalized resource results |
| Legal coincidences | Matching direction or duration does not trigger redraw or failure |
| Projection isolation | Current projection does not contain future windows or mutable truth aliases |
| Channel handoff | One current shared ID; repeated per-Node link queries do not change within-window quality |
| Plot/export consistency | Displayed intervals and stored rows match the generated snapshot |

Input errors must identify the violated field or condition and must not publish a partial resource trace.
Rounding tests must address floating-point values immediately below, at and above an integer-ms boundary.
Do not silently clamp an invalid duration. Proposed numeric representation must preserve the selected sampling-and-ceiling meaning.
Large integer timestamps must not be converted to float for membership checks.
A short example cannot establish an observed 50/50 frequency; test the probability rule separately from a small display fixture.

## Prototype and later extraction routes

Planned prototype: notebooks/03_resource_timeline.ipynb.
Planned behavior tests: tests/timeline/test_resource_timeline_notebook.py.
Planned clean-kernel runner: tests/timeline/execute_resource_timeline_notebook.py.
The Notebook path now contains the initial scaffold. The two test/runner paths remain proposals and have not been created.
Core definitions remain in the Notebook until human understanding and acceptance.
After acceptance, propose compatible src paths and centralized contracts; do not pre-extract or move existing channel/IAB types in this design task.
Before trace, provide actual source paths, requirements/tests and updated architecture; planned paths are not runtime evidence.

## Workflow boundary

The active channel change is still 9/10 and has no observed channel PR merge evidence.
The workflow permits downstream scope/design planning, but next-change specification and implementation wait for the serial delivery gate.
The user subsequently requested creating the original .ipynb file after reporting delivery alignment. The scaffold contains teaching text, accepted constants and unimplemented code cells; no functional resource generator or new workflow is created.
No diagram or test-plan approval is inferred from file generation.
Implementation later needs scoped OpenSpec acceptance, TDD RED/GREEN, a clean kernel run and human trace under the existing project process.


## Complete-code handoff before acceptance

The user requested complete corresponding code before the Notebook acceptance walkthrough, so they can trace the logic in one coherent delivery.
Before presenting this prototype for human acceptance:

1. Complete the in-scope core definitions, demonstrations, tables, plots and explicit exports.
2. Complete behavior assertions and the clean-kernel run; report actual results and remaining limits.
3. Update the architecture and absolute-path code trace against the implemented cells and tests.
4. Present the runnable Notebook and corresponding code/test evidence together for the walkthrough.

The current scaffold is not acceptance-ready. Do not ask the user to accept empty cells or an incomplete core.
This handoff requirement does not move core code to src before human acceptance or authorize unspecified features.
