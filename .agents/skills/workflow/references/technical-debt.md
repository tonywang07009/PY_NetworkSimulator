# Technical debt at change review

Run bundled ponytail-debt alongside change-wide code-review after local behavior
checks. Its marker scan is not a bug audit: no markers means no marked debt was
found, not that the code is debt-free. Keep standards/spec findings separate
from the marker ledger. Repair unmet acceptance before human trace; a backlog
entry cannot waive an approved requirement.

## Register and scope

Resolve the selected project's actual OpenSpec root. Reuse or create
<openspec-root>/tech_improve.md from the kit's management/tech_improve.md template
(installed under .agents/workflow-kit/management/). Reconcile an equivalent
existing register first; preserve unrelated records. This is a project backlog,
not a permanently active change and not a separate requirements authority.

Assign stable TI-0001-style IDs, never reuse closed IDs. Each entry retains
problem/impact, source change, real relative/absolute implementation locations,
evidence, deferral reason, applicability/limit, when to reassess, status and
subsequent approved change links. Use the user's language for the target record.
Decisions and state live here; source comments keep essential local context and
the TI ID/link. Issue/PR summaries link back instead of duplicating decisions.

## Reconcile the scan

1. Scan the selected repository's marked shortcuts, respecting Git ignores.
   Classify current-change debt, relevant existing debt and unrelated existing
   debt. Work on the first two within scope; summarize unrelated debt without
   an unsolicited cleanup or speculative register population.
2. Connect each relevant real deferral to an existing or new TI entry. Check
   missing IDs/entries, duplicate IDs, broken references, stale locations and
   fixes whose entries are still open. Confirm aliases or superseding entries
   before changing IDs. Preserve dated decisions when correcting records.
3. Unmet requirements or acceptance need repair. A simplification meeting current
   requirements may be deferred with its known limits and reassessment trigger;
   present the tradeoff during human trace. Missing evidence/trigger remains
   unresolved, not invented or silently accepted. Fix concrete in-scope issues
   directly, revalidate, and ask only about unresolved decisions or scope changes.
4. Record scan command/scope, marker counts, review/repair results and evidence
   in the existing change review record. Update the register within authorized
   workflow scope without another persistence approval. Direct standalone debt
   queries remain read-only unless the user asks to save them.

## Reassessment and closeout

A reassessment trigger starts evaluation, not automatic implementation. When
selected for work, create/link a normal scoped OpenSpec change; it follows the
same Issue/PR, WIP and human acceptance rules. Reconcile statuses before PR
preparation and project closeout. Distinguish proposed, accepted-deferred,
scheduled, resolved and superseded. Mark resolved only with linked implementation
and validation evidence; acceptance of a deferral is not resolution.

Source markers should retain concise ceiling/trigger context needed by readers
and ponytail-debt; the register owns the complete decision and its history.
