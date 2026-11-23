---
name: wizard
description: >-
  Generate an interactive bash wizard that walks a human step by step through
  manual procedures only a human can perform—provisioning infrastructure,
  configuring credentials or CI secrets, navigating third-party dashboards, or
  running one-off migrations and cutovers. Never invoke this for steps the agent
  can safely perform itself.
---

# Wizard

A **wizard** is a self-contained bash script that walks a human, step by step, through a manual procedure that is tedious to execute by hand and error-prone to re-explain every time. It opens each URL (with a clean fallback when no browser opener exists), explains exactly what to click and copy, captures values safely, writes them where they belong (`.env`, GitHub Actions secrets/variables), confirms before irreversible actions, and tracks remaining stages.

The UX library is already implemented in [scripts/template.sh](./scripts/template.sh): stage-by-stage progress, `[y/N]` confirmation gates, cross-platform URL opening (including WSL), silent `read -rs` secret entry, `0600` idempotent `.env` upserts, `gh secret`/`gh variable` writes with graceful fallback, and a closing summary. **Your job is only to scope the procedure and author its stages.** Never hand-edit the library above the `STAGES` marker.

**Storage lifecycle:** A wizard is ephemeral by default—save one-off wizards in the session scratch directory (or a clearly temporary path) and delete them when the job is done. Save under `scripts/` and commit only when the user explicitly wants a repeatable onboarding/setup path in the repository.

---

## Security & Zero-Destructive-Defaults Rules

Hold these invariants on every generated wizard:

1. **Zero destructive defaults:** Gate every irreversible, remote-mutating, or high-impact step (rotating live keys, pushing CI secrets, flipping DNS/webhooks, deleting old resources) behind `confirm "..."` — which always defaults to `[y/N]` (No). Never auto-accept on Enter.
2. **Hidden secret input (`read -rs`):** Always capture passwords, API keys, tokens, private keys, and connection strings with `ask_secret` (never `ask`).
3. **Never echo or leak secrets (`<REDACTED>`):** Never print captured secret values to stdout, stderr, logs, summaries, or chat transcripts—print only variable names or `<REDACTED>`. Never pass secret values on command-line arguments where process lists (`ps`) can expose them (`set_secret` pipes via stdin).
4. **Never execute the wizard end-to-end as the agent:** Wizards open browsers and prompt for human secrets. Verify statically (`bash -n`, `shellcheck` if installed) and hand the script to the user to run in their own terminal.

---

## Process

### 1. Scope the Procedure (Explore the Repo First)

Discover every manual step the human must perform and every value that must be captured by inspecting the repository before asking cold:

- **Setup / provisioning:** read `.env.example`, `.env.*` templates (never print real `.env` secrets—redact as `<REDACTED>`), `README.md`, `docker-compose*`, framework config, and `.github/workflows/*` (every `secrets.*` and `vars.*` reference is a concrete output the wizard must satisfy).
- **Migration / cutover:** identify the current state, the target state, and every irreversible transition between them.

Present the ordered list of stages and captured values to the user and confirm before authoring (they may add, drop, or reorder).

**Done when:** every stage is named in dependency order, and for each captured value you know:
1. where the human obtains it,
2. where it is written (`.env`, GitHub secret, GitHub variable, multiple destinations, or none for pure manual actions), and
3. whether it is **secret** (`ask_secret`) or **public** (`ask`).

### 2. Map Each Stage's Concrete Journey

For every stage, write exact, stranger-proof instructions: which URL to open, the exact menu path, where the value appears, and which variable it populates (for example: *"Dashboard → Developers → API keys → Reveal test key → copy"*).

If you are not sure of a third-party dashboard's current UI path or exact CLI command, say so explicitly and check official docs or ask the user—never fabricate UI clicks that may not exist.

**Done when:** every stage traces to concrete, verifiable human steps.

### 3. Author the Wizard from `scripts/template.sh`

Copy [scripts/template.sh](./scripts/template.sh) to the target path (session scratch directory for one-off runs, or `scripts/<name>.sh` when committing a repeatable runbook).

Replace the example stage inside `run_wizard()` below the `STAGES` marker with one `stage` per step in dependency order, using the bundled helpers:
- `banner "Title"` — opening screen
- `stage "Name"` — clears screen and advances `Stage N/M`
- `say` / `step` / `note` / `warn` — formatted instructions
- `open_url "https://..."` — opens URL before asking for values from that page
- `ask KEY "Prompt:"` — visible input for non-secret values (preserves existing `.env` default)
- `ask_secret KEY "Prompt:"` — silent `read -rs` input for secrets (never echoed)
- `write_env KEY "$KEY"` — idempotent `0600` upsert into `$ENV_FILE`
- `set_secret NAME "$VAL"` / `set_var NAME "$VAL"` — GitHub Actions secret/variable with `gh` fallback
- `pause "msg"` / `confirm "question"` — manual pacing and `[y/N]` gates before irreversible actions
- `finish` — closing summary of variable names written and any skipped manual steps

Set `TOTAL_STAGES` to the exact number of `stage` calls you wrote. Keep each stage focused on a single cohesive task so nothing scrolls off screen. Leave the library above the `STAGES` marker untouched and keep the final `run_wizard "$@"; exit` line intact.

### 4. Verify Statically and Hand Off

Run static checks only (never run the interactive wizard end-to-end yourself):

1. Check syntax: `bash -n <script>`
2. Run `shellcheck <script>` if `shellcheck` is installed (skip cleanly if absent).
3. Ensure executable permissions: `chmod 0755 <script>`
4. Trace statically: confirm `TOTAL_STAGES` matches the count of `stage` calls, every value from Step 1 is captured with the right helper (`ask` vs. `ask_secret`), every `set_secret` name exactly matches the repo's `.github/workflows/*` `secrets.*` references, no secret value is echoed anywhere, and every irreversible action sits behind `confirm`.
5. Tell the user the exact command to run in their terminal (e.g., `./<script>` or `ENV_FILE=.env.local ./<script>`). If it is a repeatable repo setup path, offer to link it from the repository's `README.md`.
