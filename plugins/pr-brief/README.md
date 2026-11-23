# PR Brief

An Antigravity plugin for drafting **visual-first pull request descriptions** and **Mk1 Eyeball walkthroughs** that human reviewers can scan and sign off on in minutes instead of wading through walls of boilerplate prose.

## What It Produces

1. **`## Summary` (Smallest Visual First):** Selects the smallest visual from a curated menu—pseudocode, call tree, component tree, shallow file tree, Mermaid diagram, scoped `diff`, or whole block—placed directly beside minimal prose.
2. **`## Evidence` (Before/After Proof + Mk1 Eyeball Walkthrough):** Pairs S-tier visual proof (screenshots/DOM captures) or A-tier execution proof (failing→passing tests, validator runs, live dev/staging probes) with an optional 2–4 step **Mk1 Eyeball Walkthrough** checklist for fast human inspection.
3. **`## Merge Danger` (Door + Blast Radius):** Classifies the change as a **two-way door** (cheap to roll back) or **one-way door** (irreversible/destructive) alongside its concrete **Blast Radius** and potential ramifications.

## Graceful Preflight

- Works cleanly in **any** git repository—with or without `gh` CLI or `GLOSSARY.md`.
- When you ask to create or update a GitHub PR, the skill checks `gh auth status` first; if `gh` is missing, unauthenticated, or offline, it degrades cleanly and outputs copy-ready Markdown without failing.
- Automatically enforces `<REDACTED>` secret hygiene on pasted logs and probe outputs.

## Included Files

- [`skills/pr-brief/SKILL.md`](./skills/pr-brief/SKILL.md) — Preflight workflow, PR body template, evidence tiers, Mk1 Eyeball walkthrough rules, and Merge Danger guidelines.
- [`skills/pr-brief/references/visual-menu.md`](./skills/pr-brief/references/visual-menu.md) — Progressive-disclosure menu of visual shapes (pseudocode, call tree, component tree, file tree, Mermaid, scoped diffs, whole block) and placement guidance.

## Example Prompts

- *"Write a visual-first PR brief for this branch against `main`."*
- *"Generate a copy-ready PR description with Before/After evidence and an Mk1 Eyeball walkthrough."*
- *"Update the current PR body with `pr-brief` and highlight whether this migration is a one-way door."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit (Matt Pocock):** The three-part PR body template (`Summary`, `Evidence` with S-tier/A-tier before/after proof, `Merge Danger` with one-way/two-way door and blast radius) is adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/pr`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Upstream Credit (Dex Horthy / Humanlayer):** The `Summary` visual menu (pseudocode, call trees, component trees, file trees, Mermaid diagrams, scoped diffs, whole blocks) and its placement guidance originate from **[Dex Horthy](https://github.com/dexhorthy)** / **Humanlayer** ([`humanlayer/show-me`](https://github.com/humanlayer/humanlayer) — [`show-me/SKILL.md`](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md)), carried forward with explicit attribution so the plugin remains standalone with zero external skill dependencies.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin (`plugin.json`, strict `name`/`description` `SKILL.md` frontmatter with credits documented in `README.md` and `references/visual-menu.md`), progressive disclosure of the visual menu into `references/visual-menu.md`, and graceful preflight supporting both authenticated `gh` CLI workflows and offline copy-ready Markdown output.
- **Original Additions & Synthesis:** Combined Matt Pocock's and Dex Horthy's visual PR standard with our **Mk1 Eyeball Walkthrough** human sign-off checklist, live dev/staging probe evidence guidance, and `<REDACTED>` secret hygiene before pasting command output.
