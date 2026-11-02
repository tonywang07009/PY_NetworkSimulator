# 600 ms resource timing in the simulator design

Date: 2026-10-31. Status: Accepted model decisions integrated into the derived design; Notebook accepted; core extracted into src/timeline on 2026-11-02.
The [decision record](../../ReferDoc/Plan/R-01_System_Model_and_Baseline_Decision_Record.md), §34.6–34.11, supplies the accepted behavior.
The [resource draft](../../Plan/resource-timeline-draft.md) supplies alternatives and acceptance scenarios.
This document does not replace OpenSpec or start a new change.

## Resource intervals

All Nodes share an outer window ID and the half-open interval [start_ns,end_ns).
The interval length is 600000000 ns, including UE occupancy.
The first start is 0. Later starts and gaps come from the scenario; no implicit period is selected.

For each Node and window:

1. Draw r uniformly over 0.60–0.75 for UE duration.
2. Round 600*r upward to whole milliseconds.
3. Convert to integer nanoseconds by multiplying by 1000000.
4. Draw one direction, UL or DL, with probability 0.5 each.

Direction and duration use separate draws with stable scenario/Node/window/kind identities.
Draws have no intended dependence across Nodes, windows or kinds.
Keep resource, channel, PHY and policy streams separate. Equal outcomes are legal and are not redrawn.

UE occupies [start_ns,ue_end_ns). Tag resource is [ue_end_ns,end_ns).
Paging, D2R and Guard share the Tag resource budget.
CW is off during UE occupancy, Paging and Guard; it is on only during D2R.
Changing the UE direction does not change the accepted fixed channel-interference model.

## Design data flow

Scenario configuration supplies the seed, Node identities and outer start/gap inputs.
ResourceTimeline keeps the generated full trace private.
The engine reveals eligible current resource to each Node; the policy receives a current observation.
Only the engine advances time and commits state.

| Proposed data group | Fields or contents | Visibility |
|---|---|---|
| Scenario input | Scenario/version/seed, shared window starts, fixed 600 ms length, accepted sampling profile | Environment configuration, not the full policy input |
| Outer-window snapshot | window_id, start_ns, end_ns, per-Node UE intervals and directions | Private environment trace |
| Current resource observation | node_id, window_id, now_ns, tag_start_ns, window_end_ns | Current Node/policy only after the resource is revealed |
| Resource trace | Node/window identity, raw duration draw, rounded duration, direction, source profile | Engine and offline evaluation |

These are data responsibilities, not final class names or new runtime types.
Config/DTO/Enum use the existing centralized-contract rule; internal mutable state stays with its owner.
The current topology/channel contracts remain in their accepted paths until a separate compatible shared-contract design is implemented.

## Event and channel integration

At outer-window start, the engine opens the current channel window once using its shared window ID and configured CW power.
UE prefixes do not permit Tag scheduling. The first eligible Tag decision for a Node follows its UE end.
The channel quality remains fixed throughout the shared window, including different per-Node Tag start times.
After a valid batch, retain CW_OFF, Guard and GUARD_END re-decision behavior.
No new batch can exceed the outer end or the run end.
Service credit still requires D2R_END < deadline; resource-end inclusion does not relax that condition.

At a shared boundary, finish prior-window consequences using the accepted same-time event rules before opening new-window channel work.
ChannelModel has one current window; opening the next one must not invalidate a still-required prior-window query.
The existing channel API binds identity and power, not wall-clock duration. ResourceTimeline/Engine enforce the 600 ms interval.
Do not add a second clock inside ChannelModel or change its PHY calculations for this design integration.

Keep the next-window CW-power announcement separate from resource visibility.
The first-window power initialization and exact announcement event placement need an implementation design before coding.
A known periodic start rule is predictable even without full-trace access; do not claim otherwise.

## Validation boundary

The accepted resource generation needs explicit scenario starts/gaps. Missing values are configuration gaps, not a reason to invent a period.
Validation must reject inconsistent intervals, overlaps and invalid Node identities before publishing a trace.
Later tests must cover rounding boundaries, unequal UE prefixes, legal repeated draws, same-seed reproduction, reordered queries and policy isolation.
The [resource draft](../../Plan/resource-timeline-draft.md#acceptance-scenarios-to-implement-after-approval) lists the ten proposed acceptance scenarios.

The accepted generation, current projection and output core now live in src/timeline. The Notebook imports them for demonstrations. The full event engine is not implemented. Remote delivery remains pending.
The current channel workflow remains 9/10 with no channel PR merge evidence; next-change specification/implementation follows the serial delivery gate.

## Notebook prototype design

See [the cell-by-cell prototype plan](resource-timeline-notebook-plan.md) for proposed teaching units, input/output records, examples and validation boundaries. It is design preparation, not executable code.

## Accepted source ownership

contracts.py owns immutable resource records. resource_timeline.py owns generation, projection and export. plotting.py owns the timing plot.
The Notebook imports these modules and retains settings, teaching text and assertions.
Compare extraction behavior with tests/timeline/fixtures/resource-before-extraction.json through test_resource_timeline_extraction.py.
