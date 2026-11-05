# Accepted EN-01 source and RF research profile

Accepted: 2026-11-03, Q-INFLUENCE-42 A. Profile: source-rf-synthetic-v0.1.
Authority: R-01 sections 66-75. Numerical research settings are accepted; runtime code and defaults are unchanged.

## Purpose and evidence level

Provide one complete, reproducible research baseline for communication-RF harvesting and UE-to-Tag transition timing.
Separate cited physical mechanisms from chosen scenario values. No paper calibrates this complete five-DU deployment.
The candidate is a synthetic operating profile with source-informed scales, not a measured farm or modem profile.
Keep source profile acceptance separate from Tag RF-to-DC/storage/circuit acceptance under EN-02.

## Accepted first-version operating values

All transmit powers below are mean RF powers at the modeled antenna feed during an active source interval.
They apply to the compatible modeled communication signal band, not to every emitted channel or to a single resource block.

| Field | Candidate | Basis and limit |
|---|---|---|
| Equivalent frequency | 915 MHz for UL/DL harvesting calculations | Already accepted research abstraction; not an actual NR channel-center declaration. |
| DU DL communication power, LOW/MEDIUM/HIGH | 18/24/30 dBm, approximately 63.096/251.189/1000 mW | Proposed six-dB scenario steps. A reviewed 915-MHz paper uses a 30-dBm source, but does not prescribe these DU levels. |
| D2R CW power, same Window states | -2/10/22 dBm | Retain the accepted channel-entry prototype mapping. Not a new measured hardware claim. |
| UE SUL communication power | 20 dBm=100 mW, fixed per UE/run; same default for this candidate | Proposed actual transmit-power setting. RedCap PC3 maximum-power requirements are a scale reference, not a requirement to transmit at maximum or proof of compliance. |
| DL harvesting source path | g_DL(d)=g0*(1 m/d)^2; g0=0.0006797973850689421 | Retain the accepted 915-MHz free-space reference, exponent 2 and isotropic antennas. One-way power gain, valid model distance 1-50 m. |
| UL harvesting source path | g_UL=10^(-5), or -50 dB, for each serving UE-to-Tag pair, fixed in this candidate | Explicit synthetic gain chosen as a controlled equal-UL-input baseline. Not derived from DU distance, UE coordinates, a measurement or RedCap requirements. |
| Effective source/Tag antenna gains | 0 dBi nominal, already included in the gain definitions | Research reference, not measured antennas. Do not add these factors twice. |
| Compatible-band capture | Ideal capture of the modeled source signal at the gain-defined RF-input reference plane | Explicit abstraction. Actual band/NR-waveform compatibility is required before a hardware-calibrated claim. |
| UE-to-Tag RF transition | T_switch=1 ms=1000000 ns | Proposed nonzero scheduler budget aligned with whole-ms occupancy. Not an inferred worst-case hardware switching time. |

The shared Window state selects both power maps; the numerical DU and CW values differ.
DU communication power is constant within each applicable local DL interval and changes only by the external Window plan.
UE power is constant across Windows. The candidate sets a common default but does not establish a general equal-UE requirement.
Continuous source activity during the local UE prefix remains the accepted research assumption.
DL uses the serving DU. UL uses its configured communicating UE. Do not sum them in the same local direction interval.
No extra UE energy waveform or dedicated UE-phase CW is added.

The DL path is a nominal deterministic harvesting path in this candidate.
Do not silently transfer or reinterpret the accepted effective D2R Window offset as an independently calibrated one-way EH fading variable.
The existing D2R Window channel variation stays unchanged. An empirical joint channel-correlation profile remains unverified.
No source-power choices are added to the scheduling Policy.

## Sources and what they support

