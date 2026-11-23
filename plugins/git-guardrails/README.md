# Git Guardrails

An Antigravity `PreToolUse` lifecycle hook plugin that intercepts `run_command` tool calls to hard-block destructive git commands and require explicit user confirmation before pushing—while keeping routine local git workflows (`git commit`, `git add`, `git status`, `git diff`, etc.) fast and uninterrupted.

## Policy Summary

| Decision | Git Commands Covered | Why |
| :--- | :--- | :--- |
| **`deny`** *(hard block)* | **Force pushes:** `git push` with `--force`, `-f` (or combined short flags like `-uf`), `--force-with-lease`, `--force-if-includes`, `--mirror`, or a `+` refspec prefix (`+main`, `+HEAD:main`) | Rewrites, overwrites, or mirror-deletes remote branch history. |
| **`deny`** *(hard block)* | **`git reset --hard`** (any flag order or ref) | Permanently discards uncommitted working-tree and index changes. |
| **`deny`** *(hard block)* | **`git clean`** with `-f` / `--force` (including combined short flags such as `-fd`, `-fx`, `-df`, `-xf`, `-d -f`) | Permanently deletes untracked files and directories. |
| **`deny`** *(hard block)* | **`git branch -D`**, `git branch --delete --force`, `git branch -d -f` / `-df` / `-fd` | Force-deletes branches that may contain unmerged commits. |
| **`deny`** *(hard block)* | **`git checkout .`**, `git checkout -- .`, `git checkout <ref> -- .`, `git checkout <ref> .` (and `./`, `:/`) | Discards all unstaged working-tree edits across the directory or repo. |
| **`deny`** *(hard block)* | **`git restore .`**, `git restore --worktree .`, `git restore --staged --worktree .`, `git restore --source=<ref> .` (and `./`, `-W`, `-SW`, `:/`) | Discards all unstaged working-tree edits across the directory or repo. |
| **`force_ask`** *(always prompt)* | **Standard non-force `git push`** | Always requires explicit user confirmation, bypassing cached "Always Allow" approvals. |
| **`allow`** | Local `git commit`, `git add`, `git status`, `git diff`, `git log`, `git branch -d`, `git checkout -b ...`, `git checkout <branch>`, `git restore <specific-file>`, `git restore --staged .` (unstages without touching working tree), non-git commands, and malformed stdin payloads (fail-open) | Preserves smooth local development and prevents hook parser errors from bricking the session. |

### Shell & Flag Awareness

[`hooks/guard_git.py`](./hooks/guard_git.py) uses a zero-dependency POSIX/bash lexer and git argument parser rather than naive regex matching:

- **Global git options & submodules:** Handles options before the subcommand (`git -C repo ...`, `git --git-dir=... ...`, `git --work-tree=... ...`, `git -c key=val ...`, `git --no-pager ...`, inline `-c alias.<name>=...`) and inspects `git submodule foreach` commands.
- **Compound commands, pipes & wrappers:** Inspects every command in `&&`, `||`, `;`, `|`, `&`, newlines, subshells, command/process substitutions (`$(...)`, `` `...` ``, `<(...)`), nested shells (`sh -c`, `bash -c`, `eval`, heredocs/here-strings into shells like `bash <<'EOF'`, and `echo`/`printf`/`cat <<'EOF'` piped into a shell), and wrappers (`env`, `sudo`, `command`, `exec`, `timeout`, `xargs`). When multiple commands appear together, the strictest decision wins (`deny` > `force_ask` > `allow`), and excessive nesting containing `git` fails safe to `force_ask` rather than `allow`.
- **False-positive protection:** Respects single quotes, double quotes, backslash escapes, comments, and quoted heredocs so commands like `git commit -m "prevent git reset --hard"` or `echo "git push --force"` are allowed without interference.

## Prerequisites

- **Python 3.10+** available as `python3` on your `PATH`.
- Zero third-party Python packages required (standard library only).

## Plugin Structure & Hook Contract

```text
plugins/git-guardrails/
├── plugin.json         # Native Antigravity plugin manifest
├── hooks.json          # Plugin-root PreToolUse config (matcher: "run_command", timeout: 5s)
├── hooks/
│   └── guard_git.py    # Executable stdlib-only Python 3 hook script
└── README.md           # You are here
```

Antigravity passes the `PreToolUse` event payload on `stdin` (`toolCall.args.CommandLine`) and reads a JSON decision object from `stdout`:

```json
{
  "decision": "deny",
  "reason": "Blocked by git-guardrails: 'git reset --hard' permanently discards uncommitted working-tree and index changes..."
}
```

## Quick Smoke Test

From `plugins/git-guardrails/`, pipe sample `PreToolUse` payloads directly into [`hooks/guard_git.py`](./hooks/guard_git.py):

```bash
echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"git push --force origin main"}}}' \
  | python3 ./hooks/guard_git.py
# -> {"decision": "deny", "reason": "..."}

echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"git push origin main"}}}' \
  | python3 ./hooks/guard_git.py
# -> {"decision": "force_ask", "reason": "..."}

echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"git commit -m \"never run git reset --hard\""}}}' \
  | python3 ./hooks/guard_git.py
# -> {"decision": "allow"}
```

To run the full unit test suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## Customization

- **Temporarily disable the hook:** Set `"enabled": false` under `"git-guardrails"` in [`hooks.json`](./hooks.json), or toggle the plugin off in Antigravity's Customizations UI.
- **Adjust blocked or gated rules:** Edit the per-subcommand rule functions in [`hooks/guard_git.py`](./hooks/guard_git.py) (`_check_git_push`, `_check_git_reset`, `_check_git_clean`, `_check_git_branch`, `_check_git_checkout`, `_check_git_restore`) and the `_GIT_SUBCOMMAND_RULES` dispatch table.
  - To hard-block *all* `git push` invocations (matching upstream's stricter posture), change `_SEV_FORCE_ASK` / `"force_ask"` at the bottom of `_check_git_push` to `_SEV_DENY` / `"deny"`.
  - To add a new rule (for example, blocking `git commit` or `git stash drop`), add a `_check_git_<subcommand>` function and register it in `_GIT_SUBCOMMAND_RULES`.

## Origin & Attribution

- **Classification:** `Combined (Original + mattpocock/skills)`
- **Upstream Credit:** Destructive git command blocklist inspired by **Matt Pocock** ([`mattpocock/skills`](https://github.com/mattpocock/skills), `skills/misc/git-guardrails-claude-code`, MIT License, Copyright (c) 2026 Matt Pocock).
- **What Changed for Antigravity & Workflow Policy:**
  - **Native Antigravity architecture (Original):** Replaced Claude Code's setup-skill + `.claude/settings.json` + `jq`/regex bash script (`exit 2` + `stderr`) with a self-contained Antigravity plugin using plugin-root [`hooks.json`](./hooks.json) (`PreToolUse`, `run_command` matcher) and a stdlib-only Python 3 shell/git parser reading `toolCall.args.CommandLine` and emitting Antigravity JSON decisions (`allow`, `force_ask`, `deny`).
  - **Expanded parser accuracy & behavioral policy:** Preserved Matt's core destructive-git blocklist while adding support for git global flags, reordered/combined flags, `+` force-push refspecs, `git branch --delete --force`, worktree-mutating `git restore`, compound shell chains, and command substitutions—without false-blocking quoted commit messages or `echo` strings. Intentionally allows local `git commit` for fluid agentic workflows and gates standard non-force `git push` with Antigravity's `force_ask` confirmation instead of an unconditional hard block.
