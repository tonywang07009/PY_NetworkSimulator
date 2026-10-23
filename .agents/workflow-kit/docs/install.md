# Agent installation guide

Use when asked to prepare this workflow on Linux, macOS, or Windows. Install the
selected tools, configure the current agent, then verify the actual capabilities.
Report in Traditional Chinese under [output.md](output.md). This is an
agent-executed procedure; install.py itself only copies kit files.

All three OS branches are targets. A complete clean-machine installation and
native macOS/Windows execution remain [Needs Verification]; documentation is not
platform acceptance evidence.

## 1. Resolve context and effects

Identify the existing target repository, kit checkout, OS/architecture, shell,
agent host/version, tools and configuration. Distinguish native Windows from
WSL, and containers from their host. Retain the user's model/effort. Ask only for
missing information that changes the installation.

Prefer project-scoped configuration and isolated project tools; reuse compatible
existing tools. Before user-level/system-level changes, show the exact path,
diff/command, effects and recovery, then obtain confirmation. Reuse authorization
already supplied for those exact effects. Host trust, plugin trust, OAuth and
administrator interactions remain user actions, not protections to bypass.

Show a concise plan: capability, existing status, selected official version,
destination and verification. Execute authorized project-local steps without
asking for each command. Stop dependent work for missing permission or an
unsupported route, while completing independent authorized work.

Read the official setup sources below for the selected release before execution.
Record versions/commits and resolved commands. Substitute every placeholder,
quote paths with spaces, and use the detected shell's syntax.

## 2. Select capabilities

[tools.md](tools.md) owns selection criteria; this guide owns installation.
The target project's toolbox owns the selected routes and actual evidence.

| Capability | Form | Needed for |
|---|---|---|
| Kit skills/resources | 18 bundled skills, docs and templates | Core workflow; install.py |
| OpenSpec | CLI | Specification lifecycle |
| Archify | Skill/renderer and supported browser | Required architecture/trace generation; offline course reading needs no renderer |
| SymDex | CLI, optionally MCP | Source relationships under the selected project route |
| RTK | CLI | Git routing where selected; hooks are a separate effect |
| Ponytail and ponytail-debt | Two bundled instruction skills | Simplification and technical-debt stages; hooks/UI remain optional |
| GitHub access | Existing connected tools or selected CLI | Issue/PR/merge evidence; installation does not authorize publication |

Bundled llm-wiki does not require the external LLM Wiki desktop application.
WikiSkill is a research source, not a dependency. CLM is future work; Jev/TypeSafe
is not selected. This guide does not install evaluation models/services.

## 3. Prepare the platform

| Platform | Detect | Isolated Python executable |
|---|---|---|
| Linux | Distribution, architecture, shell and available package tools | <venv>/bin/python |
| macOS | Intel/Apple Silicon, shell and available package tools | <venv>/bin/python |
| Windows | Native/WSL, architecture, PowerShell/cmd and Python launcher | <venv>\\Scripts\\python.exe |

Probe Python, Node/npm and Git first. Check the selected release's runtime
requirements: inspected SymDex metadata requires Python >=3.11; OpenSpec's
inspected quickstart requires Node >=20.19.0. Recheck when selecting versions.
If a runtime is missing, use its official platform setup with the effect review
above. Availability is not permission to replace an existing runtime.

For Python isolation, use `<python> -m venv <venv>` at a resolved project tool
path and invoke its executable directly; shell activation is unnecessary.
Use the matching Python/pip pair and one package-manager route. Keep tool caches
and indexes out of versioned source under the project's existing ignore policy;
propose scoped additions where necessary.

## 4. Deliver the kit

From the located kit checkout, using the detected Python executable:

```text
<python> -B verify.py
<python> install.py <absolute-existing-target-repository>
```

This delivers <target>/.agents/skills/ and .agents/workflow-kit/ containing
docs, management templates and starter prompt. It does not initialize OpenSpec,
install external tools, activate templates or modify agent settings. Verify that
the host discovers the project skill directory; resolve other hosts explicitly.

Same-name skills/resources cause a fresh-install refusal without replacement.
For an existing installation, use the upgrade procedure below. Preserve existing
third-party skills/plugins: compare duplicate providers and resolve the selected
host route rather than removing user-owned installations.

### Preview and upgrade

Fresh installs write .agents/workflow-kit/installation.json with deployed-byte
hashes and a content-derived package version. Retain it as the comparison basis.
Preview using the located kit checkout:

```text
<python> install.py <target> --upgrade --dry-run
```

This reads without writing a lock, manifest or backup. It lists file actions,
hashes and text diffs. Unchanged upstream-owned files can update automatically;
user modifications, local deletions or differing files without a known baseline
require review. Identical incoming/local bytes need no overwrite and can be
recorded as such. Extra untracked files are left alone. Review removals as well
as additions and updates. A retired locally modified file remains a decision.

Apply a conflict-free plan with `--upgrade`. Pending reviews block the entire
write, rather than performing a partial upgrade. After the user confirms the
specific file's disposition, repeat `--keep-local <managed-relative-path>` or
`--replace <managed-relative-path>` as needed alongside `--upgrade`. These are
per-file decisions, not blanket overwrite permission. For a merged custom edit,
inspect its diff, save it and explicitly keep that local file. A kept custom
file remains distinguishable from upstream on the next upgrade.

