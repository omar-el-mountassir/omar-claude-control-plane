# Claude Code is Programmable - Complete Repository Extraction

## Repository Overview

**Repository**: <https://github.com/disler/claude-code-is-programmable>  
**Purpose**: Scale your compute with Claude Code as a programmable agentic coding tool  
**Author**: IndyDevDan (disler)  
**Key Features**: Voice integration, programmatic control, MCP integration, Notion API integration

This repository demonstrates how to use Claude Code programmatically across different programming languages, showcasing the power of treating Claude Code as a programmable agentic tool rather than just an interactive assistant.

## Installation & Setup

### Prerequisites

- Python 3.8+
- UV package manager (`pip install uv`)
- Node.js (for MCP servers)
- Anthropic API key
- OpenAI API key (for voice features)
- Notion API key (for Notion integration)

### Configuration Files

#### MCP Configuration (.mcp.json)

```json
{
  "mcpServers": {
    "notionApi": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer YOUR_NOTION_API_KEY\", \"Notion-Version\": \"2022-06-28\" }"
      }
    }
  }
}
```

#### Environment Variables (.env)

```bash
NOTION_INTERNAL_INTEGRATION_SECRET=your_notion_integration_secret
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Core Tools Available in Claude Code

- **Task**: Launch an agent to perform complex tasks
- **Bash**: Execute bash commands in a shell
- **Batch**: Run multiple tools in parallel
- **Glob**: Find files matching patterns
- **Grep**: Search file contents with regex
- **LS**: List directory contents
- **Read**: Read file contents
- **Edit**: Make targeted edits to files
- **Write**: Create or overwrite files
- **NotebookRead/Edit**: Work with Jupyter notebooks
- **WebFetch**: Get content from websites

## Code Examples

### 1. Basic Shell Script Implementation

**File**: `claude_code_is_programmable_1.sh`

```bash
claude -p "make a hello.js script that prints hello" --allowedTools "Write" "Edit"
```

### 2. Python Implementation - Basic Todo App

**File**: `claude_code_is_programmable_2.py`

```python
#!/usr/bin/env -S uv run --script

# Script that runs Claude Code CLI to create a zero-dependency TypeScript todo app with Git operations

import subprocess

prompt = """

GIT checkout a NEW branch.

CREATE ./cc_todo/todo.ts: a zero library CLI todo app with basic CRUD. 

THEN GIT stage, commit and SWITCH back to main.

"""

command = ["claude", "-p", prompt, "--allowedTools", "Edit", "Bash", "Write"]

# Capture Claude's output so we can display it
process = subprocess.run(
    command,
    check=True,
    capture_output=True,
    text=True,
)

print(f"Claude process exited with output: {process.stdout}")
```

### 3. Advanced Python - Notion Integration

**File**: `claude_code_is_programmable_3.py`

```python
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "python-dotenv",
#   "rich"
# ]
# ///

# Notion integration script that uses Claude Code to process todos from a specified Notion page

import os
import sys
import subprocess
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint

# Initialize rich console
console = Console()

# Load environment variables for Notion API
load_dotenv()
NOTION_API_SECRET = os.getenv("NOTION_INTERNAL_INTEGRATION_SECRET")
if not NOTION_API_SECRET:
    console.print(
        "[bold red]ERROR: NOTION_INTERNAL_INTEGRATION_SECRET not found in environment variables.[/bold red]"
    )
    sys.exit(1)

# Check for the page name argument
if len(sys.argv) < 2:
    console.print(
        "[bold red]ERROR: Please provide a Notion page name as an argument.[/bold red]"
    )
    console.print("Usage: uv run claude_code_is_programmable_3.py <notion_page_name>")
    sys.exit(1)

page_name = sys.argv[1]

