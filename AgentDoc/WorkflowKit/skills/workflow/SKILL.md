---
name: workflow
description: Start or resume a development project spanning OpenSpec changes, with change-level checkpoints, progress summaries, local cross-project completion tracking, GitHub integration, human trace, and project knowledge closeout.
---

# Workflow

One workflow is one user-scoped project containing one or more dependent OpenSpec
changes. Count it only when the entire development scope is complete. Tasks,
individual changes, conversations, and tool calls do not count as workflows.
Respond in the user's language. The user chooses model and effort.

## User-facing output

Before asking the user for a decision (in chat or a question tool), or drafting
or revising any human-readable CLI/chat explanation, OpenSpec, README, tutorial,
project documentation, progress/validation reports or Issue/PR text, read the
kit's `docs/output.md` and apply its draft/revise and layered-reading checks. Resolve its source
or installed location through [project-context.md](references/project-context.md#resource-locations).
It is the shared writing authority for readers with basic engineering knowledge
who are new to this change. Apply its terminology, cohesion, rationale and
evidence checks while preserving project templates and this workflow's checkpoints.
Keep machine-readable CLI output and raw evidence intact.
Decision questions follow the same authority: explain the purpose, give a
relevant example, present options/tradeoffs and optional notes, and reuse
settled answers instead of adding confirmation gates.

## Teaching level

The first registered workflow for this local OS user receives full teaching;
later workflows receive brief prompts, regardless of completion count or repo.
Read the local index without writing before the entry interview to select the
level; no registered workflows means first use, even if mode preferences exist.
Follow [delivery.md](references/delivery.md#teaching-during-delivery) from the
opening overview through project closeout. Explain more whenever requested.
Persist level and delivered topic markers through [state.md](references/state.md#teaching-progress)
after scope-confirmed registration. Resume the same workflow's teaching progress
across conversations; do not repeat its opening lesson or completed explanations.
Status-only and mode-only requests do not launch teaching or consume first use.
Teaching never adds approvals or changes checkpoint mode or human acceptance.

## Start or resume

1. Begin a new workflow with `$grill-with-docs`. Read applicable `AGENTS.md`
   and only the existing records needed to ground the interview or distinguish
   a new workflow from a resume. Confirm intent, goal, non-goals, observable
   acceptance, owner, and stop conditions before project setup, registration,
   specification, or implementation. Save the interview record and question
   budget through grill-with-docs. Ask one unresolved decision at a time and
   wait for its answer; reuse answers already supplied. On resume, do not repeat
   the interview or request reconfirmation. Re-enter `$grill-with-docs` only when
   the user introduces new requirements, and clarify their scope and impact before
   updating scope or implementing them. Status-only and mode-only requests skip
   the interview and perform only the requested operation.
2. Read applicable project `AGENTS.md` and follow its tool routing. Resolve skills
   from the active catalog or sibling folders in this bundle; load them as needed.
   Resolve the selected OpenSpec project's spec/toolbox through
   [project-context.md](references/project-context.md). Decompose the problem and
   consult the installed tool guide before selecting this project's capabilities.
3. Read [state.md](references/state.md) and query the local user index. Resolve the
   current project root. Resume its sole active workflow; ask which one if several
   exist; clarify a new project if none exists. Honor an explicit new-workflow
   request. With existing OpenSpec but no index, identify its scope before
   registering it; do not create duplicate changes.
4. Reconcile the index against CLI-resolved OpenSpec paths, tasks, validation,
   and archive evidence. Explain discrepancies before updating the index. Missing
   paths require investigation, not a completion claim or counter reset.
5. Read [github.md](references/github.md) for new GitHub workflows; preserve an
   unmigrated legacy local contract. Read [architecture.md](references/architecture.md)
   after interview/design decisions and before human trace/PR preparation.
   Before continuing, summarize in four to six lines: implementation goal,
   completed/total changes, current change's tasks, validation and Issue/PR/merge state,
   next action, checkpoint mode, project spec/toolbox and actual change paths. Label unverified
   progress as such. Do not inspect other projects merely to build this summary.
6. Follow [delivery.md](references/delivery.md). Reuse settled decisions. Resume
   unfinished work directly. At a saved change boundary, a new bare `$workflow`
   invocation or request to continue authorizes the next change only after the
   current change has actually merged (or completed its retained local contract). A status-only
   request does not authorize implementation.

Example summary; replace paths and counts with verified values:

> Goal: deliver a shop with login, cart, and checkout.  
> Progress: 1/3 changes complete; cart tasks 2/4 complete; integration tests pending.  
> Next: implement quantity updates; pause after the whole cart change completes.  
> OpenSpec: `<project>/openspec/changes/shopping-cart/`.

## Checkpoints and closeout

- New workflows use one Issue and one PR per change. After scope confirmation,
  track progress in the Issue. Implement, validate, review and deliver complete
  architecture plus code-trace.md before a section-by-section human walkthrough.
  Resolve feedback and obtain acceptance, then sync specs, prepare the archive
  and update README on the same delivery branch. Use write-reviewable-pr for
  the complete PR, including code, specs and closeout documents.
- During implementation, complete TDD's local semantic check after each
  verifiable behavior. At change review run code-review and bundled ponytail-debt;
  follow [technical-debt.md](references/technical-debt.md) to reconcile markers
  and the OpenSpec improvement register before human trace.
- Wait for the user to merge. PR creation, local archive preparation, approval
  or passing CI alone is not completion. Verify actual merge evidence and Issue
  resolution before marking the change merged. One unmerged change is active;
  do not start the next even while waiting for review. Changes after acceptance
  require reconciliation and affected revalidation/acceptance.
- Default `change` mode reports the verified merged result and next change, then
  stops. `auto` may continue only after the same gates. Both modes stop for
  unresolved decisions, missing authorization/evidence or in-scope failures that
  cannot be resolved. Diagnose authorized failures before declaring a blocker.
- Complete a workflow only after all scoped changes are merged (or archived
  under an explicitly retained local contract), project acceptance is satisfied,
  and required project closeout is done. Count each workflow ID once. Legacy
  completed history is immutable and does not need retroactive GitHub records.
- After **5 complete workflows across projects for this local user**, offer `auto`
  once at closeout. Persist a pending offer before asking. No answer preserves
  the current mode and pending question; remind on resume without treating it as
  a new offer. Declining suppresses future unsolicited offers; accepting switches
  modes. Explicit user requests can select either mode at any time and also
  settle this preference. See state.md for transitions and the threshold.
- At project closeout follow [knowledge.md](references/knowledge.md) for bounded
  PARA index/summary/link maintenance, interview learning and Wiki assessment.
  This is part of new workflow scope; preserve historical optional-offer state.
  Active/shared skill promotion still needs its own exact-version authorization.

## Commands and boundaries

Understand `$workflow`, `$workflow build a booking system`, `$workflow status only`,
`$workflow switch to auto`, and `$workflow pause after each change`. For status or
mode-only requests, finish that operation without starting development.

Invocation does not expand scope or authorize commits, pushes, deployment, or
unrelated project edits. If OpenSpec CLI, a required skill, or index write access
is missing, identify the gap and next step. Do not silently install dependencies,
execute teaching snapshots, or claim unsaved progress is persistent.

For stage routing, skill replacement, storage, thresholds, and acceptance examples,
read [customization.md](references/customization.md). Leave teaching snapshots intact.
