#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validation Hook - Proof of Concept PreToolUse Hook

Purpose: Simple validation hook to test that hook system works in our environment.
This hook will log tool usage and pass through all commands for validation testing.
"""

import sys
import json
from datetime import datetime

def main():
    """Main hook execution function"""
    try:
        # Read hook payload from command line argument
        if len(sys.argv) < 2:
            print("⚠️  Hook called without payload")
            sys.exit(0)  # Pass through if no payload
            
        hook_data = json.loads(sys.argv[1])
        
        # Extract tool information
        tool_name = hook_data.get("tool_name", "unknown")
        tool_input = hook_data.get("tool_input", {})
        
        # Log the hook execution (proof that hook system works)
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"🔍 [{timestamp}] Validation Hook - Tool: {tool_name}")
        
        # Simple validation example - just log and pass through
        if tool_name in ["Bash", "Write", "Edit"]:
            print(f"✅ Validation passed for {tool_name}")
        else:
            print(f"ℹ️  Tool {tool_name} - no specific validation")
        
        # Always allow execution for proof-of-concept
        sys.exit(0)  # 0 = allow execution
        
    except json.JSONDecodeError:
        print("⚠️  Invalid JSON payload in hook")
        sys.exit(0)  # Pass through on error
        
    except Exception as e:
        print(f"⚠️  Hook error: {str(e)}")
        sys.exit(0)  # Pass through on error

if __name__ == "__main__":
    main()