# Claude Code Directory Structure & Scope Definition

**Document Purpose**: Prevent scope confusion between global and project-specific Claude Code configurations  
**Creation Date**: 2025-08-10  
**Reference**: Official Claude Code Documentation  

## Critical Scope Boundaries

### Global User Directory: `C:\Users\omarm\.claude\`

**Purpose**: Personal cross-project configuration and memory  
**Scope**: ALL Claude Code projects for user Omar El Mountassir  
**Persistence**: Permanent across all sessions and projects  

#### Global Directory Contents

```sh
C:\Users\omarm\.claude\
├── settings.json              # Personal global settings
├── CLAUDE.md                  # Global memory/instructions
├── agents/                    # User subagents (cross-project)
│   ├── custom-agent-1/
│   └── custom-agent-2/
└── projects/                  # Project workspaces
    ├── project-name-1/
    └── omar-el-mountassir/    # Your personal project namespace
        └── repo/              # Specific repository/project
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

## Memory Hierarchy & Precedence

Claude Code loads memory files in this precedence order:

1. **Enterprise Policy** (system-wide, highest precedence)
2. **Project Memory** (`[PROJECT]/.claude/CLAUDE.md`)
3. **User Memory** (`~/.claude/CLAUDE.md`)
4. **Local Project Memory** (deprecated)

**Key Rule**: Higher-level files take precedence and provide foundation for more specific memories.

## Configuration Scope Examples

### ✅ Correct Global Configuration (`C:\Users\omarm\.claude\CLAUDE.md`)

```markdown
# Global error prevention protocols
**Read-Before-Edit Rule**: ALWAYS use Read tool before Edit operations

# Universal quality standards  
- Zero warnings policy for all projects
- Test-first development approach

# Cross-project language standards
**Primary Language**: English for technical documentation
```

### ❌ Incorrect Global Configuration

```markdown
# Project-specific details (WRONG in global scope)
**MyApp Architecture**: Uses React + FastAPI backend
**Custom Commands**: `npm run dev:myapp` to start development server
**Project Path**: `/specific/project/path/myapp`
```

### ✅ Correct Project Configuration (`[PROJECT]/.claude/CLAUDE.md`)

```markdown
# Project: MyApp - E-commerce Platform
**Architecture**: React frontend + FastAPI backend + PostgreSQL
**Development**: `npm run dev` starts full stack
**Testing**: `pytest backend/` and `npm test frontend/`
```

## Directory Structure Rules

### Global Projects Organization

```
C:\Users\omarm\.claude\projects\
├── personal-namespace/          # Your projects
│   ├── repo-1/
│   ├── repo-2/
│   └── omar-el-mountassir/     # Specific project namespace
│       └── repo/               # The repository we analyzed
├── client-work/                # Client projects
│   ├── client-a/
│   └── client-b/
└── experiments/                # Temporary/learning projects
    ├── ai-experiments/
    └── tech-demos/
```

### Project Workspace Isolation

Each project in `projects/` is **completely isolated**:

- Independent `.claude/` configuration
- Separate agents and memory
- Project-specific settings and workflows
- No cross-contamination between projects

## Best Practices for Scope Management

### Before Adding to Global CLAUDE.md

Ask yourself:

1. **Universal Applicability**: Does this apply to ALL my Claude Code projects?
2. **Cross-Project Value**: Will this help across different domains/technologies?
3. **Personal Standard**: Is this a permanent part of my development approach?

If any answer is "No" → Add to project-specific configuration instead.

### Before Adding to Project CLAUDE.md

Ask yourself:

1. **Project-Specific**: Is this only relevant to this particular project?
2. **Team-Shareable**: Should other contributors know about this?
3. **Domain-Specific**: Is this specific to this technology stack/domain?

If any answer is "Yes" → Keep in project configuration.

## Error Prevention Protocol

### Scope Violation Detection

**Warning Signs of Scope Confusion:**

- Project names in global configuration
- Specific file paths in global memory  
- Technology-specific commands in global settings
- Universal principles in project-only configuration

### Correction Protocol

1. **Identify**: Determine correct scope for each configuration item
2. **Separate**: Move items to appropriate configuration files
3. **Verify**: Ensure global items are truly universal
4. **Test**: Confirm configuration loads correctly in new projects

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

**Key Insight**: The `.claude` directory is Claude Code's configuration and memory system, not a repository workspace. The `projects/` subdirectory contains actual project workspaces organized by namespace.

**Critical Rule**: Maintain strict separation between universal principles (global) and project-specific details (project-local) to prevent configuration contamination and ensure proper scope isolation.
