# Antigravity Customizations

[![Validate Customizations](https://github.com/artibyrd/antigravity-customizations/actions/workflows/validate.yml/badge.svg)](https://github.com/artibyrd/antigravity-customizations/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

A modular, version-controlled collection of reusable **Google Antigravity** plugins—starting with skills and designed to grow cleanly into agents, rules, hooks, and MCP bundles.

Every plugin in [`plugins/`](./plugins) is self-contained and intentionally scoped to **one coherent workflow**, so you can adopt individual plugins **à la carte** without pulling in unrelated opinions or all-or-nothing toggles.

---

## Plugin Catalog

Every plugin carries an explicit **Origin** label:
* **`Original`** — Authored natively for Google Antigravity from our workflows.
* **`Adapted (mattpocock/skills)`** — Translated from [Matt Pocock's `skills`](https://github.com/mattpocock/skills) (MIT License) for Antigravity's native plugin, skill, subagent, and hook conventions while preserving the core upstream workflow.
* **`Combined (Original + mattpocock/skills)`** — Synthesizes concepts from `mattpocock/skills` with our own Antigravity patterns and guardrails; each plugin's `README.md` documents exactly what came from upstream vs. what was added or altered.

| Plugin | Origin | Components | What It Does | Docs |
| :--- | :--- | :--- | :--- | :--- |
| **`plan-model-advisor`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`plan-model-advisor`) | Reviews an implementation plan before coding—auto-checking Antigravity's live model catalog, flagging ~150k context-window slicing opportunities, and outputting a **Model & Swarm Execution Brief** across `quality-first`, `balanced`, and `quota-saver` profiles. | [Plugin README](./plugins/plan-model-advisor/README.md) |
| **`knowledge-governance`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`knowledge-governance`) | Manages the 4-Tier Knowledge Taxonomy (`AGENTS.md` <800 tokens Class α/β/γ → Tier 1 Skills → optional review-only `CODING_STANDARDS.md` → Tier 2 Test Gates → Tier 3 Docs), the Demotion Highway, `/learn` Admission Gate, Living Invariants vs. Historical ADRs, and Matt Pocock's 7 retro diagnostic categories. | [Plugin README](./plugins/knowledge-governance/README.md) |
| **`diagnosing-bugs`** | `Adapted (mattpocock/skills)` | 1 Skill (`diagnosing-bugs`) + HITL script | 6-phase disciplined loop for hard bugs and performance regressions: build a tight, red-capable feedback loop first → reproduce & minimise → 3–5 falsifiable hypotheses → `[DEBUG-xxxx]` probes → seam regression test → cleanup + `<REDACTED>` secret hygiene. | [Plugin README](./plugins/diagnosing-bugs/README.md) |
| **`tdd`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`tdd`) | Vertical-slice red-green-refactor TDD at pre-agreed public seams, banning implementation-coupled mocks, tautological assertions, and horizontal slicing—paired with hermetic offline testing guardrails. | [Plugin README](./plugins/tdd/README.md) |
| **`code-review`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`code-review`) | Runs three parallel fresh Antigravity subagents (`invoke_subagent`) over `git diff <fixed-point>...HEAD`: **Axis 1 (Standards + 12 Fowler Code Smells)**, **Axis 2 (Spec Fidelity + Reality-Check/Zero-Mock lens)**, and **Axis 3 (Security)**, reported side by side without merging or reranking. | [Plugin README](./plugins/code-review/README.md) |
| **`git-guardrails`** | `Combined (Original + mattpocock/skills)` | 1 `PreToolUse` Hook (`hooks.json`) | Native Antigravity `PreToolUse` hook hard-blocking destructive git commands (`push --force`/`--mirror`, `reset --hard`, `clean -f`, `branch -D`, `checkout .`, `restore .`), `force_ask`-gating `git push`, allowing local `git commit`, and using a sandbox-aware `ask`/`allow` fallback. | [Plugin README](./plugins/git-guardrails/README.md) |
| **`writing-for-agents`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`writing-for-agents`) | Authoring guide for Antigravity skills, plugins, `AGENTS.md`, and `hooks.json` combining Matt Pocock's prompt-craft levers (context pointers, leading words, anti-negation, no-op hunting, pruning) with Antigravity schema rules and the <800-token `AGENTS.md` ceiling. | [Plugin README](./plugins/writing-for-agents/README.md) |
| **`architecture-review`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`architecture-review`) | Hotspot-scoped architecture review harmonizing Ousterhout Deep Modules (Deletion Test, Design-It-Twice parallel subagents) with a ~500 LOC soft internal decomposition trigger, Antigravity Mermaid Artifacts, and operational guardrails (safe DOM sinks, Playwright lazy-image checks, modular Justfiles). | [Plugin README](./plugins/architecture-review/README.md) |
| **`pr-brief`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`pr-brief`) | Visual-first PR body and Mk1 Eyeball walkthrough template: smallest clarifying visual (pseudocode, call/file/component tree, Mermaid, diff), Before/After Evidence, and Merge Danger (One-Way vs. Two-Way Door + Blast Radius). Credits Matt Pocock and Dex Horthy (`humanlayer/show-me`). | [Plugin README](./plugins/pr-brief/README.md) |
| **`bootstrap-approvals`** | `Original` | 1 Skill (`bootstrap-approvals`) | Repo-agnostic Antigravity IDE permission priming: dynamically discovers safe read-only commands (`Justfile`, `Makefile`, `pyproject.toml`, `package.json`, `git`, `gh`), enforces the Subprocess Isolation Rule, and strictly bans *"Spicy Prefixes"* whose sibling args can mutate state. | [Plugin README](./plugins/bootstrap-approvals/README.md) |
| **`session-handoff`** | `Adapted (mattpocock/skills)` | 1 Skill (`session-handoff`) | Compacts the current session into a sparse, absolute-path handoff artifact (`handoff_<slug>.md`) with context pointers, settled decisions, ruled-out dead ends, and exact next steps—tailored for Antigravity ↔ cross-model (e.g., Gemini → Claude) or fresh-session handoffs. | [Plugin README](./plugins/session-handoff/README.md) |
| **`artifact-governance`** | `Combined (Original + mattpocock/skills)` | 1 Skill (`artifact-governance`) | Enforces Living Document vs. Historical Artifact badges, the Append-Only Ledger Protocol for `implementation_plan.md` & `walkthrough.md` (with `transcript_full.jsonl` recovery), the Clean Scratch Script Ritual, and primary-source cited research notes. | [Plugin README](./plugins/artifact-governance/README.md) |
| **`reality-check-audit`** | `Original` | 1 Skill (`reality-check-audit`) | Runs a structured cross-model "Outsider's Honest Assessment" (`Good → Concerning → Aspirational vs. Real → Remediation Plans`) to hunt mocked/hardcoded telemetry, doc-vs-code drift, and governance bloat. | [Plugin README](./plugins/reality-check-audit/README.md) |
| **`domain-modeling`** | `Adapted (mattpocock/skills)` | 1 Skill (`domain-modeling`) | Builds and sharpens a project's domain model lazily (`GLOSSARY.md` devoid of implementation details + 3-criteria Historical ADR gate, clearly distinct from Living Invariants), paired with native `/grill-me`. | [Plugin README](./plugins/domain-modeling/README.md) |
| **`release-lifecycle`** | `Original` | 1 Skill (`release-lifecycle`) | Guides the 4-phase delivery and continuous learning cadence (`Local QA → PR/Dev Probe → Mk1 Eyeball → Release → /learn → Lean Patch`), `CHANGELOG`/`ROADMAP` symmetry, graceful preflight when `gh`/CI is absent, and topological multi-repo PR merge order. | [Plugin README](./plugins/release-lifecycle/README.md) |
| **`repo-bootstrap`** | `Original` | 1 Skill (`repo-bootstrap`) | Optional, never-required interactive scaffolder for new repos: checks tool readiness and selectively initializes a `<800`-token `AGENTS.md`, modular `Justfile` safe/gated skeleton, optional `CODING_STANDARDS.md`, `GLOSSARY.md`, `docs/adr/`, and governance tests. | [Plugin README](./plugins/repo-bootstrap/README.md) |
| **`workspace-hygiene-hooks`** | `Original` | 2 Hooks (`PostToolUse`, `Stop`) | Native plugin-root `hooks.json` with independently toggleable hooks: workspace-confined, fail-open `PostToolUse` auto-formatter (`ruff`, `prettier`, `gofmt`, `rustfmt`) and loop-safe `Stop` guard catching stray scratch/log files in workspace root. | [Plugin README](./plugins/workspace-hygiene-hooks/README.md) |
| **`prototype`** | `Adapted (mattpocock/skills)` | 1 Skill (`prototype`) | Builds throwaway single-file HTML logic prototypes or radically different toggleable UI variations to resolve design questions quickly—adapted for Antigravity Artifacts and `generative_ui`. | [Plugin README](./plugins/prototype/README.md) |
| **`wizard`** | `Adapted (mattpocock/skills)` | 1 Skill (`wizard`) + bash template | Generates safe, interactive bash runbook wizards (`template.sh`, `read -rs` secret hygiene, `[y/N]` gates) walking humans through steps agents cannot perform (infra provisioning, CI secrets, third-party dashboards, cutovers). | [Plugin README](./plugins/wizard/README.md) |

