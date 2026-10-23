---
name: write-reviewable-pr
description: Write or polish reviewable PR descriptions from the actual diff, with purpose, reading order, function flow, manual checks, module relationships and validation evidence. Use for module PRs, staged delivery or improving PR readability.
---

# Write a reviewable PR

Write for a reviewer with basic engineering knowledge who is new to this change.
Use the user's language, normally Traditional Chinese for this skill. Preserve
the approved structure in [pr-structure.md](references/pr-structure.md) and the
project's required PR template. Pure polishing keeps the supplied structure.

## Establish facts

Read applicable AGENTS.md, CONTRIBUTING.md and the PR template. Identify actual
base/head, diff (including relevant uncommitted work), governing OpenSpec, Issue
and available evidence. Read existing PR text and feedback on resume. Inspect
important functions and callers using the project's source route; report limits.

For pure wording changes, use the supplied draft and existing evidence. Preserve
scope, technical rules and validation status. Investigate only wording-dependent
facts; report specification conflicts or stale states separately. Polishing is
not a business decision or a new verification run.

Exit: observable delivered behavior, important entry points, dependencies and
validation/manual-acceptance status can be traced to evidence. Label gaps; ask
only for consequential decisions unavailable from inspection. Reuse settled
scope and preferences.

## Shared writing authority

Before drafting or polishing, read the kit's docs/output.md, resolving source
and installed resources via workflow's
[project-context guide](../workflow/references/project-context.md#resource-locations).
That document owns terminology, sentence cohesion, change rationale and evidence
wording, including drafting, layered presentation and revision checks. It ships
in .agents/workflow-kit/docs/output.md; a standalone copy of this skill also
needs that resource and its location. Preserve this skill's layout obligations.

## Compose within the existing template

- Purpose/review focus: explain the trigger, changed behavior and user outcome
  in one or two sentences, then the important review judgment. Use a concrete
  example for complex rules. Describe the final diff, not conversation history.
- Delivery scope: identify dependencies and pending behavior that affect review.
  Label future contracts beside their examples. Number batches only for an
  actual approved staged plan and preserve its sequence.
- Reading order: link a few key entry points and explain what each establishes;
  move from the user/write operation to read/rules and tests. Identify generated
  or mechanical changes so the reviewer can prioritize behavior.
- Module flow: include Mermaid with each node's action and actual function name.
  Cover the implemented main path and outcome-changing refusal/failure branches.
  For documentation/config changes, use actual file/config names and explain
  why functions do not apply. Preserve verified caller relationships.
- Manual checks: state role/preconditions, operation and observable expected
  result. Select applicable success, refusal, permissions/isolation and state
  cases; no fixed count. Link detailed request/response or setup examples.
- Module relationships: explain who provides which interface, how this change
  uses it and who takes over afterward. Include only real dependencies.
- Evidence: give actual commands, versions, results and relevant limitations.
  Keep independent review, automatic checks, GitHub CI, manual acceptance and
  reviewer approval distinct. Counts need behavior mapping. Leave unexecuted
  manual checks unchecked and link CI to the evaluated head.

Put long test matrices, environment troubleshooting and secondary examples in
GitHub details blocks or accessible documents. Keep purpose, review focus, flow
and manual-review entry points visible in the existing layout.

## Check and deliver

Verify identifiers, paths, fields, status codes, conditions, exceptions, Mermaid
relationships and checkbox states against the source. Public PR links must be
accessible repo URLs, preferably pinned to the reviewed commit. Summarize private
local OpenSpec/log evidence or link an authorized accessible copy; local absolute
paths alone are not usable GitHub navigation. Historical PRs supply presentation
examples, not current test counts or PASS claims.

Return the complete title/body or update the requested local draft. In workflow,
follow [github.md](../workflow/references/github.md): one Issue/PR per change,
publish after human trace acceptance with code/specs/archive/README together,
wait for user merge and reconcile feedback against the actual head. This skill
never merges a PR. Writing does not authorize remote updates, commits or pushes.
Complete already-authorized checks; do not launch unrelated whole-project review
or refactoring merely to write the PR.

The approved presentation originated in
[RailDocs PR 44](https://github.com/UJayJoAnDao/rail_docs/pull/44).
Skill organization follows
[writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md).
Earlier style guidance included
[Editing.tw](https://www.editing.tw/blog/academic-writing-style-tips);
current shared rules and before/after examples live in docs/output.md.
