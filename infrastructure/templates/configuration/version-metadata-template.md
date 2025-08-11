---
version: "0.1.0"
compatibility: ">=0.1.0"
last_updated: 2025-08-11
module_type: infrastructure
stability: stable
component: template
created: 2025-08-11
author: claude
description: "Standardized YAML frontmatter template for all Claude Code modules and components"
---

# Version Metadata Template

**Purpose**: Standardized YAML frontmatter template for all Claude Code modules and components  
**Version**: 0.1.0  
**Compliance**: SemVer 2.0.0  
**Created**: 2025-08-11  

---

## **Standard Metadata Format**

```yaml
---
# Core Version Information
version: "MAJOR.MINOR.PATCH[-prerelease][+build]"
compatibility: ">=X.Y.Z"
last_updated: YYYY-MM-DD

# Classification
module_type: configuration|knowledge|infrastructure|operations|memory|meta
stability: stable|beta|alpha|experimental
component: module|template|script|analysis|insight

# Dependencies (if applicable)
dependencies:
  - core: ">=3.1.0"
  - standards: ">=3.1.0"
  
# Metadata
created: YYYY-MM-DD
author: human|claude|collaborative
description: "Brief description of module purpose"
---
```

---

## **Version Format Specifications**

### **Version Components**
- **MAJOR**: Breaking changes, fundamental architecture shifts
- **MINOR**: New features, significant additions, structural improvements
- **PATCH**: Bug fixes, small improvements, configuration updates
- **prerelease**: `-alpha.N`, `-beta.N`, `-rc.N` for testing versions
- **build**: `+YYYYMMDD` or `+build.N` for development builds

### **Stability Levels**
- **stable**: Production-ready, extensively tested
- **beta**: Feature-complete, undergoing final testing
- **alpha**: Experimental, may have breaking changes
- **experimental**: Research/prototype, not for production use

### **Module Types**
- **configuration**: Core system configuration and rules
- **knowledge**: Reference materials, insights, research
- **infrastructure**: System tools, scripts, operational support
- **operations**: Behavioral patterns, workflows
- **memory**: Learning systems, error tracking
- **meta**: System self-reflection, architecture analysis

### **Component Types**
- **module**: Complete functional component
- **template**: Reusable pattern or structure
- **script**: Automation or utility tool
- **analysis**: Research output or evaluation
- **insight**: Knowledge capture or learning

---

## **Usage Examples**

### **Stable Configuration Module**
```yaml
---
version: "0.1.0"
compatibility: ">=0.1.0"
last_updated: 2025-08-11
module_type: configuration
stability: stable
component: module
dependencies:
  - core: ">=0.1.0"
created: 2025-08-10
author: collaborative
description: "Core philosophy and learning protocols"
---
```

### **Draft Knowledge Component**
```yaml
---
version: "0.1.0-alpha.1"
compatibility: ">=0.1.0"
last_updated: 2025-08-11
module_type: knowledge
stability: alpha
component: insight
created: 2025-08-11
author: claude
description: "Experimental AI workflow optimization patterns"
---
```

### **Infrastructure Script**
```yaml
---
version: "0.2.0"
compatibility: ">=0.1.0"
last_updated: 2025-08-11
module_type: infrastructure
stability: stable
component: script
dependencies:
  - core: ">=0.1.0"
created: 2025-08-08
author: human
description: "Configuration health checking and validation"
---
```

---

## **Implementation Guidelines**

### **For Existing Modules**
1. Add metadata to all `.md` files in infrastructure/modules/
2. Version according to stability and testing level
3. Set compatibility based on dependencies
4. Use collaborative authorship for human-AI work

### **For New Components**
1. Start with `0.1.0-alpha.1` for drafts
2. Progress through `0.1.0-beta.1` → `0.1.0-rc.1` → `1.0.0`
3. Follow stability progression: experimental → alpha → beta → stable
4. Document dependencies and compatibility requirements

### **Version Progression Rules**
- **Alpha**: Internal testing, rapid iteration
- **Beta**: External validation, feature freeze
- **RC**: Release candidate, final testing
- **Stable**: Production deployment

---

## **Health Check Integration**

The health check script validates:
- ✅ Version format compliance (SemVer 2.0)
- ✅ Compatibility range validity
- ✅ Required metadata presence
- ✅ Dependency version consistency
- ✅ Date format compliance

---

**Template Version**: 1.0.0  
**Next Review**: When SemVer 2.0 standards evolve or new metadata needs emerge