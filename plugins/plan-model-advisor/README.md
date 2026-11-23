# Plan Model Advisor

An Antigravity plugin that reviews your implementation plans before you write code and produces a concise **Model & Swarm Execution Brief**—matching each phase to the right Gemini 4 / Claude model, thinking effort level, scope guardrail, cross-family review pass, and `/teamwork` swarm configuration.

## Why Use It?

- **Self-updating model catalog:** Runs a read-only preflight check against Antigravity's live model list before scoring your plan—if new models or effort tiers have launched (or older ones were retired), it researches the changes and refreshes `references/model-matrix.md` automatically before making recommendations.
- **Stop guessing effort tiers:** Know when `Gemini 4 Carbon (High)` or `Gemini 4 Neon (XHigh)` is actually worth it vs. when `Orchestrator (Neon)` or `Gemini 4 Hydrogen` is the smarter call.
- **Prevent frontier over-engineering:** Automatically flags surgical or verbatim steps where heavy reasoning models tend to be *too* helpful and refactor out-of-scope code.
- **Context-window slicing & explore-first discipline (v1.2.0):** Resolves factual questions from the codebase instead of asking the user, flags oversized monolithic phases (>~150k tokens) for vertical tracer-bullet slicing, and structures swarms around a task-graph frontier with sparse context pointers.
- **Right-size swarms (`/teamwork`):** Recommends single-agent vs. a 2-worker adversarial swarm vs. a parallel multi-worker swarm—complete with non-overlapping ownership, workspace modes (`share`/`inherit`), and a ready-to-paste launch prompt that pins per-worker models.
- **Adapt to your subscription tier:** Supports three optimization profiles (`quality-first`, `balanced`, `quota-saver`) without hardcoding anyone's personal defaults.

## Optimization Profiles

| Profile | Intended For | Strategy |
| :--- | :--- | :--- |
| **`quality-first`** | Ultra / unconstrained quota | Standalone frontier models (`Carbon High`, `Neon High/XHigh`), skips Orchestrator on logic-heavy work, fresh-session `Claude Opus 5.5 (High)` audits, adversarial & parallel swarms. |
| **`balanced`** *(default)* | Pro / quota-aware daily driver | `Orchestrator (Neon)` / `Orchestrator (Carbon)` for multi-file loops, standalone frontier models for planning & security-critical logic, `Hydrogen` for docs/chores. |
| **`quota-saver`** | Free tier / tight limits / speed | `Gemini 4 Hydrogen (Medium/High/XHigh)` primary driver, `Orchestrator (Neon)` only on complex plans, skips swarms. |

### Setting Your Personal Default

Add a single line to your machine-local `~/.gemini/GEMINI.md` so you never have to repeat your tier:

```markdown
- Default `plan-model-advisor` profile: `quality-first`
```

You can always override it in any prompt (e.g., *"Review this plan using the `balanced` profile"*).

## Example Prompts

- *"Review `implementation_plan.md` with `plan-model-advisor` before we start coding."*
- *"What model and swarm settings should we use for this migration plan (`quality-first`)?"*
- *"Flag any surgical steps in this plan where a frontier model might over-engineer."*

## Automatic Freshness Checks

All model IDs, benchmark notes, and swarm patterns live in [`skills/plan-model-advisor/references/model-matrix.md`](./skills/plan-model-advisor/references/model-matrix.md). At the start of each review, the skill compares the **Tracked Model Catalog** against Antigravity's live model list (`swarm{action:"models", all:true}`):
- If the catalog matches, it skips web research and goes straight to reviewing your plan.
- If new models or effort tiers appear (or recommended models are retired), it researches the delta, updates `model-matrix.md` in place (without auto-committing), and bases its recommendations on the refreshed catalog.

## Origin & Attribution

- **Provenance:** `Combined (Original + mattpocock/skills)` *(Original Antigravity plugin, enhanced in v1.2.0 with workflow concepts from [`mattpocock/skills`](https://github.com/mattpocock/skills))*
- **Upstream Credit:** Concepts for explore-first fact gathering, vertical tracer-bullet context slicing, task-graph frontiers, and sparse context pointers are adapted from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/implement-spec`, `skills/engineering/to-tickets`, and `skills/productivity/grilling`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Translated Claude Code subagent/worktree/tracker-ticket concepts onto Antigravity's native `swarm` (`/teamwork`) workspace modes (`inherit`, `share`, `branch`), live model catalog preflight (`swarm{action:"models", all:true}`), and standalone `SKILL.md` / `references/model-matrix.md` progressive disclosure with zero issue-tracker or cross-plugin dependencies.
- **Original Additions & Synthesis:** The core plugin—including optimization profiles (`quality-first`, `balanced`, `quota-saver`), the live self-updating Gemini 4 / Claude model matrix, risk-dimension scoring, Orchestrator safety guardrails, over-engineering watchouts, and per-worker model-pinned launch prompts—is original to this repository.
