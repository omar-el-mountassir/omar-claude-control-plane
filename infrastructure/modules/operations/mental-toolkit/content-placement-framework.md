# Content Placement Decision Framework

**Purpose**: Systematic framework for optimal placement of all generated content based on usage patterns and content lifecycle  
**Created**: 2025-08-11  
**Integration**: Mental Toolkit Framework specialized protocol  

---

## 🎯 **Core Philosophy: Usage-Based Placement**

**Principle**: Place content based on HOW it will be used and accessed, not just WHAT it is.

**Evidence**: Multi-framework analysis revealed current placement issues stem from storage-oriented rather than usage-oriented categorization.

---

## 🧠 **Content Lifecycle Model**

### **Stage 1: Creation** 
- **Location**: `temp/` for drafts and work-in-progress
- **Purpose**: Active development, experimentation, initial exploration
- **Duration**: Short-term (days to weeks)
- **Next Step**: Review for permanent placement

### **Stage 2: Integration**
- **Location**: Appropriate permanent category based on usage patterns
- **Purpose**: Content reviewed, refined, ready for reference and use
- **Duration**: Active period (weeks to months)
- **Next Step**: Regular access and potential evolution

### **Stage 3: Reference**
- **Location**: Stable permanent location with proper cross-references
- **Purpose**: Referenced by future instances and ongoing work
- **Duration**: Long-term (months to years)
- **Next Step**: Potential evolution or archival

### **Stage 4: Evolution/Archive**
- **Location**: Updated in place or moved to archive subdirectories
- **Purpose**: Content superseded, historical reference, or evolved form
- **Duration**: Indefinite
- **Next Step**: Maintain or eventual cleanup

---

## 📁 **Usage-Based Directory Semantics**

### **infrastructure/** - System Components
**Usage Pattern**: Referenced automatically by system, modified systematically
**Content Types**: 
- Configuration modules (core, standards, tech stack)
- Operational protocols (task management, continuity)
- System frameworks (mental toolkit, templates)
**Placement Criteria**: Content that defines HOW the system operates
**Access Pattern**: Loaded automatically, modified by design decisions

### **knowledge/** - Permanent Intellectual Assets  
**Usage Pattern**: Referenced for decision-making, built upon over time
**Content Types**:
- Strategic insights and analysis
- System discoveries and learnings
- Foundational context and frameworks
**Placement Criteria**: Content that provides UNDERSTANDING for future decisions
**Access Pattern**: Consulted before major decisions, expanded continuously

### **data/analysis/** - Completed Analytical Work
**Usage Pattern**: Referenced as evidence, input to other analysis, implementation guidance
**Content Types**:
- Technical evaluations and comparisons
- Architecture assessments and recommendations  
- Implementation specifications and plans
**Placement Criteria**: Content that provides EVIDENCE and GUIDANCE for implementation
**Access Pattern**: Referenced during implementation, cited in other work

### **sessions/** - Session-Specific Context
**Usage Pattern**: Historical record, pattern identification, context recovery
**Content Types**:
- Session documentation and outcomes
- Decision records and rationale
- Time-bound context and progress
**Placement Criteria**: Content tied to SPECIFIC timeframes and conversation contexts
**Access Pattern**: Reviewed for continuity, analyzed for patterns

### **projects/** - Workspace and Development
**Usage Pattern**: Active work area, iterative development, collaborative space
**Content Types**:
- Project-specific analysis and documentation
- Development workspaces and prototypes
- Project-scoped frameworks and tools
**Placement Criteria**: Content that supports ACTIVE PROJECT WORK
**Access Pattern**: Frequent modification during project lifecycle

### **temp/** - Work-in-Progress (Migration Required)
**Usage Pattern**: Temporary holding, draft development, experimental work
**Content Types**: ALL content types in draft/experimental form
**Placement Criteria**: Content NOT YET READY for permanent placement
**Access Pattern**: Active modification with planned migration to permanent location
**Critical Rule**: Content should NOT remain in temp/ - must migrate with clear timeline

