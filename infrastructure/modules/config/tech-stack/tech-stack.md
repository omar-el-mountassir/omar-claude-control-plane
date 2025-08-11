---
version: "0.1.0"
compatibility: ">=0.1.0"
last_updated: 2025-08-11
module_type: configuration
stability: stable
component: module
created: 2025-08-11
author: collaborative
description: "Claude Code optimized tech stack - definitive tool choices for consistent, AI-friendly development"
---

# Tech Stack Configuration - Claude Code Optimized

**Module**: Claude Code Tech Stack Standards  
**Scope**: Definitive tool choices for ALL Claude Code development work  
**Purpose**: Eliminate decision overhead, ensure consistency, optimize for AI workflows

---

## Core Principles: Claude Code-Friendly Tools

### What Makes a Tool Claude Code Friendly?

1. **Declarative Configuration**: File-based config that Claude can read and modify
2. **Excellent Error Messages**: Clear, actionable error output that Claude can understand
3. **Predictable Behavior**: Same inputs always produce same outputs
4. **CLI-First**: Strong command-line interface for automation
5. **Documentation Quality**: Clear, comprehensive docs that Claude can learn from
6. **Minimal Hidden State**: All important state visible in files/config
7. **Fast Feedback**: Quick execution for responsive development cycles
8. **Standards Compliance**: Follows established patterns and conventions

### Anti-Patterns to Avoid

❌ **GUI-Required Tools**: Can't be fully controlled via CLI  
❌ **Hidden Configuration**: Important settings not in version-controllable files  
❌ **Poor Error Messages**: Cryptic errors that require human interpretation  
❌ **Multiple Tools for One Job**: Complexity without clear benefit  
❌ **Frequent Breaking Changes**: Unstable APIs that require constant adjustment

---

## Established Tech Stack (Definitive Choices)

### **Core Development**

#### **Python (Primary Language)**

- **Package Management**: `UV` ✅
  - **Why**: Single tool for all Python needs, 10-100x faster than pip, excellent Claude integration
  - **Commands**: `uv sync`, `uv add`, `uv run`, `uv tool`
  - **Status**: Established across system

- **Code Quality**: `Ruff` ✅
  - **Why**: Single tool for linting + formatting, extremely fast, comprehensive rules
  - **Commands**: `uv run ruff check`, `uv run ruff format`
  - **Config**: `pyproject.toml` section

- **Testing**: `pytest` ✅
  - **Why**: Clean syntax, excellent discovery, powerful fixtures, extensive plugin ecosystem
  - **Commands**: `uv run pytest`
  - **Config**: `pyproject.toml` section

#### **JavaScript/TypeScript (Secondary)**

- **Runtime**: `Bun` 🆕
  - **Why**: Single tool (run/test/bundle), extremely fast, excellent TypeScript support
  - **Commands**: `bun run`, `bun test`, `bun install`
  - **Rationale**: Replaces Node.js + npm + multiple dev tools with one fast solution

- **Testing**: `Vitest` 🆕
  - **Why**: Fast, modern, excellent defaults, great TypeScript integration
  - **Commands**: `bun vitest`
  - **Config**: `vitest.config.ts`

### **Documentation & Configuration**

#### **Documentation Generation**

- **Primary**: `MkDocs` ✅
  - **Why**: Markdown-native, simple config, excellent themes, GitHub integration
  - **Commands**: `uv run mkdocs serve`, `uv run mkdocs build`
  - **Config**: `mkdocs.yml`

- **Diagrams**: `Mermaid` 🆕
  - **Why**: Text-based (version controllable), GitHub-integrated, comprehensive diagram types
  - **Usage**: Embedded in Markdown, renders automatically in GitHub/MkDocs
  - **No installation required**: Browser-based rendering

#### **Configuration Formats**

- **Complex Configuration**: `TOML` 🆕
  - **Why**: Human-readable, supports comments, typed sections, Python-native support
  - **Use for**: `pyproject.toml`, application config files

- **Simple Data**: `JSON` ✅
  - **Why**: Universal support, no ambiguity, Claude handles perfectly
  - **Use for**: API responses, simple data exchange, settings files

- **CI/CD Configuration**: `YAML` 🆕
  - **Why**: Industry standard for GitHub Actions, readable, structured
  - **Use for**: GitHub Actions, Docker Compose

#### **Environment Management**

- **Environment Variables**: `.env` files with `python-dotenv` 🆕
  - **Why**: Standard pattern, easy to manage, clear separation of secrets
  - **Tools**: `python-dotenv` for loading, `uv add python-dotenv`

### **Automation & CI/CD**

#### **Continuous Integration**

- **Platform**: `GitHub Actions` 🆕
  - **Why**: Configuration as code, excellent documentation, integrated with GitHub
  - **Config**: `.github/workflows/*.yml`
  - **Benefits**: Free for public repos, excellent Claude Code integration

#### **File Watching & Automation**

- **File Watching**: `Python watchdog` 🆕
  - **Why**: Pure Python, reliable, cross-platform, integrates with our stack
  - **Commands**: Custom Python scripts using `watchdog.observers`

- **Task Automation**: `Python Scripts` ✅
  - **Why**: Consistent language, leverage UV ecosystem, easy to maintain
  - **Pattern**: `scripts/` directory with dedicated Python modules
  - **Execute**: `uv run python scripts/script_name.py`

