#!/bin/bash
# Claude Code Status Line Script
# Shows model and timestamp information

MODEL=$(echo "${CLAUDE_MODEL:-sonnet}")
TIMESTAMP=$(date "+%H:%M:%S")
PROJECT_PATH=$(basename "$(pwd)" 2>/dev/null || echo "")

if [[ -n "$PROJECT_PATH" && "$PROJECT_PATH" != "." ]]; then
    echo "Claude Code | $MODEL | $TIMESTAMP | 📁 $PROJECT_PATH"
else
    echo "Claude Code | $MODEL | $TIMESTAMP"
fi