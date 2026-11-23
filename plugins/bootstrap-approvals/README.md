# Bootstrap Approvals

A 100% repository-agnostic Antigravity plugin for priming IDE **"Always Allow"** command approvals in a fresh workspace or after permissions reset—fast, transparent, and strictly bounded to safe 2-token read-only command prefixes.

## Why Use It?

- **Respects the Subprocess Isolation Rule:** Wrapper scripts (`subprocess.run`, bash loops) do not register commands in Antigravity's top-level prefix approval cache. This skill runs each approved command shape as a discrete, top-level `run_command` call without chaining (`&&`, `;`), `$(...)`, or wrapper binaries so prefix generalization works cleanly.
- **Enforces the "No Spicy Prefixes" Command Boundary Law:** Audits every candidate's prefix and bans anything whose sibling arguments can mutate or destroy state—explicitly prohibiting `gcloud config`, `rm`, `git push`, `git reset`, `git clean`, `git checkout`, `git restore`, `git branch` (since `git branch --list` shares a prefix with `git branch -D`), `wrangler secret`, `terraform`, `kubectl apply`/`delete`, `docker system`, `curl -X POST`, mutating-flag linters/CLIs (`ruff check`, `cargo clippy`, `poetry version`), generic runners (`npm run`, `poetry run`, `python3 -m`), multi-level CLI namespaces (`gh pr`, `gh auth`), and unencapsulated subcommand-less binaries (`pytest`, `mypy`, `curl`) unless explicitly wrapped in a read-only `Justfile`/`Makefile` recipe or flagged with their trade-offs.
- **Zero Hardcoding (Dynamic Discovery):** Scans the active workspace's `Justfile` (`[group('...: safe')]` / read-only recipes), `Makefile`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, and strictly read-only `git` / wrapped `gh` inspection shapes.
- **Human-in-the-Loop Confirmation Gate:** Always presents the proposed command table (with each 2-token prefix and any excluded spicy commands) for your sign-off before executing a single priming call, and tolerates benign non-zero exits on inspection commands.

## Included Files

- [`skills/bootstrap-approvals/SKILL.md`](./skills/bootstrap-approvals/SKILL.md) — Subprocess Isolation Rule, "No Spicy Prefixes" Command Boundary Law, dynamic workspace discovery protocol, confirmation gate, and resilient sequential priming flow.

## Example Prompts

- *"Bootstrap safe read-only command approvals for this workspace."*
- *"Discover safe `Justfile`, test, and `git` inspection commands in this repo and prime Always Allow."*
- *"Audit which prefixes in this repo are safe to prime without introducing spicy commands."*

## Origin & Attribution

- **Provenance:** `Original`
- **Author:** Authored natively for Google Antigravity by Arthur Davis (`https://github.com/artibyrd`), generalized from multi-repository Antigravity IDE permission-priming workflows into a standalone, repo-agnostic plugin.
