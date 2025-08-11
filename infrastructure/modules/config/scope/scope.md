# Claude Code Directory Structure & Scope Definition

**Document Purpose**: Prevent scope confusion between global and project-specific Claude Code configurations  
**Creation Date**: 2025-08-10  
**Reference**: Official Claude Code Documentation  

---

## Critical Scope Boundaries

### Global User Directory: `C:\Users\omarm\.claude\`

**Purpose**: Personal cross-project configuration and memory  
**Scope**: ALL Claude Code projects for user Omar El Mountassir  
**Persistence**: Permanent across all sessions and projects  

#### Global Directory Contents

```sh
C:\Users\omarm\.claude\
├── CLAUDE.md                  # Main configuration pointer
├── settings.json              # Personal global settings
├── config/                    # Modular configuration files
│   ├── core.md               # Philosophy & learning protocols
│   ├── standards.md          # Quality gates & tools
│   ├── errors.md            # Error archive & prevention
│   └── sessions.md          # Session protocols
├── sessions/                  # Session documentation
├── docs/                     # Reference documentation
└── projects/                 # Project workspaces
```

#### What Belongs in Global Scope

✅ **Universal principles** applicable to ALL projects  
✅ **Error prevention protocols** and quality standards  
✅ **Language standards** and communication preferences  
✅ **Cross-project learning patterns** and methodologies  
✅ **Personal development tools** and workflow preferences  
✅ **Global agents** used across multiple projects  

#### What Does NOT Belong in Global Scope

❌ **Project-specific** architecture details  
❌ **Custom project tools** and specialized commands  
❌ **Domain-specific** configuration and workflows  
❌ **Project names** or specific file paths  
❌ **Repository-specific** patterns or conventions  

### Project-Specific Directory: `[PROJECT_PATH]/.claude/`

**Purpose**: Team-shared and project-specific configuration  
**Scope**: Single project/repository only  
**Persistence**: Stored in project version control  

#### Project Directory Contents

```sh
[PROJECT_PATH]/.claude/
├── settings.json              # Team-shared project settings
├── settings.local.json        # Personal project settings (not in VCS)
├── CLAUDE.md                  # Project-specific memory/instructions
└── agents/                    # Project-specific subagents
    ├── project-agent-1/
    └── domain-agent-2/
```

---

## Memory Hierarchy & Precedence

Claude Code loads memory files in this precedence order:

1. **Enterprise Policy** (system-wide, highest precedence)
2. **Project Memory** (`[PROJECT]/.claude/CLAUDE.md`)
3. **User Memory** (`~/.claude/CLAUDE.md`)
4. **Local Project Memory** (deprecated)

**Key Rule**: Higher-level files take precedence and provide foundation for more specific memories.

---

## Configuration Loading Behavior

### Startup Sequence

When Claude Code launches in a project:

1. Loads global `~/.claude/CLAUDE.md` (foundational layer)
2. Searches up directory tree for project `.claude/CLAUDE.md`
3. Merges configurations with project-specific taking precedence
4. Applies any enterprise policies on top

### Import System

Both global and project configurations can import additional files:

```markdown
# In any CLAUDE.md file
@path/to/specialized-config.md
@shared/common-patterns.md
```

---

## Validation Checklist

### Global Configuration Audit

- [ ] No project-specific names or paths
- [ ] All items apply universally across projects  
- [ ] Error prevention protocols are technology-agnostic
- [ ] Personal standards are truly permanent preferences

### Project Configuration Audit  

- [ ] All items are project/domain-specific
- [ ] Team members can understand and use configuration
- [ ] Technology stack details are appropriate
- [ ] No universal principles duplicated from global

---

**Key Insight**: The `.claude` directory is Claude Code's configuration and memory system. The `projects/` subdirectory contains workspaces, while `config/` contains the modular global configuration.

**Critical Rule**: Maintain strict separation between universal principles (global) and project-specific details (project-local) to prevent configuration contamination and ensure proper scope isolation.
