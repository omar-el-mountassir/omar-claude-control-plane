---
version: "0.1.0"
compatibility: ">=0.1.0"
last_updated: 2025-08-11
module_type: configuration
stability: stable
component: module
dependencies:
  - core: ">=0.1.0"
created: 2025-08-10
author: collaborative
description: "Quality gates, tools, file editing protocols, and technical standards"
---

# Standards Configuration - Omar El Mountassir

**Module**: Quality Gates, Tools & Technical Standards  
**Scope**: Technical standards applicable across all development work  

---

## Code Quality Gates

- **Zero Warnings Policy**: All linting warnings must be resolved
- **Test-First Development**: Write tests before implementation
- **Implementation-First Documentation**: Never document features without implementing them first
- **Dependency Verification**: Check all dependencies exist before using them
- **🚨 Framework Compliance Mandatory**: All actions must systematically apply established frameworks before execution
- **⚡ Atomic Task Format Mandatory**: All tasks must follow atomic task format specification (see @conventions/atomic-task-format.md)

---

## Error Prevention Protocols

### Before Any Technical Work

1. **Framework Application First**: Apply all relevant established frameworks systematically
2. **Template Discovery**: Check `infrastructure/templates/` for relevant templates before creating new files
3. **Research First**: Use WebFetch to check official documentation
4. **Implement Minimally**: Create smallest working example
5. **Test Thoroughly**: Verify implementation works as expected  
6. **Document Reality**: Only document what actually works

### Before Any Feature Documentation  

- [ ] Verify framework compliance with systematic application
- [ ] Verify template usage from infrastructure/templates/
- [ ] Consult official documentation
- [ ] Create working implementation
- [ ] Test configuration files
- [ ] Validate against official schemas
- [ ] Confirm external dependencies exist

---

## Mandatory Protocols

### **File Editing Protocol (Mandatory)**

**BEFORE ANY EDIT OPERATION:**

1. **ALWAYS** use Read tool to understand current file content
2. **VERIFY** exact formatting, indentation, and line structure
3. **MATCH** old_string parameter exactly as shown in Read output
4. **PRESERVE** all whitespace, tabs, and formatting from Read result
5. **CONFIRM** line numbers and content alignment before Edit

#### Quality Gate: Read-Before-Edit Rule

```bash
# FORBIDDEN PATTERN
Edit(file_path, old_string, new_string)  # ❌ NEVER edit without reading first

# REQUIRED PATTERN  
Read(file_path)                          # ✅ ALWAYS read first
Edit(file_path, old_string, new_string)  # ✅ Then edit with exact content
```

### **Automatic Reference Management Protocol (MANDATORY)**

**FOR ANY SYSTEM CHANGE, ADDITION, OR MODIFICATION:**

1. **IMMEDIATE UPDATE REQUIREMENT**: ALL related files and references MUST be updated automatically
2. **NO EXCEPTIONS**: Never leave references incomplete or outdated
3. **SYSTEMATIC IDENTIFICATION**: Before any change, identify ALL files that reference the modified content
4. **BATCH UPDATES**: Update all references in the same session as the primary change
5. **CROSS-MODULE INTEGRATION**: Ensure changes propagate through config/operations/memory/knowledge/meta modules

#### Reference Update Checklist

- [ ] Update CLAUDE.md for new modules or major features
- [ ] Update related config modules for protocol changes
- [ ] Update integration protocols for workflow changes
- [ ] Update CURRENT-WORK.md for priority changes
- [ ] Update CHANGELOG.md for architectural changes
- [ ] Validate and update all cross-references

### **Workspace vs Project Repository Protocol**

**BEFORE ANY TECHNICAL ANALYSIS:**

1. **Path Classification**: Determine if analyzing `.claude/projects/` (workspace) or external path (actual project)
2. **Scope Adjustment**:
   - **Workspaces**: Analyze as methodology/specification development
   - **Projects**: Apply full technical analysis protocols
3. **Deliverable Type**:
   - **Workspaces**: Conceptual analysis, methodology refinement, specification review
   - **Projects**: Technical implementation recommendations, code quality assessment

---

## Global Commands & Tools

### Standard Quality Gates

- Always run linting and formatting before commits
- Use official testing frameworks (never assume)
- Verify builds succeed before major changes
- Check documentation renders correctly

### External Integration Standards

- Use `gh` CLI for all GitHub operations
- Prefer MCP tools over direct bash commands where available
- Always check tool availability before use
- Document tool prerequisites and setup

---

## Python Environment Standards

