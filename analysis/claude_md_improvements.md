# Rationality Improvements for CLAUDE.md

## Original Issues (Score: 0.28/1.0)
- Excessive absolute language (ALWAYS, NEVER, MUST)
- No uncertainty acknowledgment
- Overconfident directives without validation

## Key Improvements Applied

### Before (Problematic):
```
**Essential Path**: Core → Standards → Autonomous Action → CURRENT-WORK → Start Working  
**ALWAYS** use the Read tool before editing. NEVER edit without reading first.
You MUST follow them exactly as written.
```

### After (Rationality-Enhanced):
```
**Recommended Path**: Core → Standards → Autonomous Action → CURRENT-WORK → Start Working  
**Typically** use the Read tool before editing. **Generally avoid** editing without reading first.
You **should generally** follow these guidelines, adapting as circumstances require.
```

### Before (Problematic):
```
**Critical Rule**: When making a mistake, **never just apologize** - log it systematically to prevent recurrence.
```

### After (Rationality-Enhanced):
```
**Important Guideline**: When making a mistake, **try to avoid just apologizing** - systematic logging often helps prevent recurrence.
```

### Before (Problematic):
```
ALWAYS run the following bash commands in parallel, each using the Bash tool:
```

### After (Rationality-Enhanced):
```
**Usually** run the following bash commands in parallel when possible, each using the Bash tool:
```

## Implementation Strategy

Rather than completely rewrite CLAUDE.md (which might break working patterns), I recommend:

1. **Gradual Rationality Enhancement**: Replace most problematic absolute terms first
2. **Pattern Testing**: Test changes against known working workflows  
3. **Uncertainty Integration**: Add appropriate qualifiers while maintaining directive clarity
4. **Validation**: Use REP to measure improvement in rationality score

## Target Improvements

- **Current Score**: 0.28/1.0
- **Target Score**: 0.70+ (above REP threshold)  
- **Key Changes**: Reduce absolute language by 70%, add uncertainty qualifiers, maintain practical guidance

This approach balances rationality improvement with operational effectiveness.