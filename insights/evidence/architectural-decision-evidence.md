# Architectural Decision Evidence: Directory Naming

**Decision**: Whether to use `~/.claude/system/` vs `~/.claude/insights/` vs other options  
**Date**: 2025-08-12  
**Method**: Evidence-based analysis with official documentation research  
**Status**: Evidence compiled, decision pending  

---

## **🔍 EVIDENCE SUMMARY**

### **Key Factual Findings**

1. **"System" Naming Not Official Pattern**
   - ❌ Zero references in official Claude Code documentation
   - ❌ Native directories use functional names: `commands/`, `projects/`, `shell-snapshots/`
   - ❌ No precedent for "system" directories in Claude Code architecture

2. **Functional Naming IS Official Pattern**
   - ✅ `.claude/commands/` not `.claude/system/commands/` 
   - ✅ Native directories: `projects/`, `shell-snapshots/`, `ide/`, `statsig/`
   - ✅ Pattern: Name by FUNCTION, not abstract categories

3. **Redundancy Analysis**
   - ✅ `~/.claude/` IS the Claude Code system directory
   - ❌ `~/.claude/system/` = redundant "system/system" naming
   - ✅ Should use functional naming within system directory

### **Content Analysis**

**What's Actually Inside**:
- System insights and accumulated learning
- Prevention protocols and error analysis  
- Meta-cognitive discoveries and patterns
- Evidence files and research documentation

**Best Functional Names**:
1. `insights/` - Direct match to content function
2. `intelligence/` - Broader AI learning and analysis
3. `learning/` - Focus on accumulated knowledge

---

## **📊 DECISION MATRIX**

| Option | Official Pattern | Functional Naming | Content Match | Redundancy | Score |
|--------|------------------|-------------------|---------------|------------|-------|
| `system/` | ❌ No precedent | ❌ Abstract | ⚠️ Generic | ❌ Redundant | 1/4 |
| `insights/` | ✅ Functional pattern | ✅ Descriptive | ✅ Perfect match | ✅ Clear | 4/4 |
| `intelligence/` | ✅ Functional pattern | ✅ Descriptive | ✅ Good match | ✅ Clear | 4/4 |
| `knowledge/` | ✅ Functional pattern | ✅ Descriptive | ⚠️ Broad | ✅ Clear | 3.5/4 |

---

## **💡 EVIDENCE-BASED RECOMMENDATION**

### **Primary Recommendation: `~/.claude/insights/`**

**Supporting Evidence**:
- ✅ **Official Pattern Compliance**: Follows functional naming like `.claude/commands/`
- ✅ **Content Accuracy**: Precisely describes system insights and learning
- ✅ **No Redundancy**: Avoids "system/system" naming issue
- ✅ **Future Scalable**: Can grow with more insight types

### **Alternative: `~/.claude/intelligence/`**

**Supporting Evidence**:
- ✅ **Official Pattern Compliance**: Functional naming  
- ✅ **Broader Scope**: Encompasses insights + AI reasoning + analysis
- ✅ **Future-Ready**: Suitable for advanced AI capabilities
- ⚠️ **Slightly Abstract**: Less directly descriptive of current content

---

## **🚫 REJECTED OPTIONS**

### **`~/.claude/system/` - REJECTED**

**Evidence Against**:
- ❌ **No Official Precedent**: Not found in Claude Code documentation
- ❌ **Redundant Naming**: "system" inside system directory  
- ❌ **Abstract Category**: Not functional description
- ❌ **Pattern Violation**: Doesn't follow functional naming

### **Back to `~/.claude/knowledge/` - NOT RECOMMENDED**

**Evidence Against**:
- ⚠️ **Too Broad**: Knowledge encompasses more than insights
- ⚠️ **Previous Issues**: We moved away from this structure already
- ✅ **Would Work**: But less precise than alternatives

---

## **📋 IMPLEMENTATION PLAN**

**If Decision: `~/.claude/insights/`**

1. **Rename Directory**: `~/.claude/system/` → `~/.claude/insights/`
2. **Update References**: CLAUDE.md paths from `@system/` → `@insights/`
3. **Maintain Structure**: Keep evidence/ subdirectory and files
4. **Update Documentation**: All references to new functional name

**Migration Commands**:
```bash
mv ~/.claude/system ~/.claude/insights
# Update CLAUDE.md references
# Update internal file references
```

---

## **🎯 DECISION CRITERIA MET**

1. ✅ **Factual Evidence Compiled** - Official documentation analyzed
2. ✅ **Pattern Analysis Complete** - Claude Code patterns identified  
3. ✅ **Content Analysis Done** - Actual directory contents evaluated
4. ✅ **Options Scored** - Objective comparison completed
5. ✅ **Recommendation Based on Evidence** - Not opinion, but facts

**Decision Ready**: Evidence supports `~/.claude/insights/` as optimal solution based on Claude Code patterns, content accuracy, and architectural consistency.

---

**Evidence File**: Complete analysis at `@system/evidence/claude-code-directory-analysis.md`  
**Next Step**: Execute decision based on factual evidence presented