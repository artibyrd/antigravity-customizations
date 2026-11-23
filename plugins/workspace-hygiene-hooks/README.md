# Workspace Hygiene Hooks

An Antigravity lifecycle hook plugin shipping two independently toggleable hooks for keeping edited files formatted and the workspace root free of temporary scratch scripts and debug logs:

1. **`auto-format` (`PostToolUse`)** — Formats edited workspace files after file-editing tools succeed, dispatching to whichever standard formatter is installed on `PATH` and failing open cleanly if none is present.
2. **`workspace-clean-check` (`Stop`)** — Checks the top-level workspace root for stray scratch scripts and debug logs before the agent finishes a turn, with built-in infinite-loop prevention.

## Hook Overview

### 1. `auto-format` (`PostToolUse`)

Triggered on `write_file|edit_file|replace_file_content|multi_replace_file_content|write_to_file` (timeout: `15s`, per-formatter subprocess timeout: `10s`).

- **Tool schema compatibility:** Reads `toolCall.args.Path` (Antigravity 2.0) and falls back to `toolCall.args.TargetFile` (Antigravity IDE).
- **Skip on tool failure:** If `error` is present in the `PostToolUse` payload, skips formatting immediately.
- **Workspace confinement:** Resolves real paths (`os.path.realpath`) and verifies the target file resides strictly inside one of `workspacePaths` (when non-empty), rejecting `../` traversal, symlink escapes, external paths such as `/tmp`, and files inside `artifactDirectoryPath`.
- **Fail-open multi-language dispatch:** Checks `shutil.which(...)` first, invokes the formatter without `shell=True`, suppresses formatter stdout/stderr, and always outputs `{}` with exit code `0` even if a formatter is absent, fails, or times out.

| Extensions | Formatter Command | Notes |
| :--- | :--- | :--- |
| `.py` | `ruff format <file>` | Formatting only — intentionally does **not** run `ruff check --fix` so imports and semantics are never silently altered. |
| `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`, `.css`, `.json`, `.yaml`, `.yml` | `prettier --write <file>` | Runs with the matched workspace root as working directory so local `.prettierrc` / `.prettierignore` apply. |
| `.go` | `gofmt -w <file>` | Uses standard Go formatting in place. |
| `.rs` | `rustfmt <file>` | Uses standard Rust formatting in place. |

### 2. `workspace-clean-check` (`Stop`)

Triggered when the agent execution loop stops (timeout: `5s`).

- **Infinite-loop prevention:**
  - Checks `continuationActive` **first** — if truthy, immediately returns `{"decision": "allow"}` so the hook never loops twice on the same turn.
  - Ignores any non-`NO_TOOL_CALL` `terminationReason` (such as `USER_CANCELED`, `ERROR`, `MAX_INVOCATIONS`, `MAX_FORCED_INVOCATIONS`, `MAX_TOKEN_BUDGET_EXCEEDED`, `TERMINAL_STEP_TYPE`, `TERMINAL_CUSTOM_HOOK`, `INJECTED_RESPONSE`), non-empty `error`, or `fullyIdle: false` (active background tasks).
  - Fails open with `{"decision": "allow"}` on malformed stdin JSON or missing/empty `workspacePaths`.
- **Top-level regular files only:** Uses `os.scandir` with `entry.is_file(follow_symlinks=False)` directly inside each root in `workspacePaths`. Subdirectories, symlinks, and `artifactDirectoryPath` are never flagged or traversed.
- **Generic stray filename patterns:**
  - Prefixes `scratch_`, `tmp_`, or `debug_` combined with script/log extensions (`.py`, `.sh`, `.js`, `.ts`, `.txt`, `.log`).
  - Exact filenames: `test_fail.log`, `test_output.log`, `debug.log`, `output.tmp`.
- **Decision output:** Returns `{"decision": "continue", "reason": "..."}` listing detected root files so the agent removes them or moves them to its session scratch directory; otherwise returns `{"decision": "allow"}`.

## Prerequisites

- **Python 3.10+** available as `python3` on your `PATH`.
- Zero third-party Python packages required (standard library only).
- Formatters (`ruff`, `prettier`, `gofmt`, `rustfmt`) are **optional** — install only the ones your projects use; missing formatters fail open silently.

## Plugin Structure

```text
plugins/workspace-hygiene-hooks/
├── plugin.json                   # Native Antigravity plugin manifest
├── hooks.json                    # Plugin-root PostToolUse + Stop hook config
├── hooks/
│   ├── auto_format.py            # Executable stdlib-only PostToolUse auto-formatter
│   └── check_workspace_clean.py  # Executable stdlib-only Stop workspace check
└── README.md                     # You are here
```

## Quick Smoke Test

From `plugins/workspace-hygiene-hooks/`:

```bash
# PostToolUse auto-format (always outputs {} and exits 0)
echo '{"workspacePaths":["/tmp"],"toolCall":{"name":"write_file","args":{"Path":"/tmp/example.py"}}}' \
  | python3 ./hooks/auto_format.py
# -> {}

# Stop check on a clean or non-NO_TOOL_CALL payload
echo '{"workspacePaths":["/tmp"],"continuationActive":true,"terminationReason":"NO_TOOL_CALL"}' \
  | python3 ./hooks/check_workspace_clean.py
# -> {"decision": "allow"}
```

To run the full unit test suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## Customization & Disabling Hooks Independently

Both hooks are registered as separate top-level keys in [`hooks.json`](./hooks.json), so you can disable either one independently without turning off the whole plugin:

```json
{
  "auto-format": {
    "enabled": false,
    "PostToolUse": [ ... ]
  },
  "workspace-clean-check": {
    "Stop": [ ... ]
  }
}
```

- **Disable only `auto-format`:** Add `"enabled": false` under `"auto-format"` in [`hooks.json`](./hooks.json).
- **Disable only `workspace-clean-check`:** Add `"enabled": false` under `"workspace-clean-check"` in [`hooks.json`](./hooks.json).
- **Adjust formatters or stray patterns:** Edit `FORMATTER_BY_EXT` in [`hooks/auto_format.py`](./hooks/auto_format.py) or `STRAY_PREFIXES` / `STRAY_EXTENSIONS` / `EXACT_STRAY_FILENAMES` in [`hooks/check_workspace_clean.py`](./hooks/check_workspace_clean.py).
- **Live-sync branch-switch caveat:** If you live-sync this repository's `plugins/` directory via `~/.gemini/config/plugins.json` and check out an older branch where `plugins/workspace-hygiene-hooks/` does not exist yet, Antigravity's already-loaded hooks will fail on `chdir` until you switch back to a branch containing the plugin (or toggle/reload plugins). Keep `plugins/workspace-hygiene-hooks/` merged on `main` when developing new branches.

## Origin & Attribution

- **Origin:** `Original`
- **Notes:** Generalized from our own Antigravity `PostToolUse` and `Stop` lifecycle hooks into a portable, project-agnostic plugin with multi-language fail-open formatter dispatch, strict workspace confinement, and Antigravity `Stop`-hook infinite-loop prevention.
