---
id: R-env-0001
title: Python Environment
type: env
version: 2025-08-10
status: canonical
source: .claude/codex/CLAUDE-CODEX.md
---

- **Package Manager**: UV by Astral (mandatory for all Python projects)
- **Installation**: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Project Commands**: `uv sync`, `uv add`, `uv run`, `uv test`
- **Fallback Protocol**: If UV unavailable, use pip with explicit documentation
