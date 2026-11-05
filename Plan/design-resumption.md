# Simulator design resumption

Date: 2026-10-31. Status: Discussion; no new module implementation selected.

## Source alignment

The original source directory is `/home/tonywang/115-1/system_model_mod`, as supplied by the user.
`version_1/main.pdf` is an 11-page System Model dated October 7, 2026.
Its SHA-256 matches the project copy [ReferDoc/Plan/main.pdf](../ReferDoc/Plan/main.pdf):
`78ccd849266f91d3e12b3ecc30b9f2a937c270363dc4ea5a1ae8f0908ee38bbe`.
The older `system_model.pdf` is also 11 pages; extracted text differs only in the title date, not proof that all figures match.
The 25-page PDF under ReferDoc/DesignSimluator is a secondary research guide that refers to the original slides.
It is not a replacement for the original model or a normative standard.

Read the original slides, the accepted decision record, and the applicable specification before dependent design work.
Keep later confirmed decisions explicit where they differ from the slides.

## Current scope and remaining design

| Area | Evidence and remaining work |
|---|---|
| Topology | Implemented in src/iab; original slides pp.3–6 give the scene and entity roles. |
| Channel | Implemented and accepted locally in src/channel; remote delivery remains pending. Plan's earlier pending-status passages are historical. |
| Time/resources | W03: derive the UE/DU availability model from p.10. The 600 ms length is confirmed; it includes UE occupancy (R-01 §34); shared outer intervals and independent UE draws are accepted; accepted core is now in src/timeline with a Notebook demonstration; calibrated scenario start/gap inputs remain to be supplied. |
| Access/PHY | W04: source-first order B confirmed in R-01 section 35. See [source map](../AgentDoc/openspec/discuss/2026-11-02-access-phy-source-map.md) for TBS/SDU limits, fixed resources and complete timing. Individual Paging completes before CW/parallel D2R; eight orthogonal SFS resources and one final Guard are confirmed in R-01 sections 37-38. Actual SDU as application payload is accepted in R-01 section 39; a reduced TBS set with a 64-byte cap and later expansion is accepted in section 40. Initial complete-TB members {8,16,32,64} bytes are accepted in section 41; use actual byte-valued Actions per section 42. Finite available Tag data is accepted in section 43. Workload timing/amounts, identity, segmentation and numerical PHY mapping remain open. |
| Energy | W05: define capacity, power consumption, harvesting and causal depletion against pp.3,6,11. |
| Services | W06: implement accepted credit/deadline rules against pp.7–9,11; the later strict deadline and objective decisions supersede the original expressions where stated. |
| Closed-loop simulation | W07–W10: validation, event ordering, observations, minimal policy and integrated acceptance. |
| Research comparison | W11–W15: baseline/fairness, calibration, experiment budget and the previously selected CLM route; CLM implementation remains future work. |

The original p.10 DU interval includes UE uplink before Paging/D2R.
Do not silently treat the entire interval as free Tag airtime.
The original p.11 uses a non-strict deadline inequality; the accepted simulator rule is `t < deadline`.
Do not silently revert that later decision.

## Confirmed interval meaning

Q-INFLUENCE-06: A selected. The 600 ms DU interval includes UE uplink occupancy.
Paging, D2R and Guard must fit within the remaining time. See R-01 §34.
The later accepted UE duration rule is listed below; no window repetition period is selected.

## Initial UE timing

Q-UNDERSTAND-01: A selected. All UEs start at global t=0; each Node can have a different UE end time.
The 200 ms and 150 ms examples are not fixed parameters. The notation does not specify a repetition period.

## Current UE resource contract

The 600 ms DU interval includes UE occupancy. Each window uses the 60%–75% uniform-sampling rule with upward rounding.
Q-UNDERSTAND-03 supersedes the earlier one-time-only UE rule. UE occupies the window prefix, then Tags use the remaining time for Paging/D2R/Guard.
The unrounded UE duration is 360–450 ms. Global t=0 identifies the initial interval; later intervals use their own relative origins.
Earlier 200/150 ms examples illustrate per-Node duration differences and are not values for this rule.
Numerical starts/gaps remain scenario inputs. Independent sampling, UL/DL scope and probability are confirmed below.

## Confirmed rounding

Q-UNDERSTAND-04: A selected. Sample uniformly before rounding, then use UE_ms=ceil(600*r), r uniform over 0.60–0.75.
Convert to integer nanoseconds with UE_ns=UE_ms*1000000. Do not substitute integer-uniform sampling.

## Confirmed direction scope

Q-UNDERSTAND-05: A selected. Each window's UE prefix uses a single direction, UL or DL, for its sampled duration.
The uniform duration rule is separate from the confirmed direction probabilities below.

## Confirmed direction probability

Q-INFLUENCE-10: A selected. UL and DL each have probability 0.5, reproducible with the scenario seed.
This is a scenario assumption. Independent cross-Node/window and draw-kind sampling is confirmed in Q-INFLUENCE-12.

## Remaining decision inventory

See [remaining decision areas](decision-inventory.md). No new question is active while reporting the inventory.
The unmerged channel change still permits discussion but not next-change implementation or publication.

## Resource timeline proposal

See [the full resource-timeline draft](resource-timeline-draft.md) for alternatives, recommended boundaries, interface impacts and acceptance scenarios. Both model choices are accepted. The resource core is implemented in src/timeline; calibrated numerical scenario inputs remain pending.

## Shared outer intervals accepted

Q-INFLUENCE-11: A selected. All Nodes share each 600 ms outer interval, with scenario-supplied starts/gaps.
Per-Node UE prefixes and Tag starts can differ. No numerical gap values or generation distribution are selected.
Q-INFLUENCE-12 selected separate duration/direction draws by Node/window, reproducible with stable identities and scenario seed. Random coincidences are legal.
