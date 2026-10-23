# GitHub scheduling and integration

Read when a workflow uses GitHub delivery. New workflows default to this contract;
legacy records without delivery retain local completion until deliberately
migrated. A user may explicitly choose local delivery, but report that it does
not satisfy this GitHub integration contract.

## Identity and authorization

One change has one Issue and one PR. OpenSpec owns requirements and acceptance;
the Issue mirrors approved scope, dependencies, progress and blockers. Resolve
the actual repository, target branch, publishing route, access and required
checks from project context. Do not guess a remote or impose GitHub defaults.

Publish only within existing explicit authorization for that repository/action.
Scope-approved development, writing a draft, and this kit's installation do not
authorize remote messages, commits or pushes. When authorization is missing,
prepare concrete local Issue/PR drafts and evidence first, then request only the
missing publication scope. Reuse existing authorization without repeated prompts.
Never request credentials in chat or include them in drafts/state.

## Within one change

1. After OpenSpec scope/acceptance is confirmed, create or update its Issue.
   Record goal, observable acceptance, dependencies, change ID and accessible
   spec references. Search the scoped existing mapping before creating anything;
   resume the same Issue after interruptions. Update progress and blockers during
   development, preserving human comments and unrelated sections.
2. Implement and validate, perform Standards/Spec review and necessary scoped
   cleanup, then deliver architecture/trace and obtain human trace acceptance.
3. Sync specs and prepare the archive and root README on the delivery branch.
   The archive skill owns moves/link validation. This is prepared delivery, not
   a completed change. Preserve the original/archive mapping for resumed work;
   do not create a second change when the CLI no longer lists the moved one.
4. Invoke write-reviewable-pr for the final diff, with docs/output.md as writing
   authority. Include code, specs, architecture, trace, README and archive material
   in the same PR; use the existing approved layout. Verify all reader-facing
   repo links are accessible and point to the reviewed revision. Local absolute
   paths stay in trace; provide remote links or bounded summaries in the PR.
5. Record Issue/PR URLs, base branch, current head, acceptance applicability and
   actual review/CI status. Save awaiting_merge. Wait for the user to merge;
   the agent never enables auto-merge or performs the merge under this contract.
   A closed-unmerged PR is unfinished; ask how to resume or revise scope.
6. Address PR feedback in the same change/PR. Reconcile every head update with
   acceptance and checks; changed behavior requires affected tests and human
   confirmation. Do not reuse an earlier green CI run for a different head.
7. On resume, read actual GitHub state and required-check evidence. Verify the
   PR was merged into the intended target, identify reviewed head and merge SHA,
   and check Issue closure or an explicit remaining reason before marking merged.
   Do not infer merge from an Issue closure, PR creation, approval or elapsed time.

Use available connected tools or the project's approved CLI, not a mandatory
wrapper. Save raw merge/check observations in the existing local evidence
location and reference them from state. A post-merge observation cannot be
inside the already-merged PR; it needs no automatic follow-up commit. The state
helper checks structure and reachable files, not the truth of GitHub evidence.

## Serial scheduling and recovery

Only one unmerged change is active, including during review waiting, even when
later changes have no dependency. Future scope/Issue planning may remain in the
index, but implementation and next-change specification wait. After verified
merge, change mode reports and stops; auto may start the next eligible change.
Neither mode bypasses human acceptance or manual merge. Preserve legacy counts.

Missing authorization, unavailable GitHub, failed checks, changed targets and
conflicts block their dependent publication/completion. Diagnose in scope,
retain drafts/mappings and a concrete next action, and continue independent
work within this change. Do not pretend a failed mirror or unmerged PR is done.

GitHub closing keywords depend on target/default branch rules. Read current
[linking documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
before relying on automatic closure; verify the observed result.
