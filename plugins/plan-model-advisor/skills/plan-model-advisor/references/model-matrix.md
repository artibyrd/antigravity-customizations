# Antigravity Model & Swarm Matrix

*Last verified: 2026-11-22. Checked automatically during Step 0 of `plan-model-advisor` against `swarm{action:"models", all:true}`.*

---

## Tracked Model Catalog

Exact live model IDs reflected in this matrix (used by Step 0 to detect newly released or retired models):

- **Gemini 4 Neon:** `gemini-4-neon-low`, `gemini-4-neon-medium`, `gemini-4-neon-high`, `gemini-4-neon-xhigh`
- **Gemini 4 Carbon:** `gemini-4-carbon-low`, `gemini-4-carbon-medium`, `gemini-4-carbon-high`
- **Gemini 4 Argon:** `gemini-4-argon-low`, `gemini-4-argon-medium`, `gemini-4-argon-high`
- **Gemini 4 Hydrogen:** `gemini-4-hydrogen-low`, `gemini-4-hydrogen-medium`, `gemini-4-hydrogen-high`, `gemini-4-hydrogen-xhigh`
- **Orchestrator:** `gemini-pro-orchestrator` (`Orchestrator (Carbon)`), `gemini-pro-orchestrator-neon` (`Orchestrator (Neon)`), `gemini-pro-orchestrator-argon` (`Orchestrator (Argon)`)
- **Legacy / Other Gemini:** `gemini-3.8-flash-low`, `gemini-3.8-flash-medium`, `gemini-3.8-flash-high`
- **Claude:** `claude-opus-5-5-low`, `claude-opus-5-5-medium`, `claude-opus-5-5-high`, `claude-sonnet-5-5-low`, `claude-sonnet-5-5-medium`, `claude-sonnet-5-5-high`
- **Open Weights:** `gpt-oss-120b-medium`

---

## Optimization Profiles

| Profile | Best For | Default Execution Philosophy |
| :--- | :--- | :--- |
| **`quality-first`** | Unconstrained / Ultra quota; security, accuracy, and robustness above all else | Prefer standalone frontier models (`Neon High/XHigh`, `Carbon High`) so every edit gets full reasoning; skip Orchestrator except on huge mechanical test-gated sweeps; use fresh-session cross-family reviews (`Claude Opus 5.5 High`) and 2-worker/parallel swarms whenever justified. |
| **`balanced`** *(default)* | Pro / everyday quota-aware engineering | Use `Orchestrator (Neon)` and `Orchestrator (Carbon)` as daily workhorses for multi-file build/test loops; reserve standalone `Carbon (High)` / `Neon (XHigh)` for planning and security-critical logic; use `Hydrogen (High)` for docs/chores; reserve cross-family reviews and swarms for high-stakes or clearly parallel work. |
| **`quota-saver`** | Free tier, tight rate limits, or maximum turnaround speed | Default to `Gemini 4 Hydrogen (Medium/High)` (bump to `XHigh` for hard self-contained debugging); use `Orchestrator (Neon)` only on complex multi-file plans; avoid standalone `Carbon` and swarms; use targeted single-file checklists instead of full cross-family passes. |

---

## Available Models & Ideal Roles

| Model & Effort | Strengths | Watchouts / Failure Modes | Best Plan Phases |
| :--- | :--- | :--- | :--- |
| **Gemini 4 Carbon (`High`)** | Deepest long-horizon architectural reasoning, formal/mathematical rigor, cross-system invariant analysis, near-zero benchmark shortcutting. | Slowest; highest quota burn; can over-engineer or over-abstract small, surgical code edits. | Complex system architecture, formal proofs/consensus, high-ambiguity planning, deep cross-repo refactors. |
| **Gemini 4 Neon (`XHigh`)** | Top security benchmarks (`SEC-bench Pro`, `CWE-bench v2`, `AutoBaxBench`), top Antigravity agentic coding accuracy, strong root-cause debugging. | Higher deliberation on trivial edits; overkill for pure copy/config changes. | Security-critical implementation & patching, auth/crypto/ingestion code, gnarly multi-file debugging. |
| **Gemini 4 Neon (`High`)** | Best all-around standalone implementation model; frontier coding quality on every line with crisp execution and less over-deliberation than Carbon. | Slightly less exhaustive than `Neon (XHigh)` or `Carbon (High)` on extreme edge cases. | Standard full-stack feature implementation, TypeScript/UI work, multi-file refactors, iterative test-driven work. |
| **Gemini 4 Neon (`Medium`)** | Fast, literal, accurate on well-specified changes without wandering out of scope. | Not for deep architectural ambiguity or complex security auditing. | Surgical bug fixes, well-defined single-module changes, minor UI/CSS polish. |
| **Gemini 4 Hydrogen (`Medium` / `High` / `XHigh`)** | Fastest, lowest quota burn, high verbatim/non-hallucination fidelity, minimal tendency to over-engineer untouched code. (`XHigh` punches well above its weight on self-contained tasks.) | Trails Neon/Carbon on long-horizon multi-file reasoning and subtle security logic. | Strictly verbatim doc/changelog/citation edits, YAML/config updates, small utilities, and `quota-saver` primary driver. |
| **Orchestrator (`Neon` / `Carbon`)** | Pairs a frontier read-only planner with a fast Hydrogen executor and automatic test-failure recovery; faster and significantly lower quota burn. | Hydrogen executes the actual edits; subtle flaws or invariant drift that pass existing tests may not trigger escalation back to the planner. | **`balanced` daily driver** for multi-file feature & test loops; **`quality-first` only** for huge mechanical sweeps guarded by strict automated tests. Never use for unverified security-critical code. |
| **Gemini 4 Argon (`Low`–`High`)** | Earlier Gemini 4 workhorse. | Largely superseded by Neon for coding/security and Carbon for deep reasoning. | Rarely recommended unless needed for legacy workflow parity. |
| **Claude Opus 5.5 (`High`)** | Distinct model family with different failure modes and strong adversarial/architectural critique. | Separate session required to avoid shared confirmation bias. | Fresh-session **cross-family adversarial security & code review**, pre-implementation plan stress-testing, and design sparring. |

