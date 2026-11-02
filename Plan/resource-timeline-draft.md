# UE/DU resource timeline draft

Date: 2026-10-31. Status: Outer interval structure and sampling dependence accepted. Not an implementation approval.
Scope: W03 resource timing and its interfaces. No simulator code changes are included.

## Purpose and sources

ResourceTimeline describes when UE traffic occupies a Node and when that Node can schedule Tags.
It supplies external resource events to the engine; the policy does not own the resource schedule.

- [Original System Model](../ReferDoc/Plan/main.pdf), pp.10–11: UE before Paging/D2R, within a DU interval, and completion constraints.
- [Decision record](../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md), §34.6–34.9: latest duration, recurrence, rounding and direction decisions.
- [Handoff specification](../ReferDoc/Plan/Codex_Handoff_Specification_Ambient_IoT_DES.md), §§2,3,8: resource visibility, event ownership and acceptance.
- [Channel implementation](../src/channel/channel_model.py), ChannelModel.window/link: one current window ID for all configured Nodes.

The original source is version_1/main.pdf under /home/tonywang/115-1/system_model_mod.
Its hash matches the linked project copy. The UL/DL random scenario is a later simulator decision, not a claim from the original diagram.

## Accepted resource contract

| Item | Accepted behavior |
|---|---|
| Outer interval | 600 ms, including UE occupancy |
| UE position | Prefix of each window; initial window starts at global t=0 |
| UE duration | Sample ratio r uniformly over 0.60–0.75; use ceil(600*r) ms |
| Engine time | Convert the rounded duration to integer ns |
| UE direction | Exactly one of UL or DL per Node/window; each has probability 0.5 |
| Tag resource | From that Node's UE end to the outer window end |
| Tag operations | Paging, D2R and Guard must fit; CW is active only during D2R |
| Repetition | Later windows occur. The one-time-only UE rule is superseded. |
| Reproducibility | Same accepted configuration and seed produce the same resource trace |
| Service deadline | Keep the later accepted strict t < deadline rule |

Direction and duration are separate random variables. Their dependence is part of the proposed sampling design below.
The 150–240 ms remainder is a resource budget, not a payload-only transmission duration.

## Proposed window representation

Use an outer interval [start_ns,end_ns), with end_ns=start_ns+600000000.
For Node-j, UE occupies [start_ns,ue_end_ns); Tags use [ue_end_ns,end_ns).
At ue_end_ns the UE interval is over and a Tag decision can become eligible.
The engine still checks service state, energy and batch duration before admitting a transmission.

Recommended: share the outer window ID and boundaries across Nodes; sample each Node's UE prefix separately.
This permits different Tag start times while using the existing channel window interface.
Q-INFLUENCE-11 subsequently accepted these shared outer intervals.
Asynchronous outer intervals remain an alternative, with additional channel lifetime and power-binding design work.

Illustrative window, in ms:

| Node | UE direction | UE interval | Tag resource |
|---|---|---|---|
| Node-1 | UL | [0,400) | [400,600) |
| Node-2 | DL | [0,425) | [425,600) |

The values are examples within the accepted range. Neither the durations nor directions are fixed fixtures yet.

## Decision 1: Outer starts and gaps

Let the first start be 0. For subsequent windows, start_next=end_current+gap_current.
The accepted 600 ms length does not select a gap or repetition period.

| Candidate | Impact |
|---|---|
| Shared, contiguous intervals | Small initial fixture and direct channel reuse. Future starts are inferable if the rule is known. |
| Shared intervals with scenario-supplied gaps | Represents unavailable resource between windows. Gap values and their generation model still need evidence or an accepted test assumption. |
| Different outer intervals by Node | Represents asynchronous resource availability. Requires a proposal for per-Node channel/power lifetimes before implementation. |

Selected in Q-INFLUENCE-11: shared outer intervals with scenario-supplied starts/gaps.
For initial automated fixtures, explicit gap values are sufficient; they do not define the research distribution.
Do not invent a gap distribution or silently assume a zero gap.
The source diagram shows backhaul intervals, but does not give numerical durations for them.

A known periodic rule makes future starts predictable even when the trace object is hidden.
If contiguous periodic intervals are selected, distinguish prohibited direct trace access from predictable future timing.
Do not claim that such a schedule has unpredictable future starts.

