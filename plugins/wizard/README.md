# Wizard

An Antigravity plugin for generating **interactive bash runbook wizards** that guide a human step by step through manual procedures only a human can perform—provisioning cloud/SaaS resources, configuring credentials or GitHub Actions secrets, clicking through unfamiliar third-party dashboards, or executing one-off migrations and cutovers.

> **Scope Boundary:** Use `wizard` only for steps the agent genuinely cannot perform itself (interactive OAuth/2FA logins, billing dashboards, secret generation, manual cutover sign-offs). Never wrap automatable local commands in a human wizard.

## What the Bundled Template Provides

[`skills/wizard/scripts/template.sh`](./skills/wizard/scripts/template.sh) provides a consistent, zero-dependency bash UX library above the `STAGES` marker so every generated wizard only needs focused per-stage authoring:

- **Stage-by-stage clarity:** Clears the terminal per stage (`stage "Name"`), shows `Stage N/M` progress, and keeps each step scannable.
- **Zero destructive defaults:** `confirm "..."` always defaults to `[y/N]` (No), gating every irreversible or remote-mutating action behind explicit affirmative input.
- **Secret-input safety:** `ask_secret` reads silently with `read -rs` (never echoing to the terminal), `write_env` creates `.env` and temp files with `umask 077` (`0600`) and prints only variable names (never secret values), `set_secret` pipes values via stdin to `gh secret set` (keeping secrets out of process lists), and any logged/displayed secret references use `<REDACTED>`.
- **Idempotent re-runs:** Remembers existing values in `.env` (`[Enter keeps current]`), opens URLs cross-platform (`wslview`, `explorer.exe`, `xdg-open`, `open`) with a clean manual fallback, degrades gracefully when `gh` is unavailable or unauthenticated, and finishes with a summary of written keys and remaining manual items.

## Included Files

- [`skills/wizard/SKILL.md`](./skills/wizard/SKILL.md) — 4-phase wizard scoping, stage-mapping, authoring, secret-safety, and static verification workflow.
- [`skills/wizard/scripts/template.sh`](./skills/wizard/scripts/template.sh) — Executable (`0755`) reusable bash wizard library and stage template.

## Example Prompts

- *"Scan `.env.example` and `.github/workflows/` and build an interactive wizard to configure all third-party API keys and GitHub secrets."*
- *"Create a one-off bash wizard walking me through our DNS + webhook cutover with confirmation gates before each irreversible step."*
- *"Generate a repeatable `scripts/setup-wizard.sh` onboarding script for new teammates."*

## Origin & Attribution

- **Provenance:** `Adapted (mattpocock/skills)`
- **Upstream Credit:** Adapted directly from **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills): `skills/engineering/wizard` — `SKILL.md`, `template.sh`), MIT License, Copyright (c) 2026 Matt Pocock.
- **Antigravity Adaptations:** Packaged as a standalone Antigravity plugin (`plugin.json` with `suggestedPrompts <= 3`, strict `name`/`description`-only `SKILL.md` frontmatter, executable `scripts/template.sh` under `skills/wizard/scripts/`). Hardened `write_env` temp-file creation with `umask 077`, added explicit `<REDACTED>` secret-hygiene rules and Antigravity scratch-path guidance for ephemeral one-off wizards, and gated the example `set_secret` call behind `confirm` to guarantee zero destructive defaults.
- **Behavioral Changes:** Preserves Matt's 4-step scoping/authoring/static-verification workflow and complete bash helper API (`banner`, `stage`, `say`, `step`, `note`, `warn`, `open_url`, `ask`, `ask_secret`, `write_env`, `set_secret`, `set_var`, `pause`, `confirm`, `finish`) faithfully.
