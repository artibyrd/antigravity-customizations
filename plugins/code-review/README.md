# Code Review

An Antigravity plugin that runs a **parallel two-axis diff review** via two fresh read-only subagents (`invoke_subagent`) and presents their findings side by side without merging or reranking:

- **Axis 1 — Standards:** Checks documented repo standards (automatically picking up optional `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`) plus a bundled **12 Fowler Code Smells** baseline (repo overrides baseline; skips linter-enforced rules).
- **Axis 2 — Spec + Reality Check:** Verifies spec fidelity (missing requirements, scope creep, wrong implementation—quoting the spec) alongside a **Reality-Check / Zero-Mock lens** that hunts hardcoded mocks, synthetic fallbacks, stubbed checks, swallowed errors, and unverified doc claims in production paths.

## Why Use It?

- **Strict axis separation:** Clean code that builds the wrong thing fails `## Spec`; accurate behavior that breaks conventions or introduces synthetic fallbacks fails `## Standards` or the Reality-Check lens—neither masks the other.
- **Fresh-context parallel subagents:** Spawns two isolated, read-only reviewers in parallel via `invoke_subagent` so authoring confirmation bias and cross-axis noise stay out of the review.
- **Zero-config graceful preflight:** Works in any git repository—gracefully degrades when `CODING_STANDARDS.md`, a spec document, or `gh` CLI is absent.

## Included Files

- [`skills/code-review/SKILL.md`](./skills/code-review/SKILL.md) — Graceful preflight, parallel `invoke_subagent` review prompts, Reality-Check lens, and strict non-merging aggregation rules.
- [`skills/code-review/references/fowler-smells.md`](./skills/code-review/references/fowler-smells.md) — Progressive-disclosure baseline of 12 Fowler code smells (*Refactoring*, Ch. 3) with override rules.

## Example Prompts

- *"Review my changes since `main` with `code-review`."*
- *"Run a two-axis code review since `HEAD~4` against `implementation_plan.md`."*
- *"Audit this branch diff for Fowler code smells and any hardcoded mocks or silent fallbacks."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** The two-axis Standards vs. Spec review architecture, parallel fresh subagent separation, non-merging aggregation rules, and the 12 Fowler Code Smells baseline are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/code-review`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), Antigravity `invoke_subagent` orchestration (with graceful sequential fallback), progressive disclosure of the 12 Fowler smells into `references/fowler-smells.md`, and complete removal of upstream installer/tracker hard dependencies in favor of graceful preflight (`implementation_plan.md`, `docs/`, optional `gh`).
- **Original Additions & Synthesis:** Extended Axis 2 with our **Reality-Check / Zero-Mock lens** (flagging hardcoded mock data, silent synthetic fallbacks, stubbed telemetry/checks, swallowed errors, and unverified doc/comment claims in production code—active even when no formal spec document exists).
