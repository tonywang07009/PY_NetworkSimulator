# Remaining simulator decisions

Updated: 2026-11-04. Current authority: R-01 sections 35-92 and the latest simulator interview.
This inventory separates unresolved model choices from source review and routine engineering work.
It does not approve the proposals, implementation or publication. The work areas are not a fixed question count.

## Current decision snapshot (2026-11-04, Q-INFLUENCE-51 A accepted)

Access/PHY/data/energy model selections are settled for the first research baseline. Three research groups remain: Baseline, fairness and formal experiments. They are not a fixed question count.
The accepted scenario still needs engineering integration. It adds no new state-trace model choice; current blocking choices: zero.
Q-INFLUENCE-42 A accepts the complete source-rf-synthetic-v0.1 baseline under R-01 section 75.
Q-INFLUENCE-43 selects the WCSP source; Q-INFLUENCE-44 accepts zero-input correction. Q-INFLUENCE-45 A accepts the complete tag-energy-synthetic-v0.1 numerical baseline under R-01 section 81. Q-INFLUENCE-46 A accepts ideal passive recovery. Q-INFLUENCE-47 B selects 600-ms Windows every 1000 ms with 400-ms gaps. Q-INFLUENCE-48 B permits existing Guard cleanup after evaluation end within the Window. Q-INFLUENCE-49 selects ample finite initial data to fill the chosen TBS throughout the reference run.
Influence 51; other facet counts unchanged.

| Order | Group | What remains |
|---|---|---|
| Engineering | SI-01 Scenario/integration | Configuration accepted; charging/state Notebook implemented for human trace. RF/timing and service integration remain engineering work, not unanswered model choices. |
| 1 | BL-01 Baseline | Deferred explicitly: the user will provide the algorithm later. |
| 2 | FA-01 Fairness | Cross-service normalization and evaluation sets. |
| 3 | EX-01 Experiments | Loads, seeds, uncertainty, sensitivity and calibration evidence. |

EN-03 is closed: depleted Tags use ideal passive recovery with phase-limited charging and full-operation admission at existing Policy decisions.
EN-02 numerical selection is closed: usable capacity 1 uJ, quiescent 10 nW, receive/D2R 1 uW, activation 1 nJ; converter M=10 uW, s=2e5 W^-1, z=10 uW.
These are accepted research assumptions; hardware calibration and runtime integration are not completed.
EN-01 source/RF first-version values are settled: DU 18/24/30 dBm, CW -2/10/22 dBm, UE 20 dBm,
nominal one-way DL reference, common -50-dB UL gain and 1-ms RF transition. These remain disclosed synthetic research settings.
AP-02/04/05/06 and EN-01 implementation/calibration checks are preparation, not additional unanswered preference questions.
Earlier eleven-package counts included EN-01 configuration work; configuration selection is now closed while implementation/evidence work remains.
Do not infer Tag battery credit from incident RF or substitute an unmeasured constant efficiency.
The Notebook must show RF transition timing, full-operation energy, overhead-inclusive durations and failed-transmission costs.
Earlier snapshots below are history; this section controls current status.

## Count requested on 2026-11-02

| Scope | Remaining packages | Handling |
|---|---:|---|
| Current Access/PHY, application data and energy | 7 | AP-02, AP-04 through AP-06 and EN-01 through EN-03 below |
| Later first-version study | 4 | SI-01, BL-01, FA-01 and EX-01 below |
| Total in the present first-version inventory | 11 | CLM remains future work and is excluded |

A package can contain related fields. Eleven packages do not establish eleven remaining questions.
AP-01 supply is closed. AP-02 packet-unit/retention rules are settled; prepare its identity/accounting contract without re-questioning them.
EN-03 still needs the depletion/wakeup model choice.
For AP-04 through AP-06, EN-01 and EN-02, prepare complete source-backed profiles or derivations before consolidated discussion.
Do not ask separately about source lookup, arithmetic, derived fields, names or routine validation.
Only unresolved choices that affect behavior, evidence scope or acceptance need substantive questions.
Q-INFLUENCE-20 is answered A: initial-only finite data. Do not ask this supply-model question again.
Initial byte amounts remain explicit scenario inputs, not an unresolved supply-model decision.
Q-INFLUENCE-26 is resolved by the custom selected-TBS packet/accounting answer.
Q-INFLUENCE-27 is answered A: retain undelivered data for later legal scheduling. Current Influence count is 28.
AP-02 identity/accounting draft is prepared in the fixed-profile evidence; its review remains.
The latest user revision uses tau BD with FEC, retaining BPSK, repetition 1, short ambles, interval 96 and no extra midamble (R-01 section 57).
Influence remains 28. R-01 section 58 sets seven Tags and seven legal SFS values; AP-03 is closed.
The user accepts [the pure D2R timing table](../ReferDoc/Plan/D2R_Timing_Configuration.md). Full-batch timing and integer-ns rounding remain open.