1. [Existing channel-entry profile](../../Plan/channel-entry-pack.md), sections 2-3: accepted 915-MHz reference, g0/exponent/antenna conventions and -2/10/22-dBm CW values.
2. [ITU-R P.525-5](https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.525-5-202411-I!!PDF-E.pdf), section 2.3: free-space attenuation. This does not calibrate an outdoor farm or prove the gain at distances below the modeled minimum.
3. [Reviewed TCCN paper](../Literature/A_IoT/Ambient_IoT_Topologies_TCCN2026.pdf), section IV-A, printed page 2376; [DOI](https://doi.org/10.1109/TCCN.2025.3586219): uses f=915 MHz and P=30 dBm in numerical analysis. Its exponent is 3, unlike our retained prototype exponent 2. It is a scale anchor, not a complete adopted profile. Local original checked; DOI web retrieval failed.
4. [TS 38.101-1 V18.10.0](https://www.etsi.org/deliver/etsi_ts/138100_138199/13810101/18.10.00_60/ts_13810101v181000p.pdf), clause 6.2I.1 and Table 6.2.1-1: RedCap uses PC3 requirements; n81 PC3 maximum is 23 dBm before applicable tolerances and other requirements. It does not prescribe our fixed 20-dBm setting or validate an equivalent-frequency waveform.
5. [AD9361 frequency-hopping example](https://wiki.analog.com/resources/eval/user-guides/adrv936x_rfsom/tutorials/frequency_hopping), Fastlock section: illustrates calibration/lock and approximately 15-25-us LO locking under stated conditions. This is not an end-to-end DU/Reader bound. The 1-ms candidate is a research budget, not a value taken from that example.
6. [Sakr and Hossain](https://arxiv.org/html/1405.2013), section II-C: separate communication source powers and source-to-device gains. Its multi-source, wideband and no-storage assumptions are not adopted.

No cited source supplies 18/24-dBm DU values, the -50-dB UL gain or a guaranteed 1-ms transition.
Those are proposed research settings and need disclosure and sensitivity analysis, not presentation as literature measurements.
The numbers do not certify a chosen SDR/PA board at the requested power.

## RF-input examples before nonlinear conversion

For a Tag 20 m from the DU, g_DL is -57.696805 dB.
Use P_RF,dBm=P_TX,dBm+g_dB once, without beta or squared backscatter gain.

| Local source | Incident RF, dBm | RF-input energy over 400 ms, uJ |
|---|---:|---:|
| DU LOW, 18 dBm | -39.696805 | 0.042892 |
| DU MEDIUM, 24 dBm | -33.696805 | 0.170757 |
| DU HIGH, 30 dBm | -27.696805 | 0.679797 |
| UE UL, 20 dBm with -50-dB gain | -30.000000 | 0.400000 |

The UL example deliberately gives equal incident RF to all Tags; heterogeneous UL geometry is not modeled by this candidate.
Node distance zones do not identify UE proximity. This baseline is a limitation, not a physical discovery.
A static per-link gain table can later replace the common baseline if source evidence or experiment scope requires it.
Such a replacement is not assumed or implemented by this proposal.

These numbers are RF energy at the rectifier input, not DC harvested energy or battery increments.
With nonlinear conversion F, gross DC energy is F(P_RF)*T for a constant compatible input.
Battery change must also include applicable mode/startup consumption and finite capacity.
A passive conversion cannot deliver more energy than the incident RF budget, but real efficiency and loading remain EN-02 work.
Do not assign a temporary efficiency to claim that any TBS is sustainably supported.

## Timing and energy boundaries

UE_END -> 1-ms transition -> cumulative-prefix Paging -> CW/D2R -> final 200-us Guard.
The transition is counted once at the actual UE-to-Tag phase change, not per batch or Tag.
No local source harvesting is credited during this transition; retain mode costs and do not create useful traffic.
The 600-ms Window and 360-450-ms UE occupancy leave 149-239 ms after the candidate transition.
Keep exact PHY times and accepted rounded occupancy. Never hide overruns by clipping.
A seven-Tag batch containing a 64-byte packet has a lower bound 1+12+228+0.2=241.2 ms after UE_END, even before response offsets.
It therefore cannot fit the maximum 240-ms remainder under this candidate. Reject that combination through feasibility, not a changed TBS domain.
This is a lower-bound check, not proof that all smaller batches fit.
Tag full-operation stored-energy admission still applies even when the RF source budget is large.

## Q-INFLUENCE-42: consolidated source/RF baseline [ANSWERED A]

Facet: Influence, total 42; other counts unchanged.

- A: Adopt source-rf-synthetic-v0.1 as a disclosed first-version research baseline, including its common -50-dB UL gain and 1-ms switching budget. Actual harvester/storage/mode parameters remain EN-02 decisions.
- B: Adjust the proposed whole profile before adoption; specify the power, UL-gain assumption or switching budget that needs a different research condition.

This is acceptance of a coherent synthetic scenario, not a claim of measured hardware or a full calibrated simulator.
Optional notes may provide a measured source/link/switching profile to replace the corresponding assumptions.
Answered A on 2026-11-03. No runtime configuration, source changes or RF measurements yet.

## Checks

Recomputed g0, all four 20-m RF-input examples, W/dBm/J units and the exact 241.2-ms lower bound.
Source links and evidence boundaries reviewed; product and agent-document diff checks required at task end.
No runtime tests, FBL recalibration, harvester fitting, commit, push or publication.

## Acceptance and remaining evidence (2026-11-03)

The user selected A. Adopt the complete source-rf-synthetic-v0.1 research baseline, including the common -50-dB UL gain and 1-ms transition.
Retain all source/prototype limitations above. Acceptance does not establish physical calibration or sustainable energy operation.
EN-02 must still select nonlinear RF-to-DC data, finite capacity, startup and mode costs; EN-03 must define low-energy recovery.
