# Tag energy: accepted configuration and implementation readiness

Date: 2026-11-04. Status: configuration accepted; local-first Tag energy scope authorized; executed scalar charging Notebook delivered; full runtime and human acceptance remain pending.
This document consolidates discussion decisions. It is not a new OpenSpec change or an implementation-completion claim.
Authority: R-01 sections 51, 55-58, 62-75, 78, 81-85 and 87; the existing interview retains original answers.

## Accepted reference configuration

| Area | Accepted setting |
|---|---|
| Existing topology | One Donor, five IAB Nodes and one UE per Node; retain existing Tag IDs, positions, zones and owners. |
| Resource calendar | Shared 600-ms outer Windows starting every 1000 ms from zero; 400-ms gaps. |
| UE occupancy | Local prefix ceil(600*r) ms, r uniform over 0.60-0.75; UL/DL probabilities 0.5/0.5. Retain stable seeded draws. |
| RF transition | 1 ms after UE communication and before Tag-band operations; no harvesting. |
| Tag batch | CFA, at most seven distinct Tags; fixed SFS {1,2,4,8,16,32,64} assigned by stable Tag-ID order. |
| Paging | Per-Tag Paging; fixed 27-byte TB, 42-bit full ID, M=24, minimum three PRBs; batch-local continuous CP, zero gaps. Seven messages occupy 12 ms. |
| D2R | BPSK, tau=400/3 us, FEC rate 1/3, constraint length seven, CRC16, repetition one, short seven-bit ambles. |
| Legal TBS | Complete TB sizes {8,16,32,64} bytes; maximum valid application payload {6,14,30,62} bytes. |
| D2R occupancy | {35,63,118,228} ms after accepted ceiling conversion; preserve exact nominal durations in the timing reference. |
| Guard | Full 200 us after the last D2R and CW off; no harvesting. |
| Receive rule | RELIABLE succeeds; UNREACHABLE fails; RANDOM uses the accepted whole-code FBL reference. No extra arbitrary coding gain. |
| FBL reference | k=8*N, n=3*(8*N+16), coded data-symbol rate 7500/s; rho=2*SINR*B_eq/7500 with consistent integrated noise/interference. |
| Harvesting source | Only serving DU DL or configured UE ordinary SUL during the UE prefix. No neighbor-source credit or Tag-operation/gap harvesting. |
| Source powers | DU communication LOW/MEDIUM/HIGH=18/24/30 dBm; CW=-2/10/22 dBm with shared tier; UE fixed 20 dBm. |
| Source gains | Equivalent 915 MHz; DL one-way g0=0.0006797973850689421 at 1 m, exponent two, distance domain 1-50 m. UL common synthetic gain -50 dB. |
| Storage | Usable E_max=1 uJ; E_0=1 uJ at run start only; carry residual energy across all later boundaries. |
| Mode powers | Normal quiescent/retention 10 nW; receive and D2R total mode budgets 1 uW each. Do not add quiescent power again to active totals. |
| Activation | 1 nJ when activation is required; debit before future harvest. Becoming eligible alone causes no debit. |
| Conversion | Accepted zero-input-corrected Sigmoid: M=10 uW, s=2e5 W^-1, z=10 uW. |
| Recovery | At depletion, stop normal modes and enter ideal passive charging with zero separately modeled recovery overhead and no extra cold-start threshold. |
| Recovery eligibility | At existing legal Policy times, stored energy must cover a complete legal operation before selection; no asynchronous transmission or forced full recharge. |
| Data supply | Ample finite data at t=0, no refill; derive a conservative finite initial amount from the horizon and legal transmission bounds. |
| Credit | Unique successful valid payload only; retain failed data. A shared eligible payload can serve multiple active services, with each demand cap. |
| Evaluation end | Maximum configured service deadline. Credit remains strictly before each deadline. No new Policy/Paging at or after evaluation end. |
| Final cleanup | Existing Guard may finish after evaluation end within its outer Window; reserve its complete time/energy and record cleanup end separately. |

These are accepted research settings, not a measured complete hardware profile or full standards-conformance result.
The source and converter gains, fixed mode budgets, weak-input tail and ideal recovery retain their declared calibration limits.
The existing ChannelModel's older 10000/s entry value does not prove the selected-TBS PHY mapping has already been integrated.

## Accepted small reference services

| Service | Required Tag IDs | Valid application demand | Exclusive deadline |
|---|---|---|---|
| S1 | Tag-001, Tag-002, Tag-003 | 128 bytes = 1024 bits | 15 s |
| S2 | Tag-003, Tag-004, Tag-005 | 256 bytes = 2048 bits | 20 s |

Q-INFLUENCE-50 A accepts this table. Both services start at zero, so evaluation ends at 20 s.
Require these IDs in the actual topology; do not relocate Tags or alter their owner/zone to match the table.
This is a small integration reference, not representative network load or evidence that all services can finish.

## First module scope

The teaching Notebook notebooks/04_tag_energy.ipynb now exists with executable scalar examples. The broader runtime scope below remains future work.
Keep initial business logic in the Notebook until human acceptance, following the existing module pattern.