### Architecture & Workflow Guides
* **[Agentic Pair Programming Protocol](./docs/agentic-pair-programming-protocol.md)** — End-to-end walkthrough showing how our standard 5-stage feature lifecycle strings these plugins and native Antigravity slash commands together, plus a situational decision matrix and worked example.
* **[Upstream Adaptations, Provenance & Deviations](./docs/upstream-adaptations-and-deviations.md)** — Full 19-plugin provenance table, principled rationale for every deviation from `mattpocock/skills`, and complete 39-skill accounting (including all 26 intentionally excluded skills and why).

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
├── plugins/                              # One subdirectory per installable plugin (19 plugins)
│   ├── plan-model-advisor/               # Model, effort, context-slicing & swarm advisor
│   ├── knowledge-governance/             # 4-Tier taxonomy, Demotion Highway & retro checklist
│   ├── diagnosing-bugs/                  # 6-phase red-loop debugging discipline + HITL script
│   ├── tdd/                              # Vertical-slice seam TDD + hermetic testing
│   ├── code-review/                      # Parallel 3-axis review (Standards, Spec, Security)
│   ├── git-guardrails/                   # Native PreToolUse hooks.json destructive-git guard
│   ├── writing-for-agents/               # Prompt craft + Antigravity skill/hook mechanics
│   ├── architecture-review/              # Deep Modules + ~500 LOC trigger + operational guardrails
│   ├── pr-brief/                         # Visual-first PR body & Mk1 Eyeball walkthrough standard
│   ├── bootstrap-approvals/              # Repo-agnostic Antigravity IDE permission priming
│   ├── session-handoff/                  # Sparse cross-model / fresh-session handoff artifacts
│   ├── artifact-governance/              # Living vs. Historical docs, append-only ledgers & notes
│   ├── reality-check-audit/              # Cross-model adversarial "Outsider's Honest Assessment"
│   ├── domain-modeling/                  # Lazy GLOSSARY.md + 3-criteria Historical ADR gate
│   ├── release-lifecycle/                # 4-phase cadence, graceful preflight & merge order
│   ├── repo-bootstrap/                   # Optional interactive repo governance scaffolder
│   ├── workspace-hygiene-hooks/          # Native PostToolUse formatter & Stop scratch-file guard
│   ├── prototype/                        # Throwaway HTML logic & toggleable UI prototypes
│   └── wizard/                           # Interactive human-in-the-loop bash runbook generator
├── docs/
│   ├── agentic-pair-programming-protocol.md     # Standard workflow + situational skill matrix
│   └── upstream-adaptations-and-deviations.md   # Provenance, deviations & 39-skill audit
├── scripts/
│   └── validate_customizations.py        # Zero-dependency manifest/skill/hook/doc link checker
├── tests/
│   ├── test_git_guardrails.py            # Stdlib unittest suite for git-guardrails hook
│   └── test_workspace_hygiene_hooks.py   # Stdlib unittest suite for workspace-hygiene-hooks
├── .github/workflows/validate.yml        # Automated PR & push validation + hook unit tests
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
* `SKILL.md` YAML frontmatter completeness, directory/name parity, rejection of Claude Code–only frontmatter keys, and relative markdown link resolution (including `references/`).
* Native plugin `hooks.json` placement and schema validity (rejecting misplaced `hooks/hooks.json` and verifying referenced local scripts exist) plus stdlib `unittest` coverage under `tests/`.
* Zero leaked local filesystem paths across `plugins/` and `docs/`, valid relative links in `docs/**/*.md`, and catalog parity between `plugins/` and this `README.md`.

