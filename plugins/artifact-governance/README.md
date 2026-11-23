# Artifact Governance

An Antigravity plugin that protects institutional memory across long-running sessions by classifying documents into Living Documents vs. Historical Artifacts, enforcing an append-only ledger protocol for master plans and walkthroughs, keeping scratch work tidy, and capturing cited primary-source research notes.

## Why Use It?

- **Living Document vs. Historical Artifact Taxonomy:** Tags every artifact explicitly as either a mutable **Living Document** (*"It's alive!"*) or an immutable **Historical Artifact** (*"That belongs in a museum!"*) so point-in-time records are never silently rewritten and active references do not drift.
- **Append-Only Ledger Protocol:** Prevents context-window-boundary plan clobbering by requiring a tail pre-read of `implementation_plan.md` and `walkthrough.md` to locate Milestone $M$, appending `# Milestone M+1` via `Append: true` or surgical tail edits (never blind `Overwrite: true`), routing independent follow-ups to dedicated `<topic>_implementation_plan.md` files, and providing a `transcript_full.jsonl` recovery procedure if history is ever overwritten.
- **Clean Scratch Script Ritual:** Eliminates fragile inline `python -c` / shell one-liner blobs in favor of readable scripts under the Antigravity scratch directory, keeping repository working trees clean.
- **Primary-Source Research Notes:** Delegates deep reading to a fresh-context background subagent (`invoke_subagent`) that verifies claims against primary sources (official docs, specs, source code) and saves durable, cited Markdown notes.

## Included Files

- [`skills/artifact-governance/SKILL.md`](./skills/artifact-governance/SKILL.md) — Complete artifact lifecycle taxonomy, badges, Append-Only Ledger Protocol, `transcript_full.jsonl` recovery procedure, Clean Scratch Script Ritual, and Primary-Source Research Notes workflow.

## Example Prompts

- *"Append Milestone 4 to `implementation_plan.md` following `artifact-governance` without clobbering earlier milestones."*
- *"Create a dedicated `<topic>_implementation_plan.md` for this pre-merge remediation so we preserve the master plan."*
- *"Research the target SDK's rate-limit contract against primary sources and save cited Markdown research notes."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** The fresh-context primary-source verification and cited Markdown research-note capture pattern is adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/research`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), Antigravity `invoke_subagent` delegation for research passes, and native Antigravity artifact/scratch/transcript directory conventions (`<appDataDir>/brain/<conversation-id>/`).
- **Original Additions & Synthesis:** Synthesized with our original Living Document (*"It's alive!"*) vs. Historical Artifact (*"That belongs in a museum!"*) badge taxonomy, the Append-Only Ledger Protocol for `implementation_plan.md` and `walkthrough.md` (mandatory tail pre-read, `# Milestone M+1` appending, dedicated topic artifacts, and `transcript_full.jsonl` recovery), and the Clean Scratch Script Ritual.
