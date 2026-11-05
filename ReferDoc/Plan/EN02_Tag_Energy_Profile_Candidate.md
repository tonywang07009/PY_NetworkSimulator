# EN-02 Tag energy research candidate

Date: 2026-11-03. Profile: tag-energy-synthetic-v0.1. Status: ACCEPTED under Q-INFLUENCE-45 A; numerical research baseline, not hardware calibration.
The user requests usable numerical values for recursive Tag energy updates, similar to the selected WCSP paper.
This candidate supplies explicit research parameters. It does not claim a measured, fitted or standards-certified Tag.
R-01 sections 78-79 retain the accepted model form and source limits.

## Accepted numerical research profile

| Parameter | Accepted value | Basis and limit |
|---|---|---|
| Usable maximum energy E_max | 1 uJ = 10^-6 J | Chosen research buffer. Supports several admitted packets while exposing energy scarcity. Not the WCSP 1-mJ value. |
| Initial energy E_0 | E_max | Retains the accepted full-at-run-start rule. No later resets. |
| Quiescent/retention power P_q | 0.01 uW = 10 nW | Explicit research allowance for retention/control/PMU overhead; not a measured sleep value. |
| Paging receive power P_rx | 1 uW | Whole-mode research budget, using the approximately 1-uW Device-1 target as scale. Not a receiver measurement. |
| D2R power P_d2r | 1 uW | Whole-mode research budget including reflection control and associated digital activity; not just switch power. |
| Activation energy E_start | 1 nJ = 10^-9 J | Explicit research allowance per actual operation activation. No measured startup waveform or duration. |
| Sigmoid saturation M | 10 uW = 10^-5 W | Synthetic selection with the derivative bound below; not fitted hardware saturation. |
| Sigmoid slope s | 2*10^5 W^-1 | Synthetic selection; RF input is in W. |
| Sigmoid midpoint z | 10 uW = 10^-5 W | Synthetic selection; not a measured sensitivity threshold. |

All newly proposed numbers are research assumptions. External publications support mechanisms and scale, not this complete parameter vector.
Use one total mode power at a time. Do not add P_q on top of the stated P_rx or P_d2r totals.
Use P_q in harvesting, RF transition, waiting and Guard when no receive or D2R activity occurs.
Quiescent operation assumes retained timing/configuration at the proposed cost; this is not an electrically off state.
Depleted-state shutdown and restart follow the accepted EN-03 recovery section below.
Apply activation energy when an operation needs activation/preparation. Do not charge it per bit or again for every internal waiting gap.
If activation has already occurred and no new activation is needed, do not debit it twice.
No extra startup duration is introduced by this energy allowance; physical startup timing/peak power remain [Needs Verification].

## Source rationale and evidence boundaries

The selected WCSP paper supplies a 1-mJ initial/maximum energy setting and an aggregate reflection-consumption equation.
Its original values remain a literature comparison, not evidence for this 1-uJ capacity or mode powers.
Local TR 38.769 gives an approximately 1-uW peak Device-1 study target, not a measured constant mode table.
SIGCOMM 2013 reports 0.25-uW TX and 0.54-uW RX analog-component powers, excluding whole-device overhead.
Those values motivate caution about omitted digital/PMU costs. They do not derive our 1-uW totals.
ISSCC 2023 demonstrates communication-RF charging, capacitive storage and subsequent backscatter with separately reported operating powers.
Its 25-uW active chip is a different PHY and device profile. Do not substitute its powers into this Device-1 candidate.

Primary links:
- https://modernmobile.cs.washington.edu/docs/abc.pdf
- https://wcsng.ucsd.edu/files/LTE_harvesting_ISSCC2023.pdf
- https://arxiv.org/html/1509.02956

The chosen mode totals are budgets for the accepted coded PHY, not measured FEC/BPSK/SFS circuit costs.
The highest SFS chip rate can increase real switching costs. Constant P_d2r across SFS is a proposed abstraction, not hardware evidence.
Do not add an arbitrary second FEC cost to totals already defined to include digital activity.
Validate actual hardware, coding and clock implementation before claiming empirical energy accuracy.

## Complete passive conversion candidate

Retain the accepted zero-input-corrected Sigmoid:

```text
Omega = 1/(1+exp(s*z))
L(P) = M/(1+exp(-s*(P-z)))
F(P) = (L(P)-M*Omega)/(1-Omega), P>=0
```

For the proposed coefficients, Omega=0.11920292202211755.
For all P>=0, F'(P)<=M*s/[4*(1-Omega)]=0.5676676416183064<1.
Since F(0)=0 and F is nondecreasing, 0<=F(P)<=P globally. Also F(P)<=M.
This establishes mathematical passivity without clipping. It does not establish measured conversion efficiency.
At the accepted 1-uW UL RF input, F(P)=0.2571323570959774 uW.
At 10-uW RF input, F(P)=4.323323583816936 uW.
The low-input derivative tends to about 0.2384; no hard cold-start or sensitivity threshold is represented.
Conversion at very weak DL input is therefore an uncalibrated smooth-model assumption, not verified harvester behavior.
The accepted RF domain remains approximately -47.66 to -1.68 dBm, with UL at -30 dBm.
The entire curve is synthetic, including its saturation and unmeasured low-input tail.
Do not label these three parameters as a fit to the WCSP or 915-MHz rectenna measurements.

## Event-based energy recursion

Let H_j=1 only in the accepted UE-prefix harvesting interval; otherwise H_j=0.
Use the local serving-source RF input P_in,j and actual interval duration Delta_t_j in seconds.
Split intervals at source, mode, capacity or energy-feasibility events as needed.

