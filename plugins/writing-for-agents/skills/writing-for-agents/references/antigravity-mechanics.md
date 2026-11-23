# Antigravity Packaging & Validation Mechanics

The Antigravity-specific branch of [writing-for-agents](../SKILL.md): how Antigravity discovers, budgets, and validates steering files, skills, plugins, and lifecycle hooks. Apply the universal writing levers in `SKILL.md` to every file described below.

---

## 1. Steering Files & Context Budgets (`AGENTS.md` / `GEMINI.md`)

- **Discovery:** Antigravity walks up from the working directory to the repository root, loading directory-based `AGENTS.md` and `GEMINI.md` files (plus user-global `~/.gemini/GEMINI.md` and enabled plugin `rules/AGENTS.md`). Standalone steering files do **not** use YAML frontmatter and are always active for their scope.
- **Platform Limits:** Each rule file caps at `24 KB` (`24,000` bytes) and all always-on/global rules share a `20,000`-token aggregate budget (over-budget rules are demoted to file path pointers).
- **Recommended Root `AGENTS.md` Ceiling (`<800` Tokens):** Platform caps are safety rails, not targets. Keep root `AGENTS.md` under **800 tokens** (`word_count * 1.33`) so attention stays crisp on every turn:
  - Keep only universal invariants (one crisp sentence each) and sparse navigation pointers.
  - Move mechanical checks (formatting, manifest parity, link checks, schema rules) down into fast automated tests/linters instead of spending always-on tokens.
  - Move subsystem procedures into on-demand skills (`skills/<name>/SKILL.md`) with disclosed `references/`.
  - Keep this **agent context ceiling** strictly distinct from source-code modularity thresholds (such as internal file decomposition triggers).

---

## 2. Skill Mechanics (`skills/<name>/SKILL.md`)

### Directory Layout

```text
skills/<skill-name>/
├── SKILL.md          # Required: main instructions + YAML frontmatter
├── references/       # Optional: progressive-disclosure manuals linked from SKILL.md
├── scripts/          # Optional: executable helper scripts
├── examples/         # Optional: reference implementations
└── resources/        # Optional: templates or static assets
```

### Strict Frontmatter Contract

`SKILL.md` frontmatter MUST contain **only** `name` and `description`:

```yaml
---
name: my-skill-name
description: >-
  Third-person summary of what the skill does and the exact trigger branches
  that should activate it.
---
```

- **`name`**: lowercase kebab-case matching the parent directory (`skills/<skill-name>/`).
- **`description`**: the skill's always-loaded top-level context pointer. Apply the context-pointer rules from [SKILL.md](../SKILL.md): front-load leading words, one trigger per distinct branch, zero filler.
- **Disallowed foreign frontmatter keys:** Never include non-Antigravity keys such as `disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, `agent`, or `allowed-tools`. They are unsupported in Antigravity and rejected by strict repo validation.

### Invocation, Discovery & Splitting

In Antigravity, every skill carries a `description` for discovery, while explicit human entrypoints are surfaced cleanly in `plugin.json` via `suggestedPrompts` (max 3):

- **Auto-triggered skills:** Write a sharp `description` naming the concrete trigger branches and leading words the agent should recognize autonomously.
- **Human-steered / on-demand skills:** Keep the `description` concise and specific so it does not fire spuriously, and expose clear starter prompts in `plugin.json` `suggestedPrompts`.
- **Splitting by invocation:** Split out a separate skill only when a distinct leading word or workflow branch genuinely warrants independent activation and earns its always-loaded description tokens.
- **Standalone / à la carte packaging:** Never instruct an agent to cross-invoke another optional plugin's skill as a hard dependency. Bundle shared reference files inside `references/` (or link to an external repo doc) so every plugin works standalone out of the box.

### Project-Specific Skill Overlays (`.agents/overrides/<skill-name>.md`)

When a repository needs to tighten, extend, or disable parts of a generalized skill without shadowing or forking the upstream plugin:

- **Location & Naming:** Place a plain Markdown file at `.agents/overrides/<skill-name>.md` (matching the skill's kebab-case `name`). Never name it `SKILL.md`—doing so registers a competing skill that shadows the upstream plugin and blocks updates.
- **Zero Always-On Cost:** Because `.agents/overrides/` is not indexed into the always-loaded skill catalog, overlays consume **0 tokens** until the target skill activates.
- **3-Section Delta Contract:** Structure every overlay as self-contained, harness-agnostic Markdown (readable both as a skill overlay and as a standalone project guide on non-Antigravity harnesses):
  - `## Overrides` — Base-skill thresholds or defaults this repository tightens, relaxes, or replaces.
  - `## Extensions` — Repository-specific invariants, commands, scripts, or extra verification gates.
  - `## Disabled / Not Applicable` — Optional base-skill steps or artifacts skipped in this repository.
