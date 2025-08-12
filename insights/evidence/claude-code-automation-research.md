# Claude Code Automation Research Evidence

**Date**: 2025-08-12  
**Research Scope**: Claude Code native automation dependencies  
**Purpose**: Evidence for critical directory preservation rules  

---

## **Research Findings**

### **Projects Directory Critical Discovery**

**Source**: Official Claude Code community research and documentation

**Key Finding**: `~/.claude/projects/` contains session transcripts for EVERY project where Claude Code was run

**Evidence Quote**: 
> "The `~/.claude/projects` directory contains a list of every project where you've run Claude Code, with inside each project directory being a transcript file for every session you've done."

**Automation Dependency**: Session management and project context continuity relies on this exact directory structure.

### **Hooks System Automation**

**Source**: Multiple official Claude Code sources

**Key Findings**:

**Hooks Configuration**:
> "You can create your own hooks via a .claude/settings.json file in your project directory. Claude Code hooks are shell commands that execute at various points in Claude Code's lifecycle."

**Hook Types Discovered**:
- **PreToolUse**: Before Claude executes any tool
- **PostToolUse**: After a tool completes successfully  
- **Notification**: When Claude sends notifications
- **Stop**: When Claude finishes responding

**Critical Dependency**: Exact `.claude/settings.json` location required for automatic hook execution.

### **Custom Commands Automation**

**Evidence**: 
> "Putting content into .claude/commands/fix-github-issue.md makes it available as the /project:fix-github-issue command in Claude Code. You can add your own personal commands to the ~/.claude/commands folder for commands you want available in all of your sessions."

**Team Sharing**: 
> "Custom commands stored in .claude/commands/ are automatically shared when team members clone your repository."

**Automation Impact**: Directory location is critical for:
1. Command discovery and loading
2. Team collaboration through repository sharing
3. Global vs project-specific command availability

### **Configuration Hierarchy System**

**Precedence Order Discovered**:
1. Enterprise managed policies (system-wide)
2. Command line arguments  
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

**Critical Finding**: Exact file locations required for proper configuration loading hierarchy.

### **Working Directory Context**

**Evidence**:
> "The working directory is Claude Code's primary context location where Claude operates and discovers project configuration. When you launch Claude Code, it uses the current terminal directory as the working directory and automatically reads the CLAUDE.md file if present."

**Automation Dependency**: Automatic CLAUDE.md discovery depends on working directory context.

---

## **Automation Systems Summary**

### **Directory-Dependent Automation**

1. **Session Management**: `~/.claude/projects/` structure
2. **Hook Execution**: `.claude/settings.json` location  
3. **Command Discovery**: `.claude/commands/` and `~/.claude/commands/` locations
4. **Configuration Loading**: Exact hierarchy file locations
5. **Project Context**: Working directory automatic discovery

### **Breaking Changes Risk**

**Moving ANY of these directories would break**:
- Cross-session project continuity
- Automatic hook execution  
- Custom command system
- Configuration hierarchy
- Team collaboration features
- Project context discovery

---

## **Sources**

1. **Official Claude Code Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices
2. **Claude Code Directory Excellence Guide**: Multiple community sources
3. **Working Directory Documentation**: https://claudelog.com/faqs/what-is-working-directory-in-claude-code/
4. **Hooks Automation Guide**: https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks/
5. **Complete Setup Documentation**: Multiple professional development guides

---

## **Validation**

**Research Method**: Systematic search of official documentation and community resources  
**Verification**: Cross-referenced multiple sources for consistency  
**Conclusion**: Directory structures have extensive hidden automation dependencies  

**Prevention Impact**: This research prevents system-breaking moves of critical Claude Code infrastructure.