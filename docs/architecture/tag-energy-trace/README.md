# Tag charging design trace

[繁體中文](README.zh-TW.md)

Date: 2026-11-04. This is the accepted charging model traced before implementation.
The user authorized local-first Tag energy prototyping, then requested charging trace first.
The accepted core now resides in src/energy. Notebook 04 retains teaching, settings, tables, plots and independent assertions.
Notebook 05 imports the same source and accepts explicit batch CW inputs. Full Access scheduling and service accounting remain future work.

Read the [data-flow diagram](../../../.archify/dataflow-tag-energy-src-20261106-160000/tag-energy-src.html), then the worked example below and [source/status trace](code-trace.md).
The diagram describes the design. It does not assert that the displayed operations are existing runtime calls.

## Input to stored energy

1. Obtain the current serving Node, source direction, phase, duration and Tag snapshot.
2. Select serving UE RF for UL or serving DU RF for DL. Apply the accepted one-way gain.
3. Convert RF watts to DC watts through the accepted zero-input-corrected Sigmoid.
4. Permit UE-prefix harvesting, plus completed selected members during [own D2R_END, batch CW_OFF).
   Active D2R, switch, Paging, Guard and gaps have H=0.
5. Select one total mode power. Normal quiescent power is 10 nW; passive recovery has zero separate draw.
6. Integrate harvested minus consumed energy. Handle capacity overflow and explicit depletion, then record the new state.

No activation occurs merely to harvest or become eligible. Actual selected-operation activation is a later debit.
Do not use future harvest to admit an operation.

## Existing interfaces and missing adapter

The existing `build_timeline()` creates `NodeResource.direction` and the local UE end time.
The public `current_resource()` snapshot supplies occupancy and timing, but no UL/DL direction or source power.
A planned environment adapter must pass the current compatible source and phase to energy accounting.
It must not give Policy the full future timeline.

`channel.link_budget()` computes the Reader's two-way reflected received power.
It includes reflection loss and twice the one-way gain in dB. It is not the Tag's harvesting RF input.
DL harvesting instead uses P_DU*g0/(distance_m**2) in the accepted 1-50-m domain.
UL harvesting uses the accepted fixed UE power and synthetic -50-dB effective power gain.

## Worked UL example

Use a normal Tag at 0.8 uJ during a 400-ms permitted UL interval.
This is an in-run snapshot after earlier consumption; run initialization remains 1 uJ.

```text
P_UE = 20 dBm = 0.1 W
g_UL = 10^(-50/10) = 0.00001
P_RF = 0.1 * 0.00001 = 0.000001 W = 1 uW

M = 0.00001 W
s = 200000 W^-1
z = 0.00001 W
Omega = 1/(1+exp(s*z)) = 0.1192029220
L(P) = M/(1+exp(-s*(P-z)))
F(P) = (L(P)-M*Omega)/(1-Omega) = 0.2571323571 uW

Delta_t = 400000000 ns = 0.4 s
Harvested energy = 0.2571323571 * 0.4 = 0.10285294284 uJ
Consumed energy = 0.01 * 0.4 = 0.004 uJ
Next energy = 0.8 + 0.10285294284 - 0.004 = 0.89885294284 uJ
```

Use linear watts in the exponent. Mode budgets are electrical consumption; RF input is not itself battery credit.

| Independent 400-ms case | Initial uJ | Harvested uJ | Consumed uJ | Spill uJ | Final uJ |
|---|---:|---:|---:|---:|---:|
| Normal allowed UL | 0.8 | 0.102852943 | 0.004 | 0 | 0.898852943 |
| Normal allowed UL, near capacity | 0.95 | 0.102852943 | 0.004 | 0.048852943 | 1 |
| Passive recovery, allowed UL | 0 | 0.102852943 | 0 | 0 | 0.102852943 |
| Normal inter-Window gap | 0.8 | 0 | 0.004 | 0 | 0.796 |

These are separate examples, not a generated event calendar or successful service run.
A recovering Tag stays in recovery until a valid selected operation activates it under stored-energy admission.
A normal Tag with only 0.002 uJ in a 400-ms gap depletes after 200 ms at 10 nW.
It then remains at zero in passive recovery for the remaining 200 ms. Do not continue normal draw and conceal the deficit.

## Verification and next trace section

Run `python docs/architecture/tag-energy-trace/worked-example.py` from the product root.
The Decimal calculator checks the accepted DC result, passivity slope bound, capacity/energy balance and exact depletion example.
Its [JSON output](worked-example.json) is scalar arithmetic evidence, not simulator or hardware validation.
The graph delivery receipt records its own automated gates; those do not prove charging runtime behavior.

