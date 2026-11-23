---
name: fresh-reader
description: >-
  Audits documentation for curse-of-knowledge blindness and technical precision
  across four reader personas (vibe-coder, junior-engineer, senior-engineer,
  domain-expert) using a top-down cold-start cascade sieve (`invoke_subagent`),
  triaging 100% of findings with discernment (Accept, Link, or Won't Do) until
  natural zero-edit convergence. Use when reviewing READMEs, guides, onboarding
  docs, technical specs, or any user-facing documentation.
---

# Fresh Reader

Reviews documentation through the eyes of **zero-context cold-start readers** (`invoke_subagent`) calibrated to the document's intended audience—running a **Top-Down Cascade Sieve** so documents are verified for structural/technical accuracy *before* adapting accessibility, while triaging **100% of findings** with authorial discernment until every concern is answered and every edit is re-verified.

**Core principle: 100% Addressed, Not 100% Satisfied.** Every single reader finding gets an explicit disposition (`ACCEPT`, `LINK`, or `WON'T DO` with rationale). Never silently ignore a finding, and never blindly rewrite a document to appease nitpicks.

Read [references/reader-personas.md](./references/reader-personas.md) for the four persona definitions (`vibe-coder`, `junior-engineer`, `senior-engineer`, `domain-expert`), exact top-down cascade sequences, cold-start brief snippets, and persona-scoped dismissal carryover rules.

---

## Process

### 1. Pin Scope, Target Persona & Cascade Plan

Before spawning the first reader, confirm four facts (infer sensible defaults from the doc if the user didn't specify):
1. **Target document(s):** Exact absolute paths to the file(s) under review. *(When reviewing multiple docs aimed at different audiences—e.g., a `junior-engineer` user guide alongside a `senior-engineer` maintainer doc—assign each file its own target persona so higher-level docs stop at their own sieve!)*
2. **Target persona:** One of `vibe-coder`, `junior-engineer`, `senior-engineer` *(default)*, or `domain-expert`.
3. **Top-Down Cascade Sieve sequence** (from [references/reader-personas.md](./references/reader-personas.md)):
   - `senior-engineer` target → `senior-engineer`
   - `junior-engineer` target → `senior-engineer` → `junior-engineer` *(+ optional 1-pass `senior-engineer` accuracy check if technical prose changed substantially)*
   - `vibe-coder` target → `senior-engineer` → `junior-engineer` → `vibe-coder` *(+ optional 1-pass `senior-engineer` accuracy check)*
   - `domain-expert` target → `domain-expert` *(+ optional `senior-engineer` readability pass if meant for cross-team readers)*
4. **Optional `GLOSSARY.md` pairing (`domain-modeling`):** If the repo maintains a `GLOSSARY.md`, choose either **pure cold-start** (omit `GLOSSARY.md` to test whether the doc stands alone) or **glossary-assisted cold-start** (include `GLOSSARY.md` alongside the target doc to test whether the glossary actually clarifies every domain term for the target persona).

Initialize one **Cumulative Triage Ledger** for this run (recording Sieve/Persona, Pass, Finding, Disposition, Scope [`global` vs. `persona-only`], and Rationale).

---

### 2. Spawn a Pure Cold-Start Fresh Reader (`invoke_subagent`)

For the **active sieve's persona**, spawn a fresh, read-only subagent (`TypeName: "research"`) with **zero** conversation history and **zero** priming from prior sieves, prior passes, or `WON'T DO` dismissals. *(If `invoke_subagent` is unavailable, explicitly simulate a cold-start read under the same constraints and note the fallback.)*

Give the subagent **only**:
- The exact absolute path(s) of the document(s) active in this sieve.
- The active sieve's persona brief snippet from [references/reader-personas.md](./references/reader-personas.md).
- **Reader Brief:**
  > *"You are a read-only fresh reader matching this persona: `<persona>`. Read ONLY the listed document(s) linearly from top to bottom. Do NOT inspect other repository files, code, or external context to fill in missing background—only report what breaks comprehension or accuracy on a first read of these exact files. Do NOT edit files.*
  > *Report EVERY genuine issue you hit (do not arbitrarily truncate on long docs), citing exact `file:line` or section headings, grouped into:*
  > 1. ***Blocking Confusion / Technical Flaw:** Undefined jargon for your persona, missing prerequisites/starting points, contradictory statements, unstated assumptions, notation/definition drift, or technical inaccuracies.*
  > 2. ***Friction / Missing 'How Do I Use This?':** Passages that explain what a feature does without showing what the reader actually types, runs, or configures; examples too niche/advanced for your persona; immediate unanswered next questions; or internal maintainer metadata (e.g., sprint/wave numbers) that adds noise.*
  > 3. ***Optional Polish:** Minor phrasing, ordering, or scannability improvements."*

---

### 3. Apply the 100%-Addressed Discernment Triage Gate

When the fresh reader reports back, evaluate **every single finding** as the discerning document owner against the **active sieve's persona**. Never auto-apply every suggestion and never drop a finding unaddressed.

Assign each finding exactly one disposition:

| Disposition | When to Use | Action |
| :--- | :--- | :--- |
| **`ACCEPT (Fixed)`** | Genuine comprehension blocker for this persona, technical/chronological inaccuracy, unstated assumption, missing *"how do I trigger/use this?"* example, or maintainer-only clutter. | Edit the document cleanly to resolve it. |
| **`LINK, DON'T INLINE (Fixed)`** | The concept legitimately belongs in a companion doc, plugin README, or `GLOSSARY.md`, not inlined here. | Add a crisp 1-clause plain-English gloss (calibrated to this persona) plus a clickable link to the authoritative file. If the finding exposes a missing or fuzzy domain term and the repo uses `GLOSSARY.md` (e.g., via `domain-modeling`), update or propose adding that pure-domain term in `GLOSSARY.md` rather than duplicating definitions across docs. |
| **`WON'T DO (<rationale>)`** | False positive or intentional trade-off: standard terminology expected of *this* persona, a request to inline material intentionally kept behind a progressive-disclosure link, an out-of-scope audience request, or a stylistic preference with no comprehension/accuracy loss. | Make **no edit**; record the finding, rationale, and **carryover scope** (`global` vs. `persona-only`) in the Dismissed Findings Ledger. |
| **`ALREADY DISMISSED`** | A subsequent cold-start reader raises a concern already answered by a matching ledger entry (`scope: global`, or `scope: persona-only` within the *same* persona). | Make **no edit**; point to the existing `WON'T DO` ledger entry. *(Never use a `senior-engineer` `persona-only` dismissal to silence a `junior-engineer` or `vibe-coder` flagging unfamiliar jargon!)* |

---

### 4. Converge Each Sieve Naturally, Then Advance Down the Cascade

Edits made to resolve Pass $N$'s findings can accidentally introduce *new* confusions—so never assume a fix worked without fresh eyes:

1. **Within the active sieve:**
   - If Pass $N$ made at least one `ACCEPT` or `LINK` edit, apply the edits and return to **Step 2** with a **new** pure cold-start reader of the *same* persona.
   - **Sieve convergence (Zero-Edit Stopping Condition):** The active sieve finishes the moment a pass produces **zero new `ACCEPT` or `LINK` edits** (every finding is `WON'T DO` or `ALREADY DISMISSED`).
2. **Advancing down the Top-Down Cascade:**
   - Once the active sieve converges, advance to the next persona in your Step 1 cascade plan (keeping only the documents whose target persona reaches that next sieve) and repeat Steps 2–4 until the **target persona** converges to zero-edit.
3. **Final Accuracy Sanity Check:**
   - When cascading down to `junior-engineer` or `vibe-coder`, if lower-sieve edits substantially rewrote technical claims (not just minor glosses/examples), run **one final `senior-engineer`** (or `domain-expert`) accuracy sanity check to confirm simplification did not introduce technical errors.
4. **Oscillation Tie-Breaker:**
   - If two passes oscillate on the same passage (fixing phrasing A causes a reader to flag phrasing B, and reverting re-flags A), stop immediately and present both variants to the user to pick their preference rather than thrashing.

---

### 5. Present the Cumulative Triage Table

Report the outcome concisely to the user (without re-dumping the edited documents):
- Sieve sequence completed, total passes per sieve, and confirmation of zero-edit convergence (plus accuracy sanity-check status if run).
- A single **Cumulative Fresh-Reader Triage Table** covering 100% of findings across all sieves and passes:

```markdown
| Sieve (Persona) | Pass | Location | Finding | Disposition | Action / Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `senior-engineer` | 1 | `docs/guide.md` L117 | Release steps tag before syncing `CHANGELOG.md` | `ACCEPT (Fixed)` | Reordered to sync changelog → commit → tag → push |
| `senior-engineer` | 1 | `docs/guide.md` L79 | Asks to define "public seams" | `WON'T DO (persona-only)` | Expected engineering concept for `senior-engineer` |
| `junior-engineer` | 1 | `docs/guide.md` L79 | "Public seams" unclear without example | `ACCEPT (Fixed)` | Added plain-English gloss & concrete HTTP endpoint example (re-evaluated fresh for `junior-engineer`) |
| `junior-engineer` | 2 | `README.md` L107 | Wants full formatter regex table inline | `ALREADY DISMISSED (global)` | Progressive disclosure to `plugins/workspace-hygiene-hooks/README.md` |
```