## Audit after D2R table acceptance (2026-11-02)

The current count is eleven work packages: seven current plus four later. These are not eleven unanswered preference questions.
The D2R table and seven-SFS assignment close AP-03 configuration. Receiver and full-batch validation remain separate.
AP-02 needs contract preparation/review, not another supply, segmentation or failed-data retention question.
Prioritize AP-04 batch timing, then AP-06 ns boundaries and AP-05 receiver/FBL mapping.
Prepare EN-01/EN-02 evidence in parallel as ordinary source work; resolve EN-03 before energy execution.
No new interview question is opened by this inventory request. Influence stays 28.

Already settled: initial-only finite data; selected-TBS packet units; failed data retained; service caps/sharing/deduplication;
tbs_bytes {8,16,32,64}; FEC/tau D2R timing; continuous UE RF; nonlinear conversion;
finite persistent storage; no additional leakage; stored-energy-only admission; no D2R EH.
Do not reopen those decisions while filling the remaining numerical inputs.

Implementation and validation are separate from this package count:

| Work | What remains |
|---|---|
| Contract/config preparation | Supply initial data amounts, service-content eligibility and the remaining source-backed profiles; prepare traceable byte/attempt identity and units. |
| Module implementation | Complete the accepted module workflow for Access/PHY, energy, service accounting, Validator/Engine and Policy integration under the relevant authorization. |
| Integrated checks | Full-batch timing/energy, failed-data retention, unique service credit, simultaneous completions, strict deadlines and reproducibility. |
| Human acceptance | Explain the resulting architecture/trace and validate accepted behavior through the existing module workflow. |
| Existing delivery | Channel remains 11/12 and timeline 8/9. Both open tasks concern remote delivery under publication authorization; neither is a new model decision. |

This inventory request does not authorize implementation or remote operations. CLM remains future work.

## Decision view after the seven-Tag revision

The seven current work packages contain five model/profile discussion areas and two agent-owned contract/schedule reviews. Guard selection is closed.
Do not present the eleven total work packages as eleven unanswered preference questions.

| Current decision/profile topic | What needs selection or alignment | Preparation |
|---|---|---|
| AP-05 Receiver/FBL mapping | Original hybrid restored: RELIABLE=1, UNREACHABLE=0, RANDOM=1-epsilon_FBL; selected-TBS k/n/rho mapping remains | No independent fixed probability or extra coding gain. Preserve CRC/FEC overhead. |
| AP-06 Integer-ns timing | How rational physical durations become event boundaries | Prepare exact-fraction boundary examples, preserving exclusive deadlines. |
| EN-01 Energy-source profile | Harvestable source scope, compatible band, DU/UE powers and UE geometry | Prepare source-backed DL/UL link candidates; continuous activity is already decided. |
| EN-02 Tag energy profile | Nonlinear hardware curve, capacity, mode costs and startup | Prepare coherent evidence-backed profiles; do not ask about each coefficient. |
| EN-03 Depletion/wakeup | Low-energy state outside admitted transmissions and conditions for recovery | Prepare one recharge/depletion example; full-TBS admission is already decided. |

AP-02 content/attempt identity and deduplication contract is agent-owned preparation under the accepted packet, retry and service rules.
Only a demonstrated behavior conflict would require another model question; do not reopen settled choices for naming or representation.
The four later discussion areas remain SI-01 scenario/integration, BL-01 baseline, FA-01 fairness and EX-01 experiments.
Source checks, derived values, implementation, tests and delivery are not additional preference questions.
No new interview question is opened by this inventory. Influence remains 28.

