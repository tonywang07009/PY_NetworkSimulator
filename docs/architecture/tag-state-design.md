# Tag state design: scheduled activation adaptation

Date: 2026-11-04. Authority: Q-INFLUENCE-51 A, R-01 section 91 and the accepted energy profile.
This adapted design now has an executable scheduled-state trace in notebooks/04_tag_energy.ipynb.
The general Engine and environment adapters remain outside this prototype.
The user chooses PScatter's state separation with existing activation/time budgets. No new radio wake-up procedure is added.

## States and energy meaning

| Tag state | Control meaning | Energy treatment |
|---|---|---|
| STATIC | No current communication operation; await a valid selection. | Normal quiescent 10 nW. |
| WAKING | A valid admitted operation needs activation/preparation. | Debit 1 nJ once when needed. No new state duration or packet is defined. |
| PAGING_RX | Receive the addressed CFA Paging during the supplied receiver-on interval. | Total receive power 1 uW. |
| WAIT_D2R | Retain the assigned response timing before D2R starts. | Quiescent 10 nW. It does not implement PScatter PSS synchronization. |
| BACKSCATTER | Execute the selected complete-TB transmission. | Total D2R power 1 uW for full accepted occupancy; failure does not refund energy. |
| SLEEP | Retain state between communication opportunities or during waiting/Guard context. | Normal quiescent 10 nW; Sleep is not the zero-overhead recovery state. |
| ENERGY_RECOVERY | Usable stored energy has depleted outside a completely admitted operation. | Zero separate recovery-circuit draw; only phase-permitted F(P_RF) charges storage. |

STATIC and SLEEP can share a numerical power while describing different control reasons for inactivity.
WAKING is an energy event, not an invented constant-power interval. Do not infer a physical peak or extra latency from 1 nJ alone.
The existing one-time initialization remains E_0=1 uJ; state transitions never refill the battery.

## Transition trace and guards

| From | Required event/guard | To/action |
|---|---|---|
| STATIC or SLEEP | Existing legal decision selects a permitted Tag/TBS operation; complete time and stored-energy cost fit. | WAKING if activation is needed; otherwise use the existing active operation context. |
| ENERGY_RECOVERY | At a legal decision, a valid selected operation fits including applicable activation. | WAKING; debit activation only on actual selection. Otherwise remain in recovery. |
| WAKING | Existing activation debit completes and scheduled Paging receiver-on interval starts. | PAGING_RX. No additional wake-up packet or PHY duration. |
| PAGING_RX | The addressed CFA Paging completes; existing assigned D2R timing is retained. | WAIT_D2R. No independent random Paging-error model is added. |
| WAIT_D2R | The supplied response start arrives and the accepted external CW condition holds. | BACKSCATTER. Do not start early when energy rises. |
| BACKSCATTER | Full scheduled D2R occupancy completes, regardless of receive success. | SLEEP while the batch/Guard or next opportunity is pending; return to STATIC when no current communication work remains. |
| Any normal inactive state | Energy reaches zero during background accounting. | ENERGY_RECOVERY at depletion; stop ordinary quiescent draw. |

Becoming energy-eligible alone does not activate, transmit or trigger another Policy call.
The local scheduled-activation abstraction is not evidence that a physical Tag has an implemented wake-up detector or foreknowledge of the Policy.
Receiver-on intervals and D2R times are supplied by the Access/Engine calendar; do not fabricate durations in the state machine.
For an admitted operation, reserve all activation, receive, waiting, D2R and required Guard costs before WAKING.
A failure in D2R changes the receive/data result, not the already-executed state duration or consumed energy.

## State and resource phase are separate inputs

Use P_har=H_phase*F(P_RF), with the current state selecting one applicable electrical cost.
H_phase=1 in the UE prefix or for a selected completed Tag during [own D2R_END, batch CW_OFF).
H_phase=0 during switch, Paging, active D2R, Guard and inter-Window gaps.
A normal sleeping Tag can harvest during an allowed UE prefix and still pay 10 nW.
A sleeping Tag in the 400-ms gap cannot harvest and still pays 10 nW until depletion.
An ENERGY_RECOVERY Tag in that gap stays at its current energy, with no separate recovery draw.
Guard is a batch/resource phase. It need not become another independent high-power Tag state.

