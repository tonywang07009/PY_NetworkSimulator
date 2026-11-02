# Remaining simulator decision areas

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
