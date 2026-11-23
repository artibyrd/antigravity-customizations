# Repo Bootstrap Starter Templates

Use these starter templates during Phase 4 of [repo-bootstrap](../SKILL.md). Tailor placeholders (`<repo-name>`, detected lint/test commands) to the active workspace, and scaffold **only** the missing files the user explicitly selected.

---

## 1. Lean `AGENTS.md` Starter (`<800` Tokens)

Target ~250–400 tokens on initial creation so the hard `<800`-token ceiling leaves ample room for real project invariants.

```markdown
# AGENTS.md — <repo-name>

> Tier 0 always-on invariants (hard ceiling: <800 tokens). Keep each rule to one sentence.
> Demote mechanical checks to tests/linters and subsystem runbooks to skills.

## Class α (P0 — Safety, Custody & Authority)
- Never commit secrets, tokens, or credentials; redact sensitive output as `<REDACTED>`.
- Never run destructive git or infrastructure commands (`git push --force`, `git reset --hard`, production deploys) without explicit human approval.
- Never silently fabricate mock data or fallback values in production code paths.

## Class β (P1 — Execution & Delivery)
- Run the fast local verification suite (`just check` or the project's test/lint command) before reporting work complete.
- Keep diffs focused on the agreed scope; ask before widening architectural boundaries or adding new dependencies.
- Keep mutating workflows behind explicit confirmation gates rather than mixing them into read-only inspection commands.

## Class γ (P2 — Symmetry & Navigation)
- Read `GLOSSARY.md` (if present) for domain vocabulary and `docs/adr/` (if present) before re-litigating settled architecture decisions.
- Review-only style judgement calls belong in `CODING_STANDARDS.md` (if present), not here.
- Record *why* a hard-to-reverse decision was made in an immutable ADR under `docs/adr/`; keep *what* must hold true now in tests, skills, or this file.
```

---

## 2. Modular `Justfile` Safe/Gated Skeleton

Creates three small files: a lean root `Justfile` orchestrator, `just/safe.just` for read-only inspection/QA, and `just/gated.just` for `[confirm(...)]`-protected mutating actions.

### `Justfile`

```just
# <repo-name> task runner — lean root orchestrator.
# Safe read-only recipes live in just/safe.just; mutating recipes live in just/gated.just.

set shell := ["bash", "-euo", "pipefail", "-c"]

import 'just/safe.just'
import 'just/gated.just'

# Show available recipes grouped by safety level
[group('meta: safe')]
default:
    @just --list
```

### `just/safe.just`

Tailor `lint` and `test` to the stack detected in Phase 1 (e.g., `ruff check .`, `pytest`, `npm test`, `cargo test`, `go test ./...`).

```just
# Read-only inspection and verification recipes (safe for humans and agents).

# Compact working-tree status
[group('vcs: safe')]
status:
    git status -s

# Short diff summary against HEAD
[group('vcs: safe')]
diff:
    git diff --stat

# Run static checks / linters (replace placeholder with detected linter)
[group('qa: safe')]
lint:
    @echo "TODO: wire project linter in just/safe.just (e.g. ruff check ., eslint ., cargo check)"

# Run automated test suite (replace placeholder with detected test runner)
[group('qa: safe')]
test:
    @echo "TODO: wire project test command in just/safe.just (e.g. pytest, npm test, go test ./...)"

# Run fast governance tests (when tests/governance/ is enabled)
[group('qa: safe')]
check-governance:
    @if [ -d tests/governance ]; then python3 -m unittest discover -s tests/governance -v; else echo "No tests/governance/ directory found; skipping."; fi

# Full read-only local verification gate
[group('qa: safe')]
check: lint test check-governance
```

### `just/gated.just`

Never put destructive commands in `safe.just`. Always protect mutating recipes with `[confirm(...)]`.

```just
# Mutating or irreversible workflows — always protected by [confirm(...)].
# Non-interactive CI/agent invocations require explicit authorization (`just --yes <recipe>`).

# Stage and commit current changes after explicit confirmation
[group('vcs: gated')]
[confirm('Commit staged changes on the current branch? [y/N]')]
commit message:
    git commit -m "{{message}}"

# Push current branch to origin (non-force) after explicit confirmation
[group('vcs: gated')]
[confirm('Push current branch to origin? [y/N]')]
push:
    git push
```

---

## 3. Optional Review-Only `CODING_STANDARDS.md`

Only scaffold when the user opts in (recommended for multi-module or team repositories; omit in tiny repos).