---

## Quick Decision Matrix by Profile

| Phase / Work Type | `quality-first` | `balanced` | `quota-saver` |
| :--- | :--- | :--- | :--- |
| **Complex Architecture / Math Planning** | `Gemini 4 Carbon (High)` | `Gemini 4 Carbon (High)` | `Gemini 4 Neon (High)` |
| **Standard Feature / UI Planning** | `Gemini 4 Neon (High/XHigh)` | `Gemini 4 Neon (High)` | `Gemini 4 Hydrogen (XHigh)` |
| **Security / Auth / Crypto Implementation** | `Gemini 4 Neon (XHigh)` | `Gemini 4 Neon (XHigh)` | `Gemini 4 Neon (High)` |
| **Multi-File Feature + Test Loops** | `Gemini 4 Neon (High)` | `Orchestrator (Neon)` | `Gemini 4 Hydrogen (High)` (or `Orchestrator (Neon)` if complex) |
| **Large Mechanical Test-Gated Sweep** | `Orchestrator (Carbon)` or `Orchestrator (Neon)` | `Orchestrator (Neon)` | `Gemini 4 Hydrogen (Medium/High)` |
| **Surgical Patch / Verbatim Docs / Config** | `Gemini 4 Neon (Medium)` or `Hydrogen (High)` | `Gemini 4 Hydrogen (High)` | `Gemini 4 Hydrogen (Medium)` |
| **Pre-PR Adversarial Security Audit** | Fresh `Claude Opus 5.5 (High)` | Fresh `Claude Opus 5.5 (High)` (high-risk diffs only) | Targeted self-audit checklist (or `Neon High` on critical auth files) |

---

## Swarm Patterns & Settings (`/teamwork`)

Swarms are **quota-heavy** and introduce coordination overhead; use them only when parallelism or automated peer verification clearly beats a single session.

- **`quota-saver`:** Always **Skip Swarm**.
- **`balanced`:** Recommend only for clear multi-repo/multi-interface parallel wins (skip for routine sequential work).
- **`quality-first`:** Recommend both **2-Worker Adversarial Swarms** (for high-risk sequential work) and **Multi-Worker Parallel Swarms** (for cleanly decoupled milestones).

| Pattern | When to Use | Typical Roster & Model Pinning | Workspace Modes |
| :--- | :--- | :--- | :--- |
| **Skip Swarm (Single Agent)** | Small/surgical edits, tightly coupled single-module refactors, or compact projects with no parallel seam. | Single standalone session (plus optional manual fresh-session review). | N/A |
| **2-Worker Adversarial Swarm** | Sequential or single-module work touching high-risk security, auth, crypto, ingestion, or strict invariants. | **Coordinator:** `Gemini 4 Neon (High)`<br>**`author`:** `Gemini 4 Neon (XHigh)` or `Carbon (High)`<br>**`sec-verifier`:** `Claude Opus 5.5 (High)` (cold start, never forked) | `author`: `inherit`<br>`sec-verifier`: `inherit` (read-only/test-only; bounces findings directly to `@author`) |
| **Multi-Worker Parallel Swarm** | Multi-repo rollouts or multi-interface parity milestones (e.g., CLI / MCP / TUI / Web / Docs, or backend / client / extensions) *after* shared core contracts are locked. | **Coordinator:** `Gemini 4 Neon (High)` or `Carbon (High)`<br>**2–4 scoped authors:** `Gemini 4 Neon (High/XHigh)` (or `Hydrogen High` for pure docs/changelog work)<br>**1 `verifier` per 2–4 authors:** `Claude Opus 5.5 (High)` | Concurrent same-repo authors: `share` (each commits to its own working copy, then merges cleanly)<br>Read-only verifiers / non-overlapping single authors: `inherit`<br>Full clone isolation (destructive builds/env changes): `branch` |

### Swarm Guardrails
- **Zero File Overlap:** Never assign two concurrent authors to the same file. Split by repo, subsystem, or interface boundary.
- **Prerequisites First:** Shared schemas, core domain models, and interface contracts must land before parallel workers fan out.
- **Context-Window Slicing & Sparse Briefs:** Size each worker's assignment to a bite-sized vertical slice (~150k-token working budget) drawn from the ready task-graph frontier, and pass sparse context pointers (plan paths, file paths, commit SHAs, ADRs) instead of pasting long prose into briefs.
- **Explicit Model Pinning:** Antigravity swarm coordinators default every worker to the coordinator's model unless the user explicitly specifies per-worker models—always provide a ready-to-paste launch instruction naming the exact model pins.
- **Verifier Discipline:** Verifiers inspect diffs, run test/governance gates, and `@mention` the author with findings; they never edit the author's files directly.