## Symbolic worked trace

Start from the existing in-run example: E=0.8 uJ, then allowed 400-ms UL input at 1 uW RF.
Normal quiescent charging gives E=0.89885294284 uJ. This is the previously checked scalar example, not a new run initialization.
Suppose a subsequent complete operation has already passed stored-energy and calendar admission:

```text
SLEEP/STATIC
  -> WAKING: subtract 0.001 uJ once if activation is needed
  -> PAGING_RX: subtract 1 uW * actual receiver-on duration
  -> WAIT_D2R: subtract 0.01 uW * actual waiting duration
  -> BACKSCATTER: a selected 16-byte TBS subtracts 0.063 uJ over 63 ms
  -> SLEEP: retain remaining energy and pay the required normal Guard/waiting costs
```

Active post-UE phases and Guard have zero harvest. An early completed selected Tag can harvest before batch CW_OFF. The 16-byte TB has at most 14 valid application bytes.
The example fixes no new Paging, response-offset or synchronization duration.
A selected 64-byte TBS still needs full timing and energy admission; state adaptation does not make it automatically feasible.

## Implementation boundary

Keep notebooks/04_tag_energy.ipynb as the executed scalar trace until a scoped state-machine implementation is prepared.
The next implementation design must pass actual phase/time inputs, isolate per-Tag state and test rejected activation without partial mutation.
No new Baseline, UE relay, PSS algorithm, measured power profile, source extraction or remote delivery is authorized by this state adaptation alone.
Human acceptance of the current Notebook and implementation of this state design remain separate evidence.

## Research rationale for supervisor discussion (2026-11-04)

The user accepts an assumed configuration that can be explained to the supervisor.
Explain each assumption through its source, selection reason and evidence limit. This does not establish hardware calibration.

| Assumption | Defensible selection reason | Claim boundary |
|---|---|---|
| PScatter-inspired control states | Separate Paging reception, waiting and backscatter so energy follows actual activity. | Adapted state design, not reproduction of PScatter's UE relay or hardware. |
| 1-uW receive/D2R totals | Use the already selected Device-1 study scale for a controlled research budget. | Not measured mode powers or a demonstrated circuit peak. |
| 10-nW quiescent power | Retain a nonzero background cost while distinguishing inactivity from reception/backscatter. | Synthetic retention/PMU allowance, not measured sleep power. |
| 1-uJ usable buffer | Comparable to a few 228-nJ pure 64-byte D2R costs; expose energy/TBS interaction without a 1-mJ initially full store dominating a short run. | Full operations also include activation, reception, waiting and Guard; do not promise a fixed packet count. |
| 1-nJ activation event | Retain a fixed nonzero operation-start overhead without adding an unselected radio procedure. | No measured startup waveform, peak or added latency. |
| Corrected Sigmoid parameters | Make zero input yield zero output and satisfy a global passive-conversion bound. | Mathematical consistency, not measured converter efficiency. |
| Ideal passive recovery | Keep an explicit depletion/recharge baseline while avoiding uncalibrated cold-start circuitry. | An optimistic abstraction at weak RF input, not hardware behavior. |

Use the same declared parameter snapshot across compared policies; report scope-specific conclusions.
EX-01 sensitivity analysis remains future evidence. Do not claim algorithm rankings are robust before those comparisons are performed.
No numerical parameter, deadline, power profile or state choice is changed by this explanation criterion.

## Accepted post-TBS correction and extraction (2026-11-06)

This section supersedes the earlier implementation boundary. The original Notebook trace is accepted and the core resides in src/energy.
The new CW behavior still needs human trace. See tag-energy-trace/code-trace.md for source owners and checks.
Q-CW-01 through Q-CW-05 establish explicit batch membership and CW_OFF, normal background draw, and one-way serving-DU CW input.
Guard begins at batch CW_OFF, not at each member's completion. Last-finishing members have no remaining CW interval.
Only complete selected transmissions qualify, including decoding failure. Unselected and still-reflecting Tags receive no CW credit.
Future harvest grants no admission credit. Charging alone creates no new state.
