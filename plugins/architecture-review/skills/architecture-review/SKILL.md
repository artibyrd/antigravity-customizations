---
name: architecture-review
description: >-
  Audits codebase architecture for deep-module refactoring opportunities,
  internal decomposition hygiene (~500 LOC soft trigger), interface design
  trade-offs (Design It Twice), and operational/UI/browser guardrails. Use when
  the user asks to review codebase architecture, deepen shallow modules,
  explore alternative interfaces, decompose oversized files, or audit Justfile,
  DOM-safety, browser-verification, or spec-table ergonomics.
---

# Architecture Review

Surfaces architectural friction and proposes **deepening opportunities**—refactors that turn shallow pass-through modules into **deep modules** with high caller leverage, tight maintainer locality, and clean test surfaces—alongside practical operational and UI verification guardrails.

Read the bundled reference that matches your active task:
- **Always before exploring or proposing refactors:** [references/deep-modules.md](./references/deep-modules.md) for the exact architecture vocabulary (**module**, **interface**, **implementation**, **depth**, **seam**, **adapter**, **leverage**, **locality**), the **Deletion Test**, dependency categories, and how Deep Modules harmonizes with the **~500 LOC soft internal decomposition trigger**.
- **When comparing alternative interfaces for a chosen candidate:** [references/design-it-twice.md](./references/design-it-twice.md) for the parallel `invoke_subagent` Design-It-Twice workflow.
- **When auditing toolchains (`Justfile`), CLIs, web/DOM surfaces, browser tests, or dense spec/hardware docs:** [references/operational-guardrails.md](./references/operational-guardrails.md).

---

## Process

### 1. Scope & Preflight (YAGNI + Domain Context)

Deepening pays back where code actually changes. Decide *where* to inspect before scanning:

1. **Scope:** If the user named a module, subsystem, or pain point, scope to it directly. Otherwise inspect recent git history (`git log --oneline -n 40` and/or `git log --name-only --pretty=format: -n 40`) to find high-churn hotspots and focus there first; widen only if changes are scattered.
2. **Domain & ADR preflight (graceful):** Check for `GLOSSARY.md` (domain nouns for naming seams) and `docs/adr/` (settled trade-offs you should not re-litigate). If either is absent, proceed cleanly without failing.
3. **Load vocabulary:** Read [references/deep-modules.md](./references/deep-modules.md) in full. If the scoped area touches `Justfile` recipes, CLI automation, browser/DOM code, or dense spec tables, read [references/operational-guardrails.md](./references/operational-guardrails.md) as well.

### 2. Explore via a Fresh Read-Only Subagent (`invoke_subagent`)

Spawn a fresh, read-only subagent via `invoke_subagent` (passing the scoped paths, `GLOSSARY.md` terms if present, relevant ADR summaries, and the exact vocabulary from [references/deep-modules.md](./references/deep-modules.md); fall back to an inline pass if `invoke_subagent` is unavailable).

Explore organically for concrete friction rather than rigid checklists:
- Where does understanding one domain concept require bouncing across many tiny pass-through modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where were pure helpers extracted solely for unit testing while real bugs hide in orchestration (lost **locality**)?
- Where do tightly coupled modules leak internals across their **seams**?
- Where does a file exceed **~500 LOC** and need *internal* subpackage decomposition behind a preserved deep external facade (without shattering its public interface into shallow wrappers)?
- Which hotspots are untested or awkward to test through their external interface?
- When operational surfaces are in scope, where do `Justfile` groups, non-interactive flags, zero-mock boundaries, safe DOM construction, Playwright verification, or dense spec tables violate [references/operational-guardrails.md](./references/operational-guardrails.md)?

Apply the **Deletion Test** to every suspected shallow module: if deleting it concentrates complexity across callers, it earns its keep; if complexity vanishes, it is a pass-through candidate.

### 3. Present Candidates as a Visual Antigravity Artifact

Present the survey as an **Antigravity Markdown Artifact** (`architecture_review_<slug>.md` in the conversation artifact directory; or inline / via `generative_ui` if the user asks for an interactive walkthrough) so all visuals render natively in Antigravity instead of writing external temp HTML files or invoking OS browser launchers.

Structure the artifact cleanly with zero filler:

- **Header:** Repository/scope name, date, and a one-line diagram legend (`solid node` = module, `dashed edge` = seam or leakage, `styled/highlighted node` = deepened module). Go straight into candidates.
- **Candidate Cards** (one section per candidate):
  - **Title:** Short action naming the deepening in `GLOSSARY.md` + deep-module terms (e.g., *"Collapse the Order intake pipeline"*).
  - **Metadata line:** Strength badge (`Strong` | `Worth exploring` | `Speculative`) + Dependency category (`in-process` | `local-substitutable` | `ports & adapters` | `mock`).
  - **Files:** Concise monospace list of involved files.
  - **Before / After Visuals:** Render clear Mermaid diagrams (`flowchart`, `sequenceDiagram`, or `classDiagram` — quoting labels with parentheses or brackets, styling leak edges and deep modules with `classDef`) alongside a compact Markdown table comparing before vs. after interface surface, seam placement, and hidden implementation.
  - **Problem:** One crisp sentence stating what hurts.
  - **Solution:** One crisp sentence stating what changes.
  - **Wins:** Short bullets naming gains strictly in glossary terms (*"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"replace 4 shallow wrapper tests with 1 seam suite"*). Avoid vague praise like *"cleaner code"*.
  - **ADR Callout (conditional):** Surface an ADR conflict only when real friction warrants reopening it, using a `> [!WARNING]` block explaining which ADR it contradicts and why reopening is justified.
- **Top Recommendation:** Short closing section naming the single candidate to tackle first and one sentence on why.

**Stop before proposing concrete interfaces.** Ask the user which candidate(s) they want to explore next.

### 4. Interactive Decision Loop & Design It Twice

Once the user selects a candidate:
1. Walk through its constraints, dependency category, seam placement, internal vs. external seams, and which obsolete shallow tests get deleted once seam tests exist. For broad or ambiguous design trees, suggest Antigravity's native `/grill-me`.
2. Keep domain records current inline when warranted:
   - Naming a deepened module after a newly crystallized domain concept? Offer to add or sharpen the term in `GLOSSARY.md`.
   - User rejects a candidate for a durable, load-bearing architectural trade-off? Offer to record a concise Historical ADR (`docs/adr/NNNN-*.md`) so future reviews do not re-litigate it.
3. When ready to design the new module's interface, follow [references/design-it-twice.md](./references/design-it-twice.md) to compare 3+ radically different interface proposals in parallel via `invoke_subagent`.