## Decision 2: Sampling dependence

Selected in Q-INFLUENCE-12: separate duration and direction streams by scenario seed, Node ID, window ID and draw kind.
Use stable identities so changing traversal or policy calls cannot change a Node's resource trace.
This follows the existing local-RNG pattern without selecting a new implementation interface.
Keep resource, channel, PHY and policy random streams separate.

| Candidate | Impact |
|---|---|
| Separate draws by Node/window and kind | Different Node loads and changing windows; no intended shared temporal component |
| Shared or correlated draws | Common load effects; requires an explicit coupling model and acceptance cases |

The first candidate was selected for the current simulator scenario.
Equal 50/50 marginal direction probabilities alone do not establish independence.
Pseudorandom draws can coincide; equal durations or directions across windows are legal outcomes.
Do not reject or redraw such outcomes merely to force visible differences.

Apply upward rounding after the continuous duration draw.
This produces a different discrete distribution from drawing integer milliseconds uniformly.
Do not describe the rounded integers as a new uniform distribution.
Save the draw and rounded duration in the private trace for interpretation.

## Proposed responsibility and visibility boundary

| Component | Responsibility |
|---|---|
| Scenario configuration | Accepted distribution parameters, duration, seed and outer-interval inputs |
| ResourceTimeline | Generate and retain the full per-Node resource trace |
| Engine | Reveal current resource events and commit state changes |
| Node | Build an observation from current eligible resource and current state |
| Policy | Propose Tag/TBS actions; no resource generation or full-trace access |
| Channel | Bind power and quality to the accepted current outer window identity |

These are responsibilities, not a requirement for one new class per row.
Use the existing module conventions; add only fields needed by the accepted behavior.

The engine opens the resource interval before any Node can schedule Tags.
A Node's first Tag decision occurs after its UE prefix ends, not during UE occupancy.
Re-decisions within the Tag portion still occur after Guard completion.
An interval ending at the service deadline does not change strict service-credit eligibility.
CW remains off during both UL and DL UE occupancy, Paging and Guard.
The treatment of UL/DL interference remains the accepted fixed-interference model until a separate physical model is approved.
Do not change channel interference values merely because a direction label changes.

For shared intervals, opening window w+1 must not invalidate pending channel-dependent work from w.
Use the existing same-timestamp completion and state-update rules before admitting new-window work.
Retain the existing next-CW-power announcement contract; its exact event placement needs an engineering proposal.
A power announcement does not reveal a future UE duration or SNR.

## Acceptance scenarios to implement after approval

1. A 398.2 ms duration rounds to 399 ms and converts to 399000000 ns.
2. Ratio boundary inputs 0.60 and 0.75 yield 360 and 450 ms; invalid settings are rejected.
3. Each UE interval has one direction and stays inside its outer interval.
4. Tag operations do not overlap UE occupancy; D2R plus Guard fits before the outer end.
5. Reordering Node queries or changing policy RNG calls leaves the resource trace unchanged.
6. Repeated duration or direction values are retained; no forced variation is introduced.
7. Same scenario/version/seed reproduces the complete resource trace.
8. Policy cannot access future trace values; known periodic rules are described honestly if selected.
9. UE end, Guard end, service deadline and window boundaries use the accepted same-time rules.
10. A run ending inside an outer interval admits no new batch that exceeds the actual run boundary.

For item 10, propose validation against both interval end and run end; do not extend the service run to finish a batch.
The final-window generation and cleanup behavior still belongs to the existing engine-boundary design work.
No claims about an observed 50/50 frequency are made from a few windows; the probability rule needs appropriate deterministic and statistical checks.

## Review and implementation boundary

The outer interval and sampling-dependence choices are accepted. Numeric scenario gap inputs are not yet selected.
Influence, Description and Tradeoffs are capped; do not reset counts or relabel a question to bypass a cap.
Obtain explicit permission for more questions or narrow the discussion before unresolved dependent implementation.
The current channel change remains unmerged. Discussion can proceed, but a new change is not started by this draft.
The working original model, later accepted decisions and OpenSpec remain distinct evidence layers.
