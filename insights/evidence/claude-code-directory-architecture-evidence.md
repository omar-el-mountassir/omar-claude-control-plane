# Claude Code Directory Architecture Evidence

**Date**: 2025-08-12  
**Source**: Official Claude Code Documentation Research  
**Purpose**: Evidence for global configuration directory patterns  

---

## **Research Question**

Where should global Claude Code configuration files be placed? What is the correct directory structure?

## **Documentation Evidence**

### **Official Settings Documentation**

**Source**: <https://docs.anthropic.com/en/docs/claude-code/settings>

**Key Findings**:

**Global Settings Locations**:

- User settings: `~/.claude/settings.json`
- User subagents: `~/.claude/agents/`

**Project-Specific Settings Locations**:

- Shared project settings: `.claude/settings.json` (checked into source control)
- Local project settings: `.claude/settings.local.json` (personal, not checked in)
- Project subagents: `.claude/agents/`

**Enterprise Settings Location**:

- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

### **Official Memory Documentation**

**Source**: <https://docs.anthropic.com/en/docs/claude-code/memory>

**Key Findings**:

**Claude Code Memory Locations**:

1. **Enterprise policy memory** (system-wide):

- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`

2. **Project memory**: `./CLAUDE.md` (shared with team via source control)

3. **User memory**: `~/.claude/CLAUDE.md` (personal preferences for all projects)

4. **Project memory (local, now deprecated)**: `./CLAUDE.local.md`

## **Pattern Analysis**

### **Established Global User Pattern**

**Confirmed Pattern**: `~/.claude/[category]/`

**Examples**:

- `~/.claude/settings.json` ✅
- `~/.claude/CLAUDE.md` ✅
- `~/.claude/agents/` ✅

**Therefore**: `~/.claude/rules/` ✅ follows established pattern

### **Anti-Pattern Identified**

**Incorrect**: `~/.claude/.claude/[anything]` ❌
**Evidence**: No documentation examples show nested `.claude` directories within global user space

## **Architectural Decision**

**Decision**: Place global commit rules in `~/.claude/rules/`  
**Rationale**: Follows documented pattern for global user configuration  
**Integration**: Reference in `~/.claude/CLAUDE.md` for automatic loading

## **Validation**

**Implementation**: Successfully created:

```
~/.claude/rules/
├── three-fix-protocol.md
├── commit-workflow-rules.md
└── quality-gates-commits.md
```

**Integration**: Added references to `~/.claude/CLAUDE.md` for automatic loading across all Claude Code instances

## **Future Reference**

**Principle**: Global user configuration follows flat `~/.claude/[category]/` pattern  
**Prevention**: Always verify against official documentation before assuming nested structures
