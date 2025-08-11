# Global Scripts - Omar El Mountassir

**Purpose**: Automation utilities and helper scripts for Claude Code operations  
**Last Updated**: 2025-08-10  
**Scope**: Automation scripts applicable across all Claude Code projects and workflows  

---

## Script Categories

### System Automation

- **Backup Scripts**: Automated configuration backup and restoration
- **Cleanup Scripts**: Automated log cleanup and archive management  
- **Health Check Scripts**: System health monitoring and validation
- **Migration Scripts**: Architecture evolution and upgrade automation

### Development Automation

- **Setup Scripts**: New project initialization and configuration
- **Build Scripts**: Automated testing and quality gate execution
- **Deployment Scripts**: Automated deployment and integration
- **Documentation Scripts**: Automated documentation generation and updates

### Integration Automation

- **External System Scripts**: GitHub, MCP server, and tool integrations
- **Data Sync Scripts**: Cross-system data synchronization
- **Notification Scripts**: Automated status updates and alerts
- **Monitoring Scripts**: Performance and usage monitoring automation

### Maintenance Automation

- **Update Scripts**: Automated system and dependency updates
- **Validation Scripts**: Configuration and integrity validation
- **Recovery Scripts**: Automated recovery from common issues
- **Optimization Scripts**: Performance tuning and resource optimization

---

## Script Standards

### Development Standards

- **Language**: Python preferred, bash for simple operations
- **UV Integration**: All Python scripts use UV package management
- **Error Handling**: Comprehensive error handling and logging
- **Documentation**: Complete inline documentation and usage examples

### Execution Standards

- **Idempotent**: Scripts can be run multiple times safely
- **Atomic**: Operations complete fully or rollback completely
- **Logged**: All script execution logged to appropriate logs/ directory
- **Validated**: Script success validated before completion

### Security Standards

- **No Secrets**: No hardcoded secrets or credentials
- **Least Privilege**: Scripts request minimal required permissions
- **Audit Trail**: All script actions logged for security audit
- **Safe Defaults**: Default parameters prioritize safety over convenience

---

## Integration Patterns

### With Logs Infrastructure

- All scripts log execution to global/logs/system/
- Error conditions logged to global/logs/errors/
- Performance metrics captured for optimization

### With Configuration Modules

- Scripts respect configuration standards and policies
- Configuration changes validated against quality gates
- Scripts update configuration tracking in meta module

### With External Tools

- GitHub CLI integration for repository operations
- MCP server integration for external system access
- Claude Code CLI integration for AI operations
- UV integration for Python package management

---

## Script Organization

### Core Infrastructure (`scripts/core/`)

- System health and maintenance scripts
- Backup and recovery automation
- Configuration management scripts

### Development Workflow (`scripts/dev/`)

- Project setup and initialization
- Quality gate automation
- Testing and validation scripts

### Integration (`scripts/integration/`)

- External system integration scripts
- Data synchronization automation
- Cross-platform compatibility scripts

### Utilities (`scripts/utils/`)

- Helper functions and common utilities
- Shared libraries and modules
- Development and debugging tools

---

**Quality Gate**: All scripts must be tested in isolation before integration  
**Evolution**: Script library grows from repeated manual operations and identified automation opportunities
