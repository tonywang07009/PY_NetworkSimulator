# PScatter reference for Tag state design

Date: 2026-11-04. Status: original inspected; Q-INFLUENCE-51 A accepted; state design documented; scheduled Notebook trace implemented, general runtime pending.
The user requests this paper as a reference for Tag state switching. This does not adopt its hardware powers or complete protocol.
The charging Notebook now includes the accepted scheduled state trace and awaits acceptance. It is not a complete Engine.

## Original source

Title: Energy-Efficient Paging for Duty-Cycled LTE Backscatter.
Authors: Yunyun Feng, Xin Liu, Jia Zhao, Yuan Ding, Gongpu Wang and Wei Gong.
Venue: IEEE INFOCOM 2025. DOI: 10.1109/INFOCOM55648.2025.11044777.
DOI link: https://doi.org/10.1109/INFOCOM55648.2025.11044777
User-provided original: /home/tonywang/Downloads/Energy-Efficient_Paging_for_Duty-Cycled_LTE_Backscatter.pdf
SHA256: b6929c52491c65d6049a421c1cfa472d09d6722cd86ee348a76cd9fb75c0d076.
Ten PDF pages. Text extracted with /usr/bin/pdftotext; PDF pages 4 and 8 and the Fig. 5(b) detail were visually inspected.
No licensed PDF or page image was copied into the repository.

## States and stages verified from the original

| Paper state/stage | Meaning | Evidence |
|---|---|---|
| Static | Low-activity initial state; return when the Tag has no data to transmit. | PDF p4, section III-B and Fig. 5; p6, section IV. |
| Wakeup | Decode a simple AM wake-up packet announcing impending paging. | PDF p4, section III-B; p6, Wake-up subsection. |
| Active | Identify/decode forwarded Paging and determine whether the intended UE is addressed. | PDF p4, section III-B and Fig. 5(a). |
| Sleep | Save power between paging occasions or when the UE cannot receive. Retain timing for the next occasion. | PDF p4, section III-B; p6, section IV. |
| Timing | Align with the LTE carrier/frame before backscatter, using PSS correlation. | PDF p6, Timing subsection. |
| Modulate | Backscatter during permitted UE active intervals; return to sleep at active-duration end or static when data ends. | PDF p4 Fig. 5 and p6, Modulation subsection. |

Active in this paper is not synonymous with D2R modulation. Tables distinguish paging Active, Timing and Modulation.
The clear prose sequence is Static -> Wakeup -> Active, then periodic Active/Sleep until a matching UE paging record exists, then timing and modulation.

### Source ambiguity to preserve

Fig. 5(b)'s lower arrow is drawn from Sleep toward Active and labeled 'not in paging record list or no paging'.
Section III-B and Fig. 5(a) instead describe Active -> Sleep when the UE ID is absent, then wake for the next paging cycle.
Do not copy the graphical arrow/label pair as an unambiguous operational rule.
For our proposed design, define each guard explicitly using the prose and timing example; user acceptance is still required.
The discrepancy is a source ambiguity, not evidence for an alternative physical transition.

## Power evidence and transfer limits

The verification prototype uses an Igloo nano AGLN250 FPGA and RF circuitry.
Section V, PDF p6-7, explicitly states that the IC prototype is simulated in Cadence IC6.17 Virtuoso with TSMC 0.18-um CMOS.
Do not label the IC powers as measured fabricated-ASIC values.

| State/stage | Verification power | IC simulation power | Original table |
|---|---|---|---|
| Static | 0.91 mW | 10.47 uW | Table III, PDF p8 |
| Wake-up | 3.94 mW | 45.61 uW | Table III, PDF p8 |
| Active | 9.01 mW | 59.04 uW | Table III, PDF p8 |
| Sleep | 3.00 mW | 14.35 uW | Table III, PDF p8 |
| Timing | 9.14 mW | 89 uW | Table I, PDF p7 |
| Modulation | 14.85 mW | 149.35 uW | Table I, PDF p7 |

Table I reports a different verification Sleep operating point, 2.89 mW. Do not silently substitute it for Table III's 3.00 mW.
Both sets differ from the accepted Device-1 research budgets of 10-nW quiescent and 1-uW receive/D2R.
At 14.35 uW, a 400-ms Sleep interval alone consumes 5.74 uJ, exceeding our entire 1-uJ usable buffer.
At 149.35 uW, a hypothetical 228-ms modulation interval costs 34.0518 uJ, also exceeding that buffer.
These are dimensional transfer checks, not experiments combining PScatter hardware with our PHY.
Keep accepted numerical budgets unless the user explicitly chooses a new coherent hardware/energy profile.

