# Fowler Code Smells Baseline (12 Heuristics)

Adapted from Martin Fowler, *Refactoring* (Ch. 3). Applied by the **Standards** reviewer subagent alongside any documented repo standards—and serves as the standalone baseline when a repo has no `CODING_STANDARDS.md`.

## Binding Rules

- **The repo overrides.** A documented repo standard always wins; suppress any baseline smell where the repo explicitly endorses that pattern.
- **Always a judgement call.** Flag every baseline smell as a labelled heuristic (e.g., *"possible Feature Envy"*), never as a hard policy breach.
- **Skip tooling-enforced checks.** Never waste review tokens flagging formatting, lint rules, or type errors that CI/linters already catch deterministically.

---

## The 12 Smells (*What it is* → *How to fix*)

1. **Mysterious Name:** A function, variable, or type whose name fails to reveal what it does or holds. → Rename it clearly; if no honest name fits, the underlying design is murky.
2. **Duplicated Code:** The same logic shape appears in more than one hunk or file in the diff. → Extract the shared shape and call it from both sites.
3. **Feature Envy:** A method reaches into another object's data more than its own. → Move the method onto the data it envies.
4. **Data Clumps:** The same cluster of fields or parameters repeatedly travels together (a domain type wanting to exist). → Bundle them into one structured type and pass that.
5. **Primitive Obsession:** A raw primitive or string stands in for a domain concept with its own invariants. → Wrap the concept in a small dedicated type.
6. **Repeated Switches:** The same `switch` or `if`-cascade over the same discriminant recurs across the change. → Replace with polymorphism or a single shared dispatch map.
7. **Shotgun Surgery:** One logical change forces scattered micro-edits across many files in the diff. → Consolidate what changes together into one cohesive module.
8. **Divergent Change:** One file or module is edited for multiple unrelated reasons. → Split so each module has one clear axis of change.
9. **Speculative Generality:** Abstractions, hooks, or parameters added for hypothetical needs the spec never asked for. → Delete them and inline back until a real second use case arrives.
10. **Message Chains:** Deep `a.b().c().d()` traversal that couples callers to internal object graphs. → Hide the walk behind a single method on the first object.
11. **Middle Man:** A class or function that mostly delegates straight through to another target. → Remove the pass-through and call the real target directly.
12. **Refused Bequest:** A subclass or implementer ignores or overrides most of what it inherits. → Drop the inheritance and use composition instead.
