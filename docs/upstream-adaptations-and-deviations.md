# Upstream Adaptations, Provenance & Deviations

This repository builds on and synthesizes ideas from two foundational open-source sources alongside our own Google Antigravity workflows:

* **[Matt Pocock's `skills`](https://github.com/mattpocock/skills)** — *MIT License, Copyright (c) 2026 Matt Pocock*. Source of battle-tested tactical engineering disciplines (`diagnosing-bugs`, `tdd`, `code-review`, `codebase-design`, `improve-codebase-architecture`, `domain-modeling`, `pr`, `retro`, `writing-for-agents`, `handoff`, `prototype`, `wizard`, and destructive-git guardrails).
* **[Dex Horthy / Humanlayer (`show-me`)](https://github.com/humanlayer/humanlayer)** — visual summary menu (pseudocode, call trees, component trees, file trees, Mermaid diagrams, scoped diffs, whole blocks) and placement guidance preserved via [`pr-brief`](../plugins/pr-brief/README.md) (credited upstream through Matt's `pr` skill).

Both ecosystems converged independently on the same core conviction: **software engineering fundamentals matter more in the AI era, not less**. Where `mattpocock/skills` targets **Claude Code** as a single cohesive suite with an issue-tracker workflow, `antigravity-customizations` targets **Google Antigravity** as standalone, zero-config, à la carte plugins combined with operational governance patterns extracted from our own multi-repo projects.

This document records:
1. Exact provenance for every one of our **19 plugins**.
2. Principled reasoning for every **architectural and behavioral deviation**.
3. Complete accounting of **all 39 skills** audited in `mattpocock/skills`, including the **26 skills intentionally excluded** and the specific nuances absorbed from them.

---

## 1. Three Provenance Tiers (All 19 Plugins)

Every plugin in [`plugins/`](../README.md#plugin-catalog) carries one of three explicit classifications:

* **`Original`** (5 plugins) — Authored natively for Google Antigravity from our own engineering and governance workflows.
* **`Adapted (mattpocock/skills)`** (5 plugins) — Directly translated from `mattpocock/skills` (MIT) to Antigravity's native conventions while preserving the core upstream workflow.
* **`Combined (Original + mattpocock/skills)`** (9 plugins) — Synthesizes upstream concepts from `mattpocock/skills` (and `humanlayer/show-me` for `pr-brief`) with our own Antigravity architecture, hooks, or governance rules.

| # | Plugin | Wave | Provenance Tier | Upstream Source Skill(s) & Synthesis Summary |
| :--- | :--- | :--- | :--- | :--- |
| 1 | [`plan-model-advisor`](../plugins/plan-model-advisor/README.md) | Wave 1 | `Combined (Original + mattpocock/skills)` | Original model/effort/swarm advisor; v1.2.0 absorbs explore-first, ~150k context slicing, task-graph frontier, and sparse pointer concepts inspired by `implement-spec`, `to-tickets`, and `grilling`. |
| 2 | [`knowledge-governance`](../plugins/knowledge-governance/README.md) | Wave 1 | `Combined (Original + mattpocock/skills)` | Original 4-Tier Knowledge Taxonomy, Demotion Highway, `/learn` Admission Gate, and Invariant Challenger + Matt's `skills/engineering/retro` (7 diagnostic categories & review-only `CODING_STANDARDS.md`). |
| 3 | [`diagnosing-bugs`](../plugins/diagnosing-bugs/README.md) | Wave 1 | `Adapted (mattpocock/skills)` | `skills/engineering/diagnosing-bugs` (6-phase red-capable feedback loop, `[DEBUG-xxxx]` probes, `<REDACTED>` hygiene, HITL script). |
| 4 | [`tdd`](../plugins/tdd/README.md) | Wave 1 | `Combined (Original + mattpocock/skills)` | `skills/engineering/tdd` (vertical-slice seam TDD + `tests.md` / `mocking.md`) + Original Hermetic Testing Boundary & ban on test-file helper stand-ins. |
| 5 | [`code-review`](../plugins/code-review/README.md) | Wave 1 | `Combined (Original + mattpocock/skills)` | `skills/engineering/code-review` (parallel fresh subagents, Standards + 12 Fowler Smells vs. Spec) + Original Reality-Check / Zero-Mock lens & dedicated **Axis 3 — Security**. |
| 6 | [`git-guardrails`](../plugins/git-guardrails/README.md) | Wave 1 | `Combined (Original + mattpocock/skills)` | Original native Antigravity `hooks.json` `PreToolUse` guard & stdlib Python POSIX/git parser + destructive-git blocklist inspired by `skills/misc/git-guardrails-claude-code`. |
| 7 | [`writing-for-agents`](../plugins/writing-for-agents/README.md) | Wave 2 | `Combined (Original + mattpocock/skills)` | `skills/productivity/writing-for-agents` (prompt-craft levers) + Original Antigravity `plugin.json`/`SKILL.md`/`hooks.json` mechanics and `<800`-token `AGENTS.md` ceiling. |
| 8 | [`architecture-review`](../plugins/architecture-review/README.md) | Wave 2 | `Combined (Original + mattpocock/skills)` | `skills/engineering/codebase-design` + `skills/engineering/improve-codebase-architecture` (Deep Modules, Design-It-Twice, hotspot survey) + Original ~500 LOC internal decomposition harmony & operational/UI guardrails. |
| 9 | [`pr-brief`](../plugins/pr-brief/README.md) | Wave 2 | `Combined (Original + mattpocock/skills)` | `skills/engineering/pr` + **[Dex Horthy / Humanlayer (`show-me`)](https://github.com/humanlayer/humanlayer)** visual menu + Original Mk1 Eyeball Walkthrough checklist & `<REDACTED>` probe hygiene. |
| 10 | [`bootstrap-approvals`](../plugins/bootstrap-approvals/README.md) | Wave 2 | `Original` | Native Antigravity IDE permission priming (Subprocess Isolation Rule, dynamic read-command discovery, *"No Spicy Prefixes"* ban). |
| 11 | [`session-handoff`](../plugins/session-handoff/README.md) | Wave 2 | `Adapted (mattpocock/skills)` | `skills/productivity/handoff` tailored for Antigravity ↔ cross-model (e.g., Gemini → Claude) and fresh-session artifact handoffs. |
| 12 | [`artifact-governance`](../plugins/artifact-governance/README.md) | Wave 3 | `Combined (Original + mattpocock/skills)` | Original Living vs. Historical Document lifecycle, Append-Only Ledger Protocol, and Clean Scratch Script Ritual + primary-source cited Markdown research note habit from `skills/engineering/research`. |
| 13 | [`reality-check-audit`](../plugins/reality-check-audit/README.md) | Wave 3 | `Original` | Cross-model adversarial "Outsider's Honest Assessment" (`Good → Concerning → Aspirational vs. Real → Remediation Plans`). |
| 14 | [`domain-modeling`](../plugins/domain-modeling/README.md) | Wave 3 | `Adapted (mattpocock/skills)` | `skills/engineering/domain-modeling` (lazy `GLOSSARY.md` + 3-criteria Historical ADR gate), paired with native `/grill-me` and living-invariant distinction. |
| 15 | [`release-lifecycle`](../plugins/release-lifecycle/README.md) | Wave 3 | `Original` | 4-phase delivery & continuous learning cadence, `CHANGELOG.md`/`ROADMAP.md` symmetry, graceful preflight, and Topological Multi-Repo PR Merge Order. |
| 16 | [`repo-bootstrap`](../plugins/repo-bootstrap/README.md) | Wave 3 | `Original` | Optional on-demand repository governance scaffolder (`AGENTS.md`, modular `Justfile`, `GLOSSARY.md`, `docs/adr/`, governance test skeleton). |
| 17 | [`workspace-hygiene-hooks`](../plugins/workspace-hygiene-hooks/README.md) | Wave 3 | `Original` | Native plugin-root `hooks.json` (`PostToolUse` workspace-confined auto-formatter + loop-safe `Stop` stray-file hygiene check). |
| 18 | [`prototype`](../plugins/prototype/README.md) | Wave 3 | `Adapted (mattpocock/skills)` | `skills/engineering/prototype` adapted for Antigravity Artifacts / `generative_ui` instead of OS browser launches. |
| 19 | [`wizard`](../plugins/wizard/README.md) | Wave 3 | `Adapted (mattpocock/skills)` | `skills/engineering/wizard` (interactive bash runbook generator for human-only ops, with `read -rs` secret hygiene). |

---

## 2. Key Architectural & Behavioral Deviations (and Why)

### 2.1 À La Carte Standalone Plugins + Graceful Preflight vs. Monolithic Bundle + `setup-matt-pocock-skills`

* **Upstream pattern:** `mattpocock/skills` installs as one monolithic plugin (`mattpocock-skills`) and expects a per-repo setup pass (`/setup-matt-pocock-skills`) to configure issue-tracker, triage-label, and doc-path preferences across skills that invoke one another via the Claude Code `Skill` tool.
* **Our deviation:** Every plugin under `plugins/<name>/` is completely **standalone** with zero required cross-plugin dependencies and zero mandatory setup wizard. Instead, every skill runs a **self-contained graceful preflight** (probing whether `gh`, `GLOSSARY.md`, `CODING_STANDARDS.md`, `docs/adr/`, or `implementation_plan.md` exist and degrading cleanly when absent). Users who *want* repo scaffolding can opt into [`repo-bootstrap`](../plugins/repo-bootstrap/README.md), but nothing requires it.
* **Why:** Teams adopt agent tooling incrementally. An engineer who only wants `diagnosing-bugs` or `git-guardrails` should be able to enable one plugin in `~/.gemini/config/plugins.json` (`include_only`) and get immediate value on any repo without committing repo-level setup boilerplate first.

### 2.2 4-Tier Knowledge Taxonomy (`<800`-Token `AGENTS.md`) + Optional Review-Only Tier 1.5 `CODING_STANDARDS.md`

* **Upstream pattern:** `retro` evaluates agent friction across 7 diagnostic categories and routes repo-wide coding judgment calls into `CODING_STANDARDS.md` so reviewers enforce them without crowding the implementer.
* **Our deviation:** [`knowledge-governance`](../plugins/knowledge-governance/README.md) embeds Matt's 7 retro categories and review-only `CODING_STANDARDS.md` inside our **4-Tier Knowledge Placement Taxonomy** and **Demotion Highway**:
  * **Tier 0 (`AGENTS.md`, hard `<800`-token ceiling):** Universal Class α/β/γ invariants and navigation pointers only—every candidate must pass the **`/learn` Admission Gate** (*"Why not a test?"*, *"Why not a skill?"*, token budget).
  * **Tier 1 (Progressive Skills):** Subsystem-specific workflows loaded only on demand.
  * **Optional Tier 1.5 (`CODING_STANDARDS.md`, Review-Only):** Read *only* by `code-review`'s Standards subagent, never by the implementer—giving repo-wide judgment calls that cannot be linted a zero-implementer-cost home. Small repos can omit it and rely on the bundled Fowler Smell baseline.
  * **Tier 2 (Automated Test Gates & Linters, `<3s`):** Primary destination of the **Demotion Highway** (*"If a machine can assert it deterministically in <0.3s, never waste prompt tokens on it"*).
  * **Tier 3 (`docs/` & Blueprints):** Deep specs and reference architecture.
* **Why:** Implementers operate under the highest context pressure. Combining the Demotion Highway (pushing mechanical rules into Tier 2 code) with optional Review-Only Tier 1.5 (pushing unlintable style judgments out of Tier 0) keeps `AGENTS.md` permanently lean without losing institutional memory.

### 2.3 Historical ADRs vs. Living Invariants (Complementary Lifecycles)

* **Upstream pattern:** `domain-modeling` captures durable architectural decisions in immutable ADRs gated by three criteria (*hard to reverse* + *surprising without context* + *real trade-off*).
* **Our deviation:** We adopt Matt's 3-criteria ADR gate faithfully in [`domain-modeling`](../plugins/domain-modeling/README.md), while explicitly pairing it with our **Living Document vs. Historical Artifact** taxonomy across [`knowledge-governance`](../plugins/knowledge-governance/README.md) and [`artifact-governance`](../plugins/artifact-governance/README.md):
  * **Historical ADRs (`docs/adr/NNNN-*.md`)** are **immutable museum records** answering *"WHY did we choose X over Y at time $t$?"* (only superseded by a newer ADR; zero normal-turn context cost; consulted during design/architecture reviews so agents stop re-litigating settled trade-offs).
  * **Living Invariants (`AGENTS.md` / Tier 1 / Tier 2)** are **mutable enforceable laws** answering *"WHAT must ALWAYS hold true right now?"* (`Proposed → Active → Under Review → Amended → Demoted → Retired`).
* **Why:** Separating *"why a trade-off was made"* from *"what CI or agents must currently enforce"* prevents ADRs from mutating into stale rulebooks and prevents `AGENTS.md` from filling up with historical narrative.

### 2.4 Harmonizing Ousterhout Deep Modules with a ~500 LOC Soft Trigger + Native Antigravity Artifacts

* **Upstream pattern:** `codebase-design` and `improve-codebase-architecture` promote John Ousterhout's **Deep Modules** (rich behavior behind a small interface) and warn against reflexively splitting files by line count into shallow pass-through wrappers; `improve-codebase-architecture` also renders reports to `/tmp/*.html` and opens them via `xdg-open` / `open`.
* **Our deviation:** [`architecture-review`](../plugins/architecture-review/README.md) preserves Deep Modules as the primary design philosophy (including the Deletion Test, dependency categories, and parallel Design-It-Twice subagents) while making two deliberate refinements:
  1. **Two distinct size guardrails:** Agent markdown ceilings (`<800`-token `AGENTS.md`, concise `SKILL.md` via progressive disclosure) are strictly separated from source-code modularity. In source code, **~500 LOC** serves solely as a **soft *internal* decomposition trigger** to organize cohesive, acyclic internal submodules *behind* a preserved deep public facade—never an excuse to proliferate shallow public wrappers.
  2. **Native Antigravity Artifacts:** Visual before/after module graphs and comparison tables render directly as Antigravity Markdown Artifacts (Mermaid + tables) or `generative_ui` widgets rather than writing `/tmp/*.html` files and spawning OS browser processes (which fail in headless/sandboxed environments and scatter temp files).
* **Why:** Keeping deep external interfaces intact while preventing 2,000-line god files preserves both conceptual simplicity and agent edit locality, and native Artifacts stay durable, inspectable, and sandbox-clean.

### 2.5 Extending 2-Axis `code-review` to 3 Axes (Security + Reality-Check / Zero-Mock Lens)

* **Upstream pattern:** `code-review` runs two parallel read-only subagents (`Standards` + 12 Fowler Smells vs. `Spec`) and reports them side by side without merging or reranking.
* **Our deviation:** [`code-review`](../plugins/code-review/README.md) preserves strict non-merging parallel separation, and strengthens it in two ways distilled from real production reviews:
  1. **Axis 2 (Spec + Reality Check):** Adds a **Zero-Mock / Reality-Check lens** scanning diffs for hardcoded mock responses, silent synthetic fallbacks, swallowed errors, unverified doc claims, and tests exercising local test-file helper stand-ins instead of real production handlers (reinforced in [`tdd`](../plugins/tdd/README.md)).
  2. **Axis 3 (Security):** Adds a dedicated third parallel subagent (`references/security-checklist.md`) auditing auth/trust boundaries, fail-open guards, injection & unsafe DOM sinks (`.innerHTML`, inline `onclick`), SSRF, secrets/crypto, concurrency races, and CI/hook bypasses (gracefully skipped on pure-prose diffs).
* **Why:** Security flaws and "looks-right" synthetic stubs routinely slip past reviewers focused on style or feature checklists. Giving Security its own isolated subagent ensures a critical fail-open guard or XSS sink can never be buried under cosmetic feedback.

### 2.6 Native Antigravity `hooks.json` `git-guardrails` & Sandbox-Aware Fallback

* **Upstream pattern:** `git-guardrails-claude-code` is a setup skill that writes a `jq`/regex bash script into `.claude/settings.json` (`exit 2` on stderr) and hard-blocks **all** `git push` invocations alongside destructive git commands.
* **Our deviation:** [`git-guardrails`](../plugins/git-guardrails/README.md) ships as a self-contained native Antigravity plugin with a plugin-root `hooks.json` (`PreToolUse`, `matcher: "run_command"`) backed by a zero-dependency Python 3 POSIX/bash lexer and git parser (`hooks/guard_git.py`):
  * **`deny` (hard block):** Truly destructive operations (`git push --force`/`-f`/`--force-with-lease`/`--force-if-includes`/`--mirror`/`+refspec`, `git reset --hard`, `git clean -f`, `git branch -D`/`--delete --force`, `git checkout .`, `git restore .`), including inside compound chains, subshells, heredocs, piped shells, and `git submodule foreach`.
  * **`force_ask` (always prompt):** Standard non-force `git push`—bypasses cached "Always Allow" approvals so the human explicitly confirms pushes without forcing them to leave the agent session for every branch push.
  * **`allow` (sandboxed):** Local `git commit`, `git add`, `git status`, `git diff`, and safe sandboxed commands stay fluid.
  * **`ask` (sandbox-aware fallback):** Unsandboxed (`BypassSandbox: true`) non-matching commands or malformed stdin JSON return `ask` instead of `allow`, ensuring the hook can never silently auto-approve an unrelated unsandboxed command.
* **Why:** Blocking routine `git commit` or making non-force `git push` impossible inside Antigravity adds friction without proportional safety, while regex matching over bash strings is trivially bypassed or false-triggers on quoted commit messages. Antigravity's 4-state decision contract (`deny` / `force_ask` / `ask` / `allow`) lets us express the exact risk boundary cleanly.

### 2.7 Context-Window-Aware ~150k Slicing Inside `plan-model-advisor` (Tracker-Agnostic)

* **Upstream pattern:** `to-tickets` and `implement-spec` decompose large specs into vertical tracer-bullet tickets with blocking edges on an external issue tracker (GitHub/GitLab/local files), sized so each slice completes inside one sharp agent context window.
* **Our deviation:** Rather than requiring an external issue tracker for everyday work, we folded the core execution insight—**~150k-token vertical tracer-bullet slicing, task-graph frontier identification, and sparse context pointers**—directly into [`plan-model-advisor`](../plugins/plan-model-advisor/README.md) (v1.2.0), mapped straight onto `implementation_plan.md` milestones and Antigravity `/teamwork` (`swarm`) briefs.
* **Why:** Most Antigravity sessions already plan in `implementation_plan.md` and parallelize via native `swarm` (`workspace: "share"`). Keeping context-budget slicing tracker-agnostic delivers the anti-context-fatigue benefit on day one for solo repos and multi-repo ecosystems alike.

### 2.8 Claude Code → Google Antigravity Mechanical Translation Summary

Every adapted or combined plugin applies this consistent translation checklist so zero Claude Code assumptions leak into Antigravity:

| Mechanism | Claude Code (`mattpocock/skills`) | Google Antigravity (`antigravity-customizations`) |
| :--- | :--- | :--- |
| **Packaging** | Monolithic `.claude-plugin/plugin.json` listing all skills | One standalone `plugins/<name>/plugin.json` per workflow (`suggestedPrompts` ≤ 3) |
| **`SKILL.md` Frontmatter** | Includes `disable-model-invocation`, `user-invocable`, `argument-hint`, `context: fork`, `agent`, `allowed-tools` | Strictly `name` + `description` only (enforced by `scripts/validate_customizations.py`) |
| **Cross-Skill Composition** | `Call the Skill tool with "<name>"` | Bundled progressive-disclosure `references/*.md` + optional companion notes (zero hard coupling) |
| **Lifecycle Hooks** | `.claude/settings.json` (`matcher: "Bash"`, `tool_input.command`, exit code `2`) | Plugin-root `hooks.json` (`matcher: "run_command"`, `toolCall.args.CommandLine`, JSON stdout `deny`/`force_ask`/`ask`/`allow`) |
| **Subagents & Concurrency** | `Agent` tool + manual `git worktree` management | Native `invoke_subagent`, `swarm` (`/teamwork`, `workspace: "inherit"\|"share"\|"branch"`), or `run_workflow` |
| **Visual Outputs** | `/tmp/*.html` + `xdg-open` / `open` | Antigravity Markdown Artifacts (Mermaid + tables) or `generative_ui` |
| **Steering Files** | `CLAUDE.md`, `.claude/` | `AGENTS.md` (`<800` tokens), `~/.gemini/GEMINI.md`, `.agents/` |

---

## 3. Complete 39-Skill Audit of `mattpocock/skills`: Excluded Skills & Why

We audited all **39 skills** in `mattpocock/skills` (27 published in `.claude-plugin/plugin.json` plus 12 under `skills/misc/` and `skills/in-progress/`):

* **13 upstream skills** form the direct upstream base of **12 adapted/combined plugins** in Section 1 (`diagnosing-bugs`, `tdd`, `code-review`, `git-guardrails-claude-code`, `retro`, `writing-for-agents`, `codebase-design` + `improve-codebase-architecture` → `architecture-review`, `pr`, `handoff`, `domain-modeling`, `prototype`, `wizard`).
* **26 upstream skills** were **intentionally excluded as standalone plugins**, grouped below—with explicit credit for the **4 excluded skills whose specific workflow nuances were absorbed** into our remaining 2 combined plugins (`grilling`, `implement-spec`, and `to-tickets` into [`plan-model-advisor`](../plugins/plan-model-advisor/README.md); `research` into [`artifact-governance`](../plugins/artifact-governance/README.md)).
* **Total accounted for:** `13 + 26 = 39 / 39` upstream skills (and `5 Original + 5 Adapted + 9 Combined = 19 / 19` plugins).

### 3.1 Subsumed by Native Antigravity (10 Skills)

| Upstream Skill | Native Antigravity Equivalent | Why Excluded & Targeted Nuance Absorbed |
| :--- | :--- | :--- |
| **`grill-me`** | Native `/grill-me` | Built into Antigravity as a first-class interactive slash command. |
| **`grilling`** | Native `/grill-me` | Reusable interview primitive behind Matt's grilling skills; **nuance absorbed:** the *"explore the codebase first instead of asking questions the code can answer"* rule is captured in [`plan-model-advisor`](../plugins/plan-model-advisor/README.md), [`writing-for-agents`](../plugins/writing-for-agents/README.md), and [`domain-modeling`](../plugins/domain-modeling/README.md). |
| **`grill-with-docs`** | Native `/grill-me` + [`domain-modeling`](../plugins/domain-modeling/README.md) | Composing native `/grill-me` with our standalone `domain-modeling` plugin keeps grilling and glossary/ADR authoring independently adoptable. |
| **`chief-of-staff`** | Native `/goal`, `/teamwork`, `swarm`, `schedule` | Long-running multi-agent goal orchestration and recurring schedules are first-class Antigravity primitives. |
| **`implement`** | Native agent loop + [`tdd`](../plugins/tdd/README.md) + [`code-review`](../plugins/code-review/README.md) | Wrapper orchestrating `/tdd` and `/code-review`; unnecessary once both skills are standalone plugins in our standard protocol. |
| **`implement-spec`** | Native `swarm` (`workspace: "share"`) + `run_workflow` | Antigravity manages concurrent shared workspaces natively; **nuances absorbed:** ~150k vertical slicing, task-graph frontier sequencing, and sparse context pointers are folded into [`plan-model-advisor`](../plugins/plan-model-advisor/README.md) v1.2.0. |
| **`research`** | Built-in `research` subagent + `search_web` | Background web research is built into Antigravity; **nuance absorbed:** *"prefer high-trust primary sources and save durable cited Markdown research notes"* is captured in [`artifact-governance`](../plugins/artifact-governance/README.md). |
| **`claude-handoff`** | [`session-handoff`](../plugins/session-handoff/README.md) + native `/compact` | Relies on Claude Code's CLI-specific `claude --bg` background spawner. We adapted the portable `handoff` skill into `session-handoff` instead so handoffs work across Gemini, Claude, and fresh Antigravity sessions. |
| **`ask-matt`** | Native skill discovery + `plugin.json` `suggestedPrompts` | Router over Matt's monolithic user-invoked skills; replaced by Antigravity's native skill routing and per-plugin `suggestedPrompts`. |
| **`setup-matt-pocock-skills`** | Self-contained graceful preflight + optional [`repo-bootstrap`](../plugins/repo-bootstrap/README.md) | Eliminated mandatory global per-repo configuration in favor of zero-config standalone plugins. |

### 3.2 Issue-Tracker Plumbing Deferred (4 Skills)

| Upstream Skill | What It Does Upstream | Why Deferred |
| :--- | :--- | :--- |
| **`to-spec`** | Synthesizes a conversation into a spec published to an issue tracker. | Our workflow captures specs in repo `docs/` and `implementation_plan.md` ledgers without assuming a GitHub/GitLab issue tracker. |
| **`to-tickets`** | Breaks a spec into tracer-bullet tickets with native blocking edges on a tracker. | Deferred tracker plumbing; **nuance absorbed:** the ~150k-token vertical tracer-bullet slicing and blocking-edge frontier model is built directly into [`plan-model-advisor`](../plugins/plan-model-advisor/README.md) v1.2.0. |
| **`triage`** | Moves tracker issues through a label-driven triage state machine. | Tightly coupled to external issue-tracker label taxonomies and `setup-matt-pocock-skills`. |
| **`wayfinder`** | Plans multi-session epics as a map of decision tickets on an issue tracker. | Deferred alongside tracker plumbing; multi-milestone work currently uses `implementation_plan.md` append-only ledgers + [`session-handoff`](../plugins/session-handoff/README.md). |

### 3.3 TypeScript / Course-Authoring Niche (4 Skills)

| Upstream Skill | What It Does Upstream | Why Excluded |
| :--- | :--- | :--- |
| **`migrate-to-shoehorn`** | Migrates TypeScript test files from `as` casts to `@total-typescript/shoehorn`. | Specific to a single TypeScript testing helper library; out of scope for a stack-agnostic plugin suite. |
| **`scaffold-exercises`** | Scaffolds `XX-section/XX.YY-exercise` directories linted by `ai-hero-cli`. | Purpose-built for Total TypeScript / AI Hero course authoring. |
| **`setup-pre-commit`** | Installs Husky + `lint-staged` + Prettier git pre-commit hooks for JS/TS repos. | Stack-specific JS/TS tooling; Antigravity real-time formatting is handled stack-agnostically by [`workspace-hygiene-hooks`](../plugins/workspace-hygiene-hooks/README.md). |
| **`setup-ts-deep-modules`** | Configures `dependency-cruiser` rules enforcing deep-module entry points in TypeScript packages. | TypeScript-only enforcement setup (in-progress upstream); the stack-agnostic Deep Modules discipline lives in [`architecture-review`](../plugins/architecture-review/README.md). |

### 3.4 Experimental / In-Progress / Situational Prose (8 Skills)

| Upstream Skill | What It Does Upstream | Why Excluded |
| :--- | :--- | :--- |
| **`writing-fragments`** | Exploratory interview mining raw unstructured essay fragments (`skills/in-progress/`). | Long-form prose authoring workflow outside software engineering delivery; marked in-progress upstream. |
| **`writing-beats`** | Assembles raw prose fragments into grounded article beats (`skills/in-progress/`). | Companion to `writing-fragments`; prose-authoring niche, in-progress upstream. |
| **`writing-shape`** | Shapes raw prose fragments into an article paragraph by paragraph (`skills/in-progress/`). | Companion to `writing-fragments`; prose-authoring niche, in-progress upstream. |
| **`loop-me`** | Interviews the user to spec recurring personal/life "loops" into `workflows/*.md` (`skills/in-progress/`). | Experimental personal-workflow mapper; Antigravity already provides native `/schedule` and the built-in `automation` skill. |
| **`software-factory`** | Shared vocabulary for whiteboarding autonomous ticket-to-deploy agent factories (`skills/in-progress/`). | Experimental conceptual vocabulary, not yet a concrete delivery workflow. |
| **`wait-what`** | Re-pitches an unclear agent message in plain English using `GLOSSARY.md`. | Situational conversational prompt easily invoked ad hoc; low ROI as a standalone plugin. |
| **`to-questionnaire`** | Turns a blocking question into an async Markdown questionnaire for a stakeholder. | Situational communication helper outside the core coding/review/release loop. |
| **`teach`** | Multi-session stateful tutoring workspace for learning a new topic. | Educational workflow outside core pair-programming delivery; easy to add later if desired. |

---

## See Also

* [Agentic Pair Programming Protocol](./agentic-pair-programming-protocol.md) — How all 19 plugins and native Antigravity commands chain together end to end.
* [Repository README](../README.md) — Full Plugin Catalog, Quick Start, and MIT License attribution.
