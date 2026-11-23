---
name: bootstrap-approvals
description: >-
  Repo-agnostic Antigravity IDE command approval priming for fresh workspaces
  or reset permissions. Dynamically discovers safe read-only commands from
  Justfile, Makefile, pyproject.toml, package.json, Cargo.toml, go.mod, and
  read-only git/gh shapes, enforces the Subprocess Isolation Rule and "No Spicy
  Prefixes" Command Boundary Law, confirms the list with the user, and runs
  discrete top-level run_command calls for one-pass "Always Allow" priming.
---

# Bootstrap Approvals

Primes Antigravity IDE command approvals in a fresh workspace or after permissions reset—without hardcoding repo-specific commands or ever priming destructive or overly broad prefixes.

> **Project overlay (optional):** If `.agents/overrides/bootstrap-approvals.md` exists in the workspace or repository root, read it first and apply its `Overrides`, `Extensions`, and `Disabled / Not Applicable` deltas on top of this skill.

---

## 1. The Subprocess Isolation Rule

Antigravity's permission system intercepts **top-level `run_command` tool calls** and generalizes "Always Allow" by **`binary subcommand` prefix** (typically the first two tokens).

```text
[Agent: run_command(CommandLine="git status -s")]
                      │
                      ▼
        [IDE Prefix Matching Engine]
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 [Prefix Cached]             [Unapproved Prefix]
        │                           │
        ▼                           ▼
(Executes Silently)       [IDE Approval Modal]
                                    │
                                    ▼
                        User clicks "Always Allow"
                                    │
                                    ▼
                 (Prefix Cached for Future Tool Calls)
```

- **Never use a wrapper script:** Running `subprocess.run(["just", "check"])` or a bash loop inside a script will **not** register `just check` in the IDE's approval table—child processes run inside the subshell and are invisible to the top-level dispatcher.
- **Keep each call prefix-matchable:** Execute every command shape as its own **discrete top-level `run_command` tool call**. Avoid shell chaining (`&&`, `;`, `||`), command substitutions (`$(...)`, backticks), variable expansions (`$VAR`), brace expansions (`{a,b}`), and wrapper binaries (`env`, `timeout`, `xargs`, `eval`), all of which disable prefix generalization and force exact-string matching.
- **Execution mode alignment:** Standard sandboxed commands normally auto-run without prompting. When priming approvals for commands that require host, auth, or network access outside the sandbox (or when the user explicitly asks to prime unsandboxed approvals), execute each confirmed top-level command in the mode the user wants primed—never silently elevate unconfirmed commands.

---

## 2. The "No Spicy Prefixes" Command Boundary Law

Because "Always Allow" generalizes across arguments sharing a `binary subcommand` prefix, approving a prefix whose sibling invocations can mutate or destroy state creates an unintended security bypass.

**Audit every candidate's 2-token `binary subcommand` prefix before proposing it. Never prime any prohibited prefix—even with a read-only flag attached:**

