# Project Breakdown: AI-Agentic Workflow System

This document breaks down the multi-phase project to build and govern a sophisticated AI-agentic configuration and rule management system.

---

## Phase 1: Codex Unification

* **Goal**: Consolidate the initial `CLAUDE.md` and various rule files into a single, authoritative document named `CLAUDE-CODEX.md`. This eliminates redundancy and creates a single source of truth.
* **Safety Measures**:
  * All work is performed in a separate Git worktree (`chore/claude-codex-merge`) to avoid disrupting the main branch.
  * Full backups of the original files are created with SHA256 checksums for verification and rollback.
* **Outcome**: A unified codex was created. However, this monolithic approach was deemed difficult to manage for individual rules.

---

## Phase 2: Rule Atomization

* **Goal**: Refactor the monolithic `CLAUDE-CODEX.md` by extracting each rule into its own "atomic" Markdown file. This makes the rules modular, independently editable, and easier to test.
* **Key Actions**:
  * A new worktree (`chore/rules-v2-extract`) was used for safety.
  * Rules were extracted into a new directory structure: `.claude/rules/v2/`.
  * A script (`automation/split-codex-into-rules.sh`) was created to automate the extraction.
  * The main `CLAUDE-CODEX.md` was converted into a "link-out" document, containing links to the individual rule files.
* **Outcome**: A modular and more maintainable rule system.

---

## Phase 3: Enhanced Governance

* **Goal**: Improve the system's governance by adding comprehensive metadata to the codex and making the rule index more human-friendly.
* **Key Actions**:
  * The `CLAUDE-CODEX.md` front-matter was enhanced with exhaustive metadata, including governance, architecture, security classifications, and maintenance procedures.
  * The machine-readable `INDEX.json` was replaced by a human-readable `INDEX.yaml` as the new source of truth.
  * A new script (`automation/build-index-yaml.py`) was created to generate the JSON file from the YAML source, maintaining both human and machine readability.
* **Outcome**: A system with robust, auditable governance and improved human control.

---

## Phase 4: Web Dashboard for Visualization

* **Goal**: Develop a professional web interface to showcase the CLAUDE CODEX system, making it easier to understand, manage, and "sell" as a viable solution.
* **Key Actions**:
  * A `web/` directory was created to house the interface (`index.html`, `assets/styles.css`, `assets/script.js`).
  * The dashboard is designed to be a modern, responsive interface that dynamically loads the rule data from `INDEX.json`.
* **Outcome**: A functional and professional UI for demonstrating the system's capabilities.

---

## Phase 5: Real-time Integration with Convex (Proof of Concept)

* **Goal**: Evaluate the [Convex](https://www.convex.dev/) platform as a backend to enable real-time rule synchronization, collaboration, and advanced querying.
* **Safety Measures**:
  * The plan is a **reversible Proof of Concept (POC)**, ensuring no permanent changes to the existing system.
  * Work is isolated in a new worktree (`feat/convex-poc`).
  * The existing static files remain the **Single Source of Truth (SSOT)**. Convex data is populated from these files.
* **Key Actions**:
  * Scaffold a Convex application within `integrations/convex-codex/`.
  * Create a one-way import script to sync rules from the static files to Convex.
  * Add a configuration toggle to the web dashboard to switch between the static data and the live Convex data.
* **Outcome**: A safe and structured plan to explore a powerful real-time backend without compromising the current system's stability.

---

## Phase 6: Enhancing AI Knowledge with Context7

* **Goal**: Address the "cold-start" problem for the AI by giving it access to up-to-date external documentation, specifically for new technologies like Convex.
* **Key Actions**:
  * Integrate the **Context7 MCP (Model Context Protocol)** server. This allows the AI to query for fresh library documentation on demand.
  * Configuration is stored in a project-scoped `.mcp.json` file.
  * A usage guide is created at `knowledge/platforms/context7.md`.
* **Outcome**: Claude Code can now stay current with external tools, making its analysis and plans more accurate and reliable.

---

## Phase 7: Implementing a Confidence Gate (Critical Safety Feature)

* **Goal**: Fix a critical flaw where the AI would auto-approve plans even when its confidence was below the required threshold (e.g., 0.93 < 0.95).
* **Key Actions**:
  * A new, explicit rule was added: `R-quality-gates-0004-approval-confidence-threshold.md`.
  * A machine-enforceable policy was created at `.claude/policies/approval-policy.json`.
  * A Python guard script (`automation/guards/confidence_gate.py`) was developed to check the confidence score from any given text.
  * This creates a hard gate, preventing any `APPROVE:*` action unless the confidence score is >= 0.95.
* **Outcome**: A crucial safety layer that ensures human oversight for any plan the AI is not highly confident about, preventing potentially flawed automatic actions.
