# Commit Workflow Rules

**Rule Type**: Workflow Enforcement  
**Priority**: CRITICAL - Mandatory workflow sequence  

---

## Workflow Rules (Strict Order)

### Mandatory Workflow Enforcement

#### ❌ **NEVER** Rules
- **NEVER commit without applying all three fixes first**
- **NEVER skip smoke-testing in sandbox**
- **NEVER push without explicit confirmation**
- **NEVER bypass quality validation steps**

#### ✅ **ALWAYS** Rules
- **ALWAYS run smoke-test in sandbox after fixes**
- **ALWAYS commit with proper message format**
- **ALWAYS ask for confirmation before pushing**
- **ALWAYS validate success before proceeding**

#### ⚠️ **CONFIRMATION** Rules
- **Wait for explicit confirmation before pushing**
- **Confirm smoke-test results are acceptable**
- **Verify commit message meets standards**

---

## Workflow Sequence (Mandatory)

```bash
1. Apply Three-Fix Protocol (see three-fix-protocol.md)
2. Stage relevant files only
3. Run smoke-test in sandbox
4. Commit with proper message
5. ASK before pushing
```

---

## Quality Assurance

- **No shortcuts allowed** - Full workflow every time
- **Validation required** at each step
- **Manual confirmation** for destructive operations
- **Documentation** of any workflow deviations

---

## Enforcement Priority

**HIGHEST PRIORITY**: These rules override all other commit considerations