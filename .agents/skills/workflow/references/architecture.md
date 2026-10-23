# Derived architecture and human trace

Read after the entry interview, when implementation changes the design, and
before human trace or PR preparation. OpenSpec remains authoritative; diagrams
are read-only navigation and cannot edit code or approve changes.

## Scope and files

Provide a current system overview plus full detail for the current change.
Include related existing modules as context, not an exhaustive unrelated graph.
Each detailed view covers input structures (fields, types, units, validation),
internal flow and state owners, output structures and errors, and engineering
techniques with their reason for use. Separate planned, implemented, inferred
and verified relationships. Do not invent function names before implementation.

Reuse existing architecture locations. Default: docs/architecture/system.archify.json
and system.html for the current overview; architecture.archify.json and
architecture.html in the CLI-resolved change root for the detailed snapshot.
Store generation and browser receipts beside their artifact. Keep sources and
destination links together after archive; later changes do not rewrite delivered
historical snapshots. Ordinary navigation uses relative links; code-trace.md
also records absolute capture paths per its existing archive contract.

## Archify delivery

Use the project's verified Archify route. Read its installed skill, schema and
examples for the actual version; CLI commands vary by release. Current packages
support finalize for validation, delivery, provenance and browser checks. If
only older deliver/visual-check interfaces exist, use their documented gates
and retain actual receipts. No tool installation is implicit.

Generate the design view from interview decisions after scope confirmation;
mark unresolved areas. Refresh after formal specification, implementation/review
and final spec sync. Source-backed views require scoped code inspection through
the project's source-navigation route, with actual symbols and evidence links.
Visual output needs rendered inspection when browser capability is available.
Tool absence or failed generation preserves the last good artifact and records
missing/stale status. Independent work may continue, but missing required views
block human acceptance/PR readiness and completion. Never fabricate a receipt.

## Human trace

Before starting the walkthrough, deliver both complete architecture views and
code-trace.md. Create/refresh the latter using the archive skill's
[trace contract](../../openspec-archive-change/references/code-trace.md), now
before archive rather than only during closeout. Use the real scoped tree and
every implementation file's clickable absolute and project-relative paths.

1. Explain the system overview, then the current change's input/process/output.
2. Walk the actual files and symbols along the data flow. At each relevant step
   connect OpenSpec acceptance, implementation and test/raw evidence. State what
   remains inferred, untested or unavailable.
3. Pause after each manageable section for questions or confirmation. Provide
   the full documents up front; a narrated tour alone is not the deliverable.
4. Resolve feedback, update code/views/trace and run affected checks. Reuse
   acceptance already applicable to unchanged content. Changed behavior or
   review scope needs renewed acceptance of the affected part before delivery.

Agent code-review precedes this walkthrough. Use improve-codebase-architecture
for concrete ownership/interface/readability friction and preserve agreed scope;
do not run an unsolicited repository-wide cleanup. Different requirements return
to OpenSpec; missing coverage returns to TDD. Passing automated checks and silence
do not establish human acceptance.
