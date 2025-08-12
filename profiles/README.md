# Profiles - Foundational Context Management

**Function**: Manages foundational context profiles and system specifications  
**Purpose**: Centralized storage for machine specifications, development environment, and user context  
**Replaces**: Former CONTEXT/ directory (renamed for functional naming compliance)  

---

## Directory Structure

```
profiles/
├── README.md          # This file
├── machine/           # Machine specifications and capabilities
└── development/       # Development environment and preferences
```

## Contents

### machine/
Technical specifications, performance characteristics, installed software, system capabilities

### development/  
Development environment setup, tool preferences, workflow configurations, collaboration patterns

---

## Integration

This directory supports all Claude Code operations by providing foundational context that informs:
- Tool selection and configuration
- Performance optimization decisions  
- Development workflow customization
- Collaboration pattern optimization

**Usage Pattern**: Referenced during session startup and context recovery for environment-aware decision making.