Q-INFLUENCE-29 is answered A: response delays reference the final batch-Paging end as a simulator timing abstraction.
Q-INFLUENCE-30 is answered A: M=24 with minimum-three-PRB allocation for the applicable R2D portions.
Q-INFLUENCE-31 is answered A: compact 32-bit content, 42-bit full Paging ID and 27-byte Paging TB.
See ReferDoc/Plan/Paging_R2D_Timing_Configuration.md for the 24-symbol and CP-dependent timing derivation.
The fixed batch-local Paging design is accepted: continuous CP, zero gaps, phase n modulo 7 = 0 and 12 ms for seven messages. Use exact prefixes for fewer Tags.
Influence remains 31; no new question is active. Guard, response verification, external NR alignment and full batch feasibility remain open.

## Decision status after fixed Paging acceptance

Five current groups remain for model/profile discussion: receiver/FBL mapping, ns rounding,
energy-source profile, Tag energy profile and depletion/wakeup. AP-04 Guard is fixed at 200 us; response/schedule verification remains agent-owned.
Response-offset lookup and full-batch arithmetic are agent-owned derivation, not separate questions about each numeric value.
External NR alignment remains an integration evidence limit; do not silently alter the accepted batch-local timing convention.
Paging fields, local CP phase, zero gaps and the conditional-size lookup are fixed under R-01 section 62.
Keep eleven work packages separate from question counts: five current discussion groups, two agent-owned contract/schedule reviews and four later study groups.
No new question is opened by this inventory request. Influence remains 31.

Q-INFLUENCE-32 is answered A (2026-11-03): fixed 200-us Guard, with explicit Reader/CW recovery-within-Guard assumption.
See AgentDoc/openspec/discuss/2026-11-03-guard-candidates.md. Influence remains 32; no new question is active.

## Discussion agreement

The user requested a complete inventory and continued discussion, one decision at a time, without additional continuation stops.
Within the remaining topics below, continue after each answer and present the next unresolved decision without another permission-to-continue question.
Wait for each substantive answer. Do not infer agreement from silence or change a confirmed model rule.
Keep all historical question IDs and facet counts. The current scoped continuation overrides repeated numerical-budget approval stops for these topics.
It does not reset the interview, change workflow checkpoint mode, authorize implementation or extend to unrelated work.

## Settled Access/PHY rules

| Topic | Accepted rule |
|---|---|
| Source order | Prepare source-backed configuration before implementation; do not substitute invented physical parameters |
| Policy TBS | Actual tbs_bytes in {8,16,32,64}; four choices per selected Tag; 64-byte cap and later experiment-driven additions |
| SFS resources | Seven fixed values {1,2,4,8,16,32,64} at tau; at most seven Tags per batch; assume mutual orthogonality and permit parallel D2R |
| Control/data phases | Individual Paging for every selected Tag, all completed with CW off before the CW/D2R phase |
| Batch completion | Last D2R end -> CW_OFF -> one complete Guard -> updated Observation and next Policy decision |
| Application data | Actual SDU is application payload; finite data per Tag is present at t=0 with no later arrivals; abstract upper-layer encapsulation and exclude MAC/PHY overhead |
| Service credit | Successful unique eligible data, strict deadline, demand caps, sharing and accepted simultaneous allocation rules |
| RF supply | Continuous communication RF during the UE prefix; Node DL and UE UL; dedicated energy CW remains off during UE traffic; power values remain open |
| Conversion and storage | Hardware-supported nonlinear conversion; finite persistent storage across slots/windows/cycles; full only at run start; omit additional storage leakage |
| Energy feasibility | Stored energy covers the complete operation; retain mode/startup costs; no D2R/Paging/Guard harvesting |

## Current discussion: Access/PHY and direct data dependencies

| ID | Unresolved model choice | Agent preparation and acceptance evidence |
|---|---|---|
| AP-02 | Packet-unit accounting and failed-data retention settled; traceable identity/accounting contract review remains | Prepare the contract from existing uniqueness, eligibility, deadlines, sharing and caps. Failed data remains available for later legal scheduling; no automatic retry or fixed-record layer. |
| AP-04 | Paging and 200-us Guard are fixed; response/schedule verification remains | Derive offsets, CW coverage and full batch/window/deadline checks from accepted rules. Reader/CW recovery within Guard remains an unverified assumption. |
| AP-05 | Original power-table/FBL hybrid restored; selected-TBS k/n/rho mapping remains | Preserve CRC/FEC overhead and reproducible sampling. No additional probability model. |
| AP-06 | Exact integer-ns conversion and event boundary policy | Prepare rational-duration examples and boundary checks. Keep strict deadlines and full-batch validation; do not round each chip without agreement. |

