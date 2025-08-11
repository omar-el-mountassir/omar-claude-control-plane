#!/usr/bin/env python3
"""
Claude Code Session Setup Script
Creates session directory structure with templates
"""

import os
import sys
from pathlib import Path
import datetime

# Add path for shared utilities
sys.path.append(str(Path(__file__).parent))
from claude_utils import get_claude_dir


def setup_session(date_str=None):
    """Create session directory with complete template structure"""
    
    if date_str is None:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    claude_dir = get_claude_dir()
    sessions_dir = claude_dir / "sessions"
    session_dir = sessions_dir / date_str
    
    print(f"🚀 Setting up session directory: {date_str}")
    print("=" * 50)
    
    try:
        # Create session directory
        session_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {session_dir}")
        
        # Create session index
        create_session_index(session_dir, date_str)
        print("📋 Created: session-index.md")
        
        # Create core session files
        session_files = [
            ("metadata.md", get_metadata_template(date_str)),
            ("architectural-transformation.md", get_architecture_template()),
            ("critical-insights.md", get_insights_template()),
            ("implementation-details.md", get_implementation_template())
        ]
        
        for filename, content in session_files:
            file_path = session_dir / filename
            file_path.write_text(content)
            print(f"📄 Created: {filename}")
        
        print(f"\n✅ Session setup completed!")
        print(f"📂 Session directory: {session_dir}")
        print(f"🎯 Start with: session-index.md")
        
        return session_dir
        
    except Exception as e:
        print(f"❌ Session setup failed: {e}")
        return None

def create_session_index(session_dir, date_str):
    """Create session index file"""
    
    content = f"""# Session Index - {date_str}

**Session Type**: _[Describe session type and focus]_  
**Duration**: _[Session duration]_  
**Outcome**: _[Primary outcomes and achievements]_  
**Confidence**: _[Confidence level in results]_  

---

## Session Modules

### Core Documentation
- **[Metadata](./metadata.md)** - Technical environment and session characteristics
- **[Architectural Transformation](./architectural-transformation.md)** - Architecture changes and evolution
- **[Critical Insights](./critical-insights.md)** - Key learnings and strategic patterns
- **[Implementation Details](./implementation-details.md)** - Technical implementation and validation

### Analysis Archives  
- **[Evolution Analysis](./evolution-analysis.md)** - Decision frameworks and analysis _[Create if needed]_
- **[Quality Assessment](./quality-assessment.md)** - Architecture review and ratings _[Create if needed]_

### Session Continuity
- **[Next Session Roadmap](./NEXT-SESSION-ROADMAP.md)** - Continuation guide _[Create if major work]_

---

## Session Achievements

### Major Changes
1. _[List significant changes made]_
2. _[Architecture or system improvements]_
3. _[New implementations or patterns]_

### Quality Improvements
- _[Quality gates and standards applied]_
- _[Error prevention or lessons learned]_
- _[Knowledge preservation activities]_

### Knowledge Preservation
- _[Architectural intelligence captured]_
- _[Decision records with rationale]_
- _[Reusable patterns or templates created]_

---

## Strategic Value

### Immediate Benefits
- _[Immediate improvements or capabilities]_
- _[System reliability or efficiency gains]_
- _[Development velocity improvements]_

### Long-term Impact
- _[Strategic architectural improvements]_
- _[Knowledge and learning preservation]_
- _[Foundation for future work]_

---

## Next Steps Framework

### Phase Continuation
- [ ] _[Immediate next actions]_
- [ ] _[Validation and testing needs]_
- [ ] _[Integration requirements]_

### Future Sessions
- [ ] _[Planned follow-up work]_
- [ ] _[Advanced features or optimization]_
- [ ] _[Strategic direction items]_

---

**Session Status**: _[Current status]_  
**Knowledge Preservation**: _[Level of documentation completeness]_  
**Reproducibility**: _[Ability for future sessions to continue]_
"""
    
    index_path = session_dir / "session-index.md"
    index_path.write_text(content)

