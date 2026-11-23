# Diagnosing Bugs

An Antigravity plugin enforcing a 6-phase disciplined diagnosis loop for hard bugs, intermittent flakes, and performance regressions—requiring a tight, red-capable feedback loop before forming a single hypothesis.

## The 6-Phase Loop

1. **Build a tight, red-capable feedback loop:** Construct the fastest deterministic command that reproduces the exact user symptom (failing seam test, curl/CLI harness, headless browser script, trace replay, fuzz/bisect loop, or the bundled HITL template as a last resort).
2. **Reproduce + minimise:** Confirm the exact symptom and strip inputs/steps one by one until every remaining element is load-bearing.
3. **Hypothesise:** Generate 3–5 ranked, falsifiable hypotheses with explicit predictions and surface them before testing.
4. **Instrument:** Test one variable at a time with debugger/REPL or uniquely tagged `[DEBUG-xxxx]` probes (or baseline timing + bisection for performance regressions).
5. **Fix + regression test:** Lock down a failing regression test at the real seam before applying the fix, then re-verify against the original un-minimised loop.
6. **Cleanup:** Re-verify green, `grep` out all `[DEBUG-...]` tags, remove throwaway harnesses, and record the winning root-cause hypothesis in the commit/PR message.

## Included Files

- [`skills/diagnosing-bugs/SKILL.md`](./skills/diagnosing-bugs/SKILL.md) — Complete 6-phase diagnosis discipline with `<REDACTED>` secret hygiene and optional `GLOSSARY.md` / ADR awareness.
- [`skills/diagnosing-bugs/scripts/hitl-loop.template.sh`](./skills/diagnosing-bugs/scripts/hitl-loop.template.sh) — Executable human-in-the-loop bash template for bugs that require manual UI interaction.

## Example Prompts

- *"Diagnose why checkout retries are double-charging—start by building a tight red-capable feedback loop."*
- *"Debug this intermittent test flake and raise its reproduction rate before proposing fixes."*
- *"Diagnose this API latency regression with a timing baseline and bisection harness."*

## Origin & Attribution

- **Provenance:** `Adapted (mattpocock/skills)`
- **Upstream Credit:** Adapted directly from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/diagnosing-bugs`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict Antigravity `SKILL.md` frontmatter (`name` + `description` only), bundled relative link to executable `scripts/hitl-loop.template.sh`, and graceful preflight wording for optional `GLOSSARY.md` and `docs/adr/` files.
- **Behavioral Changes:** Preserves Matt's 6-phase workflow, `<REDACTED>` secret hygiene, `[DEBUG-xxxx]` probe tagging, seam regression test discipline, and HITL loop template faithfully with no behavioral alterations.
