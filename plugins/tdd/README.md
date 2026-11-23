# Test-Driven Development

An Antigravity plugin for disciplined **vertical-slice red → green TDD** at pre-agreed public seams, paired with **hermetic offline testing guardrails** so tests stay fast, deterministic, and refactor-proof.

## Why Use It?

- **Pre-agreed seams:** Lists candidate public seams (with what each catches and misses) and aligns with the user *before* writing tests, keeping coverage focused on critical behavior instead of private internals.
- **Vertical tracer-bullet slices:** Rejects horizontal test-everything-first batches in favor of one failing test → one minimal implementation → repeat.
- **Anti-pattern defense:** Actively blocks implementation-coupled mocks, side-channel storage assertions, and tautological expectations.
- **Hermetic testing boundary:** Enforces fast, deterministic, offline execution (pinned clocks, seeded RNG, isolated temp dirs / in-memory fakes) while restricting doubles strictly to external system boundaries.

## Included Files

- [`skills/tdd/SKILL.md`](./skills/tdd/SKILL.md) — Core seam-first TDD rules, hermetic testing boundary, anti-patterns, and loop discipline.
- [`skills/tdd/references/tests.md`](./skills/tdd/references/tests.md) — Concrete good vs. bad test examples (seam tests, implementation-coupled traps, tautologies, and flakiness).
- [`skills/tdd/references/mocking.md`](./skills/tdd/references/mocking.md) — Boundary-only mocking guidelines, dependency injection, narrow SDK adapters, and in-memory fakes.

## Example Prompts

- *"Implement this endpoint with `tdd`—list the proposed seams first before writing tests."*
- *"Write a failing seam-level regression test for this edge case, then apply the minimal fix."*
- *"Review this test suite against `tdd` for implementation-coupled mocks or tautological assertions."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** Core vertical-slice seam TDD workflow, anti-pattern catalog, and supporting `tests.md` / `mocking.md` examples are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/tdd`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), bundled supporting docs under `skills/tdd/references/`, removed cross-plugin skill-tool dependencies (inlining concise deep-module seam checks directly), and added graceful preflight for optional `GLOSSARY.md` and `docs/adr/` files.
- **Original Additions & Synthesis:** Combined with our **Hermetic Testing Boundary** discipline (deterministic offline execution, pinned clocks/seeded RNG, preference for real local seams and in-memory fakes over mock frameworks, and zero synthetic stubbing of core domain logic under test).
