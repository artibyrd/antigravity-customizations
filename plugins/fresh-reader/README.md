# Fresh Reader

An Antigravity plugin that catches **curse-of-knowledge blindness** in documentation by spawning a cold-start, read-only subagent (`invoke_subagent`) with zero session context to read your docs as a first-time visitor—then triaging **100%** of its findings with discernment until every concern is answered and verified.

## Why Use It?

- **Exposes hidden context assumptions:** An agent that just built a feature or wrote a spec has the whole mental model loaded in context, so dense jargon, missing "how do I actually use this?" steps, and unexplained internal terms look obvious to it—and baffling to a newcomer.
- **100% Addressed, Not 100% Satisfied:** Fresh readers inevitably surface some false positives (standard industry terms, intentional progressive disclosure, or out-of-scope requests). Rather than blindly rewriting until the reader is "100% happy" or artificially capping passes and missing new bugs introduced by edits, the coordinator explicitly triages **every** finding into `ACCEPT`, `LINK, DON'T INLINE`, or `WON'T DO (<rationale>)`.
- **Natural Zero-Edit Convergence:** Every pass that edits a document triggers a fresh cold-start re-check to ensure the edits themselves didn't introduce *new* confusions. Previously answered `WON'T DO` items are deduplicated against a cumulative ledger, so the loop terminates cleanly the moment a pass produces zero new edits.
- **Optional `domain-modeling` / `GLOSSARY.md` Pairing:** Works standalone with zero dependencies, and pairs naturally with `domain-modeling`—run a glossary-assisted cold-start pass to test whether `GLOSSARY.md` actually makes your docs clear to newcomers, and route newly surfaced domain jargon into `GLOSSARY.md` during triage rather than duplicating definitions across docs.

## Included Files

- [`skills/fresh-reader/SKILL.md`](./skills/fresh-reader/SKILL.md) — Audience setup, pure cold-start `invoke_subagent` brief, 100%-addressed Discernment Triage Gate, cumulative `WON'T DO` ledger, zero-edit convergence loop, and oscillation tie-breaker.

## Example Prompts

- *"Run `fresh-reader` on `README.md` and `docs/` assuming an experienced developer visiting the repo for the first time."*
- *"Use `fresh-reader` to audit this onboarding guide and show me the triage table of fixes and dismissed false positives."*
- *"Check if `docs/architecture.md` explains how to actually use these tools, not just what they do."*

## Origin & Attribution

- **Provenance:** `Original`
- **Design Background:** Authored natively for Google Antigravity from real-world lessons running cold-start documentation reviewers—specifically pairing uncapped cold-start discovery with a cumulative `WON'T DO` ledger so every concern is answered without infinite nitpick loops or unverified follow-up edits.