Q-INFLUENCE-19 is answered B for finite data; Q-INFLUENCE-20 is answered A for all data available at t=0 with no later arrivals. AP-01 is closed.
Q-INFLUENCE-21 is answered A: stored energy alone must cover the complete selected operation at admission.
The user subsequently moved harvesting to the UE UL/DL phase and removed simultaneous D2R charging (R-01 section 46).
Q-INFLUENCE-22 is answered A: harvest communication RF itself, with separate DL Node-to-Tag and UL UE-to-Tag links.
Q-INFLUENCE-23 is answered B: use a hardware-supported nonlinear curve. Cross-slot storage is explicitly assumed feasible; residual energy carries across windows/cycles.
Q-INFLUENCE-24 is answered A: omit additional storage leakage and retain all applicable mode consumption.
Q-INFLUENCE-25 is answered A: continuous RF throughout the UE prefix, without assuming maximum transmit power.
Q-INFLUENCE-20 is closed. Do not infer numerical initial amounts, altered TBS candidates or calibrated energy powers.
The order follows data and timing dependencies. Source work for AP-03 through AP-06 can proceed while earlier answers are pending.
Change the order only when a real dependency or the user's steering requires it; record the reason.

## Routine work without preference questions

- Use explicit byte/bit/ns names and the accepted Action contract. Keep source-backed conversion and fixed message overhead traceable.
- Reuse the existing Config/DTO conventions and deterministic identities. Preserve original invalid Actions and atomic rejection.
- Calculate complete packet lengths and durations after profile selection. Do not turn each derived field into another approval.
- Prepare boundary cases, source references and before/after examples. Separate design acceptance, implementation tests and scientific calibration.
- If a source/profile contradicts a confirmed assumption, show the concrete mismatch before proposing a model change.

## Current energy packages

These three packages join AP-02 and AP-04 through AP-06 to form the seven-package current scope.

| ID | Remaining model choice or profile | Agent preparation |
|---|---|---|
| EN-01 | Harvestable source scope and UL/DL links: compatible bands, source powers/antennas and UE geometry | Prepare Node-to-Tag and UE-to-Tag link profiles. Preserve accepted continuous RF activity; do not infer all-source or all-band capture. |
| EN-02 | Tag hardware profile: nonlinear curve/data/range, finite capacity and mode/startup costs | Prepare a coherent evidence-backed profile and energy budget. Do not import incompatible circuit values or ask about each fitted coefficient. |
| EN-03 | Energy depletion outside an admitted operation: low-energy mode and wakeup behavior | Prepare a depletion/recharge example. Preserve full-operation admission and do not hide energy deficits through clipping. |

## Later first-version study packages

| ID | Area | Remaining work |
|---|---|---|
| SI-01 | Scenario and integration | Numerical window starts/gaps, explicit scenario inputs and run-end/event boundary behavior. Preserve settled resource, service and visibility rules. |
| BL-01 | Baseline | Complete ordering, tie rules, TBS selection and shared-Tag treatment within the accepted Action/Validator contract. |
| FA-01 | Fairness | Define cross-service normalization and evaluation sets. Preserve the service-count priority and accepted within-service accounting. |
| EX-01 | Experiments | Define loads, seeds, uncertainty and sensitivity comparisons. Prepare calibration evidence and acceptance criteria; do not count running checks as additional preference decisions. |

CLM candidate construction, delay/failure behavior and equal-information comparison remain future work, outside the eleven-package count.
This inventory does not expand implementation or publication authorization.

## Navigation and evidence limits

- [Accepted system model](../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md).
- [Access/PHY source map](../AgentDoc/openspec/discuss/2026-11-02-access-phy-source-map.md).
- [Existing simulator interview](../../PY_NetworkSimulator-agent-work/interview/2026-10-20-ambient-iot-des.md).
- [Source alignment and work areas](design-resumption.md).

OpenSpec currently lists channel 11/12 and resource timeline 8/9; their remote delivery is not complete.
The workflow index still registers the active channel workflow only. This inventory does not register another workflow or claim a merge.
No simulator or training tests ran for the inventory. Runtime integration, receiver calibration and measured training cost remain [Needs Verification].

---

