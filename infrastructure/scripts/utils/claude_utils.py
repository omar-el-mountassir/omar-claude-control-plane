#!/usr/bin/env python3
"""
Claude Code Utilities

Shared utility functions for Claude Code Python scripts.
Provides common functionality like path detection, logging setup,
constants, etc.

Usage:
    from claude_utils import get_claude_dir, REQUIRED_DIRECTORIES, BYTES_PER_MB

    config_dir = get_claude_dir()
"""

import os
from pathlib import Path
from typing import Optional


# ============================================================================
# GLOBAL CONSTANTS
# ============================================================================

# Version constants
EXPECTED_VERSION = "0.1.0"

# Directory structure constants
REQUIRED_DIRECTORIES = [
    "infrastructure/modules/config",
    "infrastructure/modules/operations",
    "infrastructure/modules/memory",
    "infrastructure/modules/knowledge",
    "infrastructure/modules/meta",
    "infrastructure/logs",
    "infrastructure/templates",
    "infrastructure/scripts",
    "infrastructure/integrations",
    "infrastructure/cache",
    "analysis",
    "knowledge"
]

CORE_SCRIPTS = [
    "infrastructure/scripts/core/backup-config.py",
    "infrastructure/scripts/core/health-check.py"
]

# Backup constants
IGNORE_PATTERNS = ['*.tmp', '__pycache__', '*.pyc', '.git', '.DS_Store']
BYTES_PER_MB = 1024 * 1024


def get_claude_dir(fallback_dir: Optional[Path] = None) -> Path:
    """Get Claude configuration directory with environment variable support.

    Checks for CLAUDE_DIR environment variable first, then falls back to:
    1. Provided fallback_dir parameter
    2. Default ~/.claude directory

    Args:
        fallback_dir: Optional fallback directory if CLAUDE_DIR not set

    Returns:
        Path to Claude configuration directory

    Example:
        # Use environment variable or default
        config_dir = get_claude_dir()

        # Use environment variable or custom fallback
        config_dir = get_claude_dir(Path("/custom/claude/path"))
    """
    # Check environment variable first
    claude_dir_env = os.environ.get('CLAUDE_DIR')
    if claude_dir_env:
        return Path(claude_dir_env).expanduser().resolve()

    # Use fallback if provided
    if fallback_dir:
        return fallback_dir.expanduser().resolve()

    # Default to ~/.claude
    return Path.home() / ".claude"


def get_claude_dir_str() -> str:
    """Get Claude configuration directory as string.

    Convenience function for shell scripts and string operations.

    Returns:
        String path to Claude configuration directory
    """
    return str(get_claude_dir())


def check_dependencies() -> bool:
    """Check if required system dependencies are available.

    Returns:
        True if all dependencies available, False otherwise
    """
    import shutil

    required_tools = ['uv']  # Add more as needed
    missing: list[str] = []

    for tool in required_tools:
        if not shutil.which(tool):
            missing.append(tool)

    if missing:
        print(f"❌ Missing required dependencies: {', '.join(missing)}")
        print("   Please install missing tools before running this script")
        return False

    return True