| Responsibility | Observable result |
|---|---|
| Energy configuration | Declared SI units, accepted defaults, rejection of invalid/nonfinite/negative values and incompatible conversion parameters. |
| RF-to-DC conversion | Zero input gives zero; output is nonnegative, bounded by input and saturation, with stable evaluation. |
| Tag state | Per-Tag stored joules and normal/recovery state, with no shared mutable battery state or later reinitialization. |
| Interval accounting | Integrate actual source/mode intervals with integer-ns external time; track harvested/consumed energy and capacity overflow. |
| Operation budget | Calculate complete receive/wait/D2R/Guard/activation costs from supplied durations; report affordability without selecting a TBS. |
| Causal activation | Reject insufficient stored energy without partial mutation; debit only a real selected activation. |
| Depletion/recovery | Resolve depletion explicitly, continue only phase-permitted passive charging and preserve causal eligibility. |
| Human trace | Readable event ledger, energy/time plot and examples tied to each accepted requirement. |

Core inputs are current RF watts, phase/mode, elapsed integer ns and explicit planned-operation intervals.
The resource/source adapters supply those inputs; the energy core does not read complete future ResourceTimeline traces.
Do not reuse the two-way D2R receive budget as a one-way harvesting input.
The module does not choose Tags, TBS, batches, fairness weights or Baseline ordering.
Use explicit event sequences for isolated verification. These are test inputs, not an additional scheduling algorithm.
Full Access, ServiceManager, Validator and Engine integration are later modules; the current request does not justify implementing them all at once.

## Required behavior checks

| Case | Independent acceptance condition |
|---|---|
| Zero RF | No DC gain; normal quiescent cost still applies until depletion. |
| Allowed UL harvesting | At 1-uW RF input, DC=0.2571323571 uW; normal 400-ms net gain=0.09885294284 uJ. |
| Forbidden phases | No harvesting during switch, Paging, D2R, Guard or inter-Window gaps. |
| Capacity | Excess harvest is discarded at 1 uJ; it is not banked for later use. |
| Selected TBS costs | D2R alone costs 35/63/118/228 nJ at the accepted 1-uW mode power. |
| Full-operation admission | Include all relevant mode intervals and activation, not only pure D2R duration. |
| Failure | Receive failure does not refund the energy of an executed full transmission. |
| Activation boundary | Handle just-below, equal and above the required stored cost; an unaffordable request changes no state. |
| Depletion | A negative-net interval reaches zero explicitly; it never leaves a negative battery or hides deficit through clipping. |
| Passive recharge | From zero, allowed 400-ms UL harvesting stores 0.10285294284 uJ before activation; forbidden intervals add zero. |
| Persistence | Window/service boundaries never refill the battery. Updating one Tag leaves another Tag unchanged. |
| Composition | Splitting a constant-source interval preserves the final energy/state, including saturation and depletion crossings. |

Before tests, map these cases into the approved OpenSpec/TDD contract with a public behavioral boundary and no irreversible side effects.
The listed values are earlier scalar checks, not new module test results.
Numerical handling of sub-ns depletion crossings must be stated during design; do not write floating-point event times into the external clock.

## Workflow output and acceptance route

Use the project-selected workflow, TDD and Ponytail contracts for implementation.
Deliver the complete executable Notebook with unit/source explanations, focused tests and a clean-kernel execution record.
Deliver an Archify system/change view and tree-form code-trace.md with actual absolute/relative implementation paths, requirements and tests.
Run Standards/Spec review and ponytail-debt, repairing actual scoped defects before human trace.
Explain each section to the user. Extract accepted core logic into src/energy only after Notebook acceptance, with independent baseline comparison.
Prepare paired README updates, specification sync and delivery material under the authorized workflow scope.
Commit, remote Issue/PR creation, push, merge and archive completion remain separately authorized/evidenced actions.
Do not claim that local acceptance or tests establish merged delivery or a completed workflow.

## Historical workflow gate and scoped resolution

The selected workflow index has one active GitHub-delivery record for add-channel-model-notebook, not a retained local-only contract.
Channel tasks are 11/12 and ResourceTimeline tasks are 8/9. Their remaining delivery work is not authorized or marked merged.
The index's stage stays spec because a remote Issue is absent; actual accepted local modules are evidenced by their tasks and validation.
Project agent.md requires: Before you start the next change, make sure that the PR has been merged.
Workflow SKILL.md states: One unmerged change is active; do not start the next even while waiting for review.
Its references/github.md also states that implementation and next-change specification wait.
The user subsequently answered "可以,先trace 充電模組", confirming the scoped local-first Tag energy exception.
Trace material is in docs/architecture/tag-energy-trace/. The immediate request is trace before implementation.
Earlier changes remain unmerged; their delivery state and publication authorization remain unchanged.
The exception does not claim full workflow completion or authorize unrelated module work.

## Accepted state-design adaptation (2026-11-04)

Q-INFLUENCE-51 A accepts the scheduled-activation adaptation described in docs/architecture/tag-state-design.md.
The existing 1-nJ activation event is retained. No additional wake-up packet or independent synchronization duration is selected.
The Notebook now implements charging and scheduled state traces with immutable snapshots.
The general Engine, RF/timing adapters and service-credit integration remain engineering work.
State-trace decisions have zero blockers; Baseline, fairness and formal experiments remain three later research groups.
