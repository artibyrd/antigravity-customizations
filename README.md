# Antigravity Customizations

[![Validate Customizations](https://github.com/artibyrd/antigravity-customizations/actions/workflows/validate.yml/badge.svg)](https://github.com/artibyrd/antigravity-customizations/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

A modular, version-controlled collection of **20 reusable Google Antigravity plugins**—shipping **18 skills** (on-demand workflow instructions for the AI) and **2 native lifecycle hook plugins** (automatic safety & hygiene checks), and structured to grow cleanly into custom subagents (separate AI workers for isolated subtasks), rules (always-on instructions), and MCP (Model Context Protocol) tool bundles.

Every plugin under [`plugins/`](./plugins) is self-contained and intentionally scoped to **one coherent workflow**, so you can adopt individual plugins **à la carte** without pulling in unrelated opinions or mandatory setup wizards.

---

## Quick Start: Adopt À La Carte

### 1. Clone the Repository

```bash
git clone https://github.com/artibyrd/antigravity-customizations.git ~/Projects/antigravity-customizations
```

> **Runtime note:** Pure skill plugins have zero runtime dependencies (bash-based helpers like `wizard` assume Linux/macOS/WSL). The two hook plugins (`git-guardrails` and `workspace-hygiene-hooks`) require **Python 3.10+** available as `python3` on `PATH` (if unavailable, omit them via `include_only` in Step 2 so hook commands do not fail).

### 2. Register Plugins with Antigravity

Pick Option 1 or Option 2 for any given plugin—do not enable the same plugin in both, because Antigravity silently shadows duplicate plugin names.

#### Option 1: Live Sync via `~/.gemini/config/plugins.json` *(Recommended)*

Register the repo's `plugins/` directory in `~/.gemini/config/plugins.json` so updates arrive automatically whenever you run `git pull`. Create the file if it does not exist yet; if it already exists, **append** the new object to its `"entries"` array rather than overwriting existing entries.

> **Important:** Use an **absolute path** (not `~`) in `~/.gemini/config/plugins.json` so Antigravity resolves it reliably—for example, `"/Users/<you>/Projects/antigravity-customizations/plugins"` on macOS or `"/home/<you>/Projects/antigravity-customizations/plugins"` on Linux (run `pwd` inside the cloned folder if unsure).

**Start small with a 4-plugin Starter Pack** using `include_only` *(if you disable Antigravity's default auto-run sandbox to require manual approval on every workspace command, omit `git-guardrails`—see its catalog entry below)*:

```json
{
  "entries": [
    {
      "path": "/home/<you>/Projects/antigravity-customizations/plugins",
      "include_only": [
        "plan-model-advisor",
        "tdd",
        "code-review",
        "git-guardrails"
      ]
    }
  ]
}
```

**Or load all 20 plugins** (and toggle individual plugins on/off anytime inside Antigravity's **Customizations / Plugins** UI):

```json
{
  "entries": [
    {
      "path": "/home/<you>/Projects/antigravity-customizations/plugins"
    }
  ]
}
```

#### Option 2: Install a Single Plugin via the Antigravity CLI (`agy`, if installed)

If you prefer copying a single plugin into `~/.gemini/config/plugins/` without editing `plugins.json`:

```bash
cd ~/Projects/antigravity-customizations
agy plugin install ./plugins/plan-model-advisor
```

Re-run `agy plugin install` to update a copied plugin, or run `agy plugin uninstall <name>` to remove it.

### 3. How Plugins Work Once Installed

After editing `~/.gemini/config/plugins.json`, reload Antigravity (or start a new chat session) so Antigravity picks up the new entries. Open Antigravity's **Customizations / Plugins** UI to confirm your plugins appear (if missing, verify `path` is absolute and your JSON is valid); you can toggle loaded plugins on/off there anytime.

* **Skills (18 plugins):** Activate in three ways—automatically when your request matches the skill's description, explicitly by naming it in chat (e.g., *"Implement this feature with `tdd`"* or *"Run `code-review` since `main`"*), or by clicking one of the plugin's **`suggestedPrompts`** (starter prompt chips shown in Antigravity's UI for enabled plugins).
* **Lifecycle Hooks (2 plugins — `git-guardrails`, `workspace-hygiene-hooks`):** Run **automatically** around the AI's tool actions with zero prompting—here, `PreToolUse` runs right before a shell command executes, `PostToolUse` runs right after the AI edits a file, and `Stop` runs right before the AI finishes its reply. To confirm `python3` is resolved and hooks fire cleanly, run the [Quick Smoke Test](./plugins/git-guardrails/README.md#quick-smoke-test). Toggle an entire hook plugin off anytime in Antigravity's **Customizations / Plugins** UI *(to disable just one hook inside a multi-hook plugin without modifying your live-synced clone, omit it via `include_only`—`plugins.json` has no `exclude` key—copy it into `~/.gemini/config/plugins/` via Option 2, and follow the disable note in its `README.md`)*.
* **Your first feature with the Starter Pack:** Create a feature branch (`git checkout -b feat/my-feature`) → type Antigravity's built-in `/plan` command paired with `tdd` (e.g., `/plan Add promo codes to checkout — use tdd to propose public test seams first`) to generate `implementation_plan.md` (visible in Antigravity's Artifacts pane) → ask *"Review `implementation_plan.md` with `plan-model-advisor`"* and apply its recommended model/effort (reasoning depth) or `/teamwork` prompt → build and commit your changes test-first (*"Implement `implementation_plan.md` with `tdd`"*, while `git-guardrails` protects your repo in the background) → ask *"Run `code-review` since `main`"*. You do **not** need to pre-create `AGENTS.md`, `GLOSSARY.md`, or a `Justfile`—every plugin works out of the box on any repo. New to the full workflow? Jump straight to the **[Agentic Pair Programming Protocol](./docs/agentic-pair-programming-protocol.md)** and its **[Checkout Promo Codes Worked Example](./docs/agentic-pair-programming-protocol.md#worked-example-end-to-end-feature-walkthrough)**.

---

## Plugin Catalog

Every plugin carries a short **Origin** label:
* **`Original`** *(6 plugins)* — Authored natively for Google Antigravity from our own workflows.
* **`Combined`** *(9 plugins — Original + [`mattpocock/skills`](https://github.com/mattpocock/skills), MIT)* — Synthesizes upstream concepts with our own Antigravity patterns and guardrails; each plugin's `README.md` explains what came from upstream vs. what was added or altered.
* **`Adapted`** *(5 plugins — [`mattpocock/skills`](https://github.com/mattpocock/skills), MIT)* — Directly translated for Antigravity's native conventions while preserving the core upstream workflow.

### Core Lifecycle Skills (8 Plugins)

| Plugin | Origin | What It Does | Docs |
| :--- | :--- | :--- | :--- |
| **`domain-modeling`** | `Adapted` | Sharpens business/product vocabulary on demand in a pure-domain `GLOSSARY.md` (no code or database jargon) and writes immutable Architecture Decision Records (`docs/adr/`, permanent notes explaining *why* a hard-to-reverse choice was made); pairs with Antigravity's native `/grill-me` requirements interview. | [README](./plugins/domain-modeling/README.md) |
| **`artifact-governance`** | `Combined` | Keeps Antigravity Session Artifacts (stored outside git per chat and viewable in Antigravity's Artifacts pane: `implementation_plan.md`, `walkthrough.md`) as append-only ledgers (with session-log recovery if overwritten), separates actively updated *Living* docs from frozen *Historical* snapshots, keeps scratch scripts out of git, and saves cited research notes. | [README](./plugins/artifact-governance/README.md) |
| **`plan-model-advisor`** | `Combined` | Reviews an implementation plan before coding—auto-checking Antigravity's live model catalog, flagging oversized phases to split into focused ~150k-token chunks (so the AI's context window stays sharp), and outputting a **Model & Swarm Execution Brief** (whether to use one agent or multiple cooperating agents via `/teamwork`) across [`quality-first`, `balanced`, and `quota-saver` profiles](#keeping-personal-preferences-decoupled). | [README](./plugins/plan-model-advisor/README.md) |
| **`tdd`** | `Combined` | Two-phase **Test-Driven Development (TDD)**: pairs with `/plan` to pick stable public test seams (entry points like HTTP endpoints or exported functions) and thin vertical slices (one behavior test + minimal code at a time) *before* coding or multi-agent swarms, then runs red → green loops (failing test → minimal code to pass, saving bigger structural cleanups for review)—banning mocks tied to private internals, tautological assertions (tests that mirror production math so they always pass), and test-file helper stand-ins (copy-pasting simplified logic into the test instead of importing real production code) while keeping tests fast, offline, and deterministic (*hermetic*). | [README](./plugins/tdd/README.md) |
| **`code-review`** | `Combined` | Spawns three parallel fresh read-only subagents (separate AI workers with zero prior chat bias) over committed branch changes (`git diff <fixed-point>...HEAD`, e.g., commits since `main`): **Standards** (+ 12 Fowler code smells—classic maintainability warnings like long parameter lists), **Spec + Reality Check** (missing requirements & hardcoded/fake production behavior), and **Security**, reported side by side as three separate reviews (never merged into one summary, so critical bugs don't get buried). | [README](./plugins/code-review/README.md) |
| **`pr-brief`** | `Combined` | Drafts concise, visual-first pull request bodies and human visual inspection (*Mk1 Eyeball*) checklists: smallest clarifying diagram/diff, Before/After evidence, and Merge Danger (One-Way vs. Two-Way Door—hard vs. easy to roll back—plus blast radius: what breaks if it fails). Credits Matt Pocock and Dex Horthy (`humanlayer/show-me`). | [README](./plugins/pr-brief/README.md) |
| **`release-lifecycle`** | `Original` | Guides the 4-phase delivery cadence (Phase 1: running your repo's tests/linters [*local QA*], staging verification & human sign-off → Phase 2: feature release → Phase 3: native `/learn` session retrospective → Phase 4: optional lean patch release for newly added tests or checks), keeping `CHANGELOG.md` and `ROADMAP.md` synced and degrading cleanly when `gh` (GitHub CLI) or CI/CD is absent. | [README](./plugins/release-lifecycle/README.md) |
| **`knowledge-governance`** | `Combined` | Keeps `AGENTS.md` (your repo's always-loaded agent instruction file) under an 800-token ceiling (~1–2 short pages, since it loads into every prompt and bloat causes the AI to ignore rules) by moving checkable rules into automated tests (the *Demotion Highway*), gating native `/learn` (session retrospective) proposals, supporting optional review-only `CODING_STANDARDS.md` (read only during `code-review` so it doesn't clutter coding prompts), and running a 7-category session retrospective. | [README](./plugins/knowledge-governance/README.md) |

### Always-On Guardrail Hooks (2 Plugins)

| Plugin | Origin | Hooks Included | What It Does | Docs |
| :--- | :--- | :--- | :--- | :--- |
| **`git-guardrails`** | `Combined` | 1 `PreToolUse` hook | Intercepts the agent's shell commands (you can still run any command manually in your own terminal) to hard-block destructive git ops (e.g., `push --force`/`--force-with-lease`/`--mirror`, `reset --hard`, `clean -f`, `branch -D`, `checkout .`, `restore .`) and always prompt before `git push`. Because Antigravity's standard sandbox auto-runs workspace commands while unsandboxed calls (`BypassSandbox: true`) require approval—and returning `allow` from a hook bypasses prompts—it returns `allow` on non-destructive sandboxed commands (matching normal sandbox auto-run) and `ask` on unsandboxed calls so your approval prompts and "Always Allow" cache stay intact. *(Assumes Antigravity's default auto-run sandbox; omit this plugin if you disable sandbox auto-run and require manual approval on every sandboxed command.)* | [README](./plugins/git-guardrails/README.md) |
| **`workspace-hygiene-hooks`** | `Original` | 2 hooks (`PostToolUse`, `Stop`) | Auto-formats edited workspace files when `ruff`, `prettier`, `gofmt`, or `rustfmt` is installed (`PostToolUse`) and prompts the agent before finishing its reply if stray scratch/log files remain in the repo root (`Stop`, stopping after one reminder so the AI can't loop forever). See its README for supported formatters and filename patterns. | [README](./plugins/workspace-hygiene-hooks/README.md) |

### Situational Diagnostics, Design & Ops Skills (10 Plugins)

| Plugin | Origin | What It Does | Docs |
| :--- | :--- | :--- | :--- |
| **`diagnosing-bugs`** | `Adapted` | 6-phase loop for hard bugs and performance regressions: build a tight failing reproduction loop first → minimize → 3–5 testable hypotheses → tagged `[DEBUG-xxxx]` temporary log probes → regression test (locking the bug fixed) at the real public seam → cleanup + secret redaction (includes a guided bash loop script when only a human can trigger the bug). | [README](./plugins/diagnosing-bugs/README.md) |
| **`architecture-review`** | `Combined` | Surveys frequently changed files (`git log` hotspots) using Ousterhout Deep Modules (*rich behavior behind a small interface*, checking whether deleting a module pushes complexity to callers rather than simply removing a thin pass-through wrapper—the *Deletion Test*), runs parallel *Design-It-Twice* explorations (designing 2+ alternative interfaces in parallel to compare trade-offs), pairs Deep Modules with a ~500-line soft trigger for internal splits, and checks optional stack-specific guardrails (avoiding unsafe HTML injection like `.innerHTML`, browser/Playwright checks, modular [`just`](https://github.com/casey/just) command-runner files). | [README](./plugins/architecture-review/README.md) |
| **`reality-check-audit`** | `Original` | Runs a structured "Outsider's Honest Assessment" (*What's Genuinely Good → What's Concerning → What's Aspirational vs. Real → Concrete Remediation Plans*)—best run in a fresh chat on a different AI model family (e.g., Claude ↔ Gemini) to break single-model blind spots (*echo chambers*) and catch hardcoded/fake telemetry or doc drift. | [README](./plugins/reality-check-audit/README.md) |
| **`fresh-reader`** | `Original` | Spawns zero-context read-only subagents across four reader personas (`domain-expert` for specialist rigor; `senior-engineer` → `junior-engineer` → `vibe-coder` for reader clarity) via a top-down cascade (checking structural accuracy before simplifying explanations), triaging 100% of findings (`ACCEPT`, `LINK`, or `WON'T DO`) until a pass produces zero new edits. | [README](./plugins/fresh-reader/README.md) |
| **`writing-for-agents`** | `Combined` | Reference for writing and trimming plugin instruction & config files (`SKILL.md`, `AGENTS.md`, `plugin.json`, `hooks.json`): concise file pointers, high-signal trigger words, positive phrasing, pruning no-op instructions (rules the model already follows by default), and Antigravity schema constraints. | [README](./plugins/writing-for-agents/README.md) |
| **`session-handoff`** | `Adapted` | Compacts an active session into a concise Session Artifact (`handoff_<slug>.md`) with absolute file pointers, settled decisions, ruled-out dead ends, and a copy-ready starter prompt to paste into a new chat—ideal for switching AI model families (e.g., Gemini → fresh Claude chat) or starting a fresh session. | [README](./plugins/session-handoff/README.md) |
| **`bootstrap-approvals`** | `Original` | Primes Antigravity IDE's "Always Allow" cache for unsandboxed or IDE-prompted read commands (e.g., `gh` GitHub CLI, network probes, or workspaces running without auto-run sandboxing) by executing discrete top-level shell reads discovered from the repo (required because the approval cache ignores commands hidden inside helper scripts) so you can click "Always Allow" once per safe command prefix—strictly banning mutating *"Spicy Prefixes"* like `git reset` or `rm`. | [README](./plugins/bootstrap-approvals/README.md) |
| **`repo-bootstrap`** | `Original` | Optional interactive scaffolder (never required by other plugins): checks local tool readiness and selectively initializes a `<800`-token `AGENTS.md`, a modular `Justfile` (Makefile-like task runner separating read-only *safe* vs. confirmation-*gated* mutating recipes), optional `CODING_STANDARDS.md`, `GLOSSARY.md`, `docs/adr/`, and automated governance test skeletons (placeholder checks for docs, schemas, and project invariants—rules that must always hold true). | [README](./plugins/repo-bootstrap/README.md) |
| **`prototype`** | `Adapted` | Builds throwaway single-file HTML logic demos or radically different toggleable UI variations to answer design questions fast—rendered via Antigravity Artifacts or `generative_ui` (Antigravity's interactive HTML widget renderer). | [README](./plugins/prototype/README.md) |
| **`wizard`** | `Adapted` | Generates safe, interactive bash runbooks (from its bundled `template.sh` with silent `read -rs` secret prompts and `[y/N]` confirm gates) walking humans step by step through tasks agents cannot perform (infra provisioning, CI secrets, third-party dashboards, production switchovers). | [README](./plugins/wizard/README.md) |

### Architecture & Workflow Guides
* **[Agentic Pair Programming Protocol](./docs/agentic-pair-programming-protocol.md)** — End-to-end walkthrough showing how the 8 core lifecycle skills, 2 always-on hook plugins, 10 situational skills, and native Antigravity slash commands chain together across a real feature.
* **[Upstream Adaptations, Provenance & Deviations](./docs/upstream-adaptations-and-deviations.md)** — Optional background for maintainers and `mattpocock/skills` migrants: full 20-plugin provenance matrix, rationale for our Antigravity deviations, and upstream audit notes.

---

## Keeping Personal Preferences Decoupled

Plugins in this repository avoid baking in personal machine paths, account tiers, or private defaults. Currently, **`plan-model-advisor`** is the only plugin that reads personal preferences from your machine-local `~/.gemini/GEMINI.md` (Antigravity's global, always-loaded personal instructions file—plain-English notes read by the AI, distinct from repo-level `AGENTS.md`; create it if it does not exist yet). `knowledge-governance` also audits `~/.gemini/GEMINI.md` during retrospectives. Example `~/.gemini/GEMINI.md` snippet *(swap `balanced` for `quality-first` [Ultra] or `quota-saver` [Free] to match your tier—or override it for a single run in chat, e.g., "review this plan using `quality-first`")*:

```markdown
# Personal Antigravity Preferences

- Default `plan-model-advisor` profile: `balanced`
- Always run `plan-model-advisor` and pause for confirmation before executing an implementation plan.
```

Built-in `plan-model-advisor` profiles (specific model names below are Antigravity's current catalog models and auto-refresh before each review):
* **`quality-first`** — Unconstrained / Ultra tier (top standalone models, cross-family reviews using two different AI families like Claude ↔ Gemini to catch blind spots, and multi-agent `/teamwork` swarms).
* **`balanced`** *(built-in default if unset in `GEMINI.md`)* — Pro / quota-aware daily driver (orchestrated fast models like `Orchestrator (Neon)` & `Orchestrator (Carbon)` for build/test loops, top standalone models for planning & security paths).
* **`quota-saver`** — Free tier / tight limits / speed (lightweight fast model like `Gemini 4 Hydrogen`, skips multi-agent swarms).

---

## Repository Architecture

*For contributors and plugin authors (skip this section if you only want to install and use plugins):*

```text
antigravity-customizations/
├── plugins/                                     # 20 standalone plugins (one directory per plugin)
│   ├── code-review/                             # Example skill plugin layout
│   │   ├── plugin.json                          # Official Antigravity manifest
│   │   ├── README.md                            # Standalone plugin docs & attribution
│   │   └── skills/code-review/
│   │       ├── SKILL.md                         # Progressive-disclosure instructions
│   │       └── references/                      # On-demand checklists & rubrics
│   ├── git-guardrails/                          # Example native hook plugin layout
│   │   ├── plugin.json
│   │   ├── README.md
│   │   ├── hooks.json                           # MUST live at plugin root
│   │   └── hooks/guard_git.py                   # Built-in Python stdlib hook script (no pip install)
│   └── ... (18 more standalone plugins)
├── docs/
│   ├── agentic-pair-programming-protocol.md     # End-to-end workflow + situational skill matrix
│   └── upstream-adaptations-and-deviations.md   # Provenance, deviations & upstream audit
├── scripts/
│   └── validate_customizations.py               # Zero-dependency manifest/skill/hook/doc checker
├── tests/
│   ├── test_git_guardrails.py                   # Stdlib unittest suite for git-guardrails hook
│   └── test_workspace_hygiene_hooks.py          # Stdlib unittest suite for workspace-hygiene-hooks
├── .github/workflows/validate.yml               # Automated PR & push validation + hook unit tests
├── Justfile                                     # Local QA recipes (`just check`)
├── LICENSE                                      # MIT
└── README.md                                    # You are here
```

### Design Principles
1. **One Coherent Purpose per Plugin:** Each folder under `plugins/` solves a single workflow problem so users can toggle or cherry-pick cleanly.
2. **Progressive Disclosure:** Keep `SKILL.md` concise and put evolving reference tables or checklists under `references/` so they stay easy to maintain without bloating agent context.
3. **Zero Silent Loader Failures:** Antigravity's plugin loader silently ignores unknown `plugin.json` fields and misplaced `hooks/hooks.json` files, and silently shadows duplicate plugin names—our validator catches all of them before merge.
4. **Zero Machine-Local Leaks:** Automated checks reject hardcoded local home paths so every plugin stays cleanly portable.

---

## Local Validation & CI

*For contributors or anyone customizing plugins locally (not required just to install and use plugins):*

If you have [`just`](https://github.com/casey/just) installed, run all local checks in one command (requires Python 3.10+; automatically runs `agy plugin validate --strict` if the Antigravity CLI is on `PATH`):

```bash
just check
```

Or run each validation gate directly without `just`:

```bash
python3 scripts/validate_customizations.py
python3 -m unittest discover -s tests -v
bash -euo pipefail -c 'for d in plugins/*/; do agy plugin validate --strict "$d"; done'  # optional, if agy CLI is installed
```

The GitHub Actions workflow ([`.github/workflows/validate.yml`](./.github/workflows/validate.yml)) runs automatically on every push to `main` and every pull request, verifying:
* `plugin.json` JSON/JSONC validity, allowed top-level schema keys, kebab-case naming, global name uniqueness, and `suggestedPrompts` limits (max 3).
* `SKILL.md` YAML frontmatter completeness, directory/name parity, rejection of Claude Code–only frontmatter keys, and relative markdown link resolution (including `references/`).
* Native plugin `hooks.json` placement and schema validity (rejecting misplaced `hooks/hooks.json` and verifying referenced local scripts exist) plus built-in Python `unittest` coverage under `tests/` (zero third-party packages).
* Zero leaked local filesystem paths across `plugins/` and `docs/`, valid relative links in `docs/**/*.md`, and catalog parity between `plugins/` and this `README.md`.

---

## Credits & Upstream Attribution

Several plugins in this repository are directly adapted from or combined with ideas from:
* **[Matt Pocock's `skills`](https://github.com/mattpocock/skills)** (*Copyright (c) 2026 Matt Pocock*, MIT License) — upstream foundation for `diagnosing-bugs`, `tdd`, `code-review`, `git-guardrails`, `knowledge-governance` (`retro`), `writing-for-agents`, `architecture-review`, `pr-brief`, `session-handoff`, `artifact-governance` (`research`), `domain-modeling`, `prototype`, `wizard`, and context-slicing / explore-first notes in `plan-model-advisor`.
* **[Dex Horthy / Humanlayer (`show-me`)](https://github.com/humanlayer/humanlayer)** — visual summary menu (pseudocode, call trees, component trees, file trees, Mermaid, diffs) and placement guidance preserved via `pr-brief`.

Because `mattpocock/skills` targets Claude Code's conventions, every adapted or combined plugin here has been re-engineered for **Google Antigravity** (strict `name`/`description` frontmatter, standalone à la carte `plugin.json` packaging with zero global setup requirements, native `invoke_subagent`/`swarm` orchestration, Antigravity Artifacts instead of `/tmp` + `xdg-open`, and plugin-root `hooks.json` JSON contracts). Each plugin's individual `README.md` includes an **`Origin & Attribution`** section, and **[`docs/upstream-adaptations-and-deviations.md`](./docs/upstream-adaptations-and-deviations.md)** explains every deviation and intentionally excluded upstream skill in detail.

---

## Adding a New Plugin

*For contributors and plugin authors:*

1. Create `plugins/<plugin-name>/plugin.json` with a unique kebab-case `name`, concise `description`, `version`, and up to 3 `suggestedPrompts` (see [`plugins/writing-for-agents/skills/writing-for-agents/references/antigravity-mechanics.md`](./plugins/writing-for-agents/skills/writing-for-agents/references/antigravity-mechanics.md) for the exact allowed manifest keys and frontmatter rules, or copy an existing plugin folder as a template).
2. Add only the files and subdirectories the plugin actually uses (`skills/<skill>/SKILL.md`, `agents/`, `rules/`, `hooks.json`, `mcp_config.json`) plus a plugin `README.md` (and, for hook plugins, a repo-root `tests/test_<plugin>.py` unittest suite).
3. Add an entry to the **Plugin Catalog** table above (and update plugin counts plus [`docs/agentic-pair-programming-protocol.md`](./docs/agentic-pair-programming-protocol.md) and [`docs/upstream-adaptations-and-deviations.md`](./docs/upstream-adaptations-and-deviations.md) with its workflow placement and provenance).
4. Run `just check` to verify Python governance checks, hook unit tests, and `agy plugin validate --strict`.

---

## License

Released under the [MIT License](./LICENSE).
