# Domain Modeling

An Antigravity plugin for actively building and sharpening a project's domain model as you design—challenging fuzzy terms, cross-referencing claims against code first, updating `GLOSSARY.md` inline with zero implementation details, and recording Historical ADRs sparingly via a strict 3-criteria gate.

Designed to pair naturally with Antigravity's native `/grill-me` command during architectural design sessions.

## Why Use It?

- **Explore-First Discipline:** Inspects the codebase, existing `GLOSSARY.md` / `GLOSSARY-MAP.md`, and `docs/adr/` before asking the user questions the repo can already answer, surfacing contradictions between speech and code immediately.
- **Lazy, Implementation-Free `GLOSSARY.md`:** Creates `GLOSSARY.md` (or multi-context `GLOSSARY-MAP.md` targets) lazily on the first resolved term, updates terms inline the moment they crystallise, lists `_Avoid_` synonyms, and forbids implementation details.
- **Strict 3-Criteria Historical ADR Gate:** Offers an ADR under `docs/adr/NNNN-slug.md` only when a decision is **hard to reverse**, **surprising without context**, AND **the result of a real trade-off**.
- **Historical ADRs vs. Living Invariants:** Clearly separates immutable point-in-time ADRs (*why we chose X over Y*) from mutable enforceable invariants (*what must hold true right now* in `AGENTS.md`, skills, or automated tests).

## Included Files

- [`skills/domain-modeling/SKILL.md`](./skills/domain-modeling/SKILL.md) — Explore-first workflow, inline glossary discipline, 3-criteria ADR gate, Historical ADRs vs. Living Invariants distinction, and `/grill-me` pairing guidance.
- [`skills/domain-modeling/references/glossary-format.md`](./skills/domain-modeling/references/glossary-format.md) — Single-context `GLOSSARY.md` and multi-context `GLOSSARY-MAP.md` format rules.
- [`skills/domain-modeling/references/adr-format.md`](./skills/domain-modeling/references/adr-format.md) — Concise ADR template, sequential numbering, 3-criteria gate examples, and immutability/superseding rules.

## Example Prompts

- *"Use `domain-modeling` to sharpen our domain language against the existing code and update `GLOSSARY.md` inline."*
- *"Evaluate whether switching our event bus passes the 3-criteria ADR gate, and draft the ADR if it qualifies."*
- *"Map our multiple bounded contexts into a `GLOSSARY-MAP.md` and flag conflicting terminology across modules."*

## Origin & Attribution

- **Provenance:** `Adapted (mattpocock/skills)`
- **Upstream Credit:** Adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/domain-modeling`, including `GLOSSARY-FORMAT.md` and `ADR-FORMAT.md`, with the explore-first codebase verification habit echoed from `skills/engineering/grilling`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), bundled progressive-disclosure references under `references/glossary-format.md` and `references/adr-format.md`, explicit pairing guidance for Antigravity's native `/grill-me` command, and an explicit boundary table distinguishing **Historical ADRs** from **Living Invariants**.