## Earlier inventory and continuation records

The material below preserves the previous inventory and discussion sequence. Its pending labels and budget gates are historical where the current sections supersede them.


Date: 2026-10-31. Scope: Existing remaining simulator plan, after R-01 §34.9.
This is a topic inventory, not a fixed question count or implementation approval.
Use [source alignment](design-resumption.md) and the accepted decision record before opening a question.

## First runnable simulator

| Area | Remaining model decisions |
|---|---|
| 1. UE/DU timing | Model structure settled in R-01 §34.10–34.11: shared scenario-timed windows and independent UE draws. Numerical start/gap inputs and research calibration remain. |
| 2. Access and PHY | Legal TBS and header/payload mapping; fixed BD/SFS/CFA resource and duration parameters; parameter sources and constraints. |
| 3. Tag energy | Capacity, consumption and startup costs; harvesting efficiency and RF allocation during reflection. Initial full energy and no CW harvesting in Guard are settled. |
| 4. Service and engine boundaries | Payload identity/eligibility details, empty-service input and end-of-run behavior. Keep settled sharing, credit allocation, strict deadline, atomic rejection and event-order rules. |

## Research comparison

| Area | Remaining research decisions |
|---|---|
| 5. Baseline and fairness | Final policy ordering, tie handling and TBS adjustment; evaluation population and fairness aggregation. Keep service-count priority. |
| 6. Calibration and experiments | Applicable physical profiles, workload matrix, seed count, comparison cases and measured computation budget. Synthetic validation does not establish outdoor performance. |
| 7. CLM integration | Candidate construction, delay treatment, failure handling and equal-information comparison with Baseline. CLM implementation remains future work. |

The two resource model choices are resolved. Six other design areas remain; numerical resource-scenario inputs still need preparation.
The seven areas do not imply seven questions. Some contain existing decisions, engineering work or source checks that need no new preference question.
Prepare bounded proposals and handle routine interfaces, validation and tests without asking about every field.
The current interview has reached its Influence, Description and Tradeoffs limits. Do not reset counts or relabel questions to bypass a limit.
Before dependent work on unresolved decisions in a capped facet, ask the user to narrow scope or explicitly permit more questions.
No additional question is asked by this status report.


## 2026-11-02 continuation

Q-TRADEOFFS-01 is answered B: prepare source-backed Access/PHY configuration before implementation.
Q-DECISION-09 is answered A: allow three additional Influence questions for Access/PHY only.
Q-INFLUENCE-13 asks about batch signalling, using 1/3 additional questions and 13/15 Influence questions in total.
Its model answer is pending. Description and Tradeoffs limits remain unchanged; preserve all historical questions.
See AgentDoc/openspec/discuss/2026-11-02-access-phy-source-map.md for source facts and remaining mappings.


## 2026-11-02 individual Paging clarification

Q-INFLUENCE-13 is answered B: individual CFA Paging for each selected Tag, with separate Scheduling Info.
Q-INFLUENCE-14 asks about Paging/D2R sequencing and Guard placement, using supplemental question 2/3 and Influence 14/15 in total.
One supplemental question remains. Keep unresolved SDU/application and fixed-profile choices visible; do not silently extend the allowance.


## 2026-11-02 parallel response clarification

Q-INFLUENCE-14 is answered C with explicit parallel D2R, sufficient orthogonal SFS resources for eight Tags and one Guard after the last response.
This supersedes the earlier serial C wording. SFS sufficiency is an accepted model assumption, not another open capacity decision.
Q-INFLUENCE-15 asks about Paging/CW phase overlap; it uses supplemental question 3/3 and Influence 15/15 in total.
No further Influence questions are permitted without a new explicit allowance. SDU/application and numerical-profile mapping remain open work.


## 2026-11-02 batch phase closeout

Q-INFLUENCE-15 is answered A: all individual Paging completes before CW/parallel D2R, followed by one Guard after the last response.
The three supplemental signalling questions are closed at Influence 15/15. No new question is active or extra allowance inferred.
Numerical PHY/R2D/Guard inputs, SDU/application mapping, FBL mapping and ns conversion remain open source/design work.
See R-01 section 38 and the Access/PHY source map. This closes phase decisions only, not implementation or complete module acceptance.


## 2026-11-02 next-decision request

