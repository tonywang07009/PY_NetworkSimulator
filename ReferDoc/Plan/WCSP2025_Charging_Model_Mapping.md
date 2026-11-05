# User-selected WCSP charging model: extraction and simulator mapping

Date: 2026-11-03. Status: original PDF inspected; zero-input-corrected Sigmoid accepted under Q-INFLUENCE-44; numerical energy profile remains open.
The user requests the charging-model form, not automatic adoption of the paper's algorithm, all coefficients or factory scenario.

## Original source and trace

Title: Throughput Optimization for Ambient IoT Systems in Indoor Factory Environments.
Authors: Tianxiao Zhang and Yong Li, Beijing University of Posts and Telecommunications.
Venue: 2025 Seventeenth International Conference on Wireless Communications and Signal Processing (WCSP).
DOI: 10.1109/WCSP68525.2025.1010215.
[Publisher record](https://ieeexplore.ieee.org/abstract/document/11352069).

User-provided original:
/home/tonywang/Downloads/Throughput_Optimization_for_Ambient_IoT_Systems_in_Indoor_Factory_Environments.pdf

SHA-256: 74aa84fa8e9628558bac2e8571c78c2bbe6e2b5e3b605434fc5e81531a647416.
Six PDF pages, 1138181 bytes. Original remains at the supplied path; no licensed PDF was copied into product or agent records.
Text extracted with /usr/bin/pdftotext. Equations on PDF pages 2-3 and Table I on PDF page 5 were visually checked.
This resolves the earlier full-text access limit in R-01 section 76.

## Paper model, without silent correction

PDF page 2, section II-B, equation (3):

```text
L(P_in) = M / (1 + exp(-s*(P_in-z)))
P_har(n,t) = L(P_in(n,t))
```

M is the asymptotic harvested-power limit, s controls slope and z is the midpoint/turn-on parameter.
Mathematically z gives L(z)=M/2; it is not a hard zero-output threshold.
P_in is RF input power; use a declared linear power unit, not dBm inside this exponent.
For SI implementation M and z have W units, s has W^-1 units and L outputs W.
The paper describes fitting M,s,z to the chosen harvester's measured input/output characteristics.

PDF page 2, equation (4): P_con(n,t)=alpha*g_n*p_n(t).
This is the paper's reflection-consumption abstraction. It is not automatically our Tag mode-cost model.
The user's instruction concerns charging form; keep the accepted explicit startup/waiting/receive/reflection costs pending EN-02 selection.

PDF page 3, equation (5):

```text
E_n(t+1) = min(E_n(t) + (1-eta_n(t))*P_har(n,t)*T
                         - eta_n(t)*P_con(n,t)*T, E_max)
eta=1: active; eta=0: inactive
```

The paper permits harvesting only when inactive and updates across slots with finite capacity.
It also states an energy-causality constraint in equation (9). Do not infer that an end-of-slot update permits spending future energy.
The paper's definition text sometimes calls P_har energy, but equation (3) and multiplication by T in equation (5) require power.
Do not introduce that terminology/unit inconsistency into the simulator.

PDF page 5, Table I lists:

| Field | Paper value | Transfer status |
|---|---|---|
| M,s,z | 0.24,150,0.014 | Individual parameter units and compatible measured circuit data are not provided in that row. Not adopted numerically. |
| Initial energy | 10^-3 J | Not adopted numerically. |
| Maximum storage | 10^-3 J | Not adopted numerically; our full-at-run-start rule is already settled. |
| Slot length | 1 ms | Not a replacement for the simulator's 600-ms Window or event durations. |
| Carrier frequency | 837 MHz | Not the accepted equivalent 915-MHz source profile. |
| Maximum allocated transmit power | 0.2 W | Not a Tag circuit-consumption value or replacement for our source/CW power maps. |

## Boundary problem for direct coefficient transfer

For positive finite M,s,z, the raw formula gives L(0)=M/(1+exp(s*z))>0.
Thus it cannot directly represent passive DC harvesting down to zero RF input over our full operating domain.
A source's limited validity domain or normalization must be explicitly stated; do not interpret a positive baseline as physical free energy.

If the table is read with W-based parameters, M=0.24 W,s=150 W^-1,z=0.014 W:

- L(0)=0.0261832370869471 W, approximately 26.18 mW.
- At our UL RF input P=1 uW, L(P)=0.0261867363014915 W.

Those are conditional unit-consistency calculations, not a claim that the paper explicitly declares every coefficient's SI unit.
The table itself does not resolve that unit convention.

## Accepted zero-input-corrected Sigmoid (Q-INFLUENCE-44)

Preserve the paper's Sigmoid family while defining a physically usable zero-input baseline:

```text
Omega = 1/(1+exp(s*z))
F(P) = (L(P)-M*Omega)/(1-Omega), P >= 0
```

The user accepted this adaptation on 2026-11-03. It differs from the equation printed in the selected WCSP paper.
It gives F(0)=0 and asymptotic limit M. Use a numerically stable logistic evaluation in a future implementation.
Zero correction alone does not make arbitrary coefficients passive.
Using the same W-based table interpretation at P=1 uW would yield F(P)=3.92771585917103 uW, still greater than RF input.
Therefore, parameters must be reselected/fitted for the actual 915-MHz low-input profile and satisfy 0<=F(P)<=P on the declared domain.
Do not fix this by silently clipping output to input; that would create a different curve and conceal unsuitable coefficients.
Source-supported sensitivity/saturation and waveform/load/reference-plane checks remain part of EN-02 evidence.

## Mapping into the accepted simulator

- Use RF inputs from accepted source-rf-synthetic-v0.1: actual local DU DL or configured UE ordinary SUL, one-way source-to-Tag power.
- Define a harvesting-phase indicator H=1 only during the accepted UE prefix; H=0 in transition, Paging, D2R and final Guard.
- Apply DC harvesting power H*F(P_in), not the paper's inactive-state flag as a substitute for phase permissions.
- Integrate over actual event intervals; retain finite capacity and residual energy across slots/windows/cycles.
- Keep applicable mode consumption in all phases, including waiting/harvesting, and charge startup costs at their causal event.
- Enforce stored-energy-only full-operation admission; do not use an unexecuted future harvesting interval to admit a packet.
- Do not hide depleted energy through lower-bound clipping. Low-energy behavior remains EN-03 work.
- Keep 915-MHz source abstraction, seven-resource limit, service objectives and timing. Do not import 837 MHz, K=2, factory heights/path loss or ABD-BB scheduling.

The general segment ledger remains E_next=min(E_max,E+(H*F(P_in)-P_mode)*Delta_t), with startup events handled separately.
Apply it only under the accepted causal/feasibility rules; it is not a complete depletion policy.

## Q-INFLUENCE-44: physical adaptation of the requested Sigmoid

Facet: Influence, total 44; other counts unchanged.
Purpose: decide whether to use the zero-input-corrected Sigmoid family with newly supported low-power parameters.
Proposal: retain the selected paper's Sigmoid structure, apply the displayed zero-input correction, and refit/reselect M,s,z with explicit passivity checks.
Example: zero RF input gives zero DC, and the current 1-uW UL input cannot yield more than 1 uW of usable passive DC.
This is a substantive boundary-model adaptation, not approval to fabricate coefficients or run implementation.
Optional notes may request exact-paper reproduction as a separately labeled comparison; no such reproduction is authorized now.
Answer: "採用". The corrected Sigmoid form is accepted; numerical Tag curve, capacity and mode costs remain open.

## Verification

Checked equation (3), equation (5), Table I and parameter meanings against PDF images.
Recomputed the zero-input and 1-uW diagnostics using scalar arithmetic.
No simulator code, runtime tests, hardware measurements, fitted curve, commit, push or publication.

## 2026-11-03 | Capacity and mode-power source alignment

The user asks whether capacity and mode consumption can follow the selected WCSP paper or another high-quality source.
This is a source review, not acceptance of new numerical parameters. Influence stays 44.

### What the selected paper supplies

| Quantity | Original evidence | Simulator consequence |
|---|---|---|
| Maximum energy | Table I, PDF page 5: E_max=10^-3 J=1 mJ=1000 uJ | A traceable simulation-capacity candidate, not a measured Device-1 capacitor specification. |
| Initial energy | Same table: E_n(0)=10^-3 J | Matches our full-at-run-start rule if that capacity is selected. |
| Reflection consumption | Equation (4), PDF page 2: P_con=alpha*g_n*p_n(t) | Equivalent active reflection cost coupled to reader allocation and link factor; not a constant whole-Tag mode table. |
| Inactive consumption | Equation (5) has no separate inactive-mode cost term | This omission is not evidence that physical idle electronics consume zero. |
| Paging receive, waiting, Guard and startup | No separate numerical power/energy values identified in the full six-page paper | Keep these explicit simulator costs open. Do not invent values or set them to zero as a paper claim. |
| Reflection-loss coefficient alpha | Defined in equation (4), but no numerical value identified in Table I or inspected text | The paper does not supply a complete numerical consumption profile for direct reproduction. |

The selected paper supports a capacity setting and aggregate consumption form.
It does not supply every mode cost required by the accepted event model.
Reader RF allocation p_n(t) is not the Tag's electrical consumption by itself.

### Primary-source alternatives inspected

| Original source | Verified values and evidence | Transfer limit |
|---|---|---|
| Liu et al., Ambient Backscatter: Wireless Communication Out of Thin Air, ACM SIGCOMM 2013, section 5/Table 1 | Analog TX 0.25 uW, analog RX 0.54 uW; prototype is tuned to 539 MHz and uses duty-cycled storage. | These are analog-component powers, not whole-Tag totals. Digital control and power management add costs. No FEC power or complete sleep/startup profile for our Tag follows. |
| Kuo et al., An LTE-Harvesting BLE-to-WiFi Backscattering Chip for Single-Device RFID-Like Interrogation, IEEE ISSCC 2023, paper 21.5 | Fabricated 65-nm chip: wake-up 4.5 uW, IF calibration 15 uW, active backscatter 25 uW; 1-uF capacitor charged to 1 V; routine about 1-2 ms. | Strong hardware precedent for communication-RF charging, storage and later backscatter. Different PHY and much higher power than the accepted approximately 1-uW Device-1 target. Values cannot be relabeled as our hardware. |
| Sha et al., High Sensitivity Near-zero Power Wakeup Receiver for Backscattering RF Tags, IEEE ISCAS 2022 | Section IV reports circuit simulation at 915 MHz and 10 kbps; paper reports 2-nW receiver consumption at 0.8 V. | Simulation, not a measured complete Tag. Wake-up pattern detection is not proof of full Paging reception, CRC/FEC, storage, sleep or D2R costs. |

Primary links:
- https://modernmobile.cs.washington.edu/docs/abc.pdf
- https://wcsng.ucsd.edu/files/LTE_harvesting_ISSCC2023.pdf
- https://ucsdwcsng.github.io/files/ISSCC_2023_paper.pdf
- https://par.nsf.gov/servlets/purl/10466311
- https://researchconnect.stonybrook.edu/en/publications/high-sensitivity-near-zero-power-wakeup-receiver-for-backscatteri/

ISSCC DOI: 10.1109/ISSCC42615.2023.10067815. ISCAS DOI: 10.1109/ISCAS48785.2022.9937291.
The local TR 38.769 Device-1 approximately 1-uW peak target remains a study assumption, not a measured mode table.
No inspected source supplies a complete, directly transferable 915-MHz Device-1 energy profile for our accepted PHY.
Do not combine the lowest component powers from unrelated devices and call the result a measured Tag.

### Capacity scale and recommendation

A dimensional check gives 1 mJ / 1 uW = 1000 s, about 1666.7 accepted 600-ms Windows.
This example assumes constant total 1-uW drain, no harvesting and no extra startup energy.
It is not a predicted lifetime or evidence that all our modes draw 1 uW.
An initially full 1-mJ capacity can hide energy scarcity in short experiments at such low drain.
Evaluate the candidate against the eventual total mode/startup ledger and experiment horizon before selecting it.

A 1-uF capacitor at 1 V stores 0.5 uJ relative to zero volts.
Usable energy between operating thresholds is 0.5*C*(V_high^2-V_low^2), before additional supply losses.
Thus the ISSCC capacitor is not equivalent to 1 mJ, nor proof that our 228-ms D2R fits its buffer.
At that chip's reported 25-uW active power, 228 ms alone would consume 5.7 uJ; this is a hypothetical duration transfer.
It is not an experiment with our waveform or a proposed mode value.

Recommendation: retain 1 mJ as a clearly labeled WCSP comparison candidate.
Retain the accepted separate mode/startup ledger and approximately 1-uW Device-1 research scope.
Select a coherent numerical profile only after the total energy/time-scale check.
Unmeasured whole-Tag costs and compatibility remain [Needs Verification].
No new capacity, mode power, startup energy, recovery policy or implementation is accepted by this review.
