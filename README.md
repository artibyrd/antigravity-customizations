# Antigravity Customizations

[![Validate Customizations](https://github.com/artibyrd/antigravity-customizations/actions/workflows/validate.yml/badge.svg)](https://github.com/artibyrd/antigravity-customizations/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

A modular, version-controlled collection of reusable **Google Antigravity** plugins—starting with skills and designed to grow cleanly into agents, rules, hooks, and MCP bundles.

Every plugin in [`plugins/`](./plugins) is self-contained and intentionally scoped to **one coherent workflow**, so you can adopt individual plugins **à la carte** without pulling in unrelated opinions or all-or-nothing toggles.

---

## Plugin Catalog

| Plugin | Components | What It Does | Docs |
| :--- | :--- | :--- | :--- |
| **`plan-model-advisor`** | 1 Skill (`plan-model-advisor`) | Reviews an implementation plan before coding and outputs a **Model & Swarm Execution Brief**—mapping each phase to the right Gemini 4 / Claude model, effort level, over-engineering guardrails, cross-family review pass, and `/teamwork` swarm roster across `quality-first`, `balanced`, and `quota-saver` profiles. | [Plugin README](./plugins/plan-model-advisor/README.md) |

---

## Quick Start: Adopt À La Carte

Clone the repository anywhere on your machine (for example, `~/Projects/antigravity-customizations`):

```bash
git clone https://github.com/artibyrd/antigravity-customizations.git ~/Projects/antigravity-customizations
```

Then choose whichever activation method fits your workflow:

### Option 1: Live Sync via `~/.gemini/config/plugins.json` *(Recommended)*

Register the repo's `plugins/` directory in your global Antigravity config so updates arrive automatically whenever you run `git pull`.

> **Important:** Use an **absolute path** (not `~`) in `~/.gemini/config/plugins.json` so Antigravity's language server resolves it reliably.

**Load specific plugins à la carte** using `include_only`:

```json
{
  "entries": [
    {
      "path": "/absolute/path/to/antigravity-customizations/plugins",
      "include_only": ["plan-model-advisor"]
    }
  ]
}
```

**Or load everything** (and toggle individual plugins on/off in Antigravity's Customizations UI):

```json
{
  "entries": [
    {
      "path": "/absolute/path/to/antigravity-customizations/plugins"
    }
  ]
}
```

### Option 2: Install a Single Plugin via the Antigravity CLI (`agy`)

If you prefer copying a single plugin into `~/.gemini/config/plugins/` without wiring up `plugins.json`:

```bash
cd ~/Projects/antigravity-customizations
agy plugin install ./plugins/plan-model-advisor
```

---

## Keeping Personal Preferences Decoupled

Plugins in this repository intentionally avoid baking in personal machine paths, account tiers, or private defaults.

To set your own defaults without forking or editing repo files, add a lightweight preference line to your machine-local `~/.gemini/GEMINI.md`. For example, if you're on Gemini Ultra and want `plan-model-advisor` to optimize purely for security, accuracy, and robustness:

```markdown
# Personal Antigravity Preferences

- Default `plan-model-advisor` profile: `quality-first`
```

Supported `plan-model-advisor` profiles:
* **`quality-first`** — Unconstrained / Ultra tier (standalone frontier models, adversarial cross-family reviews, 2-worker & parallel swarms).
* **`balanced`** *(default)* — Pro / quota-aware daily driver (`Orchestrator (Neon)` & `Orchestrator (Carbon)` for build/test loops, standalone frontier for planning & security paths).
* **`quota-saver`** — Free tier / tight limits / speed (`Gemini 4 Hydrogen` primary driver, skips swarms).

---

## Repository Architecture

```text
antigravity-customizations/
├── plugins/                              # One subdirectory per installable plugin
│   └── plan-model-advisor/
│       ├── plugin.json                   # Official Antigravity manifest
│       ├── README.md                     # Standalone plugin documentation
│       └── skills/
│           └── plan-model-advisor/
│               ├── SKILL.md              # Progressive-disclosure instructions
│               └── references/
│                   └── model-matrix.md   # Easy-to-update model & swarm reference
├── scripts/
│   └── validate_customizations.py        # Zero-dependency manifest/skill/link checker
├── .github/workflows/validate.yml        # Automated PR & push validation
├── Justfile                              # Local QA recipes (`just check`)
├── LICENSE                               # MIT
└── README.md                             # You are here
```

### Design Principles
1. **One Coherent Purpose per Plugin:** Each folder under `plugins/` solves a single workflow problem so users can toggle or cherry-pick cleanly.
2. **Progressive Disclosure:** Keep `SKILL.md` concise and put evolving reference tables (like model matrices) under `references/` so they stay easy to maintain without bloating agent context.
3. **Zero Silent Loader Failures:** Antigravity's plugin loader silently ignores unknown `plugin.json` fields, duplicate plugin names, and misplaced `hooks/hooks.json` files—our validator catches all of them before merge.
4. **Zero Machine-Local Leaks:** Automated checks reject hardcoded local home paths so every plugin stays cleanly portable.

---

## Local Validation & CI

Run all checks locally (requires Python 3.10+; also runs `agy plugin validate --strict` automatically if the Antigravity CLI is installed):

```bash
just check
```

Or run the zero-dependency Python validator directly:

```bash
python3 scripts/validate_customizations.py
```

The GitHub Actions workflow ([`.github/workflows/validate.yml`](./.github/workflows/validate.yml)) runs automatically on every push to `main` and every pull request, verifying:
* `plugin.json` JSON/JSONC validity, allowed top-level schema keys, kebab-case naming, global name uniqueness, and `suggestedPrompts` limits.
* `SKILL.md` YAML frontmatter completeness, directory/name parity, and relative markdown link resolution.
* Native plugin structure (`hooks.json` at plugin root) and zero leaked local filesystem paths.
* Catalog parity between `plugins/` and this `README.md`.

---

## Adding a New Plugin

1. Create `plugins/<plugin-name>/plugin.json` with a unique kebab-case `name`, concise `description`, `version`, and up to 3 `suggestedPrompts`.
2. Add only the subdirectories the plugin actually uses (`skills/<skill>/SKILL.md`, `agents/`, `rules/AGENTS.md`, `hooks.json`, `mcp_config.json`) plus a plugin `README.md`.
3. Add an entry to the **Plugin Catalog** table above.
4. Run `just check` to verify both Python governance checks and `agy plugin validate --strict`.

---

## License

Released under the [MIT License](./LICENSE).
