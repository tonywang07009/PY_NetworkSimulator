---
name: grill-with-docs
description: Sharpen a repository-grounded plan or design through a one-question-at-a-time interview and retain conclusion-bearing results.
disable-model-invocation: true
---

## Project context

Use applicable AGENTS.md to resolve the selected project's OpenSpec spec/toolbox.
For missing or ambiguous mappings, read the available workflow skill's
[project-context guide](../workflow/references/project-context.md).
This resolves tools and evidence only; it does not start the workflow or repeat
settled decisions. Follow this skill's own scope after context is resolved.


# Grill With Docs

For a cross-project workflow overview, read [workflow.md](workflow.md). Skip
that reference for a single already-scoped decision.

Read the current project's applicable `AGENTS.md`. Follow its tool routing and
documentation governance; resolve project paths from that project, not this
installed skill. Read only relevant contracts, source, and evidence. Inspect
facts before asking the user; mark unsupported claims `[Needs Verification]`.

1. Establish goal, non-goals, observable behavior, owner, acceptance, and
   rollback/stop conditions. Resume settled decisions rather than restarting.
   Read [interview.md](references/interview.md) to create/reuse the target
   project's interview record and use the six UNISON-derived facets, relevant
   examples, options/optional notes and persistent 10-question-per-facet budget.
2. Ask one unresolved decision at a time and wait for the answer. Record explicit
   preferences separately from inferred concerns. At the budget limit retain
   assumptions/risks and continue other facets; revisit unresolved decisions
   before dependent implementation. Never infer consent from silence.
   For evidence-dependent tradeoffs read [literature.md](references/literature.md).
3. Use `improve-codebase-architecture` for scoped candidates when ownership or
   testability is unclear. Skip a full review when the existing design suffices.
4. Retain agreed decisions and source links in the interview record; map approved
   requirements into OpenSpec without creating a competing specification. Return
   the record and derived architecture handoff to workflow. Use
   `domain-modeling` only for terminology or durable architectural decisions.
5. Use `openspec-explore` and `openspec-propose` for formal changes as needed.
   End with scope, acceptance, unresolved issues, and the next stage. Do not
   repeat approval already supplied by the user. Apply the kit's docs/output.md
   writing authority through the project-context resource route before asking
   decision questions or drafting human-readable records, including questions
   delivered through host UI tools.

The user chooses model and effort. Size the evidence pack and decision to the
task; do not prescribe model names or automatic model-switch gates.
