# Repo Bootstrap

An optional, on-demand interactive initializer for new or unconfigured repositories in Antigravity.

> **Optional — Never Required:** No other plugin in this catalog requires `repo-bootstrap`. Every plugin works standalone and degrades gracefully when `AGENTS.md`, `Justfile`, `CODING_STANDARDS.md`, `GLOSSARY.md`, `docs/adr/`, or `tests/governance/` are absent. Use `repo-bootstrap` only when you explicitly want to scaffold a clean starting layout for a repository.

## What It Does

1. **Safe Read-Only Environment Probe:** Checks local availability of `git`, `gh`, `just`, `python3`, and detected language linters/formatters using strictly non-spicy read-only commands (`--version`, `git rev-parse --abbrev-ref HEAD`, `gh auth status`), without installing packages or mutating system state.
2. **Non-Destructive Repository Audit:** Inspects the current workspace to report which governance and workflow files already exist (and estimates `AGENTS.md` token count if present). Never blindly overwrites existing files.
3. **Opt-In Scaffolding Checklist:** Lets you pick exactly which missing starters to create:
   - **Lean `<800`-token `AGENTS.md`** organized into Class α (P0 safety/custody), Class β (P1 execution/delivery), and Class γ (P2 symmetry/navigation pointers).
   - **Modular `Justfile` safe/gated skeleton** (`Justfile` + `just/safe.just` + `just/gated.just` using `[group('...: safe')]`, `[group('...: gated')]`, and native `[confirm('...')]` guards).
   - **Optional review-only `CODING_STANDARDS.md`** (Tier 1.5 judgement calls read only by reviewers, never implementers; skip in small repos).
   - **Lazy `GLOSSARY.md` & `docs/adr/` starter** (domain vocabulary without implementation details + immutable Historical ADR template and 3-part admission gate).
   - **`tests/governance/` placeholder** (fast `<0.3s` stdlib Python `unittest` gate enforcing the `AGENTS.md` token ceiling and guarding against leaked local paths).
4. **Post-Scaffold Verification:** Verifies token budget, `just --list` (if `just` is installed), and governance tests (if `python3` is installed) on the files created.

## Included Files

- [`skills/repo-bootstrap/SKILL.md`](./skills/repo-bootstrap/SKILL.md) — 4-phase interactive bootstrap protocol (read-only probe, non-destructive repo audit, opt-in checklist, tailored scaffolding and verification).
- [`skills/repo-bootstrap/references/templates.md`](./skills/repo-bootstrap/references/templates.md) — Stack-adaptable starter templates for `AGENTS.md`, modular `Justfile` (`just/safe.just` + `just/gated.just`), review-only `CODING_STANDARDS.md`, `GLOSSARY.md` / `docs/adr/README.md`, and `tests/governance/test_repo_invariants.py`.

## Example Prompts

- *"Bootstrap this repository—probe my local tooling, show what's missing, and let me pick what to scaffold."*
- *"Run a read-only readiness check on this repo and scaffold a lean AGENTS.md plus safe/gated Justfile."*
- *"Set up a minimal GLOSSARY.md, docs/adr/ starter, and tests/governance/ check without touching my existing files."*

## Origin & Attribution

- **Provenance:** `Original`
- **Author:** Authored natively for Google Antigravity by Arthur Davis (`https://github.com/artibyrd`) as a standalone, strictly optional repository initializer compatible with Antigravity's à la carte plugin design.