---

## Credits & Upstream Attribution

Several plugins in this repository are directly adapted from or combined with ideas from:
* **[Matt Pocock's `skills`](https://github.com/mattpocock/skills)** (*Copyright (c) 2026 Matt Pocock*, MIT License) — upstream foundation for `diagnosing-bugs`, `tdd`, `code-review`, `git-guardrails`, `knowledge-governance` (`retro`), `writing-for-agents`, `architecture-review`, `pr-brief`, `session-handoff`, `artifact-governance` (`research`), `domain-modeling`, `prototype`, `wizard`, and v1.2.0 slicing notes in `plan-model-advisor`.
* **[Dex Horthy / Humanlayer (`show-me`)](https://github.com/humanlayer/humanlayer)** — visual summary menu (pseudocode, call trees, component trees, file trees, Mermaid, diffs) and placement guidance preserved via `pr-brief`.

Because `mattpocock/skills` targets Claude Code's conventions, every adapted or combined plugin here has been re-engineered for **Google Antigravity** (strict `name`/`description` frontmatter, standalone à la carte `plugin.json` packaging with zero global setup requirements, native `invoke_subagent`/`swarm` orchestration, Antigravity Artifacts instead of `/tmp` + `xdg-open`, and plugin-root `hooks.json` JSON contracts). Each plugin's individual `README.md` includes an **`Origin & Attribution`** section, and **[`docs/upstream-adaptations-and-deviations.md`](./docs/upstream-adaptations-and-deviations.md)** explains every deviation and intentionally excluded upstream skill in detail.

---

## Adding a New Plugin

1. Create `plugins/<plugin-name>/plugin.json` with a unique kebab-case `name`, concise `description`, `version`, and up to 3 `suggestedPrompts`.
2. Add only the subdirectories the plugin actually uses (`skills/<skill>/SKILL.md`, `agents/`, `rules/AGENTS.md`, `hooks.json`, `mcp_config.json`) plus a plugin `README.md`.
3. Add an entry to the **Plugin Catalog** table above.
4. Run `just check` to verify both Python governance checks and `agy plugin validate --strict`.

---

## License

Released under the [MIT License](./LICENSE).
