# Claude Code Hooks Mastery - Complete Repository Extraction

## Repository Overview

**Repository**: <https://github.com/disler/claude-code-hooks-mastery>  
**Purpose**: Comprehensive mastery of Claude Code hooks with deterministic control over Claude Code behavior  
**Author**: IndyDevDan (disler)  
**Key Features**: All 8 hook types, security controls, TTS integration, sub-agents, meta-agent architecture

This repository provides complete coverage of Claude Code's hook system, demonstrating how to add deterministic (or non-deterministic) control over Claude Code's behavior through hooks and sub-agents.

## Installation & Setup

### Prerequisites

- **[Astral UV](https://docs.astral.sh/uv/getting-started/installation/)** - Fast Python package installer and resolver
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - Anthropic's CLI for Claude AI

### Optional Services

- **[ElevenLabs](https://elevenlabs.io/)** - Text-to-speech provider (with MCP server integration)
- **[ElevenLabs MCP Server](https://github.com/elevenlabs/elevenlabs-mcp)** - MCP server for ElevenLabs
- **[Firecrawl MCP Server](https://www.firecrawl.dev/mcp)** - Web scraping and crawling MCP server
- **[OpenAI](https://openai.com/)** - Language model provider + Text-to-speech provider
- **[Anthropic](https://www.anthropic.com/)** - Language model provider

## Hook Lifecycle & Complete Coverage

This repository demonstrates **all 8 Claude Code hook lifecycle events** with their JSON payloads:

### 1. UserPromptSubmit Hook

**Fires**: Immediately when user submits a prompt (before Claude processes it)  
**Payload**: `prompt` text, `session_id`, timestamp  
**Enhanced**: Prompt validation, logging, context injection, security filtering  
**Control**: **CAN BLOCK PROMPTS & ADD CONTEXT**

### 2. PreToolUse Hook

**Fires**: Before any tool execution  
**Payload**: `tool_name`, `tool_input` parameters  
**Enhanced**: Blocks dangerous commands (`rm -rf`, `.env` access)  
**Control**: **CAN BLOCK TOOL EXECUTION**

### 3. PostToolUse Hook

**Fires**: After successful tool completion  
**Payload**: `tool_name`, `tool_input`, `tool_response` with results  
**Enhanced**: Result validation, transcript conversion  
**Control**: **CANNOT BLOCK (Tool Already Executed)**

### 4. Notification Hook

**Fires**: When Claude Code sends notifications (waiting for input, etc.)  
**Payload**: `message` content  
**Enhanced**: TTS alerts - "Your agent needs your input" (30% chance includes name)  
**Control**: **CANNOT BLOCK**

### 5. Stop Hook

**Fires**: When Claude Code finishes responding  
**Payload**: `stop_hook_active` boolean flag  
**Enhanced**: AI-generated completion messages with TTS playback  
**Control**: **CAN BLOCK STOPPING**

### 6. SubagentStop Hook

**Fires**: When Claude Code subagents (Task tools) finish responding  
**Payload**: `stop_hook_active` boolean flag  
**Enhanced**: TTS playback - "Subagent Complete"  
**Control**: **CAN BLOCK SUBAGENT STOPPING**

### 7. PreCompact Hook

**Fires**: Before Claude Code performs a compaction operation  
**Payload**: `trigger` ("manual" or "auto"), `custom_instructions` (for manual), session info  
**Enhanced**: Transcript backup, verbose feedback for manual compaction  
**Control**: **CANNOT BLOCK**

### 8. SessionStart Hook

**Fires**: When Claude Code starts a new session or resumes an existing one  
**Payload**: `source` ("startup", "resume", or "clear"), session info  
**Enhanced**: Development context loading (git status, recent issues, context files)  
**Control**: **CANNOT BLOCK**

## Configuration Files

### Claude Code Settings (.claude/settings.json)

```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash(uv:*)",
      "Bash(find:*)",
      "Bash(mv:*)",
      "Bash(grep:*)",
      "Bash(npm:*)",
      "Bash(ls:*)",
      "Bash(cp:*)",
      "Write",
      "Edit",
      "Bash(chmod:*)",
      "Bash(touch:*)"
    ],
    "deny": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/post_tool_use.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/notification.py --notify"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/stop.py --chat"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/subagent_stop.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/user_prompt_submit.py --log-only"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_compact.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/session_start.py"
          }
        ]
      }
    ]
  }
}
```

## Code Examples - Hook Implementations

### 1. UserPromptSubmit Hook

**File**: `.claude/hooks/user_prompt_submit.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def log_user_prompt(session_id, input_data):
    """Log user prompt to logs directory."""
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'user_prompt_submit.json'
    
    # Read existing log data or initialize empty list
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []
    
    # Append the entire input data
    log_data.append(input_data)
    
    # Write back to file with formatting
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)


def validate_prompt(prompt):
    """
    Validate the user prompt for security or policy violations.
    Returns tuple (is_valid, reason).
    """
    # Example validation rules (customize as needed)
    blocked_patterns = [
        # Add any patterns you want to block
        # Example: ('rm -rf /', 'Dangerous command detected'),
    ]
    
    prompt_lower = prompt.lower()
    
    for pattern, reason in blocked_patterns:
        if pattern.lower() in prompt_lower:
            return False, reason
    
    return True, None


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--validate', action='store_true', 
                          help='Enable prompt validation')
        parser.add_argument('--log-only', action='store_true',
                          help='Only log prompts, no validation or blocking')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract session_id and prompt
        session_id = input_data.get('session_id', 'unknown')
        prompt = input_data.get('prompt', '')
        
        # Log the user prompt
        log_user_prompt(session_id, input_data)
        
        # Validate prompt if requested and not in log-only mode
        if args.validate and not args.log_only:
            is_valid, reason = validate_prompt(prompt)
            if not is_valid:
                # Exit code 2 blocks the prompt with error message
                print(f"Prompt blocked: {reason}", file=sys.stderr)
                sys.exit(2)
        
        # Add context information (optional)
        # You can print additional context that will be added to the prompt
        # Example: print(f"Current time: {datetime.now()}")
        
        # Success - prompt will be processed
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == '__main__':
    main()
```

### 2. PreToolUse Hook - Security & Blocking

**File**: `.claude/hooks/pre_tool_use.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import re
from pathlib import Path

def is_dangerous_rm_command(command):
    """
    Comprehensive detection of dangerous rm commands.
    Matches various forms of rm -rf and similar destructive patterns.
    """
    # Normalize command by removing extra spaces and converting to lowercase
    normalized = ' '.join(command.lower().split())
    
    # Pattern 1: Standard rm -rf variations
    patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf, etc.
        r'\brm\s+.*-[a-z]*f[a-z]*r',  # rm -fr variations
        r'\brm\s+--recursive\s+--force',  # rm --recursive --force
        r'\brm\s+--force\s+--recursive',  # rm --force --recursive
        r'\brm\s+-r\s+.*-f',  # rm -r ... -f
        r'\brm\s+-f\s+.*-r',  # rm -f ... -r
    ]
    
    # Check for dangerous patterns
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True
    
    # Pattern 2: Check for rm with recursive flag targeting dangerous paths
    dangerous_paths = [
        r'/',           # Root directory
        r'/\*',         # Root with wildcard
        r'~',           # Home directory
        r'~/',          # Home directory path
        r'\$HOME',      # Home environment variable
        r'\.\.',        # Parent directory references
        r'\*',          # Wildcards in general rm -rf context
        r'\.',          # Current directory
        r'\.\s*$',      # Current directory at end of command
    ]
    
    if re.search(r'\brm\s+.*-[a-z]*r', normalized):  # If rm has recursive flag
        for path in dangerous_paths:
            if re.search(path, normalized):
                return True
    
    return False

def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        # Check file paths for file-based tools
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                return True
        
        # Check bash commands for .env file access
        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
                r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
                r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
                r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
                r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
                r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
            ]
            
            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True
    
    return False

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check for .env file access (blocks access to sensitive environment files)
        if is_env_file_access(tool_name, tool_input):
            print("BLOCKED: Access to .env files containing sensitive data is prohibited", file=sys.stderr)
            print("Use .env.sample for template files instead", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Check for dangerous rm -rf commands
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            
            # Block rm -rf commands with comprehensive pattern matching
            if is_dangerous_rm_command(command):
                print("BLOCKED: Dangerous rm command detected and prevented", file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Ensure log directory exists
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'pre_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Gracefully handle JSON decode errors
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()
```

### 3. Stop Hook - TTS Integration

**File**: `.claude/hooks/stop.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import random
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_completion_messages():
    """Return list of friendly completion messages."""
    return [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!"
    ]


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"
    
    # Check for ElevenLabs API key (highest priority)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)
    
    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)
    
    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)
    
    return None


def get_llm_completion_message():
    """
    Generate completion message using available LLM services.
    Priority order: OpenAI > Anthropic > fallback to random message
    
    Returns:
        str: Generated or fallback completion message
    """
    # Get current script directory and construct utils/llm path
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"
    
    # Try OpenAI first (highest priority)
    if os.getenv('OPENAI_API_KEY'):
        oai_script = llm_dir / "oai.py"
        if oai_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(oai_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # Try Anthropic second
    if os.getenv('ANTHROPIC_API_KEY'):
        anth_script = llm_dir / "anth.py"
        if anth_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(anth_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # Fallback to random predefined message
    messages = get_completion_messages()
    return random.choice(messages)

def announce_completion():
    """Announce completion using the best available TTS service."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available
        
        # Get completion message (LLM-generated or fallback)
        completion_message = get_llm_completion_message()
        
        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ], 
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "stop.json")

        # Read existing log data or initialize empty list
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Handle --chat switch
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines
                    
                    # Write to logs/chat.json
                    chat_file = os.path.join(log_dir, 'chat.json')
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass  # Fail silently

        # Announce completion via TTS
        announce_completion()

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()
```

### 4. ElevenLabs TTS Integration

**File**: `.claude/hooks/utils/tts/elevenlabs_tts.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    ElevenLabs Turbo v2.5 TTS Script
    
    Uses ElevenLabs' Turbo v2.5 model for fast, high-quality text-to-speech.
    Accepts optional text prompt as command-line argument.
    
    Usage:
    - ./eleven_turbo_tts.py                    # Uses default text
    - ./eleven_turbo_tts.py "Your custom text" # Uses provided text
    
    Features:
    - Fast generation (optimized for real-time use)
    - High-quality voice synthesis
    - Stable production model
    - Cost-effective for high-volume usage
    """
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY not found in environment variables")
        print("Please add your ElevenLabs API key to .env file:")
        print("ELEVENLABS_API_KEY=your_api_key_here")
        sys.exit(1)
    
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play
        
        # Initialize client
        elevenlabs = ElevenLabs(api_key=api_key)
        
        print("🎙️  ElevenLabs Turbo v2.5 TTS")
        print("=" * 40)
        
        # Get text from command line argument or use default
        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])  # Join all arguments as text
        else:
            text = "The first move is what sets everything in motion."
        
        print(f"🎯 Text: {text}")
        print("🔊 Generating and playing...")
        
        try:
            # Generate and play audio directly
            audio = elevenlabs.text_to_speech.convert(
                text=text,
                voice_id="WejK3H1m7MI9CHnIjW9K",  # Specified voice
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128",
            )
            
            play(audio)
            print("✅ Playback complete!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        
    except ImportError:
        print("❌ Error: elevenlabs package not installed")
        print("This script uses UV to auto-install dependencies.")
        print("Make sure UV is installed: https://docs.astral.sh/uv/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Hook Error Codes & Flow Control

### Exit Code Behavior

| Exit Code | Behavior           | Description                                                                    |
| --------- | ------------------ | ------------------------------------------------------------------------------ |
| **0**     | Success            | Hook executed successfully. `stdout` shown to user in transcript mode (Ctrl-R) |
| **2**     | Blocking Error     | **Critical**: `stderr` is fed back to Claude automatically                     |
| **Other** | Non-blocking Error | `stderr` shown to user, execution continues normally                           |

### Hook-Specific Flow Control

#### UserPromptSubmit Hook - **CAN BLOCK PROMPTS & ADD CONTEXT**

- **Primary Control Point**: Intercepts user prompts before Claude processes them
- **Exit Code 2 Behavior**: Blocks the prompt entirely, shows error message to user
- **Use Cases**: Prompt validation, security filtering, context injection, audit logging

#### PreToolUse Hook - **CAN BLOCK TOOL EXECUTION**

- **Primary Control Point**: Intercepts tool calls before they execute
- **Exit Code 2 Behavior**: Blocks the tool call entirely, shows error message to Claude
- **Use Cases**: Security validation, parameter checking, dangerous command prevention

#### Stop Hook - **CAN BLOCK STOPPING**

- **Primary Control Point**: Intercepts when Claude Code tries to finish responding
- **Exit Code 2 Behavior**: Blocks stoppage, shows error to Claude (forces continuation)
- **Use Cases**: Ensuring tasks complete, validation of final state
- **Caution**: Can cause infinite loops if not properly controlled

## Claude Code Sub-Agents

Sub-agents are AI assistants that your primary Claude Code agent can delegate tasks to. They operate with specialized system prompts, tools, and separate context windows.

### Understanding Sub-Agents: System Prompts, Not User Prompts

**Critical Concept**: The content in agent files (`.claude/agents/*.md`) are **system prompts** that configure the sub-agent's behavior. They are NOT user prompts.

**Information Flow**:

```
You (User) → Primary Agent → Sub-Agent → Primary Agent → You (User)
```

### Agent File Structure

```markdown
---
name: agent-name
description: When to use this agent (critical for automatic delegation)
tools: Tool1, Tool2, Tool3  # Optional - inherits all tools if omitted
color: Cyan  # Visual identifier in terminal
model: opus # Optional - haiku | sonnet | opus - defaults to sonnet
---

# Purpose
You are a [role definition]. 

## Instructions
1. Step-by-step instructions
2. What the agent should do
3. How to report results

## Report/Response Format
Specify how the agent should communicate results back to the primary agent.
```

### The Meta-Agent

**File**: `.claude/agents/meta-agent.md`

```markdown
---
name: meta-agent
description: Generates a new, complete Claude Code sub-agent configuration file from a user's description. Use this to create new agents. Use this Proactively when the user asks you to create a new sub agent.
tools: Write, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape, mcp__firecrawl-mcp__firecrawl_search, MultiEdit
color: cyan
model: opus
---

# Purpose

Your sole purpose is to act as an expert agent architect. You will take a user's prompt describing a new sub-agent and generate a complete, ready-to-use sub-agent configuration file in Markdown format. You will create and write this new file. Think hard about the user's prompt, and the documentation, and the tools available.

## Instructions

**0. Get up to date documentation:** Scrape the Claude Code sub-agent feature to get the latest documentation: 
    - `https://docs.anthropic.com/en/docs/claude-code/sub-agents` - Sub-agent feature
    - `https://docs.anthropic.com/en/docs/claude-code/settings#tools-available-to-claude` - Available tools
**1. Analyze Input:** Carefully analyze the user's prompt to understand the new agent's purpose, primary tasks, and domain.
**2. Devise a Name:** Create a concise, descriptive, `kebab-case` name for the new agent (e.g., `dependency-manager`, `api-tester`).
**3. Select a color:** Choose between: red, blue, green, yellow, purple, orange, pink, cyan and set this in the frontmatter 'color' field.
**4. Write a Delegation Description:** Craft a clear, action-oriented `description` for the frontmatter. This is critical for Claude's automatic delegation. It should state *when* to use the agent. Use phrases like "Use proactively for..." or "Specialist for reviewing...".
**5. Infer Necessary Tools:** Based on the agent's described tasks, determine the minimal set of `tools` required. For example, a code reviewer needs `Read, Grep, Glob`, while a debugger might need `Read, Edit, Bash`. If it writes new files, it needs `Write`.
**6. Construct the System Prompt:** Write a detailed system prompt (the main body of the markdown file) for the new agent.
**7. Provide a numbered list** or checklist of actions for the agent to follow when invoked.
**8. Incorporate best practices** relevant to its specific domain.
**9. Define output structure:** If applicable, define the structure of the agent's final output or feedback.
**10. Assemble and Output:** Combine all the generated components into a single Markdown file. Adhere strictly to the `Output Format` below. Your final response should ONLY be the content of the new agent file. Write the file to the `.claude/agents/<generated-agent-name>.md` directory.

## Output Format

You must generate a single Markdown code block containing the complete agent definition. The structure must be exactly as follows:

```md
---
name: <generated-agent-name>
description: <generated-action-oriented-description>
tools: <inferred-tool-1>, <inferred-tool-2>
model: haiku | sonnet | opus <default to sonnet unless otherwise specified>
---

# Purpose

You are a <role-definition-for-new-agent>.

## Instructions

When invoked, you must follow these steps:
1. <Step-by-step instructions for the new agent.>
2. <...>
3. <...>

**Best Practices:**
- <List of best practices relevant to the new agent's domain.>
- <...>

## Report / Response

Provide your final response in a clear and organized manner.
```

```

## UV Single-File Scripts Architecture

This project leverages **[UV single-file scripts](https://docs.astral.sh/uv/guides/scripts/)** to keep hook logic cleanly separated from your main codebase. All hooks live in `.claude/hooks/` as standalone Python scripts with embedded dependency declarations.

**Benefits:**
- **Isolation** - Hook logic stays separate from your project dependencies
- **Portability** - Each hook script declares its own dependencies inline
- **No Virtual Environment Management** - UV handles dependencies automatically
- **Fast Execution** - UV's dependency resolution is lightning-fast
- **Self-Contained** - Each hook can be understood and modified independently

## Key Features Demonstrated

- **Complete hook lifecycle coverage** - All 8 hook events implemented and logging
- **Prompt-level control** - UserPromptSubmit validates and enhances prompts before Claude sees them
- **Intelligent TTS system** - AI-generated audio feedback with voice priority (ElevenLabs > OpenAI > pyttsx3)
- **Security enhancements** - Blocks dangerous commands and sensitive file access at multiple levels
- **Personalized experience** - Uses engineer name from environment variables
- **Automatic logging** - All hook events are logged as JSON to `logs/` directory
- **Chat transcript extraction** - PostToolUse hook converts JSONL transcripts to readable JSON format

## Logging System

All hooks log to `logs/` directory with structured JSON:

- `user_prompt_submit.json` - User prompt submissions with validation
- `pre_tool_use.json` - Tool use events with security blocking
- `post_tool_use.json` - Tool completion events
- `notification.json` - Notification events
- `stop.json` - Stop events with completion messages
- `subagent_stop.json` - Subagent completion events
- `pre_compact.json` - Pre-compaction events with trigger type
- `session_start.json` - Session start events with source type
- `chat.json` - Readable conversation transcript (generated by --chat flag)

## Security Implementation Examples

### 1. Command Validation (PreToolUse)

```python
# Block dangerous patterns
dangerous_patterns = [
    r'rm\s+.*-[rf]',           # rm -rf variants
    r'sudo\s+rm',              # sudo rm commands
    r'chmod\s+777',            # Dangerous permissions
    r'>\s*/etc/',              # Writing to system directories
]

for pattern in dangerous_patterns:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"BLOCKED: {pattern} detected", file=sys.stderr)
        sys.exit(2)
```

### 2. Result Validation (PostToolUse)

```python
# Validate file operations
if tool_name == "Write" and not tool_response.get("success"):
    output = {
        "decision": "block",
        "reason": "File write operation failed, please check permissions and retry"
    }
    print(json.dumps(output))
    sys.exit(0)
```

### 3. Completion Validation (Stop Hook)

```python
# Ensure critical tasks are complete
if not all_tests_passed():
    output = {
        "decision": "block",
        "reason": "Tests are failing. Please fix failing tests before completing."
    }
    print(json.dumps(output))
    sys.exit(0)
```

## Advanced JSON Output Control

Beyond simple exit codes, hooks can return structured JSON for sophisticated control:

### Common JSON Fields (All Hook Types)

```json
{
  "continue": true,           // Whether Claude should continue (default: true)
  "stopReason": "string",     // Message when continue=false (shown to user)
  "suppressOutput": true      // Hide stdout from transcript (default: false)
}
```

### PreToolUse Decision Control

```json
{
  "decision": "approve" | "block" | undefined,
  "reason": "Explanation for decision"
}
```

### Stop Decision Control

```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when blocking Claude from stopping"
}
```

## Agent Storage & Organization

**Project Agents** (`.claude/agents/`):

```
.claude/agents/
├── crypto/                    # Cryptocurrency analysis agents
│   ├── crypto-coin-analyzer-haiku.md
│   ├── crypto-coin-analyzer-opus.md
│   ├── crypto-coin-analyzer-sonnet.md
│   ├── crypto-investment-plays-*.md
│   ├── crypto-market-agent-*.md
│   ├── crypto-movers-haiku.md
│   └── macro-crypto-correlation-scanner-*.md
├── hello-world-agent.md       # Simple greeting agent
├── llm-ai-agents-and-eng-research.md  # AI research specialist
├── meta-agent.md              # Agent that creates agents
└── work-completion-summary.md # Audio summary generator
```

## Resources & References

- **Sub-Agents Video**: [Claude Code Sub-Agents](https://youtu.be/7B2HJr0Y68g)
- **Documentation**: [Claude Code Sub-Agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- **Hooks Documentation**: [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
- **Author Channel**: [IndyDevDan YouTube](https://www.youtube.com/@indydevdan)
- **AI Coding Principles**: [Principled AI Coding](https://agenticengineer.com/principled-ai-coding)

Built by [IndyDevDan](https://www.youtube.com/@indydevdan) demonstrating mastery of Claude Code hooks and sub-agent architecture.
