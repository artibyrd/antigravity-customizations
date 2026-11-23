# Logic Prototype

A single, self-contained HTML file (a **shareable demo**) that lets anyone drive a state model by clicking buttons. Use this when the question is about **business logic, state transitions, or data shape**—the kind of thing that looks reasonable on paper but only feels wrong once pushed through real cases.

Because it is one file with nothing to install, you can hand it to a non-developer (a designer, PM, or domain expert) and let them feel the model directly. It speaks their domain language, not the code's.

If the question is *"what should this look like?"*, switch to [references/ui.md](./ui.md).

---

## When This Is the Right Shape

- *"I'm not sure if this state machine handles the edge case where X then Y."*
- *"Does this data model actually let me represent the case where..."*
- *"I want to feel out what the API/domain transitions should look like before writing production code."*
- Anything where someone wants to **press buttons and watch state change**.

---

## Process

### 1. State the Question

Before writing code, write down what state model and what question you are prototyping: one clear paragraph in a **visible intro at the top of the demo** (not hidden in a code comment). A logic prototype that answers the wrong question is pure waste; making the question visible lets anyone check it immediately or AFK.

### 2. Isolate the Logic in a Portable Pure Module

Put the core logic (the part answering the question) in a single `<script>` block written as a small, pure module that can be lifted cleanly into the real codebase later. The HTML shell around it is throwaway; this module is the durable design artifact.

Choose the shape that fits the question (not whichever is easiest to wire to DOM buttons):

- **Pure reducer:** `(state, action) => state` — best when actions are discrete events over one state value.
- **State machine:** explicit states and legal transitions — best when *"which actions are even legal right now?"* is part of the question.
- **Small set of pure functions** over a plain data type — best when there is no implicit current state, only transformations.
- **Class or module with a narrow method surface** — only when the logic genuinely owns ongoing internal state.

Keep the logic module **100% pure**: zero `document`, zero DOM references, zero button handlers reaching inside it. The page calls into the module; nothing flows the other direction.

### 3. Build the Self-Contained HTML File

Save the file in the session scratch/artifact directory (`<appDataDir>/brain/<conversation-id>/scratch/prototype-<slug>.html`) — or render interactively inline via Antigravity's `generative_ui` skill — so it never pollutes the repository root.

Build it as **one plain HTML/CSS/JS file**: no framework, no bundler, no server, zero external CDN dependencies (100% offline-capable). Construct dynamic DOM updates safely with `document.createElement` and `.textContent` (avoid interpolating dynamic strings into `.innerHTML`).

Write every label in **domain language**, not implementation jargon: buttons and state read like the business, not the reducer. Lay it out cleanly top to bottom:

1. **Title and visible one-paragraph question** explaining what this demo tests (Step 1).
2. **Current state panel:** the full relevant state rendered as readable labelled fields (not a raw JSON dump), re-rendered after every click, with a clear visual callout showing **what just changed** (or why an action was rejected).
3. **Free-play buttons:** one button per action, always reachable (or clearly indicating when disabled/illegal by the state machine), so anyone can poke at the model in any order.
4. **Tabbed guided walkthroughs:** one tab per **scenario**. Each tab contains a short plain-language description of the situation and what to watch for, followed by ordered step buttons. Clicking a step dispatches that action and advances; selecting/starting a walkthrough resets to a known initial state so every run is deterministic.

Include scenarios that expose awkward cases hard to reason about on paper:
- the happy path,
- a tricky boundary or ordering edge case, and
- an attempt at an action that **should be illegal**.

Keep the styling restrained and readable: clean typography, generous spacing, one accent color, no distracting animations or gimmicks.

### 4. Hand It Over

Provide a clickable `file://` link to the saved HTML file (or open it in Antigravity's browser preview / `generative_ui` widget)—never assume `open` or `xdg-open` is available. The highest-value moments are when the user says *"wait, that shouldn't be possible"* or *"I assumed X would behave differently"*; those are bugs in the **idea**. Iterate quickly by adding actions or scenarios as questions emerge.

### 5. Capture the Answer and Clean Up

Once the prototype settles the question, follow [SKILL.md](../SKILL.md):
- Lift the validated pure logic module (reducer / state machine / functions) into the real codebase and cover it with proper production tests.
- Confirm zero throwaway prototype HTML files remain in the repository working tree before committing.
- Record the settled question and verdict in the commit, PR brief, or ADR (and keep the self-contained HTML file in the session scratch directory or on a separate throwaway branch if you want a primary-source archive).

---

## Anti-Patterns

- **Adding unit tests to the prototype.** A prototype that needs tests is no longer a prototype.
- **Wiring it to a real database or live API.** Keep state in memory unless persistence itself is the question.
- **Generalizing for imaginary future features.** Answer one question, then stop.
- **Blurring the logic and DOM shell together.** If the logic touches `document` or click handlers, it is no longer liftable.
- **Reaching for a framework, bundler, or dev server.** One offline HTML file beats a scaffolded app every time.
- **Committing the throwaway HTML shell to main.** Keep only the validated logic module in production code.