- **Two-Layer Discovery:** Customizable upstream skills include a 1-line preflight note checking `.agents/overrides/<skill-name>.md`, and repositories add a 1-line pointer in `AGENTS.md` directing agents to check `.agents/overrides/<skill>.md` before running generalized workflows.

---

## 3. Plugin Manifest (`plugin.json`)

```text
plugins/<plugin-name>/
├── plugin.json       # Required: manifest
├── README.md         # Recommended: overview, files, prompts, attribution
├── hooks.json        # Optional: lifecycle hooks (MUST be at plugin root)
├── mcp_config.json   # Optional: MCP servers
├── rules/            # Optional: rules loaded when plugin is enabled (rules/AGENTS.md)
└── skills/           # Optional: bundled skills
    └── <skill-name>/
        └── SKILL.md
```

### Allowed `plugin.json` Keys

The Antigravity loader **silently discards** unknown top-level keys. Stick strictly to the supported manifest schema:

| Key | Requirement / Constraints |
| :--- | :--- |
| `$schema` | Optional schema URI string. |
| `name` | Lowercase kebab-case; globally unique across installed plugins (duplicates silently shadow one another). |
| `displayName` | Optional human-readable title. |
| `version` | Semantic version string (e.g., `"1.0.0"`). |
| `description` | Required non-empty summary string. |
| `author` | String or `{"name": "...", "url": "https://..."}`. |
| `homepage` | Optional `https://` documentation/project URL. |
| `repository` | Optional `https://` URL or `{"type": "git", "url": "https://..."}`. |
| `logo` | Optional relative path to an existing `.png`, `.svg`, `.jpg`, `.jpeg`, or `.webp` asset. |
| `suggestedPrompts` | Optional list of **at most 3** non-empty starter prompts. |
| `disabled` | Optional boolean (`true` ships the plugin switched off by default). |

---

## 4. Native Lifecycle Hooks (`hooks.json`)

- **Root Placement Mandatory:** Native Antigravity plugins MUST place `hooks.json` directly at `<plugin-dir>/hooks.json`. A nested `hooks/hooks.json` is silently ignored by native plugin discovery.
- **Top-Level Structure:** A JSON object mapping named hooks to `enabled` (optional bool) and one or more supported events:
  - **Tool events (grouped with `matcher` regex + `hooks` array):** `PreToolUse`, `PostToolUse` (e.g., `"matcher": "run_command"`).
  - **Lifecycle events (flat array of handler objects):** `SessionStart`, `PreInvocation`, `PostInvocation`, `Stop`.
- **Handler Fields:** `type` (`"command"`, default), `command` (required shell command run with CWD = plugin root; `PLUGIN_ROOT` and `PLUGIN_DATA` env vars are provided), `timeout` (optional seconds, default `30`).
- **JSON Stdin/Stdout Contract (camelCase protojson):**
  - `PreToolUse` receives `toolCall.name` and `toolCall.args` (e.g., `toolCall.args.CommandLine` for `run_command`) plus common metadata (`cwd`, `workspacePaths`, `hookEventName`), and outputs JSON on stdout: `{"decision": "allow" | "deny" | "ask" | "force_ask", "reason": "..."}`.
  - `PostToolUse` outputs `{}`.
  - `Stop` inspects `continuationActive` (to avoid infinite loops) and outputs `{"decision": "continue", "reason": "..."}` or allows stopping.

---

## 5. Pre-Merge Validation Pitfalls

Run both `agy plugin validate --strict <plugin-dir>` and `python3 scripts/validate_customizations.py` (when in a repo that ships the validator) before committing. Common silent failures caught by validation:

| Pitfall | Consequence / Fix |
| :--- | :--- |
| Unknown top-level key in `plugin.json` | Silently ignored by the Antigravity loader → remove unsupported keys. |
| Duplicate `plugin.json` `name` | Silently shadows another plugin → use a unique kebab-case name. |
| More than 3 `suggestedPrompts` | Rejected by strict validation → keep the 3 highest-signal prompts. |
| Foreign frontmatter keys in `SKILL.md` | Rejected (`disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, `agent`, `allowed-tools`) → keep only `name` and `description`. |
| `SKILL.md` `name` ≠ directory name | Loader/validator mismatch → match kebab-case `name` to `skills/<name>/`. |
| `hooks/hooks.json` instead of root `hooks.json` | Silently skipped at runtime → move to `<plugin-dir>/hooks.json`. |
| Missing relative script in `hooks.json` `command` | Hook fails at runtime → verify every `./...` script path exists and is executable. |
| Broken relative Markdown links | Dead pointers waste agent turns → verify every relative link in `SKILL.md`, `references/*.md`, and `README.md`. |
| Machine-local absolute paths | Leaks host environment and breaks portability → use relative links or `~` / repo-relative paths instead of user-specific home paths. |
| Root `README.md` catalog drift | New plugin omitted from repo catalog → register `plugins/<name>` in the catalog when landing on `main`. |