```text
At an activation event:
    require E_j >= E_start
    E_after_start = E_j - E_start
Otherwise:
    E_after_start = E_j

During the following constant-source/mode interval:
    E_next = min(E_max,
                 E_after_start + (H_j*F(P_in,j) - P_mode,j)*Delta_t_j)
```

Activation debit occurs before future harvesting credit. Retain full-operation stored-energy admission, not just the startup check above.
Require enough stored energy for the complete planned operation, including applicable receive, waiting, D2R, Guard and activation costs.
A failed packet still consumes the complete actual transmission energy.
Do not hide underflow by applying max(0,E_next). Stop at depletion and apply the accepted EN-03 passive recovery rule outside admitted operations.
Use capacity saturation for storage overflow; excess harvest is discarded, not carried as future credit.
This accepted research ledger is not a simulator implementation. The recovery section below completes its first-version state rule.

## Scale checks

At 1-uW UL input over 400 ms in quiescent mode:

```text
Net gain = (0.2571323570959774 - 0.01) uW * 0.4 s
         = 0.09885294283839097 uJ
```

Thus E=0.100 uJ would become 0.19885294283839097 uJ if no activation occurs and capacity is not reached.
At zero RF input, the same interval loses 0.004 uJ while quiescent, provided enough energy remains.
This illustrates recursion; no 400-ms event is automatically added to the calendar.

Use the accepted rounded D2R occupancies for energy accounting:

| TBS bytes | D2R occupancy ms | D2R energy nJ at 1 uW |
|---|---|---|
| 8 | 35 | 35 |
| 16 | 63 | 63 |
| 32 | 118 | 118 |
| 64 | 228 | 228 |

For a scalar example, assume 2-ms receive, 10-ms waiting, one activation and 0.2-ms Guard.
This example does not select response timing or declare a feasible multi-Tag calendar.
Total costs for the four TBS options are 38.102, 66.102, 121.102 and 231.102 nJ.
At 100-nJ stored energy, the first two fit this example; the latter two do not.
Actual admission must use the actual calendar, receiver-on intervals and every other remaining mode interval.
The 1-uJ buffer therefore has a meaningful packet-scale range without requiring changes to TBS or duration.
The accepted seven-Tag/64-byte calendar restriction remains unchanged.

## Q-INFLUENCE-45: consolidated numerical research baseline

Facet: Influence, total 45; other facet counts unchanged. Answer: "a", accepted as A on 2026-11-03.
Purpose: select a complete numerical starting point without presenting unmeasured coefficients as hardware measurements.
A, recommended: adopt tag-energy-synthetic-v0.1 as displayed, including 1-uJ capacity and disclosed synthetic conversion/mode/activation values.
B: use the same candidate with E_max=E_0=1 mJ for WCSP capacity alignment; retain its other disclosed synthetic assumptions.
A exposes storage scarcity at packet scale. B aligns the paper's capacity but may hide energy constraints in short runs.
An optional custom answer can modify the profile or require hardware calibration before numerical acceptance.
Neither option establishes empirical accuracy. Recovery remains a separate unresolved decision.

## Verification

Scalar script /tmp/check-en02-candidate.py checks zero input, monotonicity, passivity and capacity saturation.
A derivative bound proves passivity for all nonnegative RF inputs, rather than only sampled points.
The script also checks 1001 positive RF inputs and all four TBS energy examples.
No simulator code/default changes, runtime integration, hardware measurements, commit, push or publication.

## Acceptance record

The user selected A (original answer: "a"). Adopt the complete tag-energy-synthetic-v0.1 profile displayed above.
The 1-mJ alternative is not selected. The existing filename remains stable for links.
All numerical evidence limits remain in effect. Runtime defaults and simulator code have not been changed.
EN-02 numerical configuration selection is closed for this baseline; calibration and implementation remain separate work.
Q-INFLUENCE-45 did not decide recovery. The subsequent Q-INFLUENCE-46 acceptance below supplies that rule.

## 2026-11-03 | Q-INFLUENCE-46 A accepted: ideal passive recovery

Original answer:
> A

When usable stored energy reaches zero outside an admitted operation, enter ideal passive recovery.
Disable receive, D2R and normal 10-nW quiescent operation. Recovery has zero separately modeled circuit draw and no additional cold-start threshold.
Keep only UE-prefix-permitted charging through the accepted F(P), with E_next=min(E_max,E+H*F(P)*Delta_t).
When H=0, recovery-state energy remains unchanged. Preserve accumulated energy and simulator service state; do not reset to full.
At legal Policy decisions, a recovered Tag is eligible only if stored energy covers a complete currently legal operation, including activation when needed.
Eligibility alone does not start reception, transmission or activation debit. A valid selected operation triggers the accepted activation and normal mode ledger.
If no complete legal operation fits, remain in recovery, even with positive accumulated energy.
Do not insert a new Policy call or autonomous transmission merely because a charging threshold is crossed.
Normal, non-recovery quiescent operation still costs 10 nW. The zero overhead applies only to the accepted ideal recovery state.
Split at actual depletion; do not conceal a negative-energy interval with lower-bound clipping.
Full-operation stored-energy admission still prevents mid-operation energy exhaustion under the accepted model.
Example: 400-ms allowed UL charging at 1-uW RF input stores 0.10285294284 uJ from zero before activation.
This differs from the normal quiescent net gain of 0.09885294284 uJ because recovery omits the separate 10-nW draw.
These are research assumptions, not measured cold-start or PMU behavior.
EN-03 first-version model selection is closed. Access/PHY/data/energy discussion choices are settled; implementation and calibration remain separate work.