After the signalling closeout, the user explicitly requested the next decision. Open Q-INFLUENCE-16 only: MAC SDU to useful application payload.
Influence is 16/16 for this one-question continuation; do not infer an unlimited extension or any model choice.
Compare a first-version SDU/application abstraction with detailed upper-layer accounting. The answer is pending; all settled timing/SFS rules remain in effect.


## 2026-11-02 application payload decision

Q-INFLUENCE-16 is answered A: actual MAC SDU is application data in the first simulator; abstract upper-layer encapsulation.
Preserve successful unique-content checks, existing service-credit rules and full packet time/energy cost. Actual SDU length need not fill TBS capacity.
Influence remains 16/16; no new question is active. Data filling/identity, segmentation and numerical PHY mapping remain open.
See R-01 section 39 and the Access/PHY source map for accepted examples and boundaries.


## 2026-11-02 remaining Access/PHY decisions resumed

The user requested continuing the remaining decisions. Q-INFLUENCE-17 asks about the application-data Policy TBS candidate set; Influence is 17/17 for this step.
Compare all integer sizes from 3-125 bytes with a user-selected smaller subset. No set is accepted before the answer.
Retain fixed PHY/resource mapping, R2D fields/timing, Guard/ns conversion, FBL mapping and offered-data/identity/segmentation as remaining work areas, not a fixed question count.
All accepted phase, SFS and payload rules remain in effect. No implementation or publication authorization follows.


## 2026-11-02 reduced TBS domain and extension

Q-INFLUENCE-17 is answered B with a 64-byte complete-TB cap. The user permits later candidate additions if experiments find too few choices.
Preserve that cap, explicit experiment configuration and common candidate sets across compared policies.
Q-INFLUENCE-18 asks for the exact initial members; {8,16,32,64} bytes remains proposed, not accepted. Influence is 18/18 for this clarification.
Fixed PHY/R2D/Guard values, FBL mapping and data filling/identity/segmentation remain open.


## 2026-11-02 initial TBS members accepted

Q-INFLUENCE-18 is answered A: {8,16,32,64} complete-TB bytes, represented by Action values {64,128,256,512} bits.
Maximum SDU capacities are {6,14,30,62} bytes. Actual data filling, reception success and service credit remain distinct.
Retain the 64-byte cap and permitted later expansion. Influence remains 18/18; no new question is active.
Numerical PHY/R2D/Guard values, ns conversion, FBL and offered-data/identity/segmentation remain open.


## 2026-11-02 byte-valued discrete Action correction

The user requests actual byte-valued TBS options. Use tbs_bytes/legal_tbs_bytes with {8,16,32,64}; derive TB bits at the Access/PHY calculation boundary.
This supersedes earlier bit-valued Action wording, preserving the four physical choices and 64-byte cap. Service credit remains in bits.
Keep four TBS choices per selected Tag; this is not a four-action complete scheduler. Overall training complexity is not measured.
No new question is active; counts remain unchanged. See R-01 section 42 for the current contract.

## 2026-11-03 | Reception aligned with prior CW table

R-01 section 65 records the custom Q-INFLUENCE-34 answer. Preserve LOW near/middle/far=RELIABLE/RANDOM/UNREACHABLE,
MEDIUM=RELIABLE/RELIABLE/RANDOM, HIGH=RELIABLE/RELIABLE/RELIABLE. No independent 50-percent setting is accepted.
The prior table specifies RANDOM qualitatively; numerical entries remain open before sampler implementation.
One shared constant versus separate entries is not decided. Section 64's shared-constant requirement is superseded.
FBL stays disabled; preserve CRC/FEC overhead and stored-energy admission. No source/runtime change. Influence stays 34.

## 2026-11-03 | Original hybrid reception restored

R-01 section 66 supersedes the earlier no-FBL and fixed-RANDOM-value discussion.
Q-INFLUENCE-35 A: retain RELIABLE success 1, UNREACHABLE success 0 and RANDOM success 1-epsilon_FBL(rho,k,n).
CW/zone classes stay unchanged. No extra constant probability, second FBL factor or arbitrary coding gain.
Existing channel source already implements this classification. Selected-TBS k/n/rho mapping still needs preparation and verification.
CRC/FEC time/energy overhead and all admission/accounting rules remain. Influence stays 35; no new question or code change.

## 2026-11-03 | RF transition clarification and evidence

