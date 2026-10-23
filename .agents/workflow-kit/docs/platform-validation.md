# Platform acceptance

The GitHub Actions matrix targets Linux, macOS and Windows. Its existence is
not execution evidence; link actual run/job results for the released revision.
The package tests exercise install/upgrade/collision/rollback behavior in temporary
roots. The external CLI check uses pinned OpenSpec/SymDex versions and pinned
Archify source; it exercises OpenSpec init/list, SymDex index/symbol lookup and
diagram schema validation. It does not test MCP connection, agent decisions,
RTK, browser rendering or a user's complete bootstrap.

## Actual host run

For each claimed platform, record OS/architecture, shell, agent version, selected
model/effort, kit content version, installed tool versions and command/evidence
locations. Use an approved disposable project and existing evidence storage.
An unavailable host/environment remains pending; do not copy another OS's PASS.

1. Have the selected agent read install.md. Check its environment/tool plan,
   reuse of existing tools, project-local destinations and concrete confirmation
   before user/system-scoped changes. Preserve the user's selected model.
2. Install and discover the 18 skills/resources. Confirm existing AGENTS/MCP
   settings and unrelated skills remain intact. Exercise a path containing spaces.
3. Preview an upgrade, change one installed rule, and verify automatic replacement
   stops for review. Approve an exact keep/replace decision, then inspect backup,
   manifest and retained customization. A legacy install with no manifest must
   not be assumed pristine. Confirm external tools are not silently upgraded.
4. Exercise the selected CLIs, Archify fixture generation/browser checks, and
   actual RTK routing. For MCP, verify configuration, host reload/trust, tool
   discovery and a bounded actual call using the same project/index state.
5. Simulate an unavailable tool or failed setup, then resume. Verify truthful
   partial status, retained successful work, and no fabricated readiness.
6. Run one approved behavior through local spec/implementation/test checks,
   change-wide review/debt reconciliation and human trace. Check that a genuine
   deferral lands in OpenSpec tech_improve.md and unmet acceptance still blocks.
7. Inspect decision questions and human-readable files against output.md, including
   Traditional Chinese prose, explained terms, examples, meaningful alternatives,
   layered presentation and retained evidence/unknowns.

Record separate results for package, external CLI and agent/MCP acceptance,
including failures and skipped checks. Update docs/validation.md for actual kit
release observations. CI success cannot substitute for these host observations;
reader comprehension needs task-specific feedback, not a structural score.
