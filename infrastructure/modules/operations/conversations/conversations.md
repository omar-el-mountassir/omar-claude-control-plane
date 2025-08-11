# Conversations Configuration - Omar El Mountassir

**Module**: Conversation Management & Context Protocols  
**Last Updated**: 2025-08-10  
**Scope**: Conversation-level patterns applicable across all Claude Code sessions  

---

## Conversation Types & Classification

### Technical Analysis Conversations
- **Purpose**: Deep technical investigation and evaluation
- **Protocol**: Use TodoWrite for complex multi-step analysis
- **Documentation**: Always generate final deliverable documents
- **Quality Gate**: Verify implementation before documenting

### Implementation Conversations  
- **Purpose**: Building, modifying, or fixing code
- **Protocol**: Follow Read-before-Edit mandatory workflow
- **Testing**: Run linting and type checking before completion
- **Standards**: Adhere to project conventions and existing patterns

### Planning & Architecture Conversations
- **Purpose**: System design and strategic decisions
- **Protocol**: Create structured documentation before implementation
- **Validation**: Research official documentation sources first
- **Output**: Always create reusable templates and patterns

### Learning & Error Recovery Conversations
- **Purpose**: Understanding failures and preventing recurrence
- **Protocol**: Log errors systematically using established template
- **Integration**: Update relevant config modules with learnings
- **Verification**: Test prevention protocols before documenting

---

## Context Management Protocols

### Session Continuity
- **Memory Preservation**: Use `/compact` at natural breakpoints
- **Context Switching**: Use `/clear` for completely different tasks
- **Reference Management**: Use `@` syntax for specific file/directory work
- **Quick Notes**: Use `#` shortcut for immediate memory additions

### Multi-Conversation Projects
- **State Tracking**: Document progress across conversations
- **Dependency Management**: Track inter-conversation dependencies
- **Context Handoff**: Provide clear status for continuation
- **Quality Assurance**: Maintain standards across conversation boundaries

---

## Communication Patterns

### Language Standards Integration
- **Primary Language**: English for technical content (per core.md)
- **Consistency Rule**: No language mixing within technical sections
- **Documentation**: All conversation outputs follow language standards

### Response Protocols
- **Conciseness**: Minimize output tokens while maintaining quality
- **Directness**: Answer specific queries without unnecessary elaboration
- **Tool Usage**: Batch tool calls for optimal performance
- **Proactiveness**: Take appropriate actions when requested

---

## Decision Support Patterns

### **Work Prioritization Decision Framework**

**When uncertain about what to work on**:

1. **< 30 minutes available**: Choose from Smart Quick Wins (see CURRENT-WORK.md)
2. **30-90 minutes available**: Work on Primary Focus from CURRENT-WORK.md
3. **> 90 minutes available**: Complete Primary Focus + 1 Quick Win  
4. **New session**: Follow Session Startup Guide in operations/continuity

### **Blocking Situation Protocols**

**When blocked on primary focus**:

1. **Switch to alternative task** from current context stack
2. **Log the blocker** using systematic logging system  
3. **Continue with next highest priority** task from queue
4. **Document blocking pattern** for future prevention

### **New Work Integration Protocols**

**When adding new work to system**:

1. **Urgent/Blocking**: Add to current P1 priorities immediately
2. **Important/Non-urgent**: Add to P2 queue with RICE assessment
3. **Nice-to-have**: Add to P3 with proper complexity evaluation
4. **Always**: Apply MoSCoW + RICE analysis for proper prioritization

### **Energy-Task Matching Guidelines**

**Decision support for energy optimization**:

- **High Energy Available**: Tackle complex P1 tasks, deep architecture work
- **Medium Energy Available**: Handle P2 implementation, documentation, CI/CD setup  
- **Low Energy Available**: Focus on Quick Wins, organization, planning, admin tasks

### **Context Switching Decision Rules**

**When to switch contexts vs continue**:

- **Stay in Context**: When tasks are related and switching cost is high
- **Switch Context**: When blocked, energy mismatch, or time constraint changes
- **Context Stacking**: Group related tasks to minimize switching overhead
- **Energy Matching**: Switch to energy-appropriate tasks when energy changes

---

**Next Review**: Monitor conversation patterns and update protocols as needed  
**Integration**: All conversation protocols must align with core philosophy and standards