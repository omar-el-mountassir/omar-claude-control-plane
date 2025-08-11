
# Error Logging Template

**Purpose**: Systematic error documentation for Claude Code global configuration  
**Usage**: For logging errors in `global/modules/config/errors/errors.md`  
**Created**: 2025-08-10  

---

## Quick Template (Claude Code Standard)

For simple error logging in the global errors module:

```markdown
### **CRITICAL ERROR LOGGED [DATE]**: [Brief Description]

- **Root Cause**: [Technical reason for the error]
- **Impact**: [What was affected or broken]
- **Correction**: [What was changed to fix it]
- **Prevention**: [Protocol to prevent recurrence]
- **Verification**: [How the fix was confirmed]
```

---

## Usage Instructions

1. **Use this template** for all error entries in `errors.md`
2. **Be specific** - avoid generic descriptions
3. **Focus on prevention** - what protocol will prevent recurrence
4. **Document verification** - how you confirmed the fix works
5. **Keep it concise** - 1-2 sentences per field maximum

---

## Field Guidelines

### Root Cause
- **Technical reason** not just symptoms
- **Specific**: "Used Edit without Read first" vs "Tool usage error"
- **Actionable**: Should point to clear prevention protocol

### Impact
- **What broke** or what was affected
- **Scope**: Personal workflow, project delivery, system reliability
- **Consequence**: Time lost, confusion, failed operations

### Correction
- **Specific action taken** to resolve the immediate issue
- **Reference files/modules** updated if applicable
- **Concrete changes** not just "fixed it"

### Prevention
- **Protocol or rule** that prevents recurrence
- **Actionable**: Clear steps to follow in the future
- **Integrated**: Should reference or update other config modules

### Verification
- **How you confirmed** the correction works
- **Evidence**: Test results, successful operations, protocol compliance
- **Reproducible**: Others can verify the same way

---

## Example Error Entry

### **CRITICAL ERROR LOGGED 2025-08-10**: File editing without reading first

- **Root Cause**: Systematically using Edit/MultiEdit tools without Reading file content first
- **Impact**: Edit operations fail due to mismatched string content and formatting
- **Correction**: ALWAYS use Read tool before any Edit operations
- **Prevention**: Mandatory Read-then-Edit workflow protocol implemented in standards.md
- **Verification**: No edit operations allowed without prior Read confirmation
