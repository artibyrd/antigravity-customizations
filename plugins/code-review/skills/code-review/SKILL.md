---
name: code-review
description: >-
  Three-axis diff review between HEAD and a fixed point (commit, branch, tag,
  or merge-base) via three parallel fresh subagents: Standards (repo standards
  + 12 Fowler code smells), Spec + Reality Check (spec fidelity + zero-mock
  verification), and Security (trust boundaries, injection/XSS sinks, secrets,
  SSRF, races). Use when the user asks to review a branch, PR, commit range, or
  "review since X".
---

# Code Review

Performs a three-axis diff review between `HEAD` and a user-supplied fixed point:
- **Axis 1 — Standards:** Does the diff conform to documented repo standards (including optional `CODING_STANDARDS.md`) and the bundled 12-smell Fowler baseline?
- **Axis 2 — Spec + Reality Check:** Does the diff faithfully implement the originating spec without scope creep, hardcoded mocks, synthetic fallbacks, test-file helper stand-ins, or unverified claims?
- **Axis 3 — Security:** Does the diff introduce or expose trust-boundary flaws, injection/unsafe DOM sinks, SSRF, secret leaks, cryptographic mistakes, or concurrency races?

All three axes run as **parallel, fresh read-only subagents** via `invoke_subagent` so no axis pollutes another's context. All three reports are presented side by side without merging or reranking.

> **Project overlay (optional):** If `.agents/overrides/code-review.md` exists in the workspace or repository root, read it first and apply its `Overrides`, `Extensions`, and `Disabled / Not Applicable` deltas on top of this skill.

---

## Process

### 1. Pin the Fixed Point (Preflight)

Use the fixed point the user supplied (commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If none was specified, ask for it before continuing.

Run these read-only checks once:
1. Confirm the ref resolves: `git rev-parse --verify <fixed-point>`
2. Capture the merge-base diff command: `git diff <fixed-point>...HEAD`
3. Capture the commit list: `git log <fixed-point>..HEAD --oneline`

If the ref is invalid or the diff is empty, stop and report the error here—never spawn subagents on a bad ref or empty diff.

### 2. Discover the Spec Source (Graceful Preflight)

Look for the originating specification in this order:
1. **Explicit path** supplied by the user.
2. **Active plan / repo specs:** Check `implementation_plan.md` (workspace or active artifact) or matching files under `docs/`, `specs/`, or `.scratch/`.
3. **Commit issue/PR references** (`#123`, `Closes #45`): Only if `gh` is installed and authenticated (`gh auth status`), fetch the referenced issue/PR body and comments; if `gh` is missing, unauthenticated, or offline, skip quietly without failing.
4. **If nothing is found:** Ask the user where the spec lives. If there is no spec, record `"No spec available — Spec fidelity skipped (Reality-Check lens only)"` and still run Axis 2 in **Reality-Check-only mode**.

### 3. Discover Standards Sources & Load Bundled Baselines (Graceful Preflight)

1. Scan the repo for documented coding standards: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, and any style/architecture/security guides under `docs/`. If none exist, continue cleanly using the bundled baselines alone.
2. Read [references/fowler-smells.md](./references/fowler-smells.md) and [references/security-checklist.md](./references/security-checklist.md) in full so you can paste each checklist directly into its subagent prompt (fresh subagents may not have access to plugin files outside the workspace).

### 4. Spawn All Three Subagents in Parallel (`invoke_subagent`)

Issue **all three** `invoke_subagent` calls in the same turn as **fresh, read-only** reviewers (never fork the authoring conversation; instruct every subagent not to edit any files). *(If `invoke_subagent` is unavailable, execute the three passes sequentially under the same strict separation rules.)*

#### Axis 1 — Standards Subagent Prompt
Include:
- The exact diff command (`git diff <fixed-point>...HEAD`) and commit list.
- The list of discovered repo standards files (or note that none exist).
- The full 12 Fowler Code Smells and binding rules from [references/fowler-smells.md](./references/fowler-smells.md).
- **Brief:** *"You are a read-only Standards reviewer. Do not edit files. Inspect the diff and report, per file/hunk: (a) every breach of a documented repo standard—cite the file and rule; and (b) any Fowler baseline smell you spot—name the smell and quote the hunk. Distinguish hard violations (documented standards) from judgement calls (baseline smells are always judgement calls, and documented repo standards override the baseline). Skip anything linters, formatters, or typecheckers already enforce. Under 400 words."*

#### Axis 2 — Spec + Reality-Check Subagent Prompt
Include:
- The exact diff command (`git diff <fixed-point>...HEAD`) and commit list.
- The spec file path or fetched spec text (or explicitly state `"No spec available — run Reality-Check lens only"`).
- **Brief:** *"You are a read-only Spec & Reality-Check reviewer. Do not edit files. Inspect the diff and report: (a) spec requirements missing or only partially implemented; (b) unrequested behavior / scope creep; (c) requirements implemented incorrectly—quote the spec line for each finding in (a)–(c) (omit a–c if no spec was provided); and (d) Reality-Check / Zero-Mock defects: hardcoded mock data, silent synthetic fallbacks, stubbed checks/telemetry, swallowed errors, comments/docs claiming behavior the code does not implement, or tests that exercise local helper functions re-implemented inside the test file instead of real production handlers/validators. Under 400 words."*

#### Axis 3 — Security Subagent Prompt
Include:
- The exact diff command (`git diff <fixed-point>...HEAD`) and commit list.
- Any repo security docs or threat-model pointers discovered in Step 3 (if present).
- The full checklist from [references/security-checklist.md](./references/security-checklist.md).
- **Brief:** *"You are a read-only Security reviewer. Do not edit files. Inspect the diff against the security checklist for concrete, exploitable issues: auth/trust-boundary bypasses, fail-open guards, command/SQL/path/XSS injection or unsafe DOM sinks, SSRF/untrusted ingestion, secret exposure or crypto flaws, race conditions, and CI/hook bypasses. Cite exact file:line hunks, label severity (Critical/High/Medium/Low), and explain the concrete exploit or failure mode. If the diff touches no runtime code, scripts, templates, hooks, CI, or config, reply 'No security-sensitive surface touched in this diff.' Under 400 words."*

### 5. Aggregate Without Merging or Reranking

Present all three subagent reports side by side under `## Standards`, `## Spec`, and `## Security` headings, verbatim or lightly cleaned. If no spec existed, keep the explicit note `"No spec available — Spec fidelity skipped; Reality-Check lens only"` at the top of `## Spec`.

**Never merge or rerank findings across axes.**

End with a single summary line reporting:
- Total findings per axis (`Standards: N`, `Spec & Reality Check: M`, `Security: K`), and
- The worst issue *within each axis* (if any)—never pick a single cross-axis winner.

---

## Why Three Separate Axes

A diff can pass two axes and fail the third:
- Clean, secure code that builds the wrong requirement → **Standards pass, Security pass, Spec fail.**
- Exact spec implementation that breaks repo conventions or sneaks in a hardcoded fallback → **Spec pass, Standards/Reality-Check fail.**
- Idiomatic code that matches the spec perfectly while introducing an `.innerHTML` XSS sink or fail-open auth check → **Standards pass, Spec pass, Security fail.**

Keeping all three axes strictly separated prevents any one axis from masking another.
