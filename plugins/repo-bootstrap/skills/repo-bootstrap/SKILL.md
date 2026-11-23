---
name: repo-bootstrap
description: >-
  Optional on-demand interactive initializer for new or unconfigured
  repositories. Runs a safe read-only environment readiness probe (git, gh,
  just, python3, detected stack linters/formatters), audits what already exists
  without overwriting anything, presents an opt-in checklist, and scaffolds only
  the selected starters (lean <800-token AGENTS.md, modular safe/gated Justfile,
  optional review-only CODING_STANDARDS.md, lazy GLOSSARY.md/docs/adr/, and
  tests/governance/ placeholder).
---

# Repo Bootstrap

An on-demand interactive initializer for new or unconfigured repositories.

> **Strictly Optional — Never Required:** No other plugin requires `repo-bootstrap`. Every other plugin degrades gracefully without any of these files. Run this skill only when the user explicitly asks to initialize or check repository readiness.

---

## Non-Negotiable Safety Rules

1. **Never blindly overwrite existing files.** If a target file already exists, mark it `Exists (skip by default)` in the checklist. Only inspect or propose targeted edits if the user explicitly asks to update that file.
2. **Read-only probe only.** Phase 1 runs strictly non-spicy, read-only checks. Never install tools, mutate git config, write lockfiles, or run mutating CLI flags during probing.
3. **Opt-in everything.** Never scaffold any file before presenting the audit + opt-in checklist and receiving the user's explicit selection.

---

## Phase 1: Safe Read-Only Environment Readiness Probe

First inspect the repository root (read-only file listing / reading manifests such as `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Makefile`, `Justfile`) to detect the project's language stack.

Then probe tool readiness using **only** safe, read-only invocations (discrete commands, no mutating flags):

| Tool / Area | Safe Read-Only Probe Command | Notes |
| :--- | :--- | :--- |
| **Git** | `git --version` and `git rev-parse --abbrev-ref HEAD` | If not inside a git repo, note `not initialized` (do not run `git init` automatically). |
| **GitHub CLI** | `gh --version` and (if installed) `gh auth status` | Read-only status check; degrade gracefully if unauthenticated or offline. Treat `gh auth status` as a one-off read-only check—never recommend priming "Always Allow" on the 2-token `gh auth` prefix (which also matches `gh auth logout`/`token`); wrap it in a `Justfile` recipe if repeated checks are needed. |
| **Task Runner** | `just --version` | Optional; required only if scaffolding `Justfile`. |
| **Python** | `python3 --version` | Used for zero-dependency governance tests (`tests/governance/`). |
| **Detected Stack Tools** | Probe **only** linters/formatters relevant to detected manifests using `--version` (e.g., `ruff --version`, `pytest --version`, `mypy --version`, `node --version`, `pnpm --version`, `prettier --version`, `eslint --version`, `cargo --version`, `go version`, `shellcheck --version`). | Skip tools unrelated to the detected stack. |

Summarize the results in a concise **Environment Readiness Table** (`Tool | Status | Detail`) with optional one-line install hints for anything missing.

---

## Phase 2: Non-Destructive Repository Audit

Inspect the repository for each optional governance/workflow artifact without modifying anything:

| Artifact | Check to Perform | Status to Report |
| :--- | :--- | :--- |
| `AGENTS.md` | Exists? If yes, estimate tokens (`word_count * 1.33`) and note whether it is `<800` tokens. | `Missing` or `Exists (~N tokens — skip by default)` |
| `Justfile` & `just/*.just` | Exists? Check if `just/safe.just` and `just/gated.just` exist; note if `Makefile` already serves as task runner. | `Missing` or `Exists (skip by default)` |
| `CODING_STANDARDS.md` | Exists? | `Missing (optional — skip in small repos)` or `Exists (skip by default)` |
| `GLOSSARY.md` & `docs/adr/` | Do either exist? Count existing ADRs if `docs/adr/` is present. | `Missing` or `Exists (skip by default)` |
| `tests/governance/` | Exists? Check if a `tests/` directory already exists. | `Missing` or `Exists (skip by default)` |

---

## Phase 3: Present Opt-In Checklist (Mandatory Gate)

Present the Environment Readiness Table and Repository Audit to the user, then ask them which **missing** starters they want to scaffold (use `ask_question` with `is_multi_select: true` when helpful, or a crisp numbered opt-in list):

1. **Lean `AGENTS.md` starter (`<800` tokens)** — Tier 0 always-on invariants structured into Class α (P0 safety/custody), Class β (P1 execution/delivery), and Class γ (P2 symmetry & navigation pointers), tailored to the detected stack.
2. **Modular `Justfile` safe/gated skeleton (`Justfile`, `just/safe.just`, `just/gated.just`)** — Lean root orchestrator separating read-only `[group('...: safe')]` recipes from mutating `[group('...: gated')]` recipes protected by native `[confirm('...')]` guards.
3. **Optional review-only `CODING_STANDARDS.md`** — Tier 1.5 repo-wide style judgement calls read *only* by reviewers (never implementers), keeping `AGENTS.md` lean. Recommend skipping in small single-purpose repos.
4. **Lazy `GLOSSARY.md` & `docs/adr/` starter** — Domain vocabulary file (zero implementation details) plus `docs/adr/README.md` with the 3-part Historical ADR gate (hard to reverse + surprising without context + real trade-off) and immutable ADR template.
5. **`tests/governance/` placeholder** — Fast (`<0.3s`), zero-dependency Python `unittest` starter enforcing the `AGENTS.md` `<800`-token ceiling and checking for accidental machine-local path leaks.

Wait for explicit confirmation of the selected items before writing a single file.

---

## Phase 4: Scaffold Selected Items & Verify

1. Read [references/templates.md](./references/templates.md) before writing files.
2. **Write only the user's selected missing items.** Never overwrite an existing file unless the user explicitly instructed you to replace or merge it.
3. **Tailor every placeholder to the detected repository:**
   - Replace `<repo-name>` with the actual workspace folder or manifest package name.
   - Wire `just/safe.just` `check`, `lint`, and `test` recipes to the actual commands detected in Phase 1 (or clearly marked placeholder echoes when no test/lint tool is configured yet).
   - Keep `AGENTS.md` strictly under **800 tokens** (target 250–450 tokens for a fresh starter so headroom stays high).
4. **Verify what was created (read-only checks only):**
   - If `AGENTS.md` was created: compute its word count and estimated tokens (`word_count * 1.33`) and confirm `<800` tokens.
   - If `Justfile` was created and `just` is available: run `just --list` to verify syntax and recipe grouping.
   - If `tests/governance/` was created and `python3` is available: run `python3 -m unittest discover -s tests/governance -v` to confirm the starter test passes cleanly.
5. **Report completion concisely:** list every file created, every existing file left untouched, verification results, and remind the user they can edit or delete any starter at any time.
