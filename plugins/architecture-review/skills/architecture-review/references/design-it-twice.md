# Design It Twice (Parallel Subagent Interface Exploration)

When the user selects a deepening candidate from [architecture-review](../SKILL.md) and wants to explore alternative interfaces, run this parallel `invoke_subagent` workflow (adapted from John Ousterhout's *"Design It Twice"* principle: your first interface idea is rarely the best).

Uses the exact vocabulary in [deep-modules.md](./deep-modules.md): **module**, **interface**, **implementation**, **depth**, **seam**, **adapter**, **leverage**, **locality**.

---

## Process

### 1. Frame the Problem Space

Before spawning subagents, present a concise user-facing problem brief for the chosen candidate:
- **Constraints** any candidate interface must satisfy (callers, invariants, error handling, performance, backward-compatibility or migration bounds).
- **Dependencies** and their category from [deep-modules.md](./deep-modules.md) (`in-process`, `local-substitutable`, `ports & adapters`, or `mock`).
- **Illustrative sketch:** A rough 10–20 line code sketch grounding the constraints—explicitly framed as a constraint anchor, not a final proposal.

Show this framing to the user, then proceed immediately to Step 2 so the user can think while subagents work in parallel.

### 2. Spawn 3+ Fresh Subagents in Parallel (`invoke_subagent`)

Issue **3–4 parallel `invoke_subagent` calls in the same turn**, each with a fresh, read-only context window (never fork the authoring conversation; instruct every subagent not to edit files). *(If `invoke_subagent` is unavailable, run each constrained design pass sequentially under the same strict isolation.)*

Give every subagent the same technical brief—relevant file paths, coupling details, dependency category, what sits behind the seam, the [deep-modules.md](./deep-modules.md) vocabulary, and relevant `GLOSSARY.md` terms (if present)—plus **one distinct design constraint** so the outputs are radically different:

- **Subagent 1 (Minimal Surface):** *"Minimize the interface to 1–3 entrypoints maximum. Maximize leverage per entrypoint and hide maximum orchestration behind the seam."*
- **Subagent 2 (Maximum Flexibility):** *"Maximize extensibility and composability across future caller shapes without collapsing into a shallow pass-through."*
- **Subagent 3 (Ergonomic Default Caller):** *"Optimize relentlessly for the 80% common caller: make the default call trivial with safe defaults while keeping edge cases possible."*
- **Subagent 4 (Optional — Cross-Seam Ports & Adapters):** *(Include when dependencies are `remote but owned` or `true external`.)* *"Design around explicit ports and adapters so domain logic sits in one deep in-process module decoupled from transport."*

Require each subagent to return the exact same 5-part structure:
1. **Interface:** Types, entrypoints, parameters, invariants, ordering constraints, and error modes.
2. **Caller Usage Example:** Realistic invocation showing the ergonomic cost on callers.
3. **Hidden Implementation:** Concrete complexity, state, and shallow wrappers absorbed behind the seam (including any internal subpackage split if >~500 LOC).
4. **Dependency & Adapter Strategy:** Port placement, production vs. test adapters, and how seam tests replace old shallow tests.
5. **Trade-Offs:** Where leverage and locality are strongest, and where the design is thin.

### 3. Present, Compare & Recommend

1. **Present each design sequentially** (as a concise Markdown Artifact or structured sections) so the user can absorb each alternative cleanly.
2. **Compare in prose and a compact matrix** across **depth** (caller leverage), **locality** (where future changes concentrate), **seam placement**, and **test surface**.
3. **Give an opinionated recommendation:** State which design is strongest and why—or propose a concrete hybrid combining the best parts of two designs. Give a clear engineering judgement, not a neutral menu.