---

## 🎯 **Placement Decision Tree**

### **Primary Classification Questions**

```
Generated Content →
│
├─ Does this define HOW the system operates?
│  └─ YES → infrastructure/modules/[category]/
│
├─ Does this provide UNDERSTANDING for future decisions?
│  └─ YES → knowledge/[insights|foundation]/
│
├─ Does this provide EVIDENCE or GUIDANCE for implementation?
│  └─ YES → data/analysis/
│
├─ Is this tied to SPECIFIC timeframes/conversation contexts?  
│  └─ YES → sessions/YYYY-MM-DD/
│
├─ Does this support ACTIVE PROJECT WORK?
│  └─ YES → projects/PROJECT-NAME/
│
└─ Is this NOT YET READY for permanent placement?
   └─ YES → temp/ (with migration plan)
```

### **Secondary Refinement Questions**

**For Each Category**:
1. **Will future Claude instances need this for similar tasks?** → Permanent placement required
2. **Is this building on existing content?** → Place near related content or cross-reference
3. **Does this need frequent access?** → Ensure discoverable location
4. **Will this evolve over time?** → Prefer locations that support versioning/updates

---

## ⚙️ **Decision Protocol Implementation**

### **Pre-Placement Assessment**

**Before Creating Any File**:
1. **Content Type Classification**: What kind of content is this?
2. **Usage Pattern Analysis**: How will this be accessed and used?
3. **Lifecycle Stage**: Is this draft, permanent, or evolving?
4. **Relationship Mapping**: What other content does this relate to?
5. **Future Instance Needs**: Will other Claude instances need this?

### **Systematic Decision Process**

```
Step 1: PRIMARY CLASSIFICATION
- System operation → infrastructure/
- Understanding provision → knowledge/  
- Evidence/guidance → data/analysis/
- Time-bound context → sessions/
- Active project work → projects/
- Not yet ready → temp/

Step 2: SECONDARY REFINEMENT  
- Identify specific subdirectory
- Check for related content
- Determine cross-reference needs
- Plan lifecycle transitions

Step 3: PLACEMENT EXECUTION
- Create file in determined location
- Add appropriate metadata/headers
- Create necessary cross-references  
- Document placement rationale if complex

Step 4: INTEGRATION VALIDATION
- Verify discoverability by future instances
- Confirm logical relationship to nearby content
- Test cross-references work correctly
- Update relevant index/navigation files
```

### **Common Placement Scenarios**

**Analysis Documents**:
- **Technical Analysis** → `data/analysis/technical-analysis-TOPIC-YYYY-MM-DD.md`
- **Strategic Analysis** → `knowledge/insights/strategic/strategic-analysis-TOPIC.md`  
- **System Analysis** → `knowledge/insights/system/` (if generates insights) OR `data/analysis/` (if implementation-focused)

**Framework/Protocol Documents**:
- **System Operation** → `infrastructure/modules/operations/FRAMEWORK-NAME/`
- **Decision Framework** → `infrastructure/modules/operations/mental-toolkit/FRAMEWORK-NAME.md`
- **Configuration Protocol** → `infrastructure/modules/config/PROTOCOL-NAME/`

**Implementation Plans**:
- **System Implementation** → `data/analysis/implementation-plan-SYSTEM-YYYY-MM-DD.md`
- **Project Implementation** → `projects/PROJECT-NAME/implementation/`
- **Quick Implementation** → Near related content with cross-references

**Verification/Audit Documents**:
- **System Verification** → `data/analysis/verification-SYSTEM-YYYY-MM-DD.md`  
- **Implementation Verification** → Same location as implementation being verified
- **Session Verification** → `sessions/YYYY-MM-DD/verification-TOPIC.md`

---

## 🔄 **Feedback and Optimization**

### **Placement Effectiveness Review**

**Post-Placement Questions** (Weekly Review):
1. **Can future instances easily find this content?**
2. **Does the placement support the intended usage pattern?**
3. **Are related contents appropriately linked?**
4. **Has this content been accessed as expected?**

