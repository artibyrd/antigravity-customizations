# Prototype

An Antigravity plugin for building **throwaway prototypes that answer one concrete design question fast**—before committing to production architecture or spending a day debating abstract mockups.

## Two Prototype Shapes

The question decides the shape:

1. **Logic / State-Model Prototype ([`references/logic.md`](./skills/prototype/references/logic.md)):** Answers *"Does this logic, data shape, or state machine feel right?"* Produces a single, zero-dependency, self-contained HTML file with a pure liftable logic module, a readable domain-language state panel, free-play action buttons, and tabbed guided walkthroughs covering happy paths, edge cases, and illegal transitions.
2. **UI Variation Prototype ([`references/ui.md`](./skills/prototype/references/ui.md)):** Answers *"What should this look like?"* Generates 3–5 structurally different UI variations (layout, hierarchy, primary affordance—not color tweaks) switchable via `?variant=` and a floating bottom bar with `←`/`→` keyboard shortcuts and production-build hiding.

## Antigravity Workflow Highlights

- **Zero Repo-Root Pollution:** Standalone single-file HTML prototypes are saved to the session scratch/artifact directory (or rendered inline via Antigravity's built-in `generative_ui` skill / browser preview) instead of dropping throwaway HTML files in the repository root or assuming `open`/`xdg-open`.
- **Clean Before Committing:** Fold the validated decision (or pure lifted logic module) into production code and remove all throwaway prototype routes, losing variants, and switchers from the working tree before committing.

## Included Files

- [`skills/prototype/SKILL.md`](./skills/prototype/SKILL.md) — Branch selection, 6 universal prototype rules, and Antigravity scratch/artifact + cleanup discipline.
- [`skills/prototype/references/logic.md`](./skills/prototype/references/logic.md) — Single-file interactive HTML logic & state-machine prototype workflow and anti-patterns.
- [`skills/prototype/references/ui.md`](./skills/prototype/references/ui.md) — Toggleable multi-variant UI prototype workflow (Sub-shape A existing route vs. Sub-shape B throwaway route/artifact), floating switcher spec, and anti-patterns.

## Example Prompts

- *"Build a throwaway single-file HTML logic prototype so we can click through this order cancellation state machine."*
- *"Show me 3 radically different UI layouts for the settings page with a floating variant switcher."*
- *"Prototype this permission-escalation workflow in an interactive demo before we write backend code."*

## Origin & Attribution

- **Provenance:** `Adapted (mattpocock/skills)`
- **Upstream Credit:** Adapted directly from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/prototype` — `SKILL.md`, `LOGIC.md`, `UI.md`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin (`plugin.json` with `suggestedPrompts <= 3`, strict `name`/`description`-only `SKILL.md` frontmatter, `LOGIC.md`/`UI.md` organized under `references/logic.md` and `references/ui.md`). Saves standalone single-file HTML prototypes in the session scratch/artifact directory (or renders via Antigravity's `generative_ui` skill / clickable `file://` link / browser preview) rather than polluting the repository root or assuming `open`/`xdg-open`, and explicitly cleans up in-repo throwaway files before committing.
- **Behavioral Changes:** Preserves Matt's two-branch mental model, pure liftable logic-module separation, tabbed guided walkthroughs, structural UI variation bar (`?variant=` + floating bottom switcher), and throwaway-first discipline faithfully.