### **UV Package Manager (Global Standard)**

**All Claude Code Python projects use UV by Astral** - the extremely fast Python package and project manager:

#### Installation (Windows)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Standard Commands

```bash
# Project initialization
uv sync                    # Install dependencies from pyproject.toml
uv add package             # Add new dependency  
uv run python script.py   # Run with project environment
uv run pytest            # Run tests with project dependencies

# Tool management
uv tool install ruff black mypy  # Global development tools
uvx tool                   # Run tool without installation
```

#### Benefits

- **10-100x faster** than pip for installation and dependency resolution
- **Single tool** replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv
- **Project management** with automatic virtual environments
- **Python version management** built-in (`uv python install 3.12`)

#### Quality Gate Integration

- All Python commands in quality gates must use `uv run`
- All dependency installations must use `uv add`
- All project setups must include `pyproject.toml` with UV standards

---

## Success Patterns & Quality Standards

### Systematic Approach Template

1. **Plan**: Use TodoWrite for complex tasks
2. **Research**: Check documentation before implementation
3. **Implement**: Create minimal working version
4. **Verify**: Test thoroughly before documenting
5. **Document**: Record only what works
6. **Learn**: Update error log with lessons learned

### Quality Verification Checklist

- [ ] Log all errors with prevention protocols
- [ ] Match documentation with actual implementation
- [ ] Verify and document dependencies
- [ ] Complete testing before delivery
- [ ] Create reusable templates where applicable

### Recovery Protocols

#### When Analysis Goes Undocumented

1. **STOP** current work immediately
2. Create structured documentation project
3. Clone/recreate analysis environment locally
4. Document architecture completely with examples
5. Create reusable templates
6. Verify documentation completeness before continuing

#### When Implementation Precedes Documentation

1. Research official documentation sources
2. Create minimal working implementation
3. Test in isolation
4. Validate against official schemas
5. Only then document the working solution

#### When Dependencies Are Missing

1. Check package.json/requirements.txt first
2. Verify installation status
3. Test imports in isolation
4. Add missing dependencies before proceeding
5. Document dependency requirements

---

## Language Standards

**Primary Language**: English for technical documentation and error logging  
**Secondary Language**: French for personal notes and non-technical context  
**Consistency Rule**: Never mix languages within the same technical section

---

## Documentation Standards

### Documentation Requirements

- **Analysis Documentation**: ALWAYS document technical analysis completely and structurally
- **Decision Logging**: Document architectural decisions with rationale  
- **Template Creation**: Create reusable templates for reproducible processes
- **Concrete Deliverables**: Always create tangible output documents for validation and reference

---

## System Management Standards

### **CURRENT-WORK.md Update Protocol**

**When to Update CURRENT-WORK.md**:
- ✅ **Immediately**: When changing primary focus or completing major tasks
- ✅ **End of session**: Update progress percentages and current focus context
- ✅ **Weekly**: Review and clean up completed items, update strategic direction

**What NOT to Update**:
- System management protocols (they belong in configuration modules)
- Universal commands and procedures (they belong in tech-stack or standards)
- Session management guidance (it belongs in operations/continuity)

### **Quality Gates** (Always Apply)

**For ALL file modifications**:
- [ ] Apply Read-before-Edit protocol for all file modifications
- [ ] Run health check after architectural changes
- [ ] Apply modern Python standards for all new code
- [ ] Create documentation for all new patterns and systems

**For ALL system changes**:
- [ ] Update references in related configuration modules
- [ ] Validate all cross-references and links  
- [ ] Test system health after modifications
- [ ] Document rationale for architectural decisions

### **System Health Monitoring**

**Standard System Commands** (Reference tech-stack.md for full commands):
```bash
# System health verification
uv run global/scripts/core/health-check.py --quiet

# Backup management  
uv run global/scripts/core/backup-config.py --quiet
uv run global/scripts/core/backup-config.py --list

# Session management
uv run global/scripts/utils/session-setup.py YYYY-MM-DD
```

### **Emergency Procedures**

**System Recovery**:
1. **Backup Restore**: Check `~/.claude-backups/` and restore most recent
2. **Health Check**: Run `uv run global/scripts/core/health-check.py`
3. **Configuration Validation**: Verify all module references are working
4. **Context Recovery**: Use operations/continuity protocols

**Configuration Corruption**:
1. **Immediate Backup**: Create backup of current state
2. **Module Validation**: Check each configuration module individually  
3. **Reference Repair**: Fix any broken cross-references
4. **System Test**: Verify Claude Code can load all modules successfully
