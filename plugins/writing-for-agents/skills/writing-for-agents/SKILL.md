---
name: writing-for-agents
description: >-
  Reference for writing and editing documents consumed by AI agents—skills,
  AGENTS.md, ~/.gemini/GEMINI.md, plugin references, and hook specs. Covers
  context pointers, context vs. cognitive load, information hierarchy,
  completion criteria, leading words, anti-negation, explore-first sourcing,
  no-op hunting, anti-sediment pruning, and Antigravity packaging mechanics.
  Use when authoring, reviewing, or trimming any agent-facing document.
---

# Writing for Agents

Reference for authoring any document an agent consumes: a skill, an `AGENTS.md` or `~/.gemini/GEMINI.md`, or a reference file reached by a pointer. The packaging differs; the writing does not. The same levers make each document predictable, so the agent follows the same *process* on every run rather than drifting across sessions.

When authoring or validating Antigravity plugins, skills, rules, or `hooks.json`, read [references/antigravity-mechanics.md](./references/antigravity-mechanics.md) for manifest schemas, strict `SKILL.md` frontmatter rules, root `hooks.json` placement, the `<800`-token `AGENTS.md` ceiling, and validator pitfalls.

---

## Context Pointers

A **context pointer** is a line held in the agent's active context that names out-of-context material and encodes the condition for reaching it. A skill's `description` is one; a navigation line in `AGENTS.md` pointing to a reference doc is the same object.

The pointer's *wording*—not its target—decides when the agent reaches the material and how reliably. A must-have target behind a weakly worded pointer is a variance bug: sharpen the pointer's wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches** that should trigger reaching it (a branch is a distinct case the document handles, causing different runs to take different paths). Always-loaded pointers cost tokens and attention on every turn, so prune them harder than the body:

- **Front-load the leading word** where it does its triggering work.
- **One trigger per branch.** Synonyms that rename a single branch are one branch written twice; collapse them and keep only genuinely distinct branches.
- **Cut identity the body already carries.**

---

## Context Load vs. Cognitive Load

Every document and pointer spends one of two budgets:

- **Context load** is the cost of always-loaded material on the agent's window: an `AGENTS.md` line, a `~/.gemini/GEMINI.md` rule, or a skill `description` sitting in context on every turn, spending tokens and attention whether or not it fires.
- **Cognitive load** is the cost on the human: remembering which documents, plugins, or prompts exist and when to reach for each. The human is the index. Cognitive load is not a cost to minimize blindly—it is the price of human agency; spend it where human judgement matters and remove it where it does not.

Material reached only through a pointer escapes context load at the price of the pointer's single line; material with no pointer at all rides entirely on cognitive load.

---

## Information Hierarchy & Progressive Disclosure

An agent document mixes two content types: **steps** (ordered actions the agent performs) and **reference** (definitions, rules, and facts consulted on demand). The core structural decision is where each piece sits on the **information hierarchy**, ranked by how immediately the agent needs it:

1. **In-file step** — primary tier: what the agent does, in order.
2. **In-file reference** — consulted on demand within the same file. A flat peer-set (every rule of a review on one rung) is legitimate, not a smell.
3. **Disclosed reference** — pushed into a separate file (such as `references/*.md` or an external doc) behind a context pointer, loaded only when its branch fires.

Push too little down and the top bloats; push too much down and you hide material every run needs.

- **Progressive disclosure** moves material down the ladder behind a pointer to protect the hierarchy, not merely to save tokens. Use **branching** as the disclosure test: inline what every branch needs, and disclose what only some branches reach. When a document has steps, bulky in-file reference buries them and turns obeying them into a coin flip.
- **Co-location** is the within-file companion: keep a concept's definition, rules, and caveats under one heading so reading one part brings its neighbours with it. Distinct from duplication (repeating one meaning in two places), scattering fragments one meaning across many headings.
- **Sprawl** is a document that is simply too long even when every line is unique and live—attention thins across the excess. Cure sprawl with the ladder: disclose reference behind pointers and split by branch or sequence.

---

## Steps & Completion Criteria

Every step ends on a **completion criterion**: the condition telling the agent that step is finished. Two properties make it effective:

- **Clarity** — Can the agent distinguish done from not-done? A fuzzy bound ("understanding reached") invites **premature completion**: the visible steps still ahead (**post-completion steps**) pull the agent toward *being done* before the current step is genuinely finished. Defend in order:
  1. **Sharpen the bound first** (local and cheap).
  2. Only if the bound is irreducibly fuzzy *and* you observe the agent rushing, hide the later steps across a **real context boundary** (a fresh `invoke_subagent` dispatch or a session handoff; an inline section or in-context call leaves later steps visible and clears nothing).
- **Demand** — How much work does the wording require? *"Every modified endpoint accounted for"* drives **legwork** (digging latent in the criterion rather than listed as extra sub-steps) where *"list changes"* does not. Demand binds flat reference too: *"apply every rule"* sets an exhaustiveness bar on an all-reference document.

The strongest completion criteria are both **checkable** and **exhaustive**.

---

## When to Split

Splitting one document into two spends either context load (another always-loaded pointer) or cognitive load (another artifact for the human to track), so split only when the cut earns its keep:

- **By sequence** — Split a workflow where visible post-completion steps tempt the agent to rush the step in front of it, placing the cut at a real context boundary (`invoke_subagent` or handoff). Beware merging sequences that need isolated legwork.
- **By invocation / discoverability** — Skill-specific splitting rules live in [references/antigravity-mechanics.md](./references/antigravity-mechanics.md).

---

## Leading Words & Anti-Negation

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while executing (*tight*, *red*, *tracer bullets*, *seam*, *fog of war*). Repeated as a token—never as a paragraph—it recruits pretrained priors in minimal tokens. Reach for an existing pretrained word before coining a new term that costs definition tokens.

Leading words anchor twice:
- **In the body (execution):** the agent recruits the same behaviour wherever the word appears, and inside flat reference it focuses attention on a class of defect.
- **In a pointer (invocation):** when the same word appears in user prompts, docs, and code, the agent links that shared vocabulary to the skill or reference reliably.

Hunt for restatements you can collapse into a leading word:
- *"fast, deterministic, low-overhead"* → **tight** (a *tight* feedback loop).
- *"a reproducer you can trust fails on the bug"* → **red** (a *red*-capable loop: binary and observable).

**Anti-negation:** Steering by prohibition drags the forbidden behaviour into active context and makes it *more* available (*don't think of an elephant*). The negation is a weak modifier that the activated concept often overruns.
- **Prompt the positive:** state the target behaviour directly (*"write one-line comments"*, *"construct DOM nodes with `createElement` and `.textContent`"*) so the undesired pattern is never spoken.
- Reserve explicit prohibitions for hard safety guardrails that cannot be phrased positively alone—and always pair the prohibition immediately with the positive target so attention lands on what to do.

---

## Explore-First Sourcing (The Environment Is Truth)

The **environment** is a primary source of truth: repository layout, `Justfile` / `Makefile`, `package.json`, `pyproject.toml`, config files, git history, and `--help` output.

- **Explore before asking:** Instruct agents to inspect the codebase and existing artifacts to resolve questions the repo can already answer rather than interrogating the user for facts sitting on disk.
- **Leave cheap lookups to the environment:** A document that repeats commands, directory trees, or config values an agent can read in one tool call is a stale **cache**. Document only what the environment cannot confess: unwritten conventions, trade-off rationale, non-obvious gotchas, and safety boundaries.

---

## Pruning: Single Source, No-Ops & Anti-Sediment

Every edit to an agent document should leave it sharper, not heavier:

1. **Single source of truth:** Keep each rule or meaning in one authoritative place. Duplication costs maintenance and tokens, and artificially inflates a rule's rank on the information hierarchy. (Unlike a leading word, which intentionally repeats a *token*, never a full explanation.)
2. **Anti-sediment relevance check:** Inspect every line for live relevance. Without deliberate pruning, agent docs accumulate **sediment**—stale layers that settle because adding feels safe and deleting feels risky, until real instructions are buried under dead prose. Delete lines that no longer bear on execution or that belong behind a pointer.
3. **No-op hunting (sentence by sentence):** Test each instruction against the model's default behaviour: *does this sentence actually change what the agent does compared to omitting it?* The test is model-relative, settled by running the document rather than guessing.
   - When a sentence fails the test, **delete the whole sentence** rather than trimming adjectives.
   - Grade leading words the same way: a weak word that fails to beat the default (*"be thorough"*) is a no-op; replace it with a sharper word (*"exhaustive"*, *"relentless"*) or a checkable completion criterion.
