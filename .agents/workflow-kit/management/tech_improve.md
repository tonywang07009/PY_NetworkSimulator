# Technical improvement register

Template: instantiate at the selected project's actual OpenSpec root as
tech_improve.md, not in its active changes directory. Keep an equivalent existing
register. This file tracks deferrals, not requirements or implementation consent.
Write the target record in its required language (Traditional Chinese by default).

## Entries

Add entries only for inspected, relevant findings. Use stable TI-0001-style IDs
and retain closed IDs/history. Per entry record:

- Problem and observable impact.
- Source change and governing requirement/acceptance links.
- Actual relative/absolute code locations and evidence.
- Deferral reason, applicability/limit, and when to reassess.
- Decision/date and status: proposed, accepted-deferred, scheduled, resolved,
  or superseded.
- Subsequent approved change and validation links; superseding TI ID if any.

Keep local source comments concise with the TI ID/link. Issue/PR summaries link
here. A trigger means reassess; implementation needs a normal approved change.
Retain unresolved evidence/limits explicitly. Resolve only with implementation
and verification evidence; preserve the prior decision and date.
