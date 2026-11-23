# Test-Driven Development

An Antigravity plugin for disciplined **vertical-slice red → green TDD** at pre-agreed public seams, paired with **hermetic offline testing guardrails** so tests stay fast, deterministic, and refactor-proof.

## Why Use It?

- **Planning-time seam & vertical-slice alignment (Phase A):** Works right alongside `/plan` to list candidate public seams (with what each catches and misses), validate deep-module interface shapes, and write vertical behavioral slices into `implementation_plan.md` *before* coding or launching `/teamwork` swarm workers.
- **Vertical tracer-bullet execution (Phase B):** Drives one failing test → one minimal implementation at a time against those agreed seams (with inline seam agreement for quick ad-hoc fixes), rejecting horizontal test-everything-first batches.
- **Anti-pattern defense:** Actively blocks implementation-coupled mocks, side-channel storage assertions, tautological expectations, and test-file helper stand-ins that re-implement production logic.
- **Hermetic testing boundary:** Enforces fast, deterministic, offline execution (pinned clocks, seeded RNG, isolated temp dirs / in-memory fakes) while restricting doubles strictly to external system boundaries.

## Included Files

- [`skills/tdd/SKILL.md`](./skills/tdd/SKILL.md) — Two-phase TDD contract (planning-time seam/slice design + execution-time red → green loop), hermetic testing boundary, and anti-pattern catalog.
- [`skills/tdd/references/tests.md`](./skills/tdd/references/tests.md) — Concrete good vs. bad test examples (seam tests, implementation-coupled traps, tautologies, and flakiness).
- [`skills/tdd/references/mocking.md`](./skills/tdd/references/mocking.md) — Boundary-only mocking guidelines, dependency injection, narrow SDK adapters, and in-memory fakes.

## Example Prompts

- *"Plan Milestone 2 with `/plan` and `tdd`—propose the public test seams and vertical slices first."*
- *"Implement Milestone 2 with `tdd` against the seams agreed in `implementation_plan.md`."*
- *"Write a failing seam-level regression test for this bug, then apply the minimal fix."*
- *"Review this test suite against `tdd` for implementation-coupled mocks or tautological assertions."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** Core vertical-slice seam TDD workflow, anti-pattern catalog, and supporting `tests.md` / `mocking.md` examples are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/tdd`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), bundled supporting docs under `skills/tdd/references/`, removed cross-plugin skill-tool dependencies (inlining concise deep-module seam checks directly), and added graceful preflight for optional `GLOSSARY.md` and `docs/adr/` files.
- **Original Additions & Synthesis:** Extended upstream's execution-only TDD trigger into a **two-phase Planning + Execution split** (pinning public seams and vertical behavioral slices in `implementation_plan.md` during Stage 2 so implementers and autonomous `/teamwork` swarm workers never fight a horizontal plan or stall mid-swarm), combined with our **Hermetic Testing Boundary** discipline (deterministic offline execution, pinned clocks/seeded RNG, real local seams/in-memory fakes, and zero test-file helper stand-ins or synthetic stubbing of core domain logic).
