# Session Handoff

An Antigravity plugin that compacts the current conversation into a crisp, zero-fluff handoff artifact (`handoff_<slug>.md`) optimized for **cross-model** (e.g., Gemini in Antigravity → fresh Claude session) and **fresh-session** continuations.

## Why Use It?

- **Sparse context pointers, never pasted blobs:** References authoritative plans, ADRs, commits, branches, and file line ranges instead of duplicating large files or diffs.
- **Preserves settled decisions and dead ends:** Stops the next model from re-litigating locked-in design choices or repeating failed experiments.
- **Grounded in live workspace state:** Captures exact branch, `HEAD` commit SHA, uncommitted changes, and concrete pass/fail verification status before handing off.
- **Zero repo pollution:** Writes `handoff_<slug>.md` to the Antigravity artifact directory (with inline chat or OS temp fallback) and redacts secrets/PII with `<REDACTED>`.

## Included Files

- [`skills/session-handoff/SKILL.md`](./skills/session-handoff/SKILL.md) — Live state preflight, secret redaction, sparse-pointer rules, structured `handoff_<slug>.md` template, and copy-ready starter prompt delivery.

## Example Prompts

- *"Create a `session-handoff` artifact so a fresh Claude session can pick up the remaining audit work."*
- *"Compact this session into a handoff brief focused on Phase 2 verification."*
- *"Write a cross-model handoff capturing our current git state, settled decisions, and exact next step."*

## Origin & Attribution

- **Provenance:** `Adapted (mattpocock/skills)`
- **Upstream Credit:** Adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/productivity/handoff`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin (`plugin.json`, strict `name`/`description` `SKILL.md` frontmatter stripping Claude Code–only keys), replaced Claude Code cross-skill invocation instructions with Antigravity-native skill/workflow recommendations, defaults output to `handoff_<slug>.md` in the Antigravity artifact directory (with chat and OS temp fallbacks so the git workspace stays clean), and structures the brief explicitly for Antigravity ↔ cross-model / fresh-session handoffs (live git preflight, settled decisions, dead ends, verification state, and a copy-ready starter prompt).
