# Project workflow rules

This is a source template. Merge applicable sections into the target AGENTS.md;
do not overwrite existing project rules or treat this file as an active project.

## Project context

Resolve the current workflow's project_context from the local workflow index.
Its spec_path and toolbox_path point to the selected project under the actual
OpenSpec root; wiki_root identifies persistent project knowledge.
If absent, inspect existing mappings; ask when several projects match. Do not
choose the most recently modified toolbox or load all projects.

During first setup, adapt management/openspec-project/spec.md and toolbox.md from
the installed kit into <openspec-root>/projects/<project-key>/.
This projects grouping is a kit convention, not a new OpenSpec CLI schema.
Resolve CLI-managed change/artifact paths from the CLI. Preserve existing paths.

## Tool routing

The selected project's toolbox is the single source of concrete required-first
tools, fallbacks, commands and task packets. Its spec defines routing acceptance.
The installed kit's docs/tools.md explains capabilities and selection criteria.
If these contracts conflict, identify the conflict before the dependent action;
do not silently prefer a stale duplicate rule in a skill.

Decompose the question, select the needed capabilities, verify availability, then
record the route in the toolbox. Missing required tools block only dependent
claims/actions. Explain Git/source fallback reasons; do not equate text hits with
complete call relationships. Installation links are not health evidence.

## Implementation and architecture

Find the existing owning module before creating implementation. Follow this
project's source layout; extend the owner when adequate. Reuse or delete before
introducing a new module or adapter. Apply codebase-design vocabulary and test
through the same interface callers use. Record material interface changes in
the selected change's design; full architecture scans are task-driven.

Use the existing glossary/ADRs. Add only conclusion-bearing records within scope.
Preserve the user's model, effort, acceptance and authorization. Do not require
a new proposal merely because already-approved work is being resumed.

## Delivery and evidence

Use workflow for project orchestration and the matching skill for each stage.
New workflows follow workflow's GitHub contract: one Issue and one PR per
change, full architecture/code-trace before human walkthrough, then accepted
code/specs/README/archive preparation in the same PR. The user merges; verify
actual merge before completing or starting the next change, even in auto mode.
Default change mode stops after completion. Preserve unmigrated local history.
Use workflow's architecture and GitHub references for exact gates and recovery.

Before asking the user for a decision or drafting/revising human-facing explanations, OpenSpec, README, tutorials
or Issue/PR text, apply the kit's docs/output.md writing and layout checks. Read its
installed resource location through workflow project context. Its instructions
are English; human-facing prose defaults to Traditional Chinese unless an
explicit user request or project document-language requirement takes precedence.
Evidence and raw machine outputs keep their original meaning.

After each verifiable behavior, apply TDD's local spec/implementation/test check
and repair clear in-scope issues before marking tasks done. Change-wide review
includes code-review and ponytail-debt; use workflow's technical-debt contract
to maintain <actual-openspec-root>/tech_improve.md and present deferrals at trace.

Store requirements and acceptance in OpenSpec; keep raw evidence at the project's
existing evidence location. Log long-running or side-effecting operations with
command, cwd, effects, start/end, exit code, result and next step. Do not mark PASS
without inspecting evidence. Ordinary narrow tests need no extra task framework.

## Knowledge and evolution

At new-workflow project closeout, update PARA navigation/indexes in place,
include bounded interview evidence in authorized llm-wiki capture, and retain
legacy optional-consent history. Every completed Wiki update triggers
a bounded skill-evolution assessment. Verified path/link/command-typo maintenance
may be fixed directly within scope; behavior/policy changes are quality candidates.
Keep candidates out of active skill discovery until explicit activation. Evaluate
locally before suggesting a shared update. Use the bundled skills for the exact
evidence, validation and promotion rules rather than copying them here.

## Project-specific additions

Before use, record the actual source layout, glossary/ADR locations, evidence
location, build/test commands, and any publishing restrictions in the appropriate
project records. Unfilled values are not executable commands or permission.