## Architecture and timing differences

PScatter's UE forwards LTE paging using AM; the Tag identifies the UE ID so that the UE can receive the backscatter.
Our DU/Reader pages Tags through the fixed CFA design. The configured UE is a communication-RF energy source, not an accepted paging relay.
Do not silently introduce UE paging forwarding, UE-ID matching or LTE PF/PO timing into the current topology.
PScatter's wake-up pattern is '10' with 40-us symbols: 80 us total. This is a separate wake-up packet.
That 80 us is not our 1-ms RF switch budget, not our 1-nJ activation energy and not the full existing Paging duration.
Its 1-MHz PSS sampling/three-correlation synchronization is not an accepted substitute for our D2R response offset or SFS timing.

## Proposed adaptation to the accepted simulator

| Proposed Tag state | Entry/exit intent | Existing energy mapping, pending state acceptance |
|---|---|---|
| STATIC | No currently selected communication; await a permitted operation. | Normal quiescent 10 nW. |
| WAKING | An admitted selected operation needs activation. | Existing 1-nJ activation debit; extra packet/duration is Q51. |
| PAGING_RX | Receive the addressed fixed CFA Paging. | Existing total receive budget 1 uW. No new random Paging failure model. |
| WAIT_D2R | Retain selected timing until the assigned response interval. | Quiescent 10 nW; not a claim that PSS synchronization is implemented. |
| BACKSCATTER | Execute the selected full-TBS D2R interval. | Existing total D2R budget 1 uW; failure does not refund energy. |
| SLEEP | Retain state while communication is not currently permitted or selected; includes waiting/Guard context. | Normal quiescent 10 nW. No automatic harvesting permission. |
| ENERGY_RECOVERY | Stored usable energy reaches zero outside a fully admitted operation. | Previously accepted zero separate recovery overhead; phase-limited passive charging. |

STATIC and SLEEP have different control meanings but can share the accepted numerical quiescent budget.
Recovery is separate from ordinary Sleep; ordinary Sleep is not free.
Charging permission remains the independent resource-phase gate H, not a state name.
Use P_har=H*F(P_RF) and one applicable P_mode(state), with causal activation and capacity/depletion handling.
A sleeping/retaining Tag harvests only in an allowed UE prefix; it does not charge during Guard or the 400-ms gap.
Full-operation energy/time admission still prevents depletion inside an admitted packet.
No maximum-TBS forcing, new Policy algorithm or autonomous asynchronous transmission is implied.

## Q-INFLUENCE-51: wake-up integration [ANSWERED A]

Facet: Influence, total 51; other counts unchanged. Answer: A, recorded below.
Purpose: decide whether state design adds a new radio procedure or reuses the accepted operation-activation abstraction.
A, recommended: borrow the state/control separation and map WAKING to the existing selected-operation activation debit.
Do not add a new wake-up packet or independent synchronization interval in this first version. Preserve existing CFA timing and numerical budgets.
This is a scheduled-activation research abstraction, not a demonstrated physical always-on wake-up detector.
B: add an explicit wake-up packet and separately modeled synchronization stage.
B requires new packet duration, energy/receiver behavior and full-batch timing checks before implementation; paper values are references, not automatic approvals.
Both options preserve DU/Reader topology unless the user separately changes it. Neither adopts the paper's IC powers by default.
Optional custom answers may specify another wake-up design. State transitions are proposed until this choice and its consequences are resolved.

## Delivery status

This source review does not accept a final state machine or authorize edits to existing Notebook calculations.
The current add-tag-charging-trace-notebook remains 4/7, with 24 tests and 13 clean-kernel cells previously verified.
No new state runtime/test, scheduling algorithm, hardware calibration, commit, push or publication.

## 2026-11-04 | Q-INFLUENCE-51 A accepted

Original answer:
> A

Borrow PScatter's separation of control states while retaining our accepted scheduled-operation activation abstraction.
WAKING applies the existing 1-nJ activation debit when needed. It adds no wake-up packet, 80-us interval or separate synchronization duration.
Retain current DU/Reader CFA Paging, D2R offsets, Guard, source phases and numerical energy budgets.
Do not import PScatter's UE paging relay, UE-ID protocol, LTE PF/PO schedule, PSS synchronizer or IC power values.
The adapted state/control mapping is documented in docs/architecture/tag-state-design.md.
Full-operation stored-energy/time admission remains before activation; future harvesting cannot fund it.
Influence stays 51. No new preference question or runtime implementation is implied by this design update.