def get_metadata_template(date_str):
    """Generate metadata template"""
    return f"""# Session Metadata - {date_str}

**Creation Date**: {date_str}  
**Session Type**: _[Implementation/Analysis/Planning/Architecture/etc.]_  
**Primary Focus**: _[Main objectives and scope]_  

---

## Technical Environment

### Claude Code Configuration
- **Version**: 3.0
- **Architecture**: Five-category semantic system + full infrastructure
- **Global Directory**: `~/.claude/global/`
- **Module System**: config, operations, memory, knowledge, meta

### System Information
- **Platform**: Windows (MINGW64)
- **Claude Model**: Sonnet 4 (claude-sonnet-4-20250514)
- **Tools Available**: UV package manager, Git, GitHub CLI
- **Working Directory**: `C:\\Users\\omarm\\.claude`

---

## Session Characteristics

### Session Goals
- **Primary Objective**: _[What is the main goal?]_
- **Success Criteria**: _[How do we measure success?]_
- **Quality Gates**: _[What standards must be met?]_

### Context and Dependencies
- **Previous Session**: _[Reference to previous relevant session]_
- **Dependencies**: _[What must be in place for this session?]_
- **Assumptions**: _[Key assumptions being made]_

### Scope and Limitations
- **In Scope**: _[What will be addressed]_
- **Out of Scope**: _[What will not be addressed]_
- **Time Constraints**: _[Any time limitations]_

---

## Quality Framework

### Standards Applied
- **Read-Before-Edit**: Mandatory file editing protocol
- **Documentation**: Complete decision and implementation documentation
- **Testing**: Validation of all implementations
- **Error Logging**: Systematic error capture and prevention

### Validation Methods
- **Architecture Health**: Health check script validation
- **Reference Integrity**: @ reference resolution validation
- **Version Consistency**: Cross-component version alignment
- **Implementation Testing**: Functional testing of all changes

---

**Metadata Completeness**: Complete  
**Session Tracking**: Full documentation and continuity support  
**Quality Assurance**: All quality gates and standards applied
"""

def get_architecture_template():
    """Generate architecture template"""
    return """# Architectural Transformation - Session

**Purpose**: Document architectural changes and evolution  
**Scope**: All architecture modifications and their rationale  
**Integration**: Links to global architecture intelligence  

---

## Architecture Changes

### Overview
- **From**: _[Starting architecture state]_
- **To**: _[Ending architecture state]_
- **Rationale**: _[Why these changes were needed]_

### Specific Modifications
1. **Change 1**: _[Description and rationale]_
2. **Change 2**: _[Description and rationale]_
3. **Change 3**: _[Description and rationale]_

---

## Decision Framework

### Analysis Process
- **Decision Method**: _[How decisions were made]_
- **Alternatives Considered**: _[What alternatives were evaluated]_
- **Selection Criteria**: _[How final choice was determined]_

### Scoring and Evaluation
- **Option 1**: _[Score and rationale]_
- **Option 2**: _[Score and rationale]_
- **Selected Option**: _[Score and rationale]_

---

## Implementation Impact

### Immediate Effects
- **System Changes**: _[What changed immediately]_
- **Performance Impact**: _[Any performance implications]_
- **Compatibility**: _[Backward compatibility considerations]_

### Strategic Implications
- **Future Flexibility**: _[How this enables future work]_
- **Architecture Debt**: _[Any technical debt implications]_
- **Maintenance**: _[Ongoing maintenance requirements]_

---

## Validation and Quality

### Architecture Health
- **Pre-Change**: _[Architecture state before changes]_
- **Post-Change**: _[Architecture state after changes]_
- **Health Check Results**: _[Results of validation]_

### Integration Testing
- **@ Reference Validation**: _[Reference resolution testing]_
- **Module Integration**: _[Cross-module integration testing]_
- **Functional Testing**: _[End-to-end functionality testing]_

---

**Architecture Confidence**: _[Level of confidence in changes]_  
**Evolution Quality**: _[Assessment of evolution process]_  
**Strategic Alignment**: _[Alignment with long-term architectural vision]_
"""

