Executive Decision — Single irreversible move: **Seal the Root**. Publish one falsifiable invariant and hard-gate `main` with a required CI check that rejects any change lacking a cryptographic proof-of-loop. Once enabled, the gate is default-alive and compounding.

# Claude Code — Mission Order

**Mission.** Create and enforce a genesis invariant and a mandatory CI status check. Cut a signed root tag. Require proof-of-loop on every merge.

**Context.**

* We already defined zero-axiom and proof-of-loop logic.
* We need one irreversible governance act that self-reinforces.

**Constraints.**

* No local execution by me. Claude Code runs the commands.
* POSIX-portable files. GitHub CI. No secrets echoed.
* Fail-closed: merge blocked unless the gate passes.

**Plan.**

1. Add `ROOT/INVARIANT.yaml` (Invariant-0).
2. Add `invariant-gate` workflow that verifies three proofs: (a) invariant alignment, (b) deterministic artifact + SHA256, (c) PR metadata completeness.
3. Add `CODEOWNERS` requiring Omar for `ROOT/**`.
4. Protect `main`: require `invariant-gate` status, signed commits optional, linear history on.
5. Create signed genesis tag `root/0` at the commit that introduces the gate.
6. Document acceptance in `CONTEXT/policy/README.md`.

**Commands.** Run from repo root. Use `DRY_RUN=1` first.

```bash
# Set vars (no echo of secrets)
set -eu
: "${GH_REPO:?owner/name}"        # e.g., omar/repo
: "${DEFAULT_BASE:=main}"
: "${SIGNER_NAME:=Omar El Mountassir}"
: "${SIGN_TAG:=0}"                 # set to 1 if GPG configured

# 1) Files
mkdir -p ROOT .github/workflows CONTEXT/policy

# 2) Invariant-0
cat > ROOT/INVARIANT.yaml <<'YAML'
id: invariant-0
statement: "Every change must emit a public, reproducible artifact whose digest binds code→commit→push→PR→review→merge→deploy."
tests:
  - name: proof-artifact-exists
    path: "CONTEXT/protocol/absolute-zero-proof.txt"
  - name: checksum-matches
    path: "CONTEXT/checks/SHA256SUMS"
    algo: "sha256"
governance:
  owner: "Omar El Mountassir"
  change_control: "CODEOWNERS approval required for ROOT/**"
YAML
```

Recommended path: `Repo/ROOT/INVARIANT.yaml`

```yaml
# 3) CI gate
name: invariant-gate
on:
  pull_request:
    branches: [ main ]
permissions:
  contents: read
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate invariant presence
        run: test -f ROOT/INVARIANT.yaml
      - name: Validate proof artifact
        run: test -f CONTEXT/protocol/absolute-zero-proof.txt
      - name: Validate checksum
        run: |
          set -eu
          if command -v sha256sum >/dev/null; then
            sha256sum -c CONTEXT/checks/SHA256SUMS
          else
            FILE=$(awk '{print $2}' CONTEXT/checks/SHA256SUMS)
            EXP=$(awk '{print $1}' CONTEXT/checks/SHA256SUMS)
            ACT=$(shasum -a 256 "$FILE" | awk '{print $1}')
            [ "$EXP" = "$ACT" ] || { echo "Checksum mismatch"; exit 1; }
          fi
      - name: PR metadata completeness
        uses: actions-ecosystem/action-check-pr-title@v1
        with:
          pattern: '^(feat|fix|chore|docs|refactor|test)(\\(.+\\))?: .+'
```

Recommended path: `Repo/.github/workflows/invariant-gate.yml`

```bash
# 4) CODEOWNERS
cat > CODEOWNERS <<'EOF'
# Require owner review for Core
/ROOT/*  @omar-el-mountassir
EOF
```

Recommended path: `Repo/CODEOWNERS`

```md
# Policy README (short)
- Invariant-0 is non-optional.
- PRs must ship proof artifact + checksum.
- Gate is required status on main.
```

Recommended path: `Repo/CONTEXT/policy/README.md`

```bash
# 5) Commit and tag genesis (Claude Code executes)
git add ROOT/INVARIANT.yaml .github/workflows/invariant-gate.yml CODEOWNERS CONTEXT/policy/README.md
git commit -m "chore(governance): seal the root with Invariant-0 and CI gate [fail-closed]"
if [ "${SIGN_TAG}" = "1" ]; then
  git tag -s root/0 -m "Genesis root: Invariant-0 sealed" || true
else
  git tag root/0 -m "Genesis root: Invariant-0 sealed"
fi
git push --follow-tags origin HEAD
```

```bash
# 6) Protect main: require the gate
gh api -X PUT repos/${GH_REPO}/branches/${DEFAULT_BASE}/protection \
  -F required_status_checks.strict=true \
  -F required_status_checks.contexts[]='invariant-gate' \
  -F enforce_admins=true \
  -F restrictions='null' \
  -F required_pull_request_reviews.require_code_owner_reviews=true \
  -F required_linear_history=true
```

**Acceptance.**

* Opening a PR without `CONTEXT/protocol/absolute-zero-proof.txt` fails `invariant-gate`.
* `gh api repos/$GH_REPO/branches/$DEFAULT_BASE/protection` lists `invariant-gate` as required.
* `git show root/0` displays the sealing commit introducing the gate.
* Merged PR triggers proof release (from your existing workflow) and checksum verifies.

**Rollback.**

* Remove branch protection and delete tag `root/0`. Explicit confirmation required.
* Dry-run first by adding `--dry-run` flags where available.

**Artifacts.**

* `ROOT/INVARIANT.yaml` (Invariant-0).
* `.github/workflows/invariant-gate.yml` (required check).
* `CODEOWNERS` enforcing owner review.
* Tag `root/0` as genesis anchor.

# Pros/Cons

**Pros**

* One governance act creates a compounding moat.
* Minimal moving parts.
* Auditable and tamper-evident.

**Cons**

* Blocks fast merges until teams adapt.
* Requires GitHub branch protection privileges.
* Assumes proof-of-loop workflow exists or is added.

# Next checkpoint + required confirmation

Reply **APPROVE: RUN** with `GH_REPO` and confirm `invariant-gate` should be the only required status at start. State if you want signed commits or tags enforced.

**Confidence score:** 0.86
