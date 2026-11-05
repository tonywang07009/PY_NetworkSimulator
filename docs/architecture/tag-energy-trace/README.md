# Tag charging design trace

[繁體中文](README.zh-TW.md)

Date: 2026-11-04. This is the accepted charging model traced before implementation.
The user authorized local-first Tag energy prototyping, then requested charging trace first.
The executable Notebook now implements charging and scheduled state traces. The complete charging runtime and its adapters remain future work.

Read the [data-flow diagram](../../../.archify/dataflow-tag-charging-20261104-151852/tag-charging.html), then the worked example below and [source/status trace](code-trace.md).
The diagram describes the design. It does not assert that the displayed operations are existing runtime calls.

## Input to stored energy

1. Obtain the current serving Node, source direction, phase, duration and Tag snapshot.
2. Select serving UE RF for UL or serving DU RF for DL. Apply the accepted one-way gain.
3. Convert RF watts to DC watts through the accepted zero-input-corrected Sigmoid.
4. Permit harvesting only during the UE prefix. Switch, Paging, D2R, Guard and gaps have H=0.
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

The Notebook and its OpenSpec/TDD contract now exist; human acceptance is the next module checkpoint.
Baseline remains deferred to the user's algorithm. No source extraction, commit, push or remote completion is implied.
Hardware converter response, mode totals and ideal cold start remain research assumptions.

## Executable Notebook (2026-11-04)

Open [notebooks/04_tag_energy.ipynb](../../../notebooks/04_tag_energy.ipynb) for the executable teaching trace.
It contains the scalar conversion function, four interval examples, depletion, result tables, an embedded PNG and checks.
The full Tag state/operation engine and source adapters remain future work. The Notebook awaits human acceptance.
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
RF/timing adapters and service accounting remain engineering work. Human acceptance and source extraction remain pending.
