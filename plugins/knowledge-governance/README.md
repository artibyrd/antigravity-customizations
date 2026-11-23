# Knowledge Governance

An Antigravity plugin that prevents `AGENTS.md` bloat and attention dilution by routing operational rules, `/learn` proposals, and session retrospective findings to the lowest-cost cognitive tier.

## Why Use It?

- **4-Tier Knowledge Placement Taxonomy:** Routes rules cleanly across Tier 0 (`AGENTS.md`, <800-token hard ceiling with Class α/β/γ hierarchy), Tier 1 (on-demand subsystem skills), optional review-only Tier 1.5 (`CODING_STANDARDS.md`), Tier 2 (fast shift-left automated test gates & linters), and Tier 3 (`docs/` blueprints).
- **The Demotion Highway:** *"If a machine can assert it deterministically in <0.3s, never waste prompt tokens on it."* Graduates mechanical rules out of `AGENTS.md` into deterministic tests and linters.
- **`/learn` Admission Gate & Invariant Challenger:** Requires every candidate Tier 0 rule to pass *"Why not a test?"*, *"Why not a skill?"*, and token-budget (`<800`) checks, and provides `PRESERVE` / `DEMOTE` / `AMEND` / `NULLIFY` audit dispositions.
- **Living Invariants vs. Historical ADRs:** Keeps mutable enforceable laws cleanly separated from immutable point-in-time architecture decision records.
- **7-Category Session Retrospectives:** Audits finished sessions across `Navigation`, `Automated checks`, `Coding standards`, `Global AGENTS.md`, `Tool economy`, `No-ops`, and `Information access`, ranked by severity.

## Included Files

- [`skills/knowledge-governance/SKILL.md`](./skills/knowledge-governance/SKILL.md) — Core 4-tier taxonomy, Demotion Highway, `/learn` Admission Gate, Invariant Challenger, and Living Invariants vs. ADRs guide.
- [`skills/knowledge-governance/references/retro-checklist.md`](./skills/knowledge-governance/references/retro-checklist.md) — Progressive-disclosure reference with the 7 retrospective diagnostic categories and severity-ranking guidance.

## Example Prompts

- *"Audit our `AGENTS.md` with `knowledge-governance` and list Demotion Highway candidates."*
- *"Route these `/learn` lessons through the Knowledge Admission Gate before editing any steering files."*
- *"Run a session retrospective across the 7 diagnostic categories and rank improvements by severity."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** The 7 session-retrospective diagnostic categories, the Implementation vs. Review context-pressure model, and the optional review-only `CODING_STANDARDS.md` pattern are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/retro`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only—stripping Claude Code–specific frontmatter keys), removed cross-skill invocation dependencies, mapped steering-file guidance to `AGENTS.md` and `~/.gemini/GEMINI.md`, and placed the 7 retrospective diagnostic categories in a bundled progressive-disclosure reference (`references/retro-checklist.md`).
- **Original Additions & Synthesis:** Combined with our original 4-Tier Knowledge Placement Taxonomy (Class α/β/γ `<800`-token `AGENTS.md` ceiling, Tier 1 Progressive Skills, Tier 2 Shift-Left Test Gates, Tier 3 Docs), the Demotion Highway & Invariant Lifecycle state machine, the 3-part `/learn` Admission Gate, the 4-disposition Invariant Challenger (`PRESERVE` / `DEMOTE` / `AMEND` / `NULLIFY`), and the Living Invariants vs. Historical ADRs separation—positioning `CODING_STANDARDS.md` as an optional review-only Tier 1.5 layer.
