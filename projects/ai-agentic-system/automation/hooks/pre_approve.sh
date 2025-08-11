#!/usr/bin/env bash
# pre_approve.sh — block APPROVE when confidence below threshold.
# Usage: pre_approve.sh <path-to-text-with-confidence-line> [category]
set -euo pipefail
FILE="${1:-}"
CATEGORY="${2:-integration}"
if [ -z "${FILE}" ] || [ ! -f "${FILE}" ]; then
  echo "Usage: $0 CONTEXT/approvals/<file>.txt [category]" >&2
  exit 3
fi
python automation/guards/confidence_gate.py --file "$FILE" --category "$CATEGORY"
