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

### 0. Check Model Matrix Freshness (Live Preflight)
Before scoring the plan, verify that [references/model-matrix.md](./references/model-matrix.md) reflects the models currently available in Antigravity:

1. Call `swarm` with `action: "models"` and `all: true` (read-only; does not launch a swarm) to fetch the live list of available model IDs and display names.
2. Compare the live model IDs against the **Tracked Model Catalog** in [references/model-matrix.md](./references/model-matrix.md):
   - **Up to date** (no unrecognized model IDs and no currently recommended models missing): proceed directly to Step 1 without extra web searches.
   - **Stale** (new models/effort tiers appeared, or recommended models were removed):
     1. Run targeted `search_web` queries on the new/changed models to gather their positioning, coding/security/reasoning strengths, effort tiers, speed/quota tradeoffs, and Orchestrator support.
     2. Update [references/model-matrix.md](./references/model-matrix.md) (the `Last verified` date, **Tracked Model Catalog**, **Available Models**, **Quick Decision Matrix by Profile**, and **Swarm Patterns**) so future sessions benefit too. *(Do not auto-commit or auto-push if the plugin lives in a git repo; note the file update in your brief so the user can review and commit it.)*
     3. If `model-matrix.md` is not writable or web search is unavailable, still factor the live model list into this brief and flag that the matrix needs a manual refresh.
   - **If `swarm` is unavailable:** Proceed with [references/model-matrix.md](./references/model-matrix.md) and note the `Last verified` date in the brief.

### 1. Gather Context & Resolve Profile
1. Read the target implementation plan (e.g., `implementation_plan.md`, a topic plan artifact, or the plan in chat).
2. **Explore-First Guardrail:** Resolve factual questions (file layout, test suites, existing interfaces, repo invariants) by inspecting the codebase and artifacts yourself—never ask the user questions the repo can answer. Reserve questions strictly for unstated user preferences or scope decisions.
3. If working inside a workspace, scan the root `AGENTS.md` (if present) to note critical safety invariants, governance test gates, and multi-repo boundaries.
4. Determine the active **Optimization Profile** using this precedence order:
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
| **Context-Window Budget & Bite-Sized Slicing (~150k tokens)** | Oversized monolithic phases touching many layers or dozens of files in one pass, risking context fatigue and drift. Flag these and recommend splitting into vertical tracer-bullet slices (~150k-token budget per slice, verifiable end-to-end) or expand–contract batches for wide mechanical refactors. |
| **Verification Coverage** | Whether strict automated gates (lint, typecheck, governance tests, unit/integration suites) catch regressions immediately vs. subtle logic/security flaws that tests may miss. |
| **Blindsided-Author Risk** | Whether the change is high-stakes enough that the authoring model could rationalize away its own edge cases, warranting a fresh-session cross-family review. |
| **Parallelism & Swarm Fit** | Whether phases decompose into collision-free ownership boundaries (separate repos, decoupled interfaces, distinct modules) or benefit from an automated author ↔ verifier loop vs. staying single-agent. |

### 3. Select Model & Swarm Settings
Consult [references/model-matrix.md](./references/model-matrix.md) for the active profile (`quality-first`, `balanced`, or `quota-saver`) and apply these cross-cutting guardrails:

- **Never recommend Orchestrator for subtle, poorly test-covered security logic:** Orchestrator delegates code edits to Hydrogen, which escalates reliably on failing tests but may miss quiet edge-case or invariant flaws.
- **Avoid model-switching churn:** Only recommend switching models between phases if the phases have *genuinely different* risk profiles (e.g., deep architecture → core implementation → surgical docs → adversarial review).
- **Match effort level to scope tightness:** Step down to `Neon (Medium/High)` or `Hydrogen (High)` for verbatim or tightly scoped edits where heavy reasoning models tend to over-engineer.
- **Keep swarms disciplined:** Only recommend Swarm (`/teamwork`) when parallelism or automated peer verification clearly beats a single session under the active profile. Model multi-phase work as a **task graph**—sequence prerequisite shared models/contracts *before* parallel fan-out, identify the **ready frontier** of unblocked slices, guarantee zero file overlap among concurrent authors, specify explicit per-worker model pinning, and keep worker briefs lean with **sparse context pointers** (file paths, plan sections, commit SHAs) instead of duplicating long prose.

### 4. Produce the Model & Swarm Execution Brief
Present a concise, scannable brief using this structure:

1. **Profile & Risk Summary** — Active profile (`quality-first` / `balanced` / `quota-saver`), matrix freshness status (only call out details if the matrix was just updated or is stale), and 1–2 lines summarizing the plan's primary risk drivers and relevant workspace invariants.
2. **Recommended Execution Settings** — Primary model + effort level (and whether a single setting covers the whole plan or a phase split is worthwhile).
3. **Phase-by-Phase Routing Table** *(include when the plan has 2+ distinct phases)*:
   - Columns: `Phase` | `Recommended Model & Effort` | `Why` | `Scope Guardrail`
   - Flag any monolithic phase that exceeds a comfortable **~150k-token slice** and suggest concrete vertical tracer-bullet splits.
4. **Over-Engineering Watchouts** — Call out any surgical or verbatim steps where the executing model should be explicitly instructed *not* to refactor surrounding code.
5. **Cross-Family Review Recommendation** — Clear **Yes / Optional / Skip**, specifying the review model (e.g., `Claude Opus 5.5 (High)`), what exact diff/invariants to attack, and whether a pre-implementation plan critique is worthwhile.
6. **Swarm Recommendation (`/teamwork`)** — Clear **Skip / 2-Worker Adversarial Swarm / Multi-Worker Parallel Swarm**:
   - If **Skip**: 1-sentence rationale.
   - If **Recommended**:
     - **Coordinator Model**, **Sequencing Gate** (prerequisite contracts/phases that must land first), and **Ready Frontier** (which slices can run concurrently right away).
     - **Worker Roster Table**: `Worker Name` | `Owns (No Overlap)` | `Workspace` | `Model & Effort` | `Role`
     - **Ready-to-Paste Launch Prompt**: A concise 1–2 sentence instruction the user can paste into `/teamwork` enforcing the exact worker split, workspace isolation, per-worker model pinning, and sparse context pointers (referencing plan/doc paths rather than pasting long prose).

---

## Validation
Before finalizing the brief, verify that:
- Step 0 live model freshness check was performed (and `references/model-matrix.md` was updated first if new/retired models were detected).
- Factual questions about the repo or plan were answered by reading files directly rather than asking the user.
- Every recommended model name and effort tier matches an actual live option in [references/model-matrix.md](./references/model-matrix.md).
- Every recommendation ties directly to specific files, phases, or risks in the reviewed plan (no generic boilerplate), and oversized phases (>~150k-token context scope) are flagged for vertical slicing.
- Orchestrator is *not* recommended for security-critical or poorly test-covered logic.
- If Swarm is recommended: no two concurrent authors own overlapping files, shared prerequisites and the ready frontier are explicit, worker briefs rely on sparse context pointers, and any cross-family verifier starts fresh (not forked) with explicit model pinning.