The original Notebook human trace is complete. The changed CW behavior remains subject to human trace.
Baseline remains deferred to the user's algorithm. No commit, push or remote completion is implied.
Hardware converter response, mode totals and ideal cold start remain research assumptions.

## Executable Notebook (2026-11-04)

Open [notebooks/04_tag_energy.ipynb](../../../notebooks/04_tag_energy.ipynb) for the executable teaching trace.
It contains the scalar conversion function, four interval examples, depletion, result tables, an embedded PNG and checks.
The full Access schedule and service adapters remain future work. The original core trace was accepted before extraction.
[Notebook dataflow](../../../.archify/dataflow-tag-charging-notebook-20261104-154316/tag-charging-notebook.html) describes this local prototype.
The earlier diagram remains the pre-implementation design snapshot.

## Scheduled state trace extension (2026-11-04)

The current [Notebook](../../../notebooks/04_tag_energy.ipynb) also shows seven Tag states and complete-operation admission.
Sections 11-13 define immutable snapshots, selected-operation accounting and inactive interval updates.
Sections 14-16 show success, refusal, depletion, permitted recharge and explicit reselection. Section 17 states the remaining boundary.
The [current state dataflow](../../../.archify/dataflow-tag-state-notebook-20261104-170000/tag-state-notebook.html) describes the local trace contract. Earlier diagrams remain historical views.

A selected 16-byte TB uses 63 ms D2R occupancy. The example adds 2 ms Paging, 1 ms waiting and 0.2 ms Guard.
The 1-ms wait is synthetic input, not an approved CFA offset. Complete cost is 66.012 nJ, including activation.
After allowed charging and RF switching, the example finishes at 0.83283094284 uJ.
Exact exhaustion after Guard returns ENERGY_RECOVERY; otherwise the operation returns SLEEP. Failure consumes the same full cost.

62 focused tests pass. A clean RL kernel executes 21 code cells with zero errors and saves two PNG outputs.
The state/energy PNG was inspected. These checks do not prove hardware accuracy or full simulator integration.
There are zero blocking state-model choices. Baseline, fairness and formal experiments remain three later research groups.
Full RF/timing adapters and service accounting remain engineering work. The 2026-11-06 extraction below supersedes pending extraction status.

## Source extraction and batch CW (2026-11-06)

The core previously lived in Notebook cells. Follow [the current source trace](code-trace.md) to find its new owners.
Read [the current flow](../../../.archify/dataflow-tag-energy-src-20261106-160000/tag-energy-src.html) before the Notebook 04 section 16.1 example. Earlier diagrams are historical.

| Owner | Responsibility |
|---|---|
| src/energy/contracts.py | Immutable Tag modes, snapshots and ledger results. |
| src/energy/tag_energy.py | RF/DC, complete admission, background recovery and completed-Tag CW. |
| Notebook 04 | Settings, explanations, tables, plots and independent assertions. |
| Notebook 05 | Explicit BatchCW validation, event ordering and current snapshots. |

The caller supplies batch identity, members and shared CW_OFF. Equal timestamps alone never define membership.
CW_OFF equals the final full member D2R completion. Guard begins there and has no batch CW.
An early completed member harvests while paying normal 10-nW draw until depletion. Existing passive recovery then applies.
Decoding failure does not cancel completed-transmission eligibility. Unselected and still-reflecting Tags receive no batch-CW credit.
The last-finishing member has zero tail. Future harvest never funds admission.

Use current-Window serving-DU CW power (-2/10/22 dBm), g0/distance_m**2 and the existing Sigmoid.
Distance remains 1-50 m. This is one-way RF, without reflection loss, two-way gain or Reader fading.
[The independent Decimal example](worked-cw-example.py) gives A=0.7343339972233599 uJ after Guard.
A starts at 0.8 uJ, uses 16 bytes and harvests for 55 ms at 10 dBm and 10 m.

The Notebook 05 adapter admits one supplied Paging start per explicit batch. It prepares all members before activation.
If any member fails admission, the whole declared batch is refused. This avoids retaining a refused final member's CW end.
Separate requests without a batch retain their prior no-tail behavior. This adapter is not a general batch scheduler.

Preserved behavior matches 13 pre-extraction traces. Focused energy/engine tests and clean kernels have separate receipts in OpenSpec.
The current CW correction awaits human trace. [Needs Verification] Shared CW conversion and path parameters are not hardware calibration.
