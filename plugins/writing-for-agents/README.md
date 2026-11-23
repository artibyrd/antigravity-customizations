# Writing for Agents

An Antigravity plugin for authoring, auditing, and pruning agent-facing documents—skills, plugins, `AGENTS.md`, `~/.gemini/GEMINI.md`, and lifecycle hooks—combining precision prompt craft with Antigravity-native packaging guardrails.

## Why Use It?

- **Precision Prompt Craft:** Applies high-leverage authoring principles—Context Pointers, Context Load vs. Cognitive Load, Information Hierarchy & Progressive Disclosure, checkable/exhaustive Completion Criteria, Leading Words, Anti-Negation, Explore-First Sourcing, No-op Hunting, and Anti-Sediment Pruning.
- **Antigravity-Native Mechanics:** Documents the exact `plugin.json` manifest schema, strict `SKILL.md` frontmatter (`name` and `description` only), plugin-root `hooks.json` contracts, the `<800`-token root `AGENTS.md` context ceiling, and every silent loader pitfall caught by `validate_customizations.py` and `agy plugin validate --strict`.
- **Progressive Disclosure by Example:** Keeps universal writing levers compact in `SKILL.md` and discloses Antigravity packaging and validation mechanics in `references/antigravity-mechanics.md`.

## Included Files

- [`skills/writing-for-agents/SKILL.md`](./skills/writing-for-agents/SKILL.md) — Universal prompt-craft levers for any agent-consumed document.
- [`skills/writing-for-agents/references/antigravity-mechanics.md`](./skills/writing-for-agents/references/antigravity-mechanics.md) — Progressive-disclosure guide to Antigravity steering files, skills, `plugin.json`, root `hooks.json`, and validation pitfalls.

## Example Prompts

- *"Audit and prune this `SKILL.md` for no-ops, negations, and bloated context pointers."*
- *"Help me author a new Antigravity plugin with progressive disclosure and valid `hooks.json`."*
- *"Review our `AGENTS.md` against the 800-token ceiling and information hierarchy."*

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** The core prompt-craft principles—Context Pointers, Context Load vs. Cognitive Load, Information Hierarchy & Progressive Disclosure, Co-location & Sprawl, Steps & Completion Criteria, Leading Words, Anti-Negation, Single Source of Truth, Environment-as-Truth, No-op Hunting, and Anti-Sediment Pruning—are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/productivity/writing-for-agents`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin with `plugin.json` (`suggestedPrompts` <= 3), strict `SKILL.md` frontmatter (`name` + `description` only), mapped steering-file references to `AGENTS.md` and `~/.gemini/GEMINI.md`, replaced Claude-specific `SKILL-MECHANICS.md` (`disable-model-invocation`, router-skill workarounds) with Antigravity-native discovery and `suggestedPrompts` mechanics, and framed sequence-splitting context boundaries around `invoke_subagent` and session handoffs.
- **Original Additions & Synthesis:** Replaced upstream skill mechanics with [`references/antigravity-mechanics.md`](./skills/writing-for-agents/references/antigravity-mechanics.md) covering the `<800`-token root `AGENTS.md` ceiling, Antigravity `plugin.json` schema limits, plugin-root `hooks.json` placement and camelCase protojson contracts, explore-first codebase sourcing, and the `validate_customizations.py` / `agy plugin validate --strict` pitfall checklist.
