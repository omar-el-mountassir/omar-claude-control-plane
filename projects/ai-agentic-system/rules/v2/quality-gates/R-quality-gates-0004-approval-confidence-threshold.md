---
id: R-quality-gates-0004
title: Approval Confidence Threshold
type: quality-gates
version: 2025-08-10
status: canonical
source: .claude/codex/CLAUDE-CODEX.md
---

**Rule.** Any action gated by `APPROVE:*` requires Confidence ≥ 0.95. If `<0.95`, the agent must respond:
`BLOCKED: confidence < threshold` and request clarifications to raise confidence. No auto-approval permitted.

**Scope.** Repo changes, external integrations, secrets, deployments.

**Mechanics.**

- Every Mission Order ends with `Confidence score — x.xx`.
- A pre-approval guard parses the latest score and enforces the threshold.
- Evidence: guard exit code `0` only when `score ≥ threshold`.
