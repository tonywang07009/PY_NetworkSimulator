# Workflow quality and upgrade validation: 2026-10-18

| Check | Observed result |
|---|---|
| Unit tests | 52 passed with temporary roots; installation/upgrade, local edits/deletions, absent/corrupt baseline, reviewed keep/replace, rollback, locks, symlinks, permissions and raw marker scanning |
| Skill metadata | All 18 YAML frontmatters parsed; quick_validate passed 10. Eight retain unchanged unsupported upstream/baseline metadata results, including Ponytail argument-hint |
| Linux external CLI smoke | OpenSpec 1.14.3 init/list, SymDex 0.1.26 real index/symbol lookup and pinned Archify schema validation passed in disposable projects |
| Archify 3.1.0 finalize | validate, deliver, strict check and browser-check passed; delivery 9/9, zero errors/warnings |
| Archify visual checks | Automatic provenance/readability/containment checks passed; light 1440x900 and dark 2048x1320 screenshots visually inspected |
| Offline course browser smoke | Eight dialogs, 16 nodes, navigation, references, focus/search/theme/export, desktop/mobile width and no runtime exceptions passed |
| Focused rendered inspection | Decision, tool/upgrade and implementation/debt/writing cards rendered on desktop/mobile without horizontal dialog overflow; implementation/debt mobile and embedded desktop diagram inspected |
| CI definition | Three-OS matrix, triggers and fixed action commits parsed/checked; remote jobs have not been executed |

Current diagram receipts are in course/review-implementation-debt/. The root
course/workflow.finalize.json records a failed earlier attempt that encountered
stale browser evidence. Regeneration in a fresh evidence directory passed;
PROVENANCE.json selects the current receipt. Native visualReview fields remain
pending/not-requested: the perceptual inspection above is a separate observation,
not a fabricated native reviewer receipt. Long dialogs require vertical scrolling;
phone diagrams still require pan/zoom. Latest browser captures are in temporary
/workflow-quality-preview and /workflow-quality-focused directories under /tmp.

The delivered kit now has 18 skills, local semantic checks, change-wide
code-review/ponytail-debt handoff, a project-owned tech_improve.md template,
decision-question output rules and explicit install/upgrade behavior. Those
procedural contracts are not empirical proof of reader comprehension, model
reliability or reduced cognitive load. The actual source checks used scoped
reads because SymDex did not provide a usable kit index/CLI registry; no complete
caller graph is claimed. The external CLI smoke used an isolated newer OpenSpec,
without replacing the host's existing version. No repository-wide tool setup,
shared skill activation, commit, push or publication was performed.

Native macOS/Windows runs, actual GitHub Actions jobs, clean-machine agent-led
bootstrap, MCP reload/tool invocation and Luna writing quality remain unverified.
CLM remains future work; Jev/TypeSafe is not selected. See platform-validation.md
for the separate actual-host acceptance checklist. Earlier records below apply
only to their respective revisions.

## Earlier installation-guide validation

# Agent installation guide validation: 2026-10-18

The former # MCP tools text index was replaced by docs/install.md. The English
agent guide covers Linux/macOS/Windows targets, project-scoped setup, explicit
user/system-scope change confirmation, official tool routes, MCP registration,
functional checks and recovery. README, project context, toolbox, starter prompt
and course now point to it. Existing CLM/Jev direction text was reconciled.

- 35 unit tests passed using temporary roots. The installer test checks delivery
  of the guide; existing documentation link checks also inspect its installed
  resource location. No external tools were installed by this maintenance task.
- The 8-card/16-node offline browser smoke and focused desktop/mobile tool-card
  checks passed. Screenshots in /tmp/workflow-install-guide-preview/ were
  inspected. Long mobile dialogs require vertical scrolling.
- Package verification checks installed resources, links, generated lesson data,
  hashes and provenance. No new bootstrap script or MCP configuration writer
  was introduced; install.py still discovers/copies skills and shared resources.
- Setup descriptions were checked against official OpenSpec, SymDex, RTK,
  Ponytail, Archify and Codex MCP sources. Release-specific commands and runtime
  requirements must be resolved again on the actual target before execution.

This validates guide delivery and course rendering, not external tool setup.
A clean-machine installation, native macOS/Windows execution, model-led setup,
MCP reconnection and actual tool calls under this guide remain unverified.
Module/debt refinements were pending at this earlier revision; see the current record above.
Earlier results below belong to their respective revisions.

## Earlier writing and authoring-guide validation

# English writing contract and authoring guide: 2026-10-18

- docs/output.md now uses English instructions with Traditional Chinese as the
  default human-facing language. Explicit user/project language requirements
  take precedence. Existing Traditional Chinese examples moved intact to
  docs/output-examples.zh-TW.md and load only when needed.
- writing-for-agents and its skill-mechanics/UI resources are bundled from
  mattpocock/skills commit 49dd158d1076134a641b33efb035946536778336, with
  the matching MIT license. The entrypoint adds kit/host compatibility guidance.
  Original source hashes and adapted package hashes are recorded separately.
- Evolution reads the guide only when drafting/revising an eligible candidate;
  eligibility, comparison and activation remain separate. This is a written
  contract, not a demonstrated improvement in model behavior.
- 35 unit tests passed in temporary roots, including installation of all 16
  skills, authoring references, license and Chinese examples, collision refusal
  and rollback. install.py already discovers skills dynamically; no extra branch
  was required to distribute the added skill.
- All 16 YAML frontmatters parsed. quick_validate passed 9 skills; the other 7
  retained the same pre-existing unsupported metadata results as the baseline.
- Browser smoke passed 8 dialogs, 16 diagram nodes and desktop/mobile behavior.
  Focused checks rendered the updated writing and evolution lesson cards on both
  sizes; inspected screenshots are in /tmp/workflow-writing-en-preview/.
  Vertical scrolling remains necessary on mobile. Host Chrome used fresh profiles.
- Course text and index.html were synchronized; diagram sources and artifacts
  were unchanged. Package verification checks links, deployed resources, hashes
  and provenance. Earlier validation records below refer to their own revisions.

No target-model tokenizer measurement, Luna behavior evaluation, reader study,
CLM integration, shared/global skill activation or GitHub publication was done.
English wording and reduced entry-file size do not establish token savings.

## Previous writing extension

# Writing extension validation: 2026-10-18

The current writing extension adds reader/task preparation, layered presentation,
format-specific drafting and revision checks to docs/output.md, with pointers
from the existing document-producing skills. AI Hero informs agent-instruction
authoring; the nine article practices are adapted to engineering documents.

- 35 unit tests passed using temporary roots. No runtime/helper logic changed.
- All 9 edited skills retain their frontmatter; quick_validate passed 4 and the
  5 OpenSpec skills produced the same unsupported compatibility-field result as
  the captured baseline. No new validator failure was observed.
- The browser smoke passed all 8 lesson dialogs and 16 diagram nodes. A focused
  check confirmed the updated writing lesson on desktop and mobile with no
  horizontal dialog overflow; screenshots were inspected in
  /tmp/workflow-writing-preview/. Long mobile content requires vertical scroll.
- Chrome could not start its debugging interface inside the sandbox; the same
  browser checks succeeded with approved host execution and a fresh profile.
- Course lesson text and index.html were synchronized. Diagram sources and
  Archify artifacts were unchanged; earlier generation receipts remain historical.
- Installation/resource/link/hash checks are covered by verify.py. No external
  skill was installed or activated, and no remote publication was performed.

These checks establish packaging and rendered behavior, not reader comprehension
or Luna-specific writing quality. No independent model comparison was run.
CLM evaluation and other previously inventoried workflow changes are outside
this writing-only extension.

## Earlier integration validation

# Current validation: 2026-10-18

| Check | Observed result |
|---|---|
| python -B -m unittest discover -s tests | 35 passed, using temporary project/state roots |
| Skill structure | All 15 YAML frontmatters parsed; quick_validate passed 8; 7 skills retain exactly the same unsupported frontmatter results as baseline (invocation/compatibility fields), without altering their metadata |
| State behavior | New GitHub default; legacy local resume; Issue identity, accepted head, merge evidence, unfinished-PR/WIP refusal, closeout and idempotent completion |
| Installer | 15 skills including PR; shared output/prompt; relocated doc links; collision refusal and rollback; no live interview/OpenSpec/Wiki/personal state |
| Archify 3.1.0 finalize | validate, deliver, strict check and real browser-check passed; delivery 9/9, no errors/warnings |
| Offline course browser smoke | 8 dialogs, navigation/references, 16 nodes, focus/search/theme/export, desktop/mobile width, no runtime exceptions |
| Rendered inspection | Light 1440x900 and dark 2048x1320 flow; embedded homepage; desktop/mobile interview dialog inspected |