The user confirms a UE-to-Tag frequency-switching interval. R-01 section 71 records it without choosing its duration.
Include its explicit parameter in AP-04 schedule preparation and hardware-profile evidence; it is not the 200-us post-D2R Guard.
Hardware features and source links: ReferDoc/Plan/RF_Hardware_and_Frequency_Switching_Evidence.md.
This request adds no independent interview question or simultaneous-transmission requirement. Influence stays 38.

## 2026-11-03 | Communication-source power decision

Q-INFLUENCE-39 is open: fixed-per-run separate DU/UE communication powers vs externally supplied per-Window values.
Neither adds a Policy action or automatically ties communication power to D2R CW tiers. Numerical powers remain unselected.
R-01 section 32 already fixes one logical UE per DU without coordinates. Prepare independent UE-to-Tag link-gain evidence without silently revising that model.
Influence 39; no new implementation or calibrated profile.

## 2026-11-03 | DU/UE power behavior accepted

R-01 section 72 records Q-INFLUENCE-39's custom answer: DU communication power is per Window; UE power is fixed configuration.
Q-INFLUENCE-40 is open: common communication/CW LOW/MEDIUM/HIGH Window state vs independent plans. No numerical dBm or equality of communication/CW power is implied.
Influence 40; numerical source/hardware profile preparation remains. Policy actions stay Tag/TBS.

## 2026-11-03 | Shared power state accepted; RedCap/SUL source role open

R-01 section 73 accepts Q-INFLUENCE-40 A: common LOW/MEDIUM/HIGH DU communication/CW Window state with separate dBm mappings.
UE power remains fixed. Q-INFLUENCE-41 clarifies whether proposed SUL transmission is ordinary communication RF or a new energy-only waveform.
RedCap alone does not establish SUL support, a particular band, high/fixed transmit power or continuous emission.
The equivalent 915-MHz first-version abstraction is unchanged. Numerical source/hardware parameters remain open. Influence 41.

## 2026-11-03 | EN-01 source/RF candidate for consolidated review

Q-INFLUENCE-42 is open: adopt or adjust ReferDoc/Plan/EN01_Source_RF_Profile_Candidate.md.
The synthetic candidate proposes DU DL 18/24/30 dBm, UE 20 dBm, common -50-dB UL gain and 1-ms RF transition; retained CW values are -2/10/22 dBm.
No new numerical value is accepted or implemented. One-way DL gains retain the accepted prototype reference; incident RF examples are not battery increments.
The UL equal-gain assumption and switching budget are research settings, not literature measurements. EN-02 hardware/energy choices remain open.
Influence 42; no code/runtime tests or calibration.

## 2026-11-03 | Charging-model source selected by the user

R-01 section 76 records the named WCSP 2025 paper, DOI 10.1109/WCSP68525.2025.1010215.
Its charging-model form is the requested reference. Only publisher metadata/abstract was retrieved, not the equations.
The generic interpolation/logistic question is superseded; obtain the PDF or model-equation pages before numerical adoption.
Influence stays 43. No fabricated formula or coefficients, code changes or model-calibration claim.

## 2026-11-03 capacity/mode source review

WCSP supplies a 1-mJ maximum/initial-energy candidate, not a full numerical mode-cost table.
R-01 section 79 and WCSP2025_Charging_Model_Mapping.md record the primary-source alternatives and transfer limits.
Check the initially full storage against experiment duration; do not label component-only powers as total Tag costs.
EN-02 and EN-03 remain open. Influence stays 44; no numerical capacity/mode acceptance.

## 2026-11-04 state-machine extension under discussion

The user selects PScatter as a state-design reference. Q-INFLUENCE-51 concerns whether to keep existing activation or add a new wake-up/synchronization procedure.
ReferDoc/Plan/PScatter_Tag_State_Mapping.md records the original transitions, power evidence and proposed mapping.
Existing accepted numeric energy/PHY settings remain in force; a complete adapted state machine is not yet selected.
Baseline remains deferred to the user's algorithm. No new implementation is approved by source selection alone.

## 2026-11-04 state adaptation accepted

Q-INFLUENCE-51 A keeps the existing selected-operation activation abstraction and 1-nJ cost.
No new wake-up packet or independent synchronization interval is added. State design is in docs/architecture/tag-state-design.md.
Runtime state implementation remains a later scoped task; existing numerical PHY/energy rules and deferred Baseline are preserved.
