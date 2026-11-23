# Fresh Reader

An Antigravity plugin that catches **curse-of-knowledge blindness** and **technical precision gaps** in documentation by spawning zero-context, read-only subagents (`invoke_subagent`) calibrated to four explicit reader personas—running a **Top-Down Cascade Sieve** and triaging **100%** of findings with discernment until natural zero-edit convergence.

## Why Use It?

- **Four Calibrated Reader Personas:** Not every document shares the same audience. `fresh-reader` supports **`vibe-coder`** (no coding experience), **`junior-engineer`** (knows a language & basic Git/CLI, lacks architecture/testing/workflow depth), **`senior-engineer`** *(default — experienced developer hunting project jargon & contradictions)*, and **`domain-expert`** (specialist rigor lens for math, formal specs, or deep technical articles).
- **Top-Down Cascade Sieve (Accuracy First, Accessibility Second):** Writing docs that are *both* technically accurate and easy to understand is deceptively hard. Running a single pass directly at a novice level lets vocabulary noise drown out structural contradictions; running bottom-up floods technical docs with false positives. Instead, `fresh-reader` cascades **top-down** (`senior-engineer` → `junior-engineer` → `vibe-coder`, stopping at your target tier, or `domain-expert` first for rigorous specialist docs), verifying structural accuracy before bridging conceptual accessibility—with persona-scoped `WON'T DO` carryover so a `senior-engineer` dismissal never silences a `junior-engineer` flagging unfamiliar jargon.
- **100% Addressed, Not 100% Satisfied:** Every single finding gets an explicit disposition (`ACCEPT`, `LINK, DON'T INLINE`, `WON'T DO (<rationale>)`, or `ALREADY DISMISSED`) in a cumulative ledger—no arbitrary pass caps or finding caps that miss regressions introduced by earlier edits.
- **Natural Zero-Edit Convergence:** Every edit pass is re-verified by a fresh unbiased cold-start reader until a sieve produces zero new edits, plus an accuracy sanity check if lower-tier accessibility edits substantially rewrite technical claims.
- **Optional `domain-modeling` / `GLOSSARY.md` Pairing:** Works standalone with zero dependencies, and pairs naturally with `domain-modeling`—run a glossary-assisted cold-start pass to stress-test `GLOSSARY.md` and route newly surfaced domain terms into `GLOSSARY.md` rather than duplicating definitions across docs.

## Included Files

- [`skills/fresh-reader/SKILL.md`](./skills/fresh-reader/SKILL.md) — Top-down cascade workflow, pure cold-start `invoke_subagent` brief, 100%-addressed Discernment Triage Gate, persona-scoped dismissal ledger, zero-edit convergence loop, and oscillation tie-breaker.
- [`skills/fresh-reader/references/reader-personas.md`](./skills/fresh-reader/references/reader-personas.md) — Definitions, baseline assumptions, cascade sequences, carryover rules, and brief snippets for `vibe-coder`, `junior-engineer`, `senior-engineer`, and `domain-expert`.

## Example Prompts

- *"Run `fresh-reader` on `README.md` and `docs/guide.md` targeting `junior-engineer` via the top-down cascade."*
- *"Audit `docs/math-spec.md` with `fresh-reader` at `domain-expert` rigor and show me the full triage table."*
- *"Cascade `fresh-reader` down to `vibe-coder` on our getting-started guide so someone with zero coding background can follow it."*
- *"Run a glossary-assisted `fresh-reader` pass on `docs/architecture.md` alongside `GLOSSARY.md`."*

## Origin & Attribution

- **Provenance:** `Original`
- **Design Background:** Authored natively for Google Antigravity from real-world lessons reviewing progressive-depth technical documentation—combining uncapped cold-start discovery, a persona-scoped `WON'T DO` ledger, natural zero-edit convergence, and top-down multi-tier sieving so documentation stays both technically sound and approachable for its intended audience.