# Define the allowed tools for Claude
allowed_tools = [
    # Standard Claude Code tools
    "Bash",
    "Edit",
    "View",
    "GlobTool",
    "GrepTool",
    "LSTool",
    "BatchTool",
    "AgentTool",
    "WebFetchTool",
    "Write",
    # Notion API tools
    "mcp__notionApi__API-get-user",
    "mcp__notionApi__API-get-users",
    "mcp__notionApi__API-get-self",
    "mcp__notionApi__API-post-database-query",
    "mcp__notionApi__API-post-search",
    "mcp__notionApi__API-get-block-children",
    "mcp__notionApi__API-patch-block-children",
    "mcp__notionApi__API-retrieve-a-block",
    "mcp__notionApi__API-update-a-block",
    "mcp__notionApi__API-delete-a-block",
    "mcp__notionApi__API-retrieve-a-page",
    "mcp__notionApi__API-patch-page",
    "mcp__notionApi__API-post-page",
    "mcp__notionApi__API-create-a-database",
    "mcp__notionApi__API-update-a-database",
    "mcp__notionApi__API-retrieve-a-database",
    "mcp__notionApi__API-retrieve-a-page-property",
    "mcp__notionApi__API-retrieve-a-comment",
    "mcp__notionApi__API-create-a-comment",
]

# Create the prompt for Claude
prompt = f"""
# Notion Todo Code Generation Agent

## Objective
You are an agent that will:
1. Find and read a Notion page named "{page_name}"
2. Extract all todo items from the page
3. For each incomplete todo, implement the code changes described in the todo
4. Commit the changes with a descriptive message
5. Mark the todo item as complete in Notion
6. Continue to the next todo item

## Process - Follow these steps exactly:

### Step 1: Find the Notion page
- Use the Notion API via the mcp__notionApi__API-post-search tool to search for a page with the name "{page_name}"
- Extract the page ID from the search results

### Step 2: Get page content
- Use the mcp__notionApi__API-retrieve-a-page tool to get the page details
- Use the mcp__notionApi__API-get-block-children tool to get the page blocks
- Look for any to_do blocks, which represent your todo items
- For each to_do block, capture:
  - The block ID
  - The content text
  - Whether it's already checked/completed

### Step 3: Process each todo
For each UNCHECKED todo item:
1. Read and understand the todo description
2. Implement the code changes described:
   - Use GlobTool, GrepTool, View to explore the codebase
   - Use Edit or Replace to modify or create files
   - Use Bash when necessary to run commands
3. Test your implementation if tests are available
4. Stage and commit your changes with a descriptive message:
   ```bash
   git add .
   git commit -m "Descriptive message about what was implemented"
   ```

5. Mark the todo as complete in Notion using the mcp__notionApi__API-update-a-block tool

### Step 4: Wrap up

- Provide a summary of all todos processed and changes made

## Important Notes

- Skip any todos that are already checked/complete
- Process todos in the order they appear on the page
- Make one commit per todo item
- Ensure each commit message clearly describes what was implemented
- If a todo cannot be completed, note why but don't mark it as complete
- If a todo is already completed, skip it

## Available Notion Tools

You have access to the standard Claude Code tools like Bash, Edit, Replace, View, etc., as well as the complete set of Notion API tools:

- mcp__notionApi__API-post-search: Use this to find the Notion page by name
- mcp__notionApi__API-get-block-children: Use this to retrieve the todo items from the page
- mcp__notionApi__API-update-a-block: Use this to mark todos as complete
And many other Notion API tools as needed.

Now begin your task by finding the Notion page named "{page_name}" and processing its todos.
"""

# Execute the Claude command with stream-json output format

try:
    console.print(
        f"[bold blue]🤖 Starting Claude Code to process todos from Notion page:[/bold blue] [yellow]{page_name}[/yellow]"
    )

    cmd = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "stream-json",
        "--allowedTools",
    ] + allowed_tools

    # Start the process and read output as it comes
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line buffered
    )

    # Process and display JSON output in real-time
    console.print("\n[bold green]📊 Streaming Claude output:[/bold green]")
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break

        syntax = Syntax(line, "json", theme="monokai", line_numbers=False)
        console.print(syntax)

    # Check for any errors
    stderr = process.stderr.read()
    if stderr:
        console.print(f"[bold red]⚠️ Error output from Claude:[/bold red]\n{stderr}")

    # Get return code
    return_code = process.wait()
    if return_code == 0:
        console.print(f"[bold green]✅ Claude Code completed successfully[/bold green]")
    else:
        console.print(
            f"[bold red]❌ Claude Code failed with exit code: {return_code}[/bold red]"
        )
        sys.exit(return_code)