| Category | Prohibited ("Spicy" / Broad) Prefixes | Why It Is Banned |
| :--- | :--- | :--- |
| **Cloud & Edge CLIs** | `gcloud config`, `wrangler secret`, `aws iam`, `az account` | `gcloud config list` shares prefix with `gcloud config set`; `wrangler secret list` shares prefix with `wrangler secret put`/`delete`. |
| **Filesystem** | `rm`, `rmdir`, `mv`, `chmod`, `chown` | Destructive or state-mutating file operations. |
| **Git Mutations & Mixed Subcommands** | `git push`, `git reset`, `git clean`, `git checkout`, `git restore`, `git branch`, `git rebase`, `git merge`, `git tag` | Rewrites history, overwrites working trees, or mutates remotes. Note: `git branch --list` is banned because its `git branch` prefix matches `git branch -D`; use `git show-ref --heads` or `git rev-parse --abbrev-ref HEAD` instead. |
| **Infrastructure & Containers** | `terraform`, `kubectl apply`, `kubectl delete`, `kubectl patch`, `kubectl edit`, `docker system`, `docker rm`, `docker rmi` | Mutates or destroys cloud infrastructure, clusters, or local containers/volumes. |
| **Mutating HTTP & Subcommand-less Binaries** | `curl -X POST` / `-X PUT` / `-X PATCH` / `-X DELETE` / `-d` (and bare `curl`), `pytest`, `mypy` | Binaries with no subcommand generalize across all arguments (for example, `curl` accepts `-X POST`; `pytest --basetemp=<dir>` deletes that directory's contents; `mypy` accepts arbitrary cache/config paths). Wrap them in read-only `Justfile`/`Makefile` recipes when available; otherwise flag the trade-off explicitly in the confirmation table instead of presenting them as plain safe. |
| **Linters & Package CLIs with Mutating Flags** | `ruff check`, `cargo clippy`, `poetry version` | `ruff check --fix` / `--unsafe-fixes` and `cargo clippy --fix` rewrite source files; `poetry version patch` / `poetry version 2.0.0` rewrites `pyproject.toml`. Encapsulate read-only lint/check invocations in `just lint` / `make lint` recipes instead. |
| **Multi-Level CLI Namespaces** | `gh pr`, `gh auth`, `gh run`, `gh repo` | `gh pr view` shares a 2-token prefix with `gh pr merge`/`close`; `gh auth status` shares prefix with `gh auth logout`/`token`. Encapsulate read-only `gh` checks in `Justfile`/`Makefile` recipes (e.g., `just pr-view`, `just auth-check`). |
| **Generic Script Runners & Shells** | `npm run`, `pnpm run`, `yarn run`, `poetry run`, `uv run`, `npx`, `python3 -m`, `bash -c`, `sh -c`, `python3 -c`, `eval`, `sudo` | 2-token runner prefixes can execute arbitrary scripts or mutating targets (`npm run deploy`, `poetry run ...`). Prefer strictly read-only built-ins (`npm test` when `"test"` is read-only) or explicit safe `just`/`make` recipes. |
| **Mutating Task Recipes** | `just release`, `just deploy`, `just commit`, `just pr-merge`, `npm publish`, `cargo publish` | Triggers deployments, releases, merges, or package publishes. |

**Safe Encapsulation Pattern:** Whenever a needed read-only check belongs to a spicy, subcommand-less, or multi-level CLI (`gcloud`, `terraform`, `gh`, `curl`, `ruff check`, `cargo clippy`, `pytest`, `mypy`, `poetry run`), wrap the exact read-only command inside a dedicated `Justfile` or `Makefile` recipe (e.g., `just lint`, `just test`, `just auth-check`, `just pr-view`, `just tf-validate`). Because the recipe name is the second token, priming `just lint` or `just pr-view` never authorizes `--fix` or `just pr-merge`.

---

## 3. Dynamic Workspace Discovery (Zero Hardcoding)

Inspect the current workspace using read-only file reads (`read_file` / directory inspection) to discover what tooling actually exists. Propose **only** safe commands genuinely present in this repository:

1. **`Justfile` (and imported `just/*.just` files):**
   - Inspect recipe annotations and bodies. Prefer recipes explicitly marked safe (e.g., `[group('...: safe')]`, `[group('qa')]`, `[group('check')]`) and strictly read-only verification/inspection recipes (`check`, `lint`, `test`, `typecheck`, `status`, `diff`, `pr-view`, `pr-checks`, `auth-check`, `validate`, `doctor`).
   - Exclude any recipe whose body mutates state, writes commits/releases, deploys, cleans files, or runs destructive commands.
2. **`Makefile`:**
   - Inspect read-only QA/inspection targets (`check`, `test`, `lint`, `typecheck`, `validate`, `status`); exclude `clean`, `deploy`, `release`, `install`, `publish`, and mutating formatters (unless the user explicitly opts in).
3. **`pyproject.toml`:**
   - Prefer read-only `Justfile`/`Makefile` wrappers (`just test`, `just lint`, `just typecheck`) when they exist, plus `poetry check` (if Poetry is configured—never `poetry version`, which rewrites `pyproject.toml`).
   - Exclude `ruff check` (`--fix` / `--unsafe-fixes` rewrites source) and generic runners (`poetry run`, `uv run`, `python3 -m`).
   - For subcommand-less binaries (`pytest`, `mypy`) when no `Justfile`/`Makefile` wrapper exists, do **not** list them as plain safe—flag the broad single-token prefix trade-off (e.g., `pytest --basetemp=<dir>` deletes directory contents) explicitly in the confirmation table so the user decides whether to approve or wrap them.
4. **`package.json`:**
   - Detect the package manager (`pnpm`, `npm`, `yarn`, `bun`) and propose safe built-in read-only commands (`npm test`, `pnpm test`, `yarn test`, `bun test`) only if a read-only `"test"` script is defined. Avoid priming generic `npm run` / `pnpm run` prefixes; suggest encapsulating custom read-only scripts in `Justfile`/`Makefile` instead.
5. **`Cargo.toml`:**
   - Propose read-only Rust checks (`cargo check`, `cargo test`); exclude `cargo clippy` (`--fix` rewrites source—wrap in `just lint`/`make lint` instead), `cargo publish`, and `cargo clean`.
6. **`go.mod`:**
   - Propose read-only Go checks (`go test ./...`, `go vet ./...`).
7. **Standard Read-Only `git` & `gh` Inspection Shapes:**
   - **Git (when `.git` exists):** Read-only 2-token subcommands only:
     - `git status -s`
     - `git diff --stat` *(note in Safety Rationale: `git diff --output=<file>` can overwrite a file)*
     - `git log -n 5 --oneline` *(note in Safety Rationale: `git log --output=<file>` can overwrite a file)*
     - `git rev-parse --abbrev-ref HEAD`
     - `git show-ref --heads`
   - **GitHub CLI (`gh`):** Prefer repo-defined read-only `Justfile`/`Makefile` wrappers (e.g., `just pr-view`, `just pr-checks`, `just auth-check`). If the repo has a GitHub remote and no wrapper recipes exist, do **not** auto-include `gh pr` / `gh auth` / `gh run` in the default safe list—explicitly flag the 2-token prefix trade-off (`gh pr` also covers `gh pr merge`) and let the user decide whether to skip them or add a safe `Justfile` wrapper.

---

## 4. Mandatory Confirmation Gate (Before Running Anything)

**Never start firing priming commands silently.** Present the discovered plan to the user first:

1. Show a compact table grouped by category:
   - **Command** (exact literal string to run)
   - **Source** (`Justfile`, `pyproject.toml`, `git`, etc.)
   - **Prefix Primed** (the 2-token `binary subcommand` prefix—or single-token binary if subcommand-less—that "Always Allow" will generalize)
   - **Safety Rationale & Caveats** (why sibling arguments cannot mutate state, plus explicit caveats for any edge case such as `git diff --output=<file>`, `git log --output=<file>`, or opt-in subcommand-less binaries like `pytest`/`mypy`)
2. List any **excluded / spicy** recipes, mutating-flag CLIs (`ruff check`, `cargo clippy`, `poetry version`), or broad prefixes (`git branch`, `gh pr`, `npm run`, `terraform`, etc.) discovered in the workspace with the reason each was omitted.
3. Wait for the user to confirm, trim, or add specific read-only commands before starting the priming sequence.

---

## 5. Sequential Execution & Error Resilience

Once the user confirms the list:

1. **One command per tool call:** Execute each confirmed command sequentially as a standalone, top-level `run_command` call (`WaitMsBeforeAsync: 5000`) so the user can click **"Always Allow"** cleanly on each modal prompt in a single pass.
2. **Tolerate non-zero exits:** Read-only inspection commands frequently exit non-zero for benign reasons (for example, a read-only `just pr-view` on a branch with no open PR, an auth check when signed out, or a failing test suite). Log the exit code without trying to debug or fix it mid-pass, and proceed to the next command.
3. **Report completion summary:** Finish with a concise table showing every command executed, its exit code (`0` vs. non-zero), and any skipped items.