```markdown
# Coding Standards (Review-Only)

> **Audience:** Code reviewers and review subagents ONLY. Implementers do not load this file on every turn.
> **Rule of Thumb:** Never list anything here that a linter, formatter, or typechecker already enforces. Put only repo-wide judgement calls here.

## Module & Interface Design
- Prefer deep modules with small, clear interfaces over shallow pass-through wrappers.
- Keep public contracts explicit and well-typed; isolate external I/O behind thin adapters only when a real seam exists.

## Error Handling & Observability
- Fail closed with actionable error context; never swallow exceptions silently or return synthetic fallback data in production paths.
- Redact credentials, tokens, and PII (`<REDACTED>`) in logs, errors, and diagnostic output.

## Testing Discipline
- Test behavior through public seams rather than internal implementation details.
- Prefer deterministic, hermetic local tests over brittle live-network dependencies.
```

---

## 4. Lazy `GLOSSARY.md` & `docs/adr/README.md`

### `GLOSSARY.md`

```markdown
# Domain Glossary

> Keep entries concise and strictly about **domain meaning**—zero implementation details, file paths, or library names. Add terms lazily as ambiguity arises.

| Term | Definition |
| :--- | :--- |
| *(Add domain terms as they emerge)* | *Clear one-sentence business definition.* |
```

### `docs/adr/README.md`

````markdown
# Architecture Decision Records (ADRs)

Historical, immutable point-in-time records explaining **why** a significant decision was made.

## When to Write an ADR (All 3 Criteria Required)

Create `docs/adr/NNNN-short-kebab-title.md` only when a decision is:
1. **Hard to reverse** once built or deployed,
2. **Surprising without context** to a future contributor or agent, and
3. **The result of a real trade-off** where credible alternatives were weighed.

> **ADRs vs. Living Invariants:** ADRs are immutable history (*why* we chose X at time *t*); supersede them with a newer ADR rather than rewriting history. Enforceable current rules (*what* must hold true today) live in tests, linters, skills, or `AGENTS.md`.

## Template (`NNNN-short-title.md`)

```markdown
# ADR-NNNN: <Short Decision Title>

- **Status:** Accepted | Superseded by ADR-XXXX
- **Date:** YYYY-MM-DD

## Context
What problem, constraint, or force made this decision necessary?

## Decision
What did we choose?

## Alternatives Considered
What credible options were rejected and why?

## Consequences
What trade-offs, risks, or follow-on constraints does this decision create?
```
````

---

## 5. `tests/governance/test_repo_invariants.py`

A fast (`<0.3s`), stdlib-only Python `unittest` placeholder demonstrating Tier 2 automated governance checks.

```python
"""Fast (<0.3s) repository governance checks (stdlib Python only).

Add deterministic structural invariants here instead of spending prompt tokens
in AGENTS.md.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = REPO_ROOT / "AGENTS.md"
AGENTS_TOKEN_CEILING = 800

# Guard against accidentally committing machine-local home directory paths.
LOCAL_PATH_PATTERNS = (
    re.compile(r"/" + r"home/[A-Za-z0-9._-]+/"),
    re.compile(r"/" + r"Users/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\" + r"Users\\[A-Za-z0-9._-]+\\"),
)
SCAN_EXTENSIONS = {".md", ".py", ".sh", ".json", ".toml", ".yaml", ".yml", ".just"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build", "target"}


class RepoGovernanceTests(unittest.TestCase):
    def test_agents_md_stays_under_token_ceiling(self) -> None:
        if not AGENTS_MD.is_file():
            self.skipTest("AGENTS.md not present (optional)")
        words = len(AGENTS_MD.read_text(encoding="utf-8").split())
        estimated_tokens = int(words * 1.33)
        self.assertLessEqual(
            estimated_tokens,
            AGENTS_TOKEN_CEILING,
            f"AGENTS.md is ~{estimated_tokens} tokens ({words} words), exceeding the "
            f"{AGENTS_TOKEN_CEILING}-token ceiling. Demote rules to tests, skills, or docs/.",
        )

    def test_no_machine_local_path_leaks(self) -> None:
        leaks: list[str] = []
        for path in REPO_ROOT.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if not path.is_file() or path.suffix.lower() not in SCAN_EXTENSIONS:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pat in LOCAL_PATH_PATTERNS:
                match = pat.search(text)
                if match:
                    leaks.append(f"{path.relative_to(REPO_ROOT)}: {match.group(0)}")
        self.assertEqual(leaks, [], f"Found machine-local path leaks: {leaks}")


if __name__ == "__main__":
    unittest.main()
```
