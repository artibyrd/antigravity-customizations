# Reality Check Audit

An Antigravity plugin for running an adversarial, evidence-backed **"Outsider's Honest Assessment"** across an entire repository, milestone, dashboard, or documentation suite to break single-model and author echo chambers.

Unlike diff-level code review, `reality-check-audit` zooms out to the whole system and asks the hard question: *what here is genuinely working engineering, what is silently drifted or over-engineered, and what is still aspirational?*

## Why Use It?

- **Breaks single-model echo chambers:** Designed to be run on a different model family (or a fresh read-only subagent) than the one that authored the codebase, surfacing blind spots that incremental coding turns miss.
- **Hunts the four classic drift classes:** Systematically checks for (1) mocked/hardcoded telemetry and silent synthetic fallbacks, (2) doc-vs-code drift and projections presented as observed metrics, (3) governance bloat and over-engineering relative to product code, and (4) subtle structural or security assumptions.
- **Anti-false-positive verification discipline:** Requires reading the real implementation, tests, and data before making any accusation—and explicitly retracts or qualifies initial suspicions when deeper code reads disprove them.
- **Structured, actionable output:** Delivers a point-in-time Historical Artifact report flowing cleanly from **What's Genuinely Good → What's Concerning → What's Aspirational vs. Real (table) → Concrete Remediation Plans**.

## Included Files

- [`skills/reality-check-audit/SKILL.md`](./skills/reality-check-audit/SKILL.md) — Scoping preflight, cross-model/fresh-context audit rules, active hunt targets, evidence verification protocol, and the structured Outsider's Honest Assessment report template.

## Example Prompts

- *"Run a `reality-check-audit` across this repo—be brutally honest about what is real vs. aspirational."*
- *"Audit our docs, README claims, and dashboards against the shipped code and produce concrete remediation plans."*
- *"Check whether our governance docs and tooling have grown disproportionate to our actual product code."*

## Origin & Attribution

- **Provenance:** `Original`
- **Author:** Authored natively for Google Antigravity by Arthur Davis (`https://github.com/artibyrd`), generalized from cross-model milestone audit workflows into a standalone, repo-agnostic plugin.
