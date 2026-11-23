---
name: session-handoff
description: >-
  Compact the current conversation into a crisp, zero-fluff handoff artifact
  (handoff_<slug>.md) for a fresh session or cross-model handoff (for example,
  handing off from Gemini in Antigravity to a fresh Claude session). Uses
  sparse context pointers, live git state, settled decisions, open questions,
  verification status, and the exact next step. Use when the user asks for a
  handoff, session summary for a new chat, or cross-model continuation brief.
---

# Session Handoff

Compacts the current session into a crisp handoff brief so a fresh agent—whether the same model after a context reset or a different model family (e.g., Gemini → Claude)—can pick up immediately with zero warm-up drift.

---

## 1. Preflight Live State (Verify, Don't Guess)

Before writing, capture ground-truth workspace state with quick read-only checks (gracefully skipping git commands if the workspace is not a git repository):

1. **Git state:** `git branch --show-current`, `git rev-parse --short HEAD`, and `git status -s` (note uncommitted or untracked changes clearly).
2. **Active artifacts & pointers:** Identify exact paths for active `implementation_plan.md`, `walkthrough.md`, specs, ADRs (`docs/adr/`), PRs/issues, and key modified files.
3. **Next-session focus:** If the user stated what the next session is for (e.g., *"Claude will run the security audit"* or *"continue Phase 2 implementation"*), tailor every section toward that focus and drop unrelated history.

---

## 2. Hard Rules

- **Redact secrets and PII first:** Replace API keys, tokens, passwords, cookies, private endpoints, and personally identifiable information with `<REDACTED>`.
- **Sparse context pointers only:** Never paste large file contents, full diffs, or entire specs into the handoff. Point to authoritative artifacts by exact path (with line ranges when helpful), commit SHA, branch name, or URL.
- **No workspace pollution:** Save the artifact to the active Antigravity **artifact directory** as `handoff_<slug>.md` (where `<slug>` is a short lowercase kebab-case topic, e.g., `handoff_wave2-review.md`). If no artifact directory is available—or if the user asks for chat-only or temp output—output the handoff directly in chat or save to the OS temporary directory (`$TMPDIR`, `/tmp`, or `%TEMP%`). Never write scratch handoff files into the git repository unless the user explicitly asks.

---

## 3. Handoff Document Structure (`handoff_<slug>.md`)

Keep the entire document tight and scannable (typically 40–100 lines):

```markdown
# Session Handoff: <Short Title>

- **Generated:** <ISO date or timestamp>
- **Next-Session Goal:** <1-2 sentences defining what the receiving agent should accomplish>
- **Workspace / Branch / HEAD:** `<repo-name>` · `<branch>` @ `<short-sha>` (<clean | N uncommitted files>)

## Exact Next Step

<Single concrete first action—exact command, file to inspect, or decision to make—so the next session starts moving immediately.>

## Sparse Context Pointers

| Artifact / File | Why It Matters |
| :--- | :--- |
| `<path/to/implementation_plan.md>` | Active plan; start at Milestone/Phase X |
| `<path/to/file.py#L40-L95>` | Core seam touched in this session |
| `<commit SHA or PR/issue URL>` | Preceding change or open discussion |

## Settled Decisions (Do Not Re-Litigate)

- **<Decision>:** <1-line rationale and scope boundary so the next model does not undo or re-ask it.>

## Open Questions, Risks & Ruled-Out Dead Ends

- **Open:** <Unresolved question or blocker awaiting user/tool verification.>
- **Dead end ruled out:** <Approach tried and rejected, with the reason, so the next agent does not repeat it.>

## Verification State

- **Passed:** `<exact command>` (<brief result>)
- **Failed / Pending:** `<exact command>` (<redacted failure summary or "not yet run">)

## Suggested Skills & Workflows

- **`<skill-name>`** (or `/slash-command`) — <1-line reason why the next session should load it>
```

---

## 4. Delivery

After writing `handoff_<slug>.md` (or printing it in chat if requested):

1. Report the exact artifact path (or confirm inline delivery) without re-summarizing the entire artifact.
2. Provide a 1–2 line **copy-ready starter prompt** the user can paste directly into the fresh or cross-model session to bootstrap from the handoff (e.g., *"Read `handoff_<slug>.md`, inspect the listed context pointers, and execute the Exact Next Step."*).
