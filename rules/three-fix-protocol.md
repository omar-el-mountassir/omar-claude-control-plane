# Three-Fix Protocol

**Rule Type**: Pre-Commit Mandatory  
**Priority**: CRITICAL - Must be applied before ANY commit  

---

## Protocol Requirements

### Always Apply Before Any Commit (No Exceptions)

#### 1. Normalize Line Endings
- **Check**: Scan all files for line ending inconsistencies
- **Fix**: Ensure platform-appropriate line endings across codebase
- **Command**: `git config core.autocrlf true` (Windows)
- **Validation**: No mixed line endings in staged files

#### 2. Align @next/mdx with Next 14.2.5
- **Check**: Verify MDX dependencies match Next.js version compatibility
- **Fix**: Update package versions for proper compatibility
- **Validation**: Package.json shows compatible versions
- **Test**: MDX compilation works without errors

#### 3. Ignore Noisy Local Files
- **Check**: Scan staging area for development artifacts
- **Fix**: Update .gitignore to exclude unwanted files
- **Clean**: Remove noisy files from staging area
- **Validation**: Only intended files in staging

---

## Enforcement Rules

- ❌ **NEVER PROCEED** to commit without completing all three fixes
- ✅ **ALWAYS VERIFY** each fix is properly applied
- 🔍 **VALIDATE SUCCESS** before moving to next step

---

## Success Criteria

- [ ] Normalize line endings across all files
- [ ] Align @next/mdx with Next 14.2.5
- [ ] Remove noisy local files from staging area
- [ ] Validate and confirm all fixes working