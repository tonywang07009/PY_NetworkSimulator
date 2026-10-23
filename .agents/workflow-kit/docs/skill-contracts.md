# Skill responsibility and handoff audit

This records the user-approved kit change; it is not an active OpenSpec project.
Runtime context resolution belongs to workflow's project-context reference.
Design vocabulary belongs to codebase-design.
Shared user-facing writing rules belong to [output.md](output.md). Workflow and
the bundled write-reviewable-pr skill read that authority; it governs
wording, not PR layout, evidence truth, machine output or lifecycle checkpoints.
The PR and writing-for-agents skills are included in the 18-skill bundle.

## Authoring instructions

When creating or revising agent instructions, use the bundled
[writing-for-agents](../../skills/writing-for-agents/SKILL.md) reference, sourced from
[AI Hero](https://www.aihero.dev/skills-writing-for-agents). Evolution loads it
only for qualified candidate authoring; skill-creator handles packaging. Neither
guide determines eligibility, measured improvement, or activation. Human-facing
drafting and layout remain owned by [output.md](output.md): English instructions,
Traditional Chinese output by default, with explicit language requirements taking
precedence. Examples are disclosed only when needed.

| Skill | Input interface | Output / next owner |
|---|---|---|
| workflow | Goal/resume and project context | New-workflow grill-with-docs interview before delivery; resume without reconfirmation unless the user adds requirements; verified summary, serial Issue/PR delivery, human trace, manual-merge checkpoint and included project closeout |
| grill-with-docs | Unresolved decision and evidence | Persisted six-facet interview, bounded questions/evidence, explicit preferences and architecture handoff |
| codebase-design | Scoped interface question | Depth, seam, adapter, leverage and locality vocabulary |
| domain-modeling | Domain term or durable decision | Authorized existing glossary/ADR update |
| writing-for-agents | Agent-facing document or qualified evolution candidate | Instruction-authoring reference and conditional skill mechanics; no evaluation or activation authority |
| improve-codebase-architecture | Concrete friction and scope | Before/after candidates, then selected design discussion |
| openspec-explore | Question and existing records | Findings without unsolicited implementation |
| openspec-propose | Selected goal and acceptance | CLI/schema-resolved artifacts for apply |
| openspec-apply-change | Change and context files | Implemented tasks with validation/review or bounded blocker |
| openspec-sync-specs | Delta and canonical specs | Reconciled behavior; no duplicate tool route |
| openspec-archive-change | Human-accepted change and evidence | Prepared archive with verified diagrams/code-trace.md; workflow still awaits manual PR merge |
| write-reviewable-pr | Reviewed diff, Issue, specs and evidence | Approved PR layout using docs/output.md; publication only within authorization, user merges |
| tdd | Approved acceptance and public interface | RED/GREEN and affected regression evidence |
| ponytail | Scoped implementation and user-selected level | Simplest sufficient change, preserving required behavior and local semantic checks |
| ponytail-debt | Selected repository and review scope | Marker findings; workflow reconciles OpenSpec tech_improve.md without treating an empty scan as quality proof |
| code-review | Fixed point, current work and requirements | Separate Standards/Spec findings |
| llm-wiki | Project, operation and bounded sources | Knowledge update plus one evolution assessment |
| skill-evolution | Patterns, events, target and history | Maintenance/refusal/candidate/validation/promotion result |

## Architecture changes

- All skills resolve the selected project spec/toolbox without copying its route.
  The installed resource pack supplies the shared guide and management templates.
- Root AGENTS governs this kit; management holds inactive student templates.
  Actual tools and commands vary at the project toolbox seam.
- The architecture deletion test matches codebase-design: vanishing complexity
  favors deletion; complexity redistributed to callers indicates useful depth.
- OpenSpec exploration respects subsequent explicit implementation instructions;
  archive stops when required sync fails. Routine handoffs are not new approvals.
- TDD allows useful post-GREEN refactoring and existing acceptance records when
  the user explicitly excludes OpenSpec. Protected tests remain specifically scoped.
- Wiki/evolution share one bounded update/assessment identity. Feedback does not
  recurse. Candidates remain outside active discovery until user activation.
- The existing workflow state helper owns the optional project_context extension;
  legacy completion counts remain intact.
- The same helper assigns full teaching to the first registered workflow and
  brief prompts to later workflows, preserving per-workflow level and delivered
  topic markers on resume. Delivery owns explanation quality; teaching does not
  change checkpoint mode, human acceptance, or completion counts. Legacy records
  remain readable without inventing prior lessons.
- No router skill, speculative adapter or parallel implementation was added.
- Archive owns the per-change code trace format and path verification; workflow
  reports its archived location. The tree follows actual project paths and nesting,
  marks omitted branches, and links canonical acceptance without duplicating it.
- Workflow owns human change acceptance and the subsequent root README update
  after change completion. The README is the current project user manual and file
  guide; its actual tree and verified usage complement the archived code trace.
  Both checkpoint modes require this closeout and reuse existing human acceptance.

## Validation map

| Behavior | Check |
|---|---|
| Install resources without activating templates or overwriting settings | tests/test_install.py |
| Upgrade preview, explicit local decisions, backup/rollback, path and lock boundaries | tests/test_upgrade.py |
| Real marked-debt scan includes tracked/untracked files and respects ignores | tests/test_debt_scan.py |
| Actual OpenSpec/SymDex/Archify CLI operations in temporary roots | tests/smoke_tools.py; CI matrix, distinct from agent/MCP acceptance |
| Resume project context; preserve legacy counts | tests/test_workflow_state.py |
| Distinct current tasks, holdout, resource changes and regression refusal | tests/test_evolution.py through the actual evaluation CLI |
| Course data, local links and installed resources agree | verify.py / course/build.py |
| Offline Archify diagram, lesson dialogs, node focus/search/theme, page width | tests/test_course_browser.mjs with a fresh browser profile |

Manual contract walkthroughs:
- Missing SymDex uses only the declared fallback; no unsupported complete-call-graph claim.
- Verified archive moves are maintenance, not quality candidates.
- One quality event yields insufficient-evidence, while retaining the Wiki finding.
- Two same-root-cause events plus relevant positive/negative evidence may produce
  one isolated candidate; no active skill changes during assess.
- One task repeated twice is insufficient. Changed candidate resources require
  new version evidence. A current regression prevents readiness.
- Readiness is not activation: the target, version, user decision and rollback
  source are checked by promotion.
- Evaluation feedback updates the originating Wiki record without another trigger.

These walkthroughs check procedural consistency, not measured agent improvement.
Real candidates still require real task execution and evidence review.

## Updated delivery contract

- grill-with-docs owns interview records, six facet budgets, examples/options and
  literature-based tradeoffs; explicit preferences differ from inferred concerns.
- workflow architecture.md owns current system/change views and full documents
  before section-by-section human trace. Archive owns actual path verification.
- workflow github.md owns one Issue/PR per change, same-PR code/specs/README/archive
  preparation, manual merge and single-unmerged-change scheduling. state.py checks
  its structural completion gate while retaining version-1 local history.
- Project closeout maintains PARA navigation in place and routes bounded interview
  knowledge to Wiki/evolution. Candidate promotion remains separately authorized.
- Installer copies 18 skills, shared resources and starter prompt; no live project
  state, external tool download or global/shared skill activation occurs.
- Required checks include test_workflow_state.py (merge/acceptance/evidence/WIP),
  test_install.py (PR/resource delivery and rollback) and the rendered course smoke.
