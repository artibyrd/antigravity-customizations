# Code Review

An Antigravity plugin that runs a **parallel three-axis diff review** via three fresh read-only subagents (`invoke_subagent`) and presents their findings side by side without merging or reranking:

- **Axis 1 — Standards:** Checks documented repo standards (automatically picking up optional `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`) plus a bundled **12 Fowler Code Smells** baseline (repo overrides baseline; skips linter-enforced rules).
- **Axis 2 — Spec + Reality Check:** Verifies spec fidelity (missing requirements, scope creep, wrong implementation—quoting the spec) alongside a **Reality-Check / Zero-Mock lens** that hunts hardcoded mocks, synthetic fallbacks, stubbed checks, swallowed errors, test-file helper stand-ins, and unverified doc claims.
- **Axis 3 — Security:** Audits concrete, exploitable weaknesses across auth/trust boundaries, fail-open guards, injection & unsafe DOM sinks (`.innerHTML`, inline `onclick`), SSRF & untrusted ingestion, secrets/crypto, concurrency races, and CI/hook bypasses (gracefully skipping pure-prose diffs).

## Why Use It?

- **Strict axis separation:** Clean, secure code that builds the wrong thing fails `## Spec`; accurate behavior that breaks conventions fails `## Standards`; spec-faithful, idiomatic code with an XSS sink or fail-open guard fails `## Security`—no axis masks another.
- **Fresh-context parallel subagents:** Spawns three isolated, read-only reviewers in parallel via `invoke_subagent` so authoring confirmation bias and cross-axis noise stay out of the review.
- **Zero-config graceful preflight:** Works in any git repository—gracefully degrades when `CODING_STANDARDS.md`, a spec document, or `gh` CLI is absent.

## Included Files

- [`skills/code-review/SKILL.md`](./skills/code-review/SKILL.md) — Graceful preflight, parallel `invoke_subagent` three-axis prompts, Reality-Check lens, and strict non-merging aggregation rules.
- [`skills/code-review/references/fowler-smells.md`](./skills/code-review/references/fowler-smells.md) — Progressive-disclosure baseline of 12 Fowler code smells (*Refactoring*, Ch. 3) with override rules.
- [`skills/code-review/references/security-checklist.md`](./skills/code-review/references/security-checklist.md) — Progressive-disclosure security checklist for Axis 3 (trust boundaries, injection/DOM sinks, SSRF, secrets/crypto, races, CI/hooks).

## Example Prompts

- *"Review my changes since `main` with `code-review`."*
- *"Run a three-axis code review since `HEAD~4` against `implementation_plan.md`."*
- *"Audit this branch diff for Fowler code smells, hardcoded mocks, and security vulnerabilities."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** The multi-axis Standards vs. Spec review architecture, parallel fresh subagent separation, non-merging aggregation rules, and the 12 Fowler Code Smells baseline are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/code-review`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), Antigravity `invoke_subagent` orchestration (with graceful sequential fallback), progressive disclosure of reference checklists under `references/`, and complete removal of upstream installer/tracker hard dependencies in favor of graceful preflight (`implementation_plan.md`, `docs/`, optional `gh`).
- **Original Additions & Synthesis:**
  - Extended Axis 2 with our **Reality-Check / Zero-Mock lens** (flagging hardcoded mocks, silent synthetic fallbacks, stubbed checks, swallowed errors, unverified doc claims, and tests exercising local test-file stand-ins instead of real production handlers).
  - Added **Axis 3 — Security** (`references/security-checklist.md`) as a dedicated parallel subagent so security defects cannot be buried under style or spec feedback.