def get_insights_template():
    """Generate insights template"""
    return """# Critical Insights - Session

**Purpose**: Key learnings, breakthrough realizations, and strategic patterns  
**Strategic Value**: High-value insights for future reference and application  
**Integration**: Feeds into global knowledge and architectural intelligence  

---

## Breakthrough Insights

### 1. [Insight Category]

**Key Discovery**: _[What was discovered or realized]_  

**Evidence/Process**: _[How this insight was discovered]_  

**Strategic Implication**: _[Why this matters for future work]_  

**Application Pattern**: _[How to apply this insight]_

### 2. [Insight Category]

**Key Discovery**: _[What was discovered or realized]_  

**Evidence/Process**: _[How this insight was discovered]_  

**Strategic Implication**: _[Why this matters for future work]_  

**Application Pattern**: _[How to apply this insight]_

---

## Decision-Making Intelligence

### Process Insights
- **What Worked**: _[Successful decision-making approaches]_
- **What Didn't**: _[Less effective approaches]_
- **Improvements**: _[How to improve decision-making]_

### Pattern Recognition
- **Recurring Themes**: _[Patterns observed across decisions]_
- **Success Indicators**: _[Signs of good decisions]_
- **Warning Signs**: _[Signs of problematic decisions]_

---

## Implementation Excellence

### Quality Patterns
- **Effective Practices**: _[What led to high-quality implementations]_
- **Error Prevention**: _[What prevented errors effectively]_
- **Efficiency Gains**: _[What made work more efficient]_

### Learning Integration
- **Knowledge Gaps**: _[Areas where learning was needed]_
- **Skill Development**: _[Capabilities that improved]_
- **Process Refinement**: _[How processes were improved]_

---

## Strategic Pattern Recognition

### Architecture Patterns
- **Successful Patterns**: _[Architectural approaches that worked]_
- **Anti-Patterns**: _[Approaches to avoid]_
- **Evolution Patterns**: _[How architecture should evolve]_

### Workflow Patterns
- **Effective Workflows**: _[Work approaches that succeeded]_
- **Optimization Opportunities**: _[Areas for workflow improvement]_
- **Automation Potential**: _[Work that could be automated]_

---

## Future Application Guidelines

### For Next Sessions
1. _[Specific guidance for immediate future work]_
2. _[Process improvements to implement]_
3. _[Quality standards to maintain]_

### For Strategic Decisions
1. _[Long-term strategic guidance]_
2. _[Architectural decision principles]_
3. _[Risk mitigation approaches]_

---

**Insight Confidence**: _[Confidence level in insights]_  
**Strategic Value**: _[Assessment of strategic importance]_  
**Knowledge Integration**: _[How insights integrate with existing knowledge]_
"""