### **Pattern Learning**

**Monthly Placement Analysis**:
- Which placements led to successful content reuse?
- What content became "homeless" or hard to find?
- Which categories are over/under-utilized?
- What placement decisions would I change in retrospect?

### **Framework Evolution**

**Quarterly Framework Review**:
- Update decision tree based on placement experience
- Refine directory semantics based on actual usage
- Add new categories if systematic gaps identified
- Improve integration with task management workflows

---

## 🎯 **Integration with Operations**

### **Task Management Integration**

**Pre-Task Content Planning**:
- Consider what content will be generated
- Plan placement strategy before creation
- Prepare cross-reference structure
- Identify content lifecycle expectations

**Post-Task Placement Review**:
- Validate all content placed optimally  
- Check cross-references work correctly
- Confirm discoverability for future instances
- Document any placement challenges for framework improvement

### **Quality Gates Integration**

**Content Placement Checklist**:
- [ ] **Placement Decision**: Applied systematic decision tree
- [ ] **Usage Optimization**: Placed based on how content will be used
- [ ] **Lifecycle Consideration**: Appropriate for current lifecycle stage
- [ ] **Cross-References**: All necessary links created and tested
- [ ] **Future Discovery**: Discoverable by future Claude instances
- [ ] **Integration**: Properly integrated with related content

---

## 📊 **Success Metrics**

### **Placement Quality Indicators**

**Good Placement Signs**:
- Content gets referenced/reused by future instances
- Location feels intuitive when searching for content
- Related content is easily discoverable nearby
- No confusion about where to find specific content types

**Poor Placement Signs**:  
- Content never gets referenced after creation
- Searching for content requires checking multiple locations
- Similar content scattered across different categories
- Uncertainty about where to place new content of similar type

### **System Health Metrics**

**Monthly Assessment**:
- **temp/ Health**: How much content stuck in temporary status?
- **Cross-Reference Integrity**: All links functional?
- **Category Balance**: Any categories becoming too large/complex?
- **Discovery Success**: Can standard content types be found quickly?

---

## 🚀 **Advanced Applications**

### **Content Migration Strategies**

**When Content Outgrows Category**:
1. **Analysis → Knowledge**: When analysis generates permanent insights
2. **temp/ → Permanent**: When drafts become finalized content  
3. **Project → Infrastructure**: When project tools become system tools
4. **Session → Data**: When session insights become general guidance

### **Cross-Reference Optimization**

**Strategic Linking**:
- Link from general to specific (knowledge/ → data/analysis/)
- Link related methodologies (mental toolkit components)
- Link evidence chains (analysis → implementation → verification)
- Link temporal sequences (session → outcome → integration)

### **Automated Placement Suggestions**

**Future Enhancement Opportunities**:
- Content type detection based on file content/structure
- Automatic suggestion of placement location
- Batch migration tools for content reorganization
- Placement effectiveness analytics and recommendations

---

## 📚 **Quick Reference**

### **Decision Shortcuts**

**System Operation** → `infrastructure/modules/`  
**Permanent Understanding** → `knowledge/`  
**Implementation Evidence** → `data/analysis/`  
**Time-Bound Context** → `sessions/`  
**Active Project Work** → `projects/`  
**Work-in-Progress** → `temp/` (migrate ASAP)

### **Common Patterns**

**New Framework** → `infrastructure/modules/operations/FRAMEWORK/`  
**Technical Analysis** → `data/analysis/TOPIC-analysis-YYYY-MM-DD.md`  
**System Discovery** → `knowledge/insights/system/README.md` (add section)  
**Strategic Insight** → `knowledge/insights/strategic/TOPIC-analysis.md`  
**Verification Document** → Same location as content being verified  

---

**Status**: Production Ready - Apply to all content generation  
**Integration**: Part of Mental Toolkit Framework systematic protocols  
**Next Evolution**: Usage analytics and automated placement optimization