Upgrades lock cooperating installers, recheck content, save changed originals
and the prior manifest under .agents/workflow-kit-backups/, and roll back applied
files on failure. If an external writer changes an applied file, recovery stops
with the backup location rather than overwriting that edit. Resolve a stale lock
only after checking its owning process. Preserve backups until verified recovery.

Kit upgrades do not upgrade external CLIs, runtimes or plugins. Probe their
compatibility; reuse compatible versions and propose only necessary changes
with effects/verification. Never rewrite agent MCP configuration as an implicit
kit upgrade. [Platform validation](platform-validation.md) separates CI checks
from actual agent/host acceptance.

## 5. Install selected tools

### OpenSpec

Read the [official quickstart](https://github.com/Fission-AI/OpenSpec#quick-start).
For project isolation, use npm's prefix option:

```text
npm install --prefix <node-tool-root> @fission-ai/openspec@<selected-version>
```

Invoke <node-tool-root>/node_modules/.bin/openspec on POSIX, or openspec.cmd in
that directory on native Windows. Check that exact executable's version/help.
Reusing a compatible global install is allowed; creating one requires the user
scope decision. After target-project scope confirmation, inspect existing
OpenSpec before initializing absent state. Reconcile generated skills with this
kit's skills; preserve existing owners. This teaching kit is not a live target.

### SymDex

Read the [official install/MCP guide](https://github.com/husnainpk/SymDex).
Install the lean core in the chosen isolated environment:

```text
<venv-python> -m pip install symdex==<selected-version>
```

Resolve the sibling symdex executable in bin/ or Scripts/. Probe help/version,
then index only the selected target or a permitted temporary fixture using
the installed CLI's project-local state option. Query a known symbol/outline.
Semantic extras and embedding-model downloads are a separate optional choice.

### RTK

Use [official platform installation](https://github.com/rtk-ai/rtk#installation).
Prefer a verified release binary at a scoped location where supported. Upstream
also documents Homebrew and Windows winget; user/system changes need the earlier
effect review. Check package identity using `rtk --version` and `rtk gain`, then
exercise scoped Git inspection. Resolve PATH/command-cache issues before retrying.
Installing RTK does not imply hooks or `rtk init -g` authorization.

### Archify

Read [official installation options](https://github.com/tt-a1i/archify#installation-options).
Use a project-local skill route supported by the host, or a recorded checkout
when a CLI path is needed. Retain renderer files and references, not SKILL.md
alone. Resolve entrypoint, Node/browser requirements and commands for that
version. Generate a small fixture and run its documented finalize/delivery gates,
retaining real receipts. A discoverable skill/browser alone is insufficient.
Do not depend on the author's ignored .tools/archify; course reading uses shipped
HTML and does not require installing the renderer.

### Ponytail and ponytail-debt

Read [upstream installation](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md).
The kit already delivers both instruction skills and licenses. Reconcile an
existing plugin provider instead of installing another copy. Verify discovery and
exercise debt detection on a temporary marked fixture. Plugin/lifecycle-hook
installation and user-level activation need the earlier effect review. Preserve
existing AGENTS.md rather than replacing it with upstream rules.

## 6. Configure selected MCP connections

CLI tools and skills are not automatically MCP servers. Inspect the current
host's actual format and registration interface. Back up existing configuration,
merge only the selected entry and retain unrelated settings. Resolve server
identity to avoid collisions with other project configurations.

For SymDex STDIO, resolve absolute executable, `serve` arguments, working
directory and project state path. Use the same state for CLI indexing and MCP
queries. A host-launched process may not inherit terminal PATH.

[Official Codex MCP documentation](https://developers.openai.com/codex/mcp/)
supports project .codex/config.toml in trusted projects. Resolve fields from the
installed host and documentation; generic mcpServers JSON is not TOML. Other
hosts need their supported schema. A user-scoped-only route requires the concrete
diff and confirmation; do not silently widen installation scope.

After required reload/trust interactions, verify registration, tool discovery
and a bounded call against the expected indexed project. If reconnection is
unavailable, report verification pending rather than connected. Recovery removes
only newly added failed entries within authorization, preserving working servers.

## 7. Verify and report

Use existing toolbox/evidence locations to record OS/architecture, versions,
absolute executables, official source/version, config diff/backup, commands,
exit status, observed result, recovery and remaining action. Installation alone
does not create live OpenSpec, Wiki, interview or personal workflow state.

Report each selected capability as ready, reused-and-verified, partial, failed or
not-selected. Ready requires its actual operation, not file presence. A required
capability still pending means the environment is not fully ready. Distinguish
skill delivery, CLI execution, MCP registration and successful agent calls.
Report platform results separately; use bounded retries for diagnosed failures
and resume incomplete steps instead of reinstalling successful ones.

Package tests do not validate external setup. Complete Linux/macOS/Windows
bootstrap acceptance needs actual runs on each platform. Retain the selected
model and label Luna-specific reliability unverified until exercised.