def get_implementation_template():
    """Generate implementation template"""
    return """# Implementation Details - Session

**Purpose**: Technical implementation steps, validation, and quality assurance  
**Scope**: All technical work performed and its validation  
**Quality**: Complete implementation documentation for reproducibility  

---

## Implementation Summary

### Overview
- **Total Files Modified**: _[Number of files changed]_
- **Total Files Created**: _[Number of new files]_
- **Architecture Changes**: _[High-level changes made]_
- **Quality Gates**: _[Quality standards applied]_

### Success Metrics
- **All Implementations Successful**: _[Yes/No with details]_
- **Quality Gates Passed**: _[Specific validations completed]_
- **Error Rate**: _[Number of errors encountered and resolved]_

---

## Detailed Implementation Steps

### Phase 1: _[Implementation Phase Name]_

#### Changes Made
1. **File**: `_[file path]_`
   - **Action**: _[Created/Modified/Moved]_
   - **Purpose**: _[Why this change was needed]_
   - **Content**: _[Description of content changes]_

2. **File**: `_[file path]_`
   - **Action**: _[Created/Modified/Moved]_
   - **Purpose**: _[Why this change was needed]_
   - **Content**: _[Description of content changes]_

#### Validation Results
- **Quality Check**: _[Validation method and results]_
- **Testing**: _[Testing performed and outcomes]_
- **Integration**: _[Integration testing results]_

### Phase 2: _[Implementation Phase Name]_

#### Changes Made
1. **File**: `_[file path]_`
   - **Action**: _[Created/Modified/Moved]_
   - **Purpose**: _[Why this change was needed]_
   - **Content**: _[Description of content changes]_

#### Validation Results
- **Quality Check**: _[Validation method and results]_
- **Testing**: _[Testing performed and outcomes]_

---

## Technical Validation

### Architecture Health Check
- **Pre-Implementation**: _[Architecture state before changes]_
- **Post-Implementation**: _[Architecture state after changes]_
- **Health Check Results**: _[Complete health check output]_

### Quality Gate Compliance
- **Read-Before-Edit**: _[Compliance with mandatory protocol]_
- **Version Consistency**: _[Version alignment verification]_
- **Reference Integrity**: _[@ reference resolution validation]_
- **Documentation Standards**: _[Documentation quality verification]_

### Functional Testing
- **Script Testing**: _[All scripts tested and results]_
- **Template Testing**: _[Template validation results]_
- **Integration Testing**: _[Cross-component integration results]_

---

## Error Management

### Errors Encountered
1. **Error**: _[Description of error]_
   - **Resolution**: _[How it was resolved]_
   - **Prevention**: _[How to prevent in future]_

2. **Error**: _[Description of error]_
   - **Resolution**: _[How it was resolved]_
   - **Prevention**: _[How to prevent in future]_

### Error Prevention Applied
- **Protocols Used**: _[Which error prevention protocols were applied]_
- **Quality Gates**: _[Quality gates that prevented errors]_
- **Validation Methods**: _[Validation approaches that caught issues]_

---

## Performance and Optimization

### Implementation Efficiency
- **Time to Complete**: _[Actual time spent vs estimated]_
- **Error Rate**: _[Number of errors per implementation step]_
- **Rework Required**: _[Amount of rework needed]_

### System Performance
- **Backup Performance**: _[Backup script execution time and size]_
- **Health Check Performance**: _[Health check execution time]_
- **Overall System**: _[General system performance observations]_

---

## Reproducibility Documentation

### Complete File List
```
_[List all files created or modified with their purposes]_
```

### Command Sequence
```bash
_[Complete sequence of commands that could reproduce this work]_
```

### Dependencies Required
- **System Requirements**: _[Required system components]_
- **Tool Requirements**: _[Required development tools]_
- **Configuration Requirements**: _[Required configuration states]_

---

**Implementation Confidence**: _[Confidence in implementation quality]_  
**Reproducibility**: _[Ability to reproduce this implementation]_  
**Technical Quality**: _[Assessment of technical implementation quality]_
"""

def main():
    """Main entry point with input validation."""
    import sys
    import re
    
    # Parse and validate arguments
    if len(sys.argv) > 2:
        print("Usage: python session-setup.py [YYYY-MM-DD]")
        print("  YYYY-MM-DD: Optional date in ISO format (default: today)")
        sys.exit(1)
    
    date_str = None
    if len(sys.argv) == 2:
        date_str = sys.argv[1].strip()
        
        # Validate date format if provided
        if date_str and not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            print("❌ Error: Date must be in YYYY-MM-DD format")
            print("   Example: python session-setup.py 2025-08-11")
            sys.exit(1)
        
        # Validate date is reasonable (not too far in past/future)
        try:
            from datetime import datetime, timedelta
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now()
            
            if parsed_date > today + timedelta(days=365):
                print("❌ Error: Date cannot be more than 1 year in the future")
                sys.exit(1)
            elif parsed_date < today - timedelta(days=3650):  # 10 years
                print("❌ Error: Date cannot be more than 10 years in the past")
                sys.exit(1)
                
        except ValueError:
            print("❌ Error: Invalid date format")
            print("   Example: python session-setup.py 2025-08-11")
            sys.exit(1)
    
    # Execute session setup
    try:
        setup_session(date_str)
    except KeyboardInterrupt:
        print("\n⚠️  Session setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during session setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()