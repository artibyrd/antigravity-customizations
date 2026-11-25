---
name: artifact-governance
description: >-
  Governs Living Document vs. Historical Artifact lifecycle badges, enforces
  the Append-Only Ledger Protocol for implementation_plan.md and walkthrough.md
  with transcript_full.jsonl recovery, keeps scratch scripts out of the repo
  working tree, and captures cited primary-source research notes. Use when
  creating or updating plans, walkthroughs, audits, scratch scripts, or
  research notes across multi-step sessions.
---

# Artifact Governance

Protects institutional memory and repository hygiene across long-running sessions by classifying every document's mutability, preventing accidental overwrites of cumulative plan ledgers, keeping temporary scripts isolated, and grounding research notes in primary sources.

> **Project overlay (optional):** If `.agents/overrides/artifact-governance.md` exists in the workspace or repository root, read it first and apply its `Overrides`, `Extensions`, and `Disabled / Not Applicable` deltas on top of this skill.

---

## 1. Document Lifecycle Taxonomy & Badges

Classify every substantial document or artifact into exactly one paradigm and place its badge at the top:

| Paradigm | Mutability | When to Use | Rule |
| :--- | :--- | :--- | :--- |
| **🟢 Living Document** (*"It's alive!"*) | Mutable, single source of truth | Active `implementation_plan.md` & `walkthrough.md` ledgers, roadmaps, architecture overviews, API specs, operational runbooks | Update in place (or append for ledgers) so guidance stays synchronized with current system reality. |
| **🏛️ Historical Artifact** (*"That belongs in a museum!"*) | Strictly immutable snapshot | ADRs, incident post-mortems, benchmark/profiling runs, point-in-time audits, tagged release notes, meeting summaries | Never edit or rewrite after completion. Record new context in a separate dated artifact, addendum, or superseding document. |

### Living Document Badge
```markdown
> [!NOTE]
> **Classification:** 🟢 **Living Document** (*"It's alive!"*)
> **Status:** Active / Evolving | **Last Updated:** YYYY-MM-DD
> **Purpose:** [Single-sentence role as current source of truth]
```

### Historical Artifact Badge
```markdown
> [!IMPORTANT]
> **Classification:** 🏛️ **Historical Artifact** (*"That belongs in a museum!"*)
> **Status:** Immutable Snapshot | **Recorded:** YYYY-MM-DD
> **Purpose:** [Single-sentence snapshot scope and context]
```

---

## 2. The Append-Only Ledger Protocol

`implementation_plan.md` and `walkthrough.md` are **cumulative append-only ledgers** for an entire release epoch or multi-milestone initiative—never single-task scratchpads.

### Non-Negotiable Rules
1. **Mandatory Tail Pre-Read:** Before modifying an existing `implementation_plan.md` or `walkthrough.md`, read the tail of the file to confirm its structure and identify the highest existing milestone number $M$.
2. **Append `# Milestone M+1` Only:** Separate the new section with `---`, title it `# Milestone M+1: <Title>`, and write it using `write_file` with `Append: true` or a surgical tail `edit_file`.
3. **Never Blindly Overwrite:** Calling `write_file(..., Overwrite: true)` on an existing `implementation_plan.md` or `walkthrough.md` with only a new task's content destroys prior milestone history and is strictly forbidden.
4. **Surgical Amendments Only on Request:** Modify earlier milestone sections only when the user explicitly asks to revise the master plan itself, using targeted `edit_file` edits on the specific lines.
5. **Dedicated Topic Artifacts for Independent Follow-Ups:** Route standalone sub-proposals, exploratory designs, UI audits, or pre-merge remediation plans to a dedicated artifact file in `<appDataDir>/brain/<conversation-id>/<topic>_implementation_plan.md` (or `<topic_slug>.md`) rather than crowding or overwriting the master ledger.

### Automatic Recovery (`transcript_full.jsonl`)
If `implementation_plan.md` or `walkthrough.md` is accidentally clobbered or truncated:
1. **Halt other work immediately.** Do not layer further edits onto the damaged file.
2. **Locate the prior state:** Inspect `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` to find the step index where the previous full ledger was written or edited.
3. **Extract complete text:** Read that exact line from `transcript_full.jsonl` (never truncated) to recover the intact historical milestones verbatim.
4. **Restore and re-append:** Restore the full historical ledger first, verify all preceding milestone headings (`# Milestone 1` … `# Milestone M`) are contiguous, and only then append `# Milestone M+1`.

---

## 3. Artifact Topology & Clean Scratch Script Ritual

Keep artifacts organized and repository working trees free of temporary tooling:

- **Master Milestone Ledger:** `<appDataDir>/brain/<conversation-id>/implementation_plan.md`
- **Execution & Validation Ledger:** `<appDataDir>/brain/<conversation-id>/walkthrough.md`
- **Topic Plans, Audits & Research Notes:** `<appDataDir>/brain/<conversation-id>/<descriptive_slug>.md` (or the repo's established notes path when the user wants it committed)
- **Temporary Scripts & Intermediate Data:** `<appDataDir>/brain/<conversation-id>/scratch/`

### Clean Scratch Script Ritual
- **No inline code blobs:** Do not run multi-line `python3 -c "..."`, `node -e "..."`, or brittle nested-quote shell blobs for data processing, log inspection, or verification checks.
- **Write repeatable scratch files:** Save one-off scripts under `<appDataDir>/brain/<conversation-id>/scratch/<descriptive_name>.py` (or `.sh`) and run them cleanly (`python3 <scratch_dir>/<script>.py`).
- **Zero repo pollution:** Never drop temporary scripts, scratch logs, or intermediate dumps into the repository root or source directories.
- **Right-shape formatting & plain English:** Reserve Markdown tables for genuinely uniform tabular data with short cells; present narrative summaries, multi-file indices, and audit findings as headings with one-item-per-line bullet lists, and avoid sentences packed with walls of inline backtick snippets.

---

## 4. Primary-Source Research Notes

When investigating an external API, library behavior, specification, or technical question:

1. **Delegate heavy reading to a fresh context:** When reading legwork is substantial, spawn a read-only background subagent via `invoke_subagent` with a fresh context window so large doc reads do not bloat the main implementation turn.
2. **Verify against primary sources:** Trace every technical claim back to the source that owns it—official documentation, RFCs/specifications, first-party APIs, or the library's own source code. Never treat secondary blog posts, forum summaries, or memory as sufficient verification.
3. **Capture cited Markdown notes:** Write findings into a single concise Markdown file with:
   - The appropriate lifecycle badge (typically **🏛️ Historical Artifact** with `Recorded: YYYY-MM-DD` for point-in-time doc lookups, or **🟢 Living Document** if maintained alongside the repo).
   - Inline source links or citations for every non-trivial claim (URL, version/date checked, or exact file/line path).
   - Clear separation between verified facts and any remaining open questions.
4. **Respect repository conventions:** Save the note where the repository already stores research or design notes (e.g., `docs/research/`, `docs/notes/`). If the repo has no such convention—or the research is session-scoped—save it in `<appDataDir>/brain/<conversation-id>/research_<slug>.md` and report the exact path to the user.
