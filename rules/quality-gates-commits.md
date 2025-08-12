# Quality Gates for Commits

**Rule Type**: Quality Assurance Gates  
**Priority**: CRITICAL - Mandatory validation checkpoints  

---

## Standard Pre-Commit Sequence

### Phase 1: Three-Fix Application
```bash
1. Apply three fixes (see three-fix-protocol.md)
   ✓ Normalize line endings
   ✓ Align @next/mdx with Next 14.2.5  
   ✓ Ignore noisy local files
```

### Phase 2: Staging and Validation
```bash
2. git add [relevant files]
   ✓ Only intended files staged
   ✓ No unwanted artifacts included
   ✓ All necessary changes captured
```

### Phase 3: Testing Gate
```bash
3. Smoke-test sandbox
   ✓ Application starts without errors
   ✓ Core functionality works
   ✓ No breaking changes introduced
```

### Phase 4: Commit Gate  
```bash
4. git commit with proper message
   ✓ Message follows established format
   ✓ Describes changes clearly
   ✓ Includes context and rationale
```

### Phase 5: Push Confirmation
```bash
5. Ask before git push
   ✓ User explicitly confirms push
   ✓ Remote repository impact understood
   ✓ No destructive operations without consent
```

---

## Quality Gate Criteria

### Gate 1: Fix Validation
- [ ] Apply all three fixes successfully
- [ ] Resolve conflicts or errors in application
- [ ] Verify changes are working

### Gate 2: Staging Validation  
- [ ] Stage only intended files
- [ ] Exclude sensitive or unwanted files
- [ ] Capture all necessary changes

### Gate 3: Testing Validation
- [ ] Pass smoke-test in sandbox
- [ ] Detect no breaking changes
- [ ] Confirm core functionality working

### Gate 4: Commit Validation
- [ ] Meet commit message standards
- [ ] Document changes properly
- [ ] Include context and rationale

### Gate 5: Push Authorization
- [ ] Get user explicit approval for push
- [ ] Complete impact assessment
- [ ] Avoid destructive operations without consent

---

## Gate Failure Protocol

**If ANY gate fails:**
1. **STOP** the commit process immediately
2. **REPORT** the specific failure
3. **FIX** the issue completely  
4. **RESTART** from the failed gate
5. **VALIDATE** all subsequent gates

---

## Success Criteria

**ALL gates must pass** before any commit operation completes