---
name: prototype
description: >-
  Build a throwaway prototype to answer a design question fast. Use when the
  user wants to sanity-check whether a state model or business logic feels right
  (single-file interactive HTML demo) or explore several radically different
  toggleable UI variations before committing to production code.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

---

## Pick a Branch

Identify which question is being answered from the user's prompt, the surrounding code, or by asking if the user is available:

- **"Does this logic / state model feel right?"** → Read [references/logic.md](./references/logic.md). Build a single self-contained HTML file (free-play buttons plus tabbed guided walkthroughs over a pure liftable logic module) that pushes the state machine through edge cases hard to reason about on paper and that a non-developer can drive.
- **"What should this look like?"** → Read [references/ui.md](./references/ui.md). Generate several radically different UI variations (default 3, max 5) switchable via a `?variant=` URL parameter and a floating bottom bar.

The two branches produce very different artifacts, so picking the wrong one wastes the whole prototype. If the question is genuinely ambiguous and the user is unreachable, default to whichever branch better matches the surrounding code (a backend/domain module → logic; a page or UI component → UI) and state the assumption visibly at the top of the prototype.

---

## Rules That Apply to Both Branches

1. **Throwaway from day one, and never pollute the repo root.**
   - **Standalone HTML prototypes** (all logic prototypes, and standalone UI explorations with no host web app): save to the session **scratch or artifact directory** (`<appDataDir>/brain/<conversation-id>/scratch/prototype-<slug>.html`) — or render interactively inline using Antigravity's built-in `generative_ui` skill / browser preview — so nothing throwaway clutters the repository root.
   - **In-app UI prototypes** (variants embedded in an existing app route): obey the project's existing routing convention, name files/routes unmistakably with `prototype`, and keep every throwaway file easy to delete before committing.
2. **Trivial to view and run (no shell-opener assumptions).**
   - Never assume `open` or `xdg-open` exists in the environment.
   - For standalone HTML prototypes, present a clickable `file://` link to the scratch/artifact file, preview it in Antigravity's browser view, or render it interactively with `generative_ui`.
   - For in-app UI prototypes, launch or document one single project command (`pnpm dev`, `npm run dev`, `just dev`, `python3 ...`) and give the exact URL with `?variant=` keys.
3. **No persistence by default.** State lives in memory. Persistence is usually the thing the prototype is *checking*, not something it should depend on. If the question explicitly involves a database or storage, use a scratch DB or local file with an unmistakable `PROTOTYPE_WIPE_ME` name.
4. **Skip the polish.** No tests, no error handling beyond keeping the prototype runnable, no premature abstractions. The goal is learning fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), render the full relevant state visibly so the user can see what changed.
6. **Capture the answer and clean up before committing.**
   - Fold only the validated decision into production code (lift the pure logic module; rewrite the winning UI cleanly with real tests and error handling).
   - **Clean up before committing to main:** remove all throwaway prototype files, losing variants, and switcher bars from the repository working tree before committing.
   - Preserve the verdict (the question settled and why) in the commit message, PR brief, or ADR, and optionally keep the throwaway prototype in the session scratch directory or on a separate throwaway git branch as a primary source.