except subprocess.CalledProcessError as e:
    console.print(f"[bold red]❌ Error executing Claude Code: {str(e)}[/bold red]")
    sys.exit(1)
except Exception as e:
    console.print(f"[bold red]❌ Unexpected error: {str(e)}[/bold red]")
    sys.exit(1)

```

### 4. Voice-Enabled Claude Code Assistant

**File**: `voice_to_claude_code.py` (21KB+ full implementation)

**Key Features**:
- Real-time speech recognition using RealtimeSTT
- Claude Code integration for programmable AI coding
- Text-to-speech responses using OpenAI TTS
- Conversation history tracking
- Voice trigger activation

**Configuration Constants**:
```python
TRIGGER_WORDS = ["claude", "cloud", "sonnet", "sonny"]
STT_MODEL = "small.en"  # Options: tiny.en, base.en, small.en, medium.en, large-v2
TTS_VOICE = "nova"  # Options: alloy, echo, fable, onyx, nova, shimmer
DEFAULT_CLAUDE_TOOLS = [
    "Bash",
    "Edit", 
    "Write",
    "GlobTool",
    "GrepTool",
    "LSTool",
    "Replace",
]
```

**Usage Examples**:

```bash
# Basic usage
uv run voice_to_claude_code.py

# With specific conversation ID
uv run voice_to_claude_code.py --id "my-chat-id"

# With initial prompt
uv run voice_to_claude_code.py --prompt "create a hello world script"

# With both ID and prompt
uv run voice_to_claude_code.py --id "my-chat-id" --prompt "create a hello world script"
```

### 5. Anthropic Web Search Tool

**File**: `anthropic_search.py`

```python
#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "anthropic",
#   "rich",
#   "python-dotenv",
# ]
# ///

# CLI tool for searching the web using Anthropic's Claude with citation tracking and formatted output

import argparse
import os
import json
import sys
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from dotenv import load_dotenv

# Initialize console for rich output
console = Console()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Search the web using Anthropic's Claude."
    )
    parser.add_argument("query", help="The search query")
    parser.add_argument(
        "--max-uses", type=int, default=3, help="Maximum number of web searches"
    )
    parser.add_argument(
        "--model", default="claude-3-7-sonnet-20250219", help="Claude model to use"
    )
    parser.add_argument("--domains", help="Comma-separated list of allowed domains")
    parser.add_argument("--blocked", help="Comma-separated list of blocked domains")
    parser.add_argument(
        "--location", help="Location format: 'US,California,San Francisco'"
    )
    parser.add_argument(
        "--timezone", help="IANA timezone ID (e.g., 'America/Los_Angeles')"
    )
    return parser.parse_args()

