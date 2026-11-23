# Architecture Review

An Antigravity plugin for surveying codebase hotspots, deepening shallow modules behind clean seams, exploring radically different interfaces in parallel, and auditing operational, DOM-safety, and browser-verification guardrails.

## Why Use It?

- **Ousterhout Deep Modules Vocabulary:** Grounds every review in precise shared language (`module`, `interface`, `implementation`, `depth`, `seam`, `adapter`, `leverage`, `locality`), the **Deletion Test**, dependency categories, and replace-don't-layer seam testing.
- **Deep Modules + ~500 LOC Harmony:** Explicitly separates agent markdown context ceilings (`<800`-token `AGENTS.md`) from source-code modularity—using **~500 LOC** as a soft *internal* decomposition trigger behind a preserved deep external facade rather than splintering code into shallow public wrappers.
- **Visual Antigravity Markdown Artifacts:** Produces crisp before/after Mermaid diagrams and comparison tables inside Antigravity Markdown Artifacts (or `generative_ui`)—zero throwaway `/tmp/*.html` files or OS browser launchers.
- **Design It Twice (`invoke_subagent`):** Spawns 3+ fresh parallel subagents with distinct design constraints to compare alternative module interfaces on depth, locality, and seam placement before you commit to one.
- **Operational & UI Verification Guardrails:** Bundles practical checks for modular `Justfile` safe/gated groups, non-interactive CLI flags, zero-mock fail-closed UIs, safe DOM construction, Playwright lazy-image scroll verification, and plain-English + Minimum/Recommended hardware spec tables.

## Included Files

- [`skills/architecture-review/SKILL.md`](./skills/architecture-review/SKILL.md) — End-to-end hotspot survey, fresh subagent exploration, Antigravity Markdown Artifact report format, and interactive decision loop.
- [`skills/architecture-review/references/deep-modules.md`](./skills/architecture-review/references/deep-modules.md) — Shared Deep Modules glossary, principles, ~500 LOC internal decomposition harmony, dependency categories, seam discipline, and replace-don't-layer testing.
- [`skills/architecture-review/references/design-it-twice.md`](./skills/architecture-review/references/design-it-twice.md) — Parallel `invoke_subagent` Design-It-Twice interface comparison workflow.
- [`skills/architecture-review/references/operational-guardrails.md`](./skills/architecture-review/references/operational-guardrails.md) — Generalized `Justfile`, non-interactive CLI, zero-mock, safe DOM, Playwright browser verification, and spec-table clarity guardrails.

## Example Prompts

- *"Survey recent git hotspots for deep-module refactoring candidates and produce a visual artifact."*
- *"Run Design It Twice with parallel subagents to compare interface designs for this module."*
- *"Audit our Justfile, web UI, and browser tests against operational and DOM-safety guardrails."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** The Deep Modules vocabulary and principles (`DEEPENING.md`, `DESIGN-IT-TWICE.md`, deletion test, dependency categories, replace-don't-layer testing) and the YAGNI `git log` hotspot architecture survey workflow are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/codebase-design` and `skills/engineering/improve-codebase-architecture`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only—stripping Claude-only frontmatter keys), replaced cross-skill invocations with bundled progressive-disclosure `references/`, mapped subagent exploration and Design-It-Twice onto Antigravity `invoke_subagent`, replaced `/tmp/*.html` + `xdg-open` reports with native Antigravity Markdown Artifacts (Mermaid + tables) / `generative_ui`, and paired the interactive decision loop with native `/grill-me` and graceful `GLOSSARY.md` / `docs/adr/` preflight.
- **Original Additions & Synthesis:**
  - Harmonized Ousterhout Deep Modules with our **~500 LOC soft internal decomposition trigger** (keeping internal submodules acyclic behind a deep external facade) while distinguishing source-code modularity from agent markdown context ceilings (`<800`-token `AGENTS.md`).
  - Added [`references/operational-guardrails.md`](./skills/architecture-review/references/operational-guardrails.md) synthesizing our generalized operational & UI architecture standards: modular `Justfile` safe vs. gated groups + `[confirm(...)]` + Point-of-Action Guidance Banners, non-interactive CLI flags, zero-mock production boundary & fail-closed empty states, safe DOM construction (`createElement` + `.textContent` + URL scheme allowlisting), the Automated Browser Verification Gate (including Playwright lazy-image `scrollIntoView()` verification), and plain-English companion explanations with separated Minimum vs. Recommended hardware rows.