### **Data & Storage**

#### **Database**

- **Single-User/Development**: `SQLite` 🆕
  - **Why**: Zero-config, file-based, excellent Python integration, perfect for Claude Code
  - **Tools**: Built into Python, use `sqlite3` or `sqlalchemy`

- **Multi-User/Production**: `PostgreSQL` 🆕
  - **Why**: Industry standard, excellent documentation, reliable, feature-rich
  - **Tools**: `psycopg2-binary` with `sqlalchemy`

#### **Data Serialization**

- **Simple Data Exchange**: `JSON` ✅
- **Configuration Files**: `TOML` 🆕  
- **CI/CD & Docker**: `YAML` 🆕
- **Binary Data**: `Pickle` (Python-only) or `msgpack` (cross-language)

---

## Integration Patterns

### **Project Structure Template**

```sh
project/
├── pyproject.toml          # UV dependencies + tool config
├── .env                    # Environment variables
├── .github/workflows/      # GitHub Actions
├── scripts/                # Automation scripts
├── src/                    # Source code
├── tests/                  # pytest tests
├── docs/                   # MkDocs documentation
└── mkdocs.yml             # Documentation config
```

### **Quality Gates Integration**

```bash
# Standard quality check sequence
uv run ruff check         # Linting
uv run ruff format --check # Formatting 
uv run pytest            # Testing
uv run mkdocs build       # Documentation build
```

### **Development Workflow**

```bash
# Setup new project
uv sync                   # Install dependencies
uv run pytest            # Verify tests pass
uv run mkdocs serve       # Start docs server

# Daily development
uv run ruff check --fix   # Auto-fix issues
uv run pytest -xvs       # Run tests with output
uv run python scripts/   # Run automation
```

---

## Evaluation Framework

### **Adding New Tools** (Decision Process)

1. **Claude Code Compatibility Check**:
   - ✅ Can Claude configure it via files?
   - ✅ Are error messages clear and actionable?
   - ✅ Is CLI interface comprehensive?
   - ✅ Is behavior predictable and deterministic?

2. **Integration Assessment**:
   - ✅ Works well with existing stack?
   - ✅ Doesn't duplicate existing functionality?
   - ✅ Adds clear value over alternatives?
   - ✅ Has good documentation for Claude to learn from?

3. **Maintenance Considerations**:
   - ✅ Actively maintained project?
   - ✅ Stable API/configuration?
   - ✅ Good community support?
   - ✅ Reasonable resource requirements?

### **Tool Replacement Process**

1. **Document Current Usage**: Audit existing implementations
2. **Create Migration Plan**: Step-by-step transition approach  
3. **Update Standards**: Modify this document with new choices
4. **Systematic Replacement**: Update projects consistently
5. **Validation**: Ensure all functionality preserved

---

## Migration Strategy

### **From Inconsistent to Standardized**

#### **Phase 1**: Foundation (Immediate)

- ✅ UV already established
- ✅ Ruff + pytest already in use
- 🆕 Document MkDocs as standard
- 🆕 Establish GitHub Actions as CI standard

#### **Phase 2**: Enhancement (Next Sprint)  

- 🆕 Add Bun for JS/TS projects
- 🆕 Implement Mermaid for diagrams
- 🆕 Standardize on SQLite for local data
- 🆕 Create project templates with full stack

#### **Phase 3**: Optimization (Ongoing)

- Monitor tool performance and Claude integration
- Evaluate new tools against framework
- Continuously optimize configuration patterns
- Build institutional knowledge base

---

## Quick Reference

### **One-Command Setup**

```bash
# New Python project with full stack
uv init project-name
cd project-name
uv add ruff pytest mkdocs python-dotenv
# Copy standard configs from templates/
```

### **Daily Commands**

```bash
uv run ruff check --fix     # Code quality
uv run pytest             # Testing  
uv run mkdocs serve        # Documentation
uv run python scripts/    # Automation
```

### **Integration Commands**

```bash
# CI/CD check (what GitHub Actions runs)
uv run ruff check && uv run pytest && uv run mkdocs build
```

### **System Management Commands**

```bash
# System health verification
uv run global/scripts/core/health-check.py --quiet

# Configuration backup management
uv run global/scripts/core/backup-config.py --quiet    # Create backup
uv run global/scripts/core/backup-config.py --list     # List backups

# Session management
uv run global/scripts/utils/session-setup.py YYYY-MM-DD

# Emergency recovery
ls ~/.claude-backups/                                   # Check available backups
uv run global/scripts/core/health-check.py            # Full diagnostic
```

---

## Success Metrics

### **Consistency Indicators**

- Zero tool selection decisions needed for new projects
- 100% of projects follow standard structure  
- Standard quality gates pass across all projects
- Documentation generation works universally

### **Claude Code Optimization**

- Reduced session startup time (no tool research needed)
- Consistent error handling across tools
- Predictable automation behavior
- Seamless cross-project knowledge transfer

### **Quality Improvements**

- Faster development cycles with optimized toolchain
- Better error messages and debugging experience
- Consistent code quality across all projects
- Automated quality assurance with minimal overhead

---

**Tech Stack Status**: 🚀 **PRODUCTION READY** - All Claude Code instances should use these definitive choices  
**Update Protocol**: Major changes require documentation here + announcement to all development  
**Next Review**: Monthly assessment of tool performance and new options
