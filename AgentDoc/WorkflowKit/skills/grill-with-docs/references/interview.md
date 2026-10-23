# Interview record and question budget

For an authorized interview, use the target project's interview/ directory;
create it only if absent. Reuse an equivalent existing record and index. A path
occupied by a file or pointing outside the selected project needs reconciliation,
not replacement. Kit installation never creates live interview records.

Use interview/README.md for topic, status and links. Name each workflow record
YYYY-MM-DD-work-topic.md using its start date; continue it across sessions.
For a distinct same-day workflow with the same topic, add -2, -3, etc. after
checking that it is not a resume. Never overwrite another record.

Record goal, project/workflow identity, date, six facet counts, question IDs,
answers, optional notes, confirmed decisions, evidence locators, assumptions,
risks, unresolved decisions and links to specs, architecture and delivered changes.
Preserve observable answers and decisions, not hidden reasoning or unrelated
private conversation. Annotate corrections with dates and superseding links.

## Six facets

Adapt UNISON decision analysis to a product-development interview. The examples
below illustrate a campus lost-and-found tool; replace them with the user's
actual domain and do not adopt example requirements without agreement.

| Facet | Decision | Example |
|---|---|---|
| Understand | User, situation and current problem | Students must search many unrelated posts to find an item. |
| Niche | Valuable improvement, scope and non-goals | Improve finding an item first; defer claim adjudication. |
| Influence | Data, actors, dependencies and constraints | Uploading a photo affects storage, permissions and search. |
| Description | Facts, evidence and uncertainty | "Pictures are easier" is a hypothesis until supported. |
| Tradeoffs | Alternatives, value, cost and risk | Compare keyword, category and image search under actual constraints. |
| Decision/feedback | Choice, acceptance, stop and rollback | Evaluate representative searches and agree observable acceptance. |

Before each question briefly state its purpose and one relevant example. Ask
one unresolved decision at a time, normally with 2-3 options, a recommendation
and tradeoff, a free-text alternative and optional notes. Show facet and count.
Do not bundle several decisions into one question or present all six facets at
once. Reuse existing answers and evidence; no minimum question count applies.

Each facet has at most 10 substantive questions, including followups and final
clarification. Persist counts across resumes. Reserve remaining questions for
pre-implementation decisions. At the limit, retain uncertainty, its provisional
assumption, risk and affected work, then discuss another facet. Before any
dependent implementation, return to unresolved decisions and wait for answers.
If the cap leaves no room, explain it and ask whether to narrow scope or allow
additional questions; never silently reset the budget or treat silence as consent.
Independent authorized work may proceed. Ten is a user-selected workflow limit,
not a scientifically established cognitive-load threshold.

End a facet with a concise decision/evidence/gap summary. At interview closeout,
link the settled scope to OpenSpec and the derived Archify view using workflow's
[architecture contract](../../workflow/references/architecture.md).

## Learning from previous interviews

Read only the selected project's relevant interview index and linked records,
plus existing Wiki patterns; do not scan other projects or collect global user
profiles. Explicit preferences carry their source, date and applicability and
can be reused immediately. Inferred concerns remain [Needs Verification] and
may guide a question, not silently add a requirement or exclude alternatives.
Current instructions override stale preferences; record corrections and scope.

At project closeout, pass bounded interview events and outcomes through llm-wiki
capture to skill-evolution assess. Repeated citations of one interview are one
event. Retain counterevidence and rejection reasons; quality candidates still
need the existing eligibility, comparison and activation gates. Do not rewrite
historical answers, mutate active skills or write personal/global memory here.
