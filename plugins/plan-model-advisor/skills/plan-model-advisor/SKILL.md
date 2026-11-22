---
name: plan-model-advisor
description: >-
  Reviews an implementation plan and recommends the optimal Antigravity model
  settings, effort levels, cross-family review passes, and swarm configurations
  for executing it. Use when the user asks to review an implementation plan for
  model or swarm selection, asks which model/effort/swarm settings to use for
  upcoming work, or right after finalizing an implementation plan when execution
  routing advice is requested.
---

# Plan Model Advisor

Evaluates an implementation plan and produces a concise **Model & Swarm Execution Brief** tailored to the plan's risk profile and the user's optimization tier (`quality-first`, `balanced`, or `quota-saver`).

Read [references/model-matrix.md](./references/model-matrix.md) for current model capabilities, effort tiers, profile policies, and swarm patterns before making recommendations.

---

## Procedure

### 1. Gather Context & Resolve Profile
1. Read the target implementation plan (e.g., `implementation_plan.md`, a topic plan artifact, or the plan in chat).
2. If working inside a workspace, scan the root `AGENTS.md` (if present) to note critical safety invariants, governance test gates, and multi-repo boundaries.
3. Determine the active **Optimization Profile** using this precedence order:
   - **Explicit in prompt** (e.g., *"use quality-first"*, *"I'm on Pro"*, *"optimize for quota"*).
   - **User rules** (e.g., a preference line in `~/.gemini/GEMINI.md` or workspace `AGENTS.md` such as `Default plan-model-advisor profile: quality-first`).
   - **Fallback default:** `balanced` (state this explicitly in the brief so the user knows they can override with `quality-first` or `quota-saver`).

### 2. Score the Plan Across Risk & Structure Dimensions
Evaluate each phase or milestone of the plan against:

| Dimension | High-Signal Indicators |
| :--- | :--- |
| **Security & Trust Boundaries** | Auth/RBAC, untrusted input parsing, SSRF/XSS/SQLi surfaces, cryptography/signing, secrets, production infra/deploy scripts. |
| **Architectural & Algorithmic Depth** | Cross-repo contracts, DB/schema migrations, concurrency/async state, formal math/consensus logic, large structural refactors. |
| **Surgical Precision / Over-Engineering Risk** | Tight 1–3 file fixes, verbatim doc/citation/rule edits, CSS/theme tweaks, config changes where an overly helpful frontier model might refactor out-of-scope code. |
| **Verification Coverage** | Whether strict automated gates (lint, typecheck, governance tests, unit/integration suites) catch regressions immediately vs. subtle logic/security flaws that tests may miss. |
| **Blindsided-Author Risk** | Whether the change is high-stakes enough that the authoring model could rationalize away its own edge cases, warranting a fresh-session cross-family review. |
| **Parallelism & Swarm Fit** | Whether phases decompose into collision-free ownership boundaries (separate repos, decoupled interfaces, distinct modules) or benefit from an automated author ↔ verifier loop vs. staying single-agent. |

### 3. Select Model & Swarm Settings
Consult [references/model-matrix.md](./references/model-matrix.md) for the active profile (`quality-first`, `balanced`, or `quota-saver`) and apply these cross-cutting guardrails:

- **Never recommend Orchestrator for subtle, poorly test-covered security logic:** Orchestrator delegates code edits to Hydrogen, which escalates reliably on failing tests but may miss quiet edge-case or invariant flaws.
- **Avoid model-switching churn:** Only recommend switching models between phases if the phases have *genuinely different* risk profiles (e.g., deep architecture → core implementation → surgical docs → adversarial review).
- **Match effort level to scope tightness:** Step down to `Neon (Medium/High)` or `Hydrogen (High)` for verbatim or tightly scoped edits where heavy reasoning models tend to over-engineer.
- **Keep swarms disciplined:** Only recommend Swarm (`/teamwork`) when parallelism or automated peer verification clearly beats a single session under the active profile. Sequence prerequisite shared models/contracts *before* parallel fan-out, guarantee zero file overlap among concurrent authors, and specify explicit per-worker model pinning.

### 4. Produce the Model & Swarm Execution Brief
Present a concise, scannable brief using this structure:

1. **Profile & Risk Summary** — Active profile (`quality-first` / `balanced` / `quota-saver`) + 1–2 lines summarizing the plan's primary risk drivers and relevant workspace invariants.
2. **Recommended Execution Settings** — Primary model + effort level (and whether a single setting covers the whole plan or a phase split is worthwhile).
3. **Phase-by-Phase Routing Table** *(include when the plan has 2+ distinct phases)*:
   - Columns: `Phase` | `Recommended Model & Effort` | `Why` | `Scope Guardrail`
4. **Over-Engineering Watchouts** — Call out any surgical or verbatim steps where the executing model should be explicitly instructed *not* to refactor surrounding code.
5. **Cross-Family Review Recommendation** — Clear **Yes / Optional / Skip**, specifying the review model (e.g., `Claude Opus 5.5 (High)`), what exact diff/invariants to attack, and whether a pre-implementation plan critique is worthwhile.
6. **Swarm Recommendation (`/teamwork`)** — Clear **Skip / 2-Worker Adversarial Swarm / Multi-Worker Parallel Swarm**:
   - If **Skip**: 1-sentence rationale.
   - If **Recommended**:
     - **Coordinator Model** + **Sequencing Gate** (any prerequisite phase that must land before fanning out).
     - **Worker Roster Table**: `Worker Name` | `Owns (No Overlap)` | `Workspace` | `Model & Effort` | `Role`
     - **Ready-to-Paste Launch Prompt**: A concise 1–2 sentence instruction the user can paste into `/teamwork` to enforce the exact worker split, workspace isolation, and per-worker model pinning.

---

## Validation
Before finalizing the brief, verify that:
- Every recommended model name and effort tier matches an actual option in [references/model-matrix.md](./references/model-matrix.md).
- Every recommendation ties directly to specific files, phases, or risks in the reviewed plan (no generic boilerplate).
- Orchestrator is *not* recommended for security-critical or poorly test-covered logic.
- If Swarm is recommended: no two concurrent authors own overlapping files, shared prerequisites are sequenced first, and any cross-family verifier starts fresh (not forked) with explicit model pinning.
