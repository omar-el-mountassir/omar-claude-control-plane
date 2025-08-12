# Claude Code Directory Naming Convention

**Status**: 🔒 **STANDARD** - Evidence-based naming rules  
**Date**: 2025-08-12  
**Scope**: All `~/.claude/` directory organization  
**Evidence Base**: Official Claude Code documentation analysis  

---

## **🎯 CORE PRINCIPLE**

***Functional Naming Over Abstract Categories***

Directory names should describe **WHAT THE CONTENT DOES**, not abstract organizational concepts.

---

## **📋 NAMING CONVENTION RULES**

### **Rule 1: Functional Description**

✅ **Good**: `commands/`, `insights/`, `agents/`, `templates/`  
❌ **Bad**: `system/`, `stuff/`, `misc/`, `data/`

**Rationale**: Function-based names immediately communicate purpose and content.

### **Rule 2: No Redundant System References**

✅ **Good**: `~/.claude/insights/`  
❌ **Bad**: `~/.claude/system/insights/`

**Evidence**: `~/.claude/` IS the system directory - avoid "system/system" redundancy.

### **Rule 3: Descriptive Not Generic**

✅ **Good**: `prevention-protocols/`, `automation-rules/`  
❌ **Bad**: `files/`, `documents/`, `content/`

### **Rule 4: Singular vs Plural Consistency**

✅ **Preferred**: Plural for collections (`agents/`, `rules/`, `insights/`)  
✅ **Acceptable**: Singular for single concepts (`documentation/`, `analysis/`)

**Pattern**: Follow existing Claude Code native patterns (plural: `projects/`, `shell-snapshots/`)

---

## **🏗️ DIRECTORY CATEGORIES**

### **Claude Code Native** (❌ NEVER RENAME)

```sh
/.claude/           # Internal Claude Code structure
/ide/               # IDE integration  
/projects/          # Session tracking
/shell-snapshots/   # Shell history
/statsig/           # Analytics
/todos/             # Native todo system
```

### **User Configuration** (Functional Names)

```sh
/agents/            # AI agents and specialists
/rules/             # Behavioral rules and protocols
/insights/          # System learning and intelligence
/conventions/       # Standards and consistency rules
/templates/         # Reusable templates and scaffolding
```

### **User Content** (Descriptive Names)

```sh
/scripts/           # Automation scripts
/sessions/          # Session documentation
/examples/          # Example code and demonstrations
/docs/              # User documentation
```

### **User Organization** (Purpose-Based)

```sh
/concepts/          # Proof-of-concepts and prototypes
/infrastructure/    # System infrastructure modules
/knowledge/         # Knowledge base and foundation
```

---

## **✅ APPROVED PATTERNS**

### **Single-Level Descriptive**

- `/insights/` - System learning and intelligence
- `/agents/` - AI specialists and automation
- `/rules/` - Behavioral protocols and standards
- `/conventions/` - Standards and consistency rules
- `/templates/` - Reusable scaffolding and patterns

### **Multi-Level Functional**

- `/insights/evidence/` - Supporting research and proof
- `/templates/automation/` - Automation-specific templates
- `/knowledge/foundation/` - Foundational knowledge base

---

## **❌ ANTI-PATTERNS**

### **Abstract Categories**

- `/system/` - Redundant within system directory
- `/misc/` - Non-descriptive catch-all
- `/stuff/` - No functional meaning
- `/data/` - Too generic

### **Redundant Hierarchies**

- `/system/system-*` - Double system reference
- `/claude/claude-*` - Double tool reference  
- `/config/configuration/` - Redundant naming

### **Non-Functional Names**

- `/files/` - Describes format, not function
- `/documents/` - Describes type, not purpose
- `/content/` - No specific meaning

---

## **🎯 DECISION FRAMEWORK**

### **Before Creating New Directory**

1. **Function Check**: What does this content DO?
2. **Description Check**: Does the name immediately communicate purpose?
3. **Redundancy Check**: Am I repeating concepts already in the path?
4. **Pattern Check**: Does this follow established functional naming?

### **Naming Decision Tree**

```sh
1. What function does this serve? → Use functional name
2. Is it a collection or single concept? → Plural vs singular
3. Does name avoid redundancy with parent path? → Check hierarchy
4. Would a new user understand immediately? → Clarity test
```

---

## **🔄 MIGRATION STANDARDS**

### **When Renaming Directories**

1. **Evidence First**: Research Claude Code patterns and official documentation
2. **Document Decision**: Create evidence file with rationale  
3. **Update References**: All CLAUDE.md and cross-references
4. **Validate**: Ensure all links and references work
5. **Archive Decision**: Preserve reasoning for future reference

### **Reference Update Pattern**

```markdown
# FROM: @old-name/file.md
# TO:   @new-name/file.md
# Update in: CLAUDE.md + all internal cross-references
```

---

## **📚 EVIDENCE BASE**

**Official Claude Code Patterns**:

- `.claude/commands/` - Functional naming for custom slash commands
- Native directories use descriptive functional names
- No abstract "system" categories in official documentation

**Analysis Source**: @insights/evidence/claude-code-directory-analysis.md  
**Decision Record**: @insights/evidence/architectural-decision-evidence.md

---

## **🚀 ENFORCEMENT**

### **Quality Gate Integration**

- All new directories must pass functional naming check
- Directory creation should include purpose documentation
- Regular audit of naming consistency

### **Future Reference**

- This convention applies to ALL future `~/.claude/` organization
- Violations should be flagged and corrected systematically
- Updates to this standard require evidence-based justification

---

**Convention Status**: 🔒 **ACTIVE STANDARD**  
**Next Review**: When Claude Code releases new organizational features  
**Enforcement**: Automatic quality gate integration recommended
