#!/usr/bin/env python3
"""
confidence_gate.py — Enforces approval confidence thresholds.
Usage:
  # from stdin
  printf "Confidence score — 0.93\n" | python automation/guards/confidence_gate.py --stdin
  # from file
  python automation/guards/confidence_gate.py --file CONTEXT/tmp/approval.txt --category integration
Exit codes: 0 pass, 2 fail, 3 parse error.
"""
import re, sys, json, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT/".claude/policies/approval-policy.json"

def load_policy():
    if POLICY.exists():
        return json.loads(POLICY.read_text(encoding="utf-8"))
    return {"default_threshold": 0.95, "categories": {}}

def parse_confidence(text: str):
    # Match variants like "Confidence score — 0.93" or "Confidence score - 0.97"
    m = re.findall(r"Confidence\s*score\s*[—\-:]\s*([01](?:\.\d{1,3})?)", text, flags=re.I)
    return float(m[-1]) if m else None

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--file")
    ap.add_argument("--threshold", type=float)
    ap.add_argument("--category")
    args = ap.parse_args()

    if args.stdin:
        src = sys.stdin.read()
    elif args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"ERR: missing {p}", file=sys.stderr); sys.exit(3)
        src = p.read_text(encoding="utf-8")
    else:
        print("ERR: provide --stdin or --file", file=sys.stderr); sys.exit(3)

    score = parse_confidence(src)
    if score is None:
        print("ERR: could not find 'Confidence score — x.xx'", file=sys.stderr); sys.exit(3)

    policy = load_policy()
    thr = args.threshold if args.threshold is not None else policy.get("default_threshold", 0.95)
    if args.category:
        thr = policy.get("categories", {}).get(args.category, thr)

    ok = score >= thr
    status = "PASS" if ok else "BLOCK"
    print(f"{status}: confidence={score:.2f} threshold={thr:.2f}")
    sys.exit(0 if ok else 2)

if __name__ == "__main__":
    main()
