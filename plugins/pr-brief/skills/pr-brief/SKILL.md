---
name: pr-brief
description: >-
  Write a visual-first pull request description and Mk1 Eyeball review
  walkthrough: smallest clear visual (pseudocode, call tree, component tree,
  file tree, Mermaid, or diff), concrete Before/After Evidence, and Merge
  Danger (One-Way vs. Two-Way Door plus Blast Radius). Works with gh CLI when
  authenticated or outputs copy-ready Markdown without gh. Use when drafting,
  updating, or reviewing a PR description or walkthrough.
---

# PR Brief

Drafts concise, visual-first pull request descriptions built for fast human (**Mk1 Eyeball**) review.

Skip all preambles and keep prose brief. Match the repository's domain vocabulary from `GLOSSARY.md` (if present; skip quietly if absent).

---

## 1. Graceful Preflight

Before drafting, ground the brief in the actual diff and runtime evidence:

1. **Inspect the diff:** Run `git diff <base>...HEAD --stat` and `git log <base>..HEAD --oneline` (default `<base>` to `main` or the user-specified target branch/commit). Read changed hunks as needed so every diagram, symbol, and file path is accurate.
2. **Gather real evidence:** Check recent test/validator output, screenshots, or live probe results from this session. Never fabricate or extrapolate evidence—if Before/After proof is missing, run the check (if safe and local) or mark the gap explicitly for the user to supply.
3. **Redact secrets first:** Replace tokens, cookies, API keys, passwords, or private credentials in any pasted output with `<REDACTED>`.
4. **Choose delivery mode cleanly:**
   - **Draft / walkthrough requested (default):** Output copy-ready Markdown directly in chat (or save to a walkthrough artifact if requested).
   - **Create or update PR on GitHub requested:** Probe `gh auth status` first. If `gh` is installed and authenticated, confirm before creating/updating with `gh pr create` or `gh pr edit`. If `gh` is missing, unauthenticated, or offline, degrade gracefully—say so in one line and output the complete copy-ready Markdown without failing.

---

## 2. PR Body Template

Use this structure verbatim:

```markdown
## Summary

<smallest visual that makes the key point clear—see references/visual-menu.md>

## Evidence

- **Before:** <screenshot, failing test output, or prior probe>
- **After:** <screenshot, passing test output, or verified probe>

<!-- Include when human visual/runtime sign-off is needed -->
### Mk1 Eyeball Walkthrough
1. <exact route, command, or file to open>
2. <concrete behavior or visual invariant to confirm>

## Merge Danger

**Door:** <one-way or two-way>

<optional: 1-2 sentences explaining rollback cost or irreversibility>

**Blast Radius:** <concise scope label, e.g., Isolated / Single-module / API-consumers / Cross-service>

<optional: concrete ramifications—layout shift, consumer breakages, downstream deploy order, migration notes>
```

---

## 3. Section Rules

### Summary

Read [references/visual-menu.md](./references/visual-menu.md) and pick the **smallest visual** that makes the key change immediately obvious:

- **Pseudocode** for logic or algorithm changes
- **Call tree** for runtime control flow
- **Component tree** for UI structure, state, and module boundaries
- **Shallow file tree** for file responsibility or broad refactors
- **Mermaid diagram** for component interaction, control flow, or data flow
- **Scoped `diff`** when the surrounding shape already exists and the delta is the point
- **Whole block** when most of the code is new or omitted context hides ownership/order

Place each visual immediately next to the short text it supports. Keep only load-bearing calls, files, props, states, and boundaries. Pick one visual—or a small pair for multi-part PRs—never all of them.

### Evidence (and Mk1 Eyeball Walkthrough)

Provide concrete proof that the change works, comparing **Before** and **After**:

- **S-tier (Visual / UI changes):** Before/After screenshots, recordings, or browser DOM verification captures when the environment supports it.
- **A-tier (Execution & Live Probes):** Test results, validator output, console output, or live dev/staging probe responses. For bug fixes or TDD changes, show the exact test case (or minimal pseudocode) that failed before and passes after.
- **Mk1 Eyeball Walkthrough:** Whenever a change affects rendered UI, CLI ergonomics, docs layout, or live operational endpoints, add a 2–4 step human inspection checklist (exact URL/command, expected state, edge case to eyeball) so the reviewer can sign off in under two minutes. Omit this subsection for purely internal refactors with comprehensive automated proof.

### Merge Danger

Force an honest assessment of reversibility and impact:

- **Door (`one-way` vs. `two-way`):**
  - **Two-way door:** Cheap and safe to roll back (`git revert`, config toggle, isolated additive change).
  - **One-way door:** Hard or impossible to reverse cleanly (destructive data/schema migration, dropped public API/contract, secret rotation, irreversible external side effect). State the rollback or mitigation plan explicitly.
- **Blast Radius:** Name the real scope of impact and enumerate concrete failure modes to watch for (layout shift, mobile responsiveness, consumer contract breakages, hook/CI gating regressions, or multi-repo merge ordering).
