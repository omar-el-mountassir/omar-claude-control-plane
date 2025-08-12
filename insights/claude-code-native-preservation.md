# Claude Code Native Directory Preservation Rules

**Priority**: 🚨 **CRITICAL** - System Breaking Prevention  
**Scope**: All Claude Code instances and future sessions  
**Last Updated**: 2025-08-12  

---

## 🚨 **NEVER MOVE - CRITICAL AUTOMATION DEPENDENCIES**

### **❌ ABSOLUTELY FORBIDDEN TO MOVE**

#### 1. **`~/.claude/projects/`** 🚨

- **Function**: Contains session transcripts for EVERY project where Claude Code was run
- **Automation**: Project discovery and session history management
- **Risk**: Moving breaks all project context and session continuity

#### 2. **`.credentials.json`**

- **Function**: Authentication system (root location required)
- **Risk**: Moving breaks all Claude Code authentication

#### 3. **`~/.claude/settings.json`** & **`.claude/settings.local.json`**

- **Function**: Configuration hierarchy and user preferences
- **Risk**: Moving breaks configuration loading system

#### 4. **`.claude/`** (Project directories)

- **Function**: Internal Claude Code structure with hooks automation
- **Automation**: PreToolUse, PostToolUse lifecycle hooks
- **Risk**: Moving breaks project-level automation and team collaboration

#### 5. **`.claude/commands/`**

- **Function**: Custom slash commands automatically loaded
- **Automation**: Command discovery and team sharing
- **Risk**: Moving breaks custom command system

#### 6. **`shell-snapshots/`**

- **Function**: Claude Code shell history system
- **Risk**: Moving breaks shell session continuity

#### 7. **`statsig/`**

- **Function**: Analytics and telemetry system
- **Risk**: Moving breaks usage analytics

#### 8. **`todos/`**

- **Function**: Native todo system file storage
- **Risk**: Moving breaks todo persistence

#### 9. **`ide/`**

- **Function**: IDE integration lock files
- **Risk**: Moving breaks IDE integrations

---

## 🔍 **AUTOMATION DEPENDENCIES DISCOVERED**

### **Critical Automation Systems**

**Hooks System**:

- **Location Dependency**: `.claude/settings.json` in project directories
- **Function**: Executes shell commands at lifecycle points (PreToolUse, PostToolUse)
- **Impact**: Guaranteed automation that doesn't rely on Claude "remembering"

**Custom Commands**:

- **Location Dependency**: `.claude/commands/` and `~/.claude/commands/`
- **Function**: Custom slash commands automatically discovered and loaded
- **Impact**: Team-shared commands through repository cloning

**Session Management**:

- **Location Dependency**: `~/.claude/projects/`
- **Function**: Project list + transcript files for every session
- **Impact**: Cross-session continuity and project context

**Configuration Hierarchy**:

- **Location Dependency**: Exact directory structure for settings precedence
- **Function**: Enterprise → Project → User configuration layering
- **Impact**: Proper configuration loading and precedence

---

## 🛡️ **PREVENTION PROTOCOLS**

### **Before ANY File/Directory Movement**

1. **❓ RESEARCH FIRST**: Check this list and official documentation
2. **🔍 VERIFY**: Is this directory/file part of Claude Code's native infrastructure?
3. **⚠️ AUTOMATION CHECK**: Does this have hidden automation dependencies?
4. **🚫 NEVER ASSUME**: Directory structures may have invisible automation

### **When Uncertain**

1. **STOP**: Don't move anything without verification
2. **DOCUMENT**: Research the directory/file function first
3. **VALIDATE**: Check official Claude Code documentation
4. **CONFIRM**: Verify with user if automation dependencies exist

### **Safe Movement Rules**

✅ **SAFE TO MOVE**: User-created content without automation dependencies  
⚠️ **VERIFY FIRST**: Any directory that might have automation  
❌ **NEVER MOVE**: Anything on the critical list above  

---

## 📚 **Evidence Sources**

**Official Documentation**:

- Claude Code Settings: <https://docs.anthropic.com/en/docs/claude-code/settings>
- Claude Code Memory: <https://docs.anthropic.com/en/docs/claude-code/memory>
- Claude Code Best Practices: <https://www.anthropic.com/engineering/claude-code-best-practices>

**Research Evidence**: @insights/evidence/claude-code-automation-research.md

---

## 🔗 **Integration**

**CLAUDE.md Reference**:

```markdown
### **System Intelligence** (Critical)
- **Native Preservation**: @insights/claude-code-native-preservation.md - NEVER MOVE automation
```

**System Insights Integration**: Referenced in @insights/README.md prevention protocols

---

## ⚡ **QUICK REFERENCE**

**Before moving ANY directory**: Check this list first!  
**When in doubt**: DON'T MOVE - Research and verify first  
**Critical rule**: Native Claude Code infrastructure is UNTOUCHABLE

---

**Status**: 🔒 **LOCKED** - Critical system preservation rules  
**Next Review**: When Claude Code releases new automation features