New records: course/workflow.finalize.json, workflow.finalize-summary.json,
workflow.delivery.json, workflow.browser-check.json, current-visual/ and
current-preview/. Course diagrams describe the approved workflow policy, not an
observed production project's execution or an exhaustive caller graph.
The browser gate permits readable vertical scroll; large diagrams on phones
still need pan/zoom. Perceptual inspection does not measure user comprehension.

Archify was explicitly requested from https://github.com/tt-a1i/archify and
placed in ignored .tools/archify at b25142deac4b19b293e45b6bf6d69351d3c8f3b6.
The sandbox denied a Node renderer spawn (EPERM); the authorized host execution
completed generation and browser checks. No source code in Archify was changed.
SymDex MCP had no kit index and CLI registry access failed; source relationships
were checked through scoped direct reads and behavior tests, not a complete
indexed graph. No dependency was auto-installed for source navigation.

The new lifecycle was not exercised against a real remote GitHub repository.
No Issue/PR was published, no commit/push/merge or active shared skill change
was performed. Interview/learning/readability effectiveness and TypeSafe scoring
are not proven by these structural and fixture checks. Jev scoring, tag policy
and cross-project profile sharing remain deferred.

Package-wide integrity is checked by python -B verify.py after refreshing the
current provenance and checksums; historical receipts below are not substituted
for current verification.

## Historical validation record (preserved)

# Validation record

Validated on 2026-09-10 on Windows with Python 3.12, Node 24 and Microsoft Edge.

| Check | Result |
|---|---|
| `python -B -m unittest discover -s tests` | 22 tests passed: workflow state, isolated installer and evolution evaluation CLI |
| `python -B verify.py` | Course data, local references, installation/refusal paths, package hashes and provenance checked |
| Official skill-creator `quick_validate.py` | workflow, llm-wiki and skill-evolution passed |
| PyYAML 6.0.3 | All 14 skill frontmatters and agent YAML files parsed |
| `node tests/test_course_browser.mjs <edge-path> course/current-preview` | 8 lesson dialogs, navigation, references, 10 Archify nodes, focus/close, search, theme toggle, export menu, desktop/mobile page width and absence of runtime exceptions passed |

Browser checks used a fresh headless Edge profile and offline file URLs. The
built-in browser could not initialize in this host; the approved external Edge
test provided rendered validation. Screenshots are in course/current-preview/;
the desktop course and desktop/mobile flow were visually inspected.

## Archify regeneration

The user selected the adjacent local archify project, version 2.17.0-dev.1.
`course/workflow.archify.json` is now the maintained diagram source. The former
custom HTML template and its data file were replaced. Plain `course/build.py`
updates lessons only; `--archify-root ../archify` invokes the actual CLI delivery
and saves its receipt without modifying the generated artifact afterward.

```text
diagram_type: workflow
output: course/workflow.html
specification_sha256: c24b6c7fcf2ff9076a4d0c891928593d9b1837a1bb50001bcc51bb4356a9ad35
artifact_sha256: e10652825b49c9313241c3490550cfb28d77d48f00622e7f491b00333e99a6ad
validation: 9/9 showcase, 0 errors, 0 warnings
browser_evidence: passed
visual_review: passed (desktop scope)
correction_rounds: 0
```

Delivery evidence: course/workflow.delivery.json. Official automated evidence:
course/workflow.visual-check.json, generated with ARCHIFY_CHROME pointing to
the installed Edge executable. All four desktop measurements passed:
1440x900, 1600x1000, 1920x1080 and 2048x1320. Both endpoint sizes were captured
in light and dark themes. An image-capable reviewer inspected the light large
desktop, dark small desktop and embedded course screenshots; nodes, labels,
return branch and policy cards were legible without intersecting routes.
The initial layout validation rejected a backward mainPath; the corrected source
limits mainPath to the forward intake segment and preserves every delivery edge.
Unlabeled edges connect sequential steps whose action is stated by their nodes;
branch conditions retain explicit labels.

Mobile width checks measure document containment only. At 390px the Archify
viewer requires pan/zoom and part of its fixed toolbar falls outside the visible
area. Mobile visual completeness is not claimed. The generated runtime was left
intact; the course provides a direct standalone diagram link. Export-menu opening
was tested; exported-file quality was not tested.

Tests use temporary projects. No live OpenSpec, Wiki, personal completion state
or active shared-skill candidate was created by these checks.

The evolution CLI checks hashes and declared evidence records. It does not judge
the content of evidence or measure agent quality. Real candidates need actual
project tasks, evidence review and the specified activation decision. Procedural
walkthroughs are documented in [skill-contracts.md](skill-contracts.md).