def get_search_results(args):
    """Query Anthropic API with web search enabled."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Parse domain lists
    allowed_domains = args.domains.split(",") if args.domains else None
    blocked_domains = args.blocked.split(",") if args.blocked else None

    # Build the web search tool
    web_search_tool = {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": args.max_uses,
    }

    # Add domain filtering if specified (can't use both)
    if allowed_domains:
        web_search_tool["allowed_domains"] = allowed_domains
    elif blocked_domains:
        web_search_tool["blocked_domains"] = blocked_domains

    # Add location if specified
    location = parse_location(args.location, args.timezone)
    if location:
        web_search_tool["user_location"] = location

    try:
        # Make API request
        response = client.messages.create(
            model=args.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": args.query}],
            tools=[web_search_tool],
        )
        return response
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        return None
```

**Usage Examples**:

```bash
# Basic search
./anthropic_search.py "your search query"

# With domain filtering
./anthropic_search.py "javascript best practices" --domains "developer.mozilla.org,javascript.info"

# Block specific domains
./anthropic_search.py "climate change" --blocked "unreliablesource.com,fakenews.org"

# With location context
./anthropic_search.py "local restaurants" --location "US,California,San Francisco" --timezone "America/Los_Angeles"

# Increase maximum searches
./anthropic_search.py "complex research topic" --max-uses 5

# Use different Claude model
./anthropic_search.py "your query" --model "claude-3-5-sonnet-latest"
```

## Claude Code Response Formats

```bash
# Text output
claude -p 'hello, run git ls-files, how many files are in the current directory' --output-format text > test.txt

# JSON output
claude -p 'hello, run git ls-files, how many files are in the current directory' --output-format json > test.json

# Stream JSON output
claude -p --continue 'hello, run git ls-files, how many files are in the current directory' --output-format stream-json > test.stream.json
```

## Key Patterns & Techniques

### 1. Programmatic Claude Code Execution

The core insight is treating Claude Code as a programmable tool rather than just an interactive assistant:

```python
# Basic pattern
command = ["claude", "-p", prompt, "--allowedTools", "Edit", "Bash", "Write"]
process = subprocess.run(command, capture_output=True, text=True)
```

### 2. Tool Restrictions for Safety

Restrict Claude Code to specific tools for controlled execution:

```bash
claude -p "make a hello.js script" --allowedTools "Write" "Edit"
```

### 3. Stream Processing for Real-time Feedback

```python
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, 
    text=True,
    bufsize=1,  # Line buffered
)

while True:
    line = process.stdout.readline()
    if not line and process.poll() is not None:
        break
    # Process line in real-time
```

### 4. MCP Integration Pattern

```python
allowed_tools = [
    # Standard Claude Code tools
    "Bash", "Edit", "Write",
    # MCP tools for specific services
    "mcp__notionApi__API-post-search",
    "mcp__notionApi__API-get-block-children",
    "mcp__notionApi__API-update-a-block",
]
```

### 5. Voice Integration Architecture

- **Input**: RealtimeSTT for speech-to-text
- **Processing**: Claude Code for task execution
- **Output**: OpenAI TTS for text-to-speech
- **Conversation**: YAML-based history persistence

## Dependencies

### Core Dependencies

```python
# Required for all implementations
subprocess  # Built-in Python
python-dotenv  # Environment variable management
rich  # Rich terminal output

# Voice features
RealtimeSTT  # Real-time speech recognition
openai  # TTS capabilities
sounddevice  # Audio playback
soundfile  # Audio file handling
numpy  # Audio data processing

# Anthropic integration
anthropic  # Direct API access for web search
```

### UV Script Format

All Python scripts use the UV script format for dependency management:

```python
#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "python-dotenv",
#   "rich",
#   "anthropic"
# ]
# ///
```

## Architecture Insights

### 1. Claude Code as Infrastructure

The repository demonstrates treating Claude Code as programmable infrastructure rather than just a chat interface.

### 2. Multi-Modal Integration

Voice → Claude Code → Action represents a complete autonomous system.

### 3. External Service Integration

MCP servers enable Claude Code to interact with external APIs (Notion, GitHub, etc.).

### 4. Output Format Control

Different output formats (text, JSON, stream-json) enable different integration patterns.

### 5. Tool Restriction Security

Controlling available tools provides security and predictability for autonomous operations.

## Resources & References

- **Main Video**: [Why This Is Important for Next Generation Engineering](https://youtu.be/2TIXl2rlA6Q)
- **Voice Demo**: [Voice to Claude Code Video](https://youtu.be/LvkZuY7rJOM)
- **Anthropic Docs**: [Claude Code Tutorials](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#use-claude-as-a-unix-style-utility)
- **Best Practices**: [Agentic Coding Guide](https://www.anthropic.com/engineering/claude-code-best-practices)
- **Aider Comparison**: [Aider Scripting Documentation](https://aider.chat/docs/scripting.html)
- **Author Resources**: [Principled AI Coding](https://agenticengineer.com/principled-ai-coding)

Built by [IndyDevDan](https://www.youtube.com/@indydevdan) with Claude Code and Principled AI Coding methodologies.
