---
name: fresh-reader
description: >-
  Audits documentation for curse-of-knowledge blindness by spawning a cold-start
  read-only subagent with zero prior context to read as a newcomer, triaging
  100% of findings with discernment (Accept, Link, or Won't Do), and re-verifying
  edits until a pass produces zero new edits. Use when reviewing READMEs, guides,
  onboarding docs, or any user-facing documentation written by a context-loaded
  agent or maintainer.
---

# Fresh Reader

Reviews user-facing documentation through the eyes of a **zero-context newcomer** (`invoke_subagent`), then triages **100% of findings** with authorial judgment so every genuine confusion is fixed, every edit pass is re-verified, and every false positive is transparently answered as `WON'T DO` rather than causing endless rewrites.

**Core principle: 100% Addressed, Not 100% Satisfied.** Every single reader finding gets an explicit disposition (`ACCEPT`, `LINK`, or `WON'T DO` with rationale). Never silently ignore a finding, and never blindly rewrite a document to appease nitpicks.

---

## Process

### 1. Pin Scope & Target Audience

Before spawning the reader, confirm two facts (infer sensible defaults from the doc if the user didn't specify):
1. **Target document(s):** Exact absolute paths to the file(s) under review.
2. **Target audience persona:** Who is supposed to read this? *(Default: "an experienced software engineer visiting this repository for the first time with zero knowledge of internal project jargon, other repos, or how these docs were created.")*
3. **Optional `GLOSSARY.md` pairing (`domain-modeling`):** If the repo maintains a `GLOSSARY.md`, choose either **pure cold-start** (omit `GLOSSARY.md` to test whether the doc stands alone) or **glossary-assisted cold-start** (include `GLOSSARY.md` alongside the target doc to test whether the glossary actually clarifies every domain term for a newcomer).

Initialize an empty **Cumulative Triage Ledger** for this run (tracking every finding across passes, its disposition, and rationale).

---

### 2. Spawn a Pure Cold-Start Fresh Reader (`invoke_subagent`)

Spawn a fresh, read-only subagent (`TypeName: "research"`) with **zero** conversation history and **zero** priming from prior passes or `WON'T DO` dismissals. *(If `invoke_subagent` is unavailable, explicitly simulate a cold-start read under the same constraints and note the fallback.)*

Give the subagent **only**:
- The exact absolute path(s) of the target document(s).
- The target audience persona.
- **Reader Brief:**
  > *"You are a read-only fresh reader matching this persona: `<persona>`. Read ONLY the listed document(s) linearly from top to bottom. Do NOT inspect other repository files, code, or external context to fill in missing background—only report what breaks comprehension on a first read of these exact files. Do NOT edit files.*
  > *Report EVERY genuine confusion or gap you hit (do not arbitrarily truncate on long docs), citing exact `file:line` or section headings, grouped into:*
  > 1. ***Blocking Confusion:** Undefined project-specific jargon/acronyms, missing prerequisites/starting points, contradictory statements, or unexplained internal references.*
  > 2. ***Friction / Missing 'How Do I Use This?':** Passages that explain what a feature does without showing what the reader actually types, runs, or configures; immediate unanswered next questions; or internal maintainer metadata (e.g., sprint/wave numbers) that adds noise for a reader.*
  > 3. ***Optional Polish:** Minor phrasing, ordering, or scannability improvements."*

---

### 3. Apply the 100%-Addressed Discernment Triage Gate

When the fresh reader reports back, evaluate **every single finding** as the discerning document owner. Never auto-apply every suggestion and never drop a finding unaddressed.

Assign each finding exactly one disposition:

| Disposition | When to Use | Action |
| :--- | :--- | :--- |
| **`ACCEPT (Fixed)`** | Genuine comprehension blocker, undefined project jargon, missing *"how do I trigger/use this?"* concrete example, or maintainer-only clutter. | Edit the document cleanly to resolve it. |
| **`LINK, DON'T INLINE (Fixed)`** | The concept legitimately belongs in a companion doc, plugin README, or `GLOSSARY.md`, not inlined here. | Add a crisp 1-clause plain-English gloss plus a clickable link to the authoritative file. If the finding exposes a missing or fuzzy domain term and the repo uses `GLOSSARY.md` (e.g., via `domain-modeling`), update or propose adding that pure-domain term in `GLOSSARY.md` rather than duplicating definitions across docs. |
| **`WON'T DO (<rationale>)`** | False positive or intentional trade-off: standard industry terminology expected of the target audience (`git diff`, `PR`, `YAML`, `TDD`, `Mermaid`), a request to inline material intentionally kept behind a progressive-disclosure link, an out-of-scope audience request, or a stylistic preference with no real comprehension loss. | Make **no edit**; record the finding and concrete rationale in the **Dismissed Findings Ledger**. |
| **`ALREADY DISMISSED`** *(Pass 2+)* | A subsequent cold-start reader independently raises a concern whose substance is already answered in the Dismissed Findings Ledger. | Make **no edit**; point to the existing `WON'T DO` ledger entry. |

---

### 4. Re-Verify Edits & Converge Naturally

Edits made to resolve Pass $N$'s confusions can accidentally introduce *new* confusions—so never assume a fix worked without fresh eyes:

1. **If Pass $N$ made at least one `ACCEPT` or `LINK` edit:**
   - Apply the edits cleanly.
   - Return to **Step 2** and spawn a **new** cold-start fresh reader against the updated document(s). *(Keep the new reader 100% pure—do NOT feed it your Dismissed Findings Ledger; perform deduplication yourself in Step 3 so the reader stays genuinely unbiased.)*
2. **Natural Stopping Condition (Zero-Edit Convergence):**
   - **STOP** the moment a fresh-reader pass yields **zero new `ACCEPT` or `LINK` edits** (every finding from that pass is either resolved or classified as `WON'T DO` / `ALREADY DISMISSED`).
   - At that point, **100% of reader concerns have been answered**, and the final document text has been verified end-to-end by an unbiased cold-start reader.
3. **Oscillation Tie-Breaker:**
   - If two passes oscillate on the same passage (fixing phrasing A causes a reader to flag phrasing B, and reverting re-flags A), stop immediately and present both variants to the user to pick their preference rather than thrashing.

---

### 5. Present the Cumulative Triage Table

Report the outcome concisely to the user (without re-dumping the edited documents):
- Total passes run and confirmation of zero-edit convergence.
- A single **Cumulative Fresh-Reader Triage Table** covering 100% of findings across all passes:

```markdown
| Pass | Location | Finding | Reader Severity | Disposition | Action / Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/guide.md` L42 | Doesn't show how to create an ADR | Friction | `ACCEPT (Fixed)` | Added concrete prompt example & `references/adr-format.md` link |
| 1 | `README.md` L18 | Asks to explain what `git diff` is | Optional Polish | `WON'T DO` | Target audience is experienced developers; standard git term |
| 2 | `README.md` L18 | Re-raised `git diff` explanation | Optional Polish | `ALREADY DISMISSED` | See Pass 1 `WON'T DO` entry |
```
