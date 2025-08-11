# MCP Capability Inventory - Quick Reference

**Purpose**: Fast lookup of specialized MCP server capabilities for systematic tool selection  
**Last Updated**: 2025-08-11  
**Usage**: Check this BEFORE selecting tools for any domain-specific tasks  

---

## 📂 **Filesystem Operations** → `mcp__filesystem`

### **Why Use MCP Version**
- **Bulk Operations**: Read/write multiple files simultaneously
- **Advanced Permissions**: Proper permission handling and security
- **Tree Operations**: Directory tree visualization and manipulation
- **Pattern Matching**: Advanced search with exclusion patterns
- **Atomic Operations**: Safe, transactional file operations

### **Core Capabilities**
- `read_file` - Single file reading with encoding detection
- `read_multiple_files` - Bulk file reading (efficient for analysis)
- `write_file` - Safe file writing with proper encoding
- `edit_file` - Line-based editing with git-style diff output
- `create_directory` - Directory creation with nested support
- `list_directory` - Enhanced directory listing with file/dir distinction
- `directory_tree` - JSON tree structure with recursive visualization
- `move_file` - Safe file/directory moving and renaming
- `search_files` - Pattern-based search with exclusion capabilities
- `get_file_info` - Detailed metadata (size, permissions, timestamps)

### **When to Use MCP Instead of Generic**
- ✅ **Multi-file operations** (reading/writing multiple files)
- ✅ **Directory analysis** (tree structures, bulk operations)
- ✅ **Advanced search** (pattern matching with exclusions)
- ✅ **Permission-sensitive operations** (security considerations)
- ✅ **Bulk analysis** (processing multiple files systematically)

### **Use Generic When**
- Single file read/write with no special requirements
- Simple directory listing without tree structure needed

---

## 🌐 **Web Content** → `mcp__fetch`

### **Why Use MCP Version**
- **Image Processing**: Automatic image extraction and processing
- **Content Optimization**: Markdown conversion, content cleaning
- **Caching**: Built-in 15-minute cache for repeated requests
- **Robots.txt Handling**: Respects and can override robots.txt restrictions
- **File Saving**: Automatic saving to organized directory structure

### **Core Capabilities**
- **Enhanced Content Fetching**: URL content with markdown conversion
- **Image Processing**: Extract, merge, resize, and optimize images
- **Pagination Support**: Handle large content with start indices
- **Quality Control**: JPEG quality settings, size optimization
- **Local Storage**: Save processed content to ~/Downloads/mcp-fetch/
- **Base64 Support**: Return base64 for AI display (Claude Desktop)

### **Advanced Features**
- **Image Merging**: Multiple images combined into single JPEG
- **Animation Handling**: GIF to static image conversion
- **Dimension Control**: Maximum width/height settings
- **Batch Processing**: Process multiple images with pagination
- **Format Optimization**: Automatic format selection and compression

### **When to Use MCP Instead of Generic**
- ✅ **Image-heavy pages** (automatic image processing)
- ✅ **Content analysis** (markdown conversion, cleaning)
- ✅ **Repeated fetching** (caching benefits)
- ✅ **Documentation generation** (file saving capabilities)
- ✅ **Visual content** (image extraction and optimization)

### **Use Generic When**
- Simple text-only page fetching
- Quick one-off content lookup without processing needs

---

## 🐙 **GitHub Operations** → `mcp__github`

### **Why Use MCP Version**
- **Atomic Operations**: Proper API usage with transaction safety
- **Batch Processing**: Multiple file operations in single commits
- **Full API Coverage**: Complete GitHub API access
- **State Management**: Proper handling of repository state
- **Authentication**: Secure credential management

### **Core Capabilities**
- `create_repository` - Repository creation with full configuration
- `get_file_contents` - File/directory content retrieval
- `create_or_update_file` - Single file operations with commit handling
- `push_files` - Multiple files in single commit (atomic)
- `create_issue` - Issue creation with full metadata
- `create_pull_request` - PR creation with advanced options
- `fork_repository` - Repository forking to account/organization
- `create_branch` - Branch creation from any source branch
- `list_commits` - Commit history with pagination
- `search_repositories` - Advanced repository search
- `search_code` - Cross-repository code search
- `search_issues` - Advanced issue/PR search
- `merge_pull_request` - PR merging with method selection

### **Advanced Operations**
- `get_pull_request_files` - PR file change analysis
- `create_pull_request_review` - Code review creation
- `get_pull_request_comments` - Review comment retrieval
- `update_pull_request_branch` - Branch synchronization
- `get_pull_request_status` - CI/CD status checking

### **When to Use MCP Instead of Generic**
- ✅ **Multi-file commits** (atomic operations)
- ✅ **Repository management** (creation, configuration)
- ✅ **Advanced searching** (code, issues, repositories)
- ✅ **PR workflows** (reviews, status checking, merging)
- ✅ **Batch operations** (multiple API calls)

### **Use Generic When**
- Simple git commands in existing repository
- Local git operations without remote API needs

---

## 🤖 **Browser Automation** → `mcp__puppeteer`

### **Why Use MCP Version**
- **Full Browser Control**: Complete Puppeteer capabilities
- **Interactive Operations**: Click, fill, select, hover actions
- **Screenshot Capabilities**: Full page and element-specific screenshots
- **JavaScript Execution**: Run custom scripts in browser context
- **Dynamic Content**: Handle modern SPAs and dynamic content

### **Core Capabilities**
- `puppeteer_navigate` - Navigate to URLs with launch options
- `puppeteer_screenshot` - Screenshots (full page or element-specific)
- `puppeteer_click` - Click elements by CSS selector
- `puppeteer_fill` - Fill input fields with values
- `puppeteer_select` - Select dropdown options
- `puppeteer_hover` - Hover over elements
- `puppeteer_evaluate` - Execute JavaScript in browser console

### **Advanced Features**
- **Launch Configuration**: Headless/headed mode, custom arguments
- **Element Targeting**: CSS selector-based element interaction
- **Screenshot Options**: Size control, element-specific capture, base64 encoding
- **Security Settings**: Dangerous option controls with safety flags
- **Context Management**: Persistent browser sessions

### **When to Use MCP Instead of Generic**
- ✅ **Dynamic websites** (JavaScript-heavy, SPAs)
- ✅ **Interactive testing** (form filling, clicking, navigation)
- ✅ **Screenshot capture** (documentation, testing)
- ✅ **Modern web apps** (requires browser execution)
- ✅ **Automated workflows** (multi-step browser interactions)

### **Use Generic When**
- Static content fetching (no JavaScript execution needed)
- Simple HTTP API interactions

---

## ⏰ **Time Operations** → `mcp__time`

### **Why Use MCP Version**
- **Timezone Expertise**: IANA timezone support with automatic detection
- **Conversion Capabilities**: Between any timezone pairs
- **System Integration**: Automatic local timezone detection
- **Precision Handling**: Proper time calculation and formatting

### **Core Capabilities**
- `get_current_time` - Current time in specified timezone
- `convert_time` - Convert time between timezone regions

### **Specialized Features**
- **IANA Timezone Support**: Full timezone database access
- **Automatic Detection**: System timezone automatic identification
- **Global Collaboration**: Multi-timezone coordination support
- **Precision Timing**: Accurate time calculations

### **When to Use MCP Instead of Generic**
- ✅ **Timezone operations** (conversions, multi-zone coordination)
- ✅ **Session timestamps** (accurate timezone-aware logging)
- ✅ **Global collaboration** (scheduling across timezones)
- ✅ **Automated operations** (time-based triggers)

### **Use Generic When**
- Simple local time operations
- Basic timestamp generation without timezone considerations

---

## 🎯 **Tool Selection Decision Tree**

### **Step 1: Domain Classification**
```
What domain does this task belong to?
├── File operations → Check mcp__filesystem
├── Web content → Check mcp__fetch
├── GitHub operations → Check mcp__github
├── Browser automation → Check mcp__puppeteer
├── Time/timezone → Check mcp__time
└── Other → Use appropriate generic tools
```

### **Step 2: Capability Assessment**
```
Does the MCP version provide valuable enhancements?
├── YES: Advanced features would add significant value
│   └── → Use MCP server
├── MAYBE: Some enhanced features available
│   └── → Consider complexity vs benefit
└── NO: Generic tool is specifically better for this use case
    └── → Use generic tool
```

### **Step 3: Post-Task Review**
```
After completing task:
├── Could MCP server have done this better?
├── What enhanced features would have been valuable?
├── How can I improve tool selection next time?
└── → Update mental model and selection patterns
```

---

## 🚀 **Quick Decision Prompts**

**Before Any Tool Selection**:
- "What domain is this task in?"
- "Is there a specialized MCP server for this?"
- "What enhanced capabilities would the MCP version provide?"
- "Would those enhancements add meaningful value here?"

**Default Decision Rule**: 
> **Use MCP server unless generic tool is specifically better for this exact use case**

**Post-Task Reflection**:
- "What MCP opportunities did I miss?"
- "How can I better recognize MCP-appropriate tasks?"
- "What patterns should inform future tool selection?"

---

**Status**: Production Ready - Use for all tool selection decisions  
**Integration**: Referenced from system insights and mental toolkit framework  
**Next Update**: Add new MCP servers as they become available