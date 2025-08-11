# 150-Word Documentation Standard

## Purpose

All agents, modules, and tools in Omar's Claude Code ecosystem MUST have exactly one **definitive description** of exactly **150 words or fewer**. This standard enforces consistency, prevents documentation bloat, and ensures governance-layer enforcement.

## Requirements

### Content Structure (≤150 words total)

1. **Purpose statement** (20-30 words): What this agent/module does
2. **Core functions** (60-80 words): Primary capabilities and use cases  
3. **Constraints & limitations** (20-30 words): What it doesn't do, prerequisites
4. **Usage examples** (10-20 words, optional): Basic invocation patterns

### Format Requirements

- **Exactly ≤150 words** (enforced in CI)
- **Single authoritative source** per agent/module
- **No ambiguous language** - concrete, actionable descriptions
- **Zero outdated references** - linked to live code/configuration

### Enforcement

- **CLI `--help` output**: Embedded as primary description
- **Web dashboards**: Used in all UI components
- **PR descriptions**: Auto-populated from definitive docs
- **API/Agent registry**: Single source metadata
- **CI pipeline**: Automatic word count validation, build failure on violation

## Compliance

**Build fails** if any documentation exceeds 150 words or lacks required structure elements.