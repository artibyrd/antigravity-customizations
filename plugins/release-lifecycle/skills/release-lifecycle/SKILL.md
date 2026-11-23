---
name: release-lifecycle
description: >-
  Guides the 4-phase delivery and continuous learning lifecycle (Local QA,
  Branch/PR & Dev Probe, Mk1 Eyeball Sign-Off, Feature Release, /learn
  Retrospective, Lean Patch Release) with Self-Contained Graceful Preflight
  that cleanly degrades when gh or CI/CD is absent, CHANGELOG.md vs. ROADMAP.md
  symmetry, and Topological Multi-Repo PR Merge Order. Use when preparing a
  release, verifying release readiness, coordinating multi-repo PR merges, or
  running a post-release /learn patch cycle.
---

# Release Lifecycle

Delivers features cleanly and turns every release boundary into a structured improvement loop—without assuming any specific CI platform, issue tracker, or cloud host.

> **Project overlay (optional):** If `.agents/overrides/release-lifecycle.md` exists in the workspace or repository root, read it first and apply its `Overrides`, `Extensions`, and `Disabled / Not Applicable` deltas on top of this skill.

---

## 1. Self-Contained Graceful Preflight (Always Run First)

Never assume GitHub Actions, `gh` CLI, `Justfile`, `CHANGELOG.md`, `ROADMAP.md`, or cloud staging environments exist. Probe the active workspace first:

1. **Git topology:** Check `git remote -v`, `git rev-parse --abbrev-ref HEAD`, and `git status -sb`.
2. **GitHub CLI availability:** If `gh` is on `PATH`, check `gh auth status` (do not fail if `gh` is missing or unauthenticated).
3. **CI/CD pipelines:** Check whether `.github/workflows/` (or other CI configs such as `.gitlab-ci.yml`, `cloudbuild.yaml`) exists.
4. **Local QA runner:** Inspect `Justfile`, `Makefile`, `pyproject.toml`, `package.json`, `Cargo.toml`, or `go.mod` to discover the repo's real check/test command (e.g., `just check`, `pytest`, `npm test`, `cargo test`).
5. **Release files & version manifests:** Detect `CHANGELOG.md`, `ROADMAP.md`, and version sources (`pyproject.toml`, `package.json`, `plugin.json`, `Cargo.toml`, `VERSION`, etc.).

### Graceful Degradation Matrix

| Detected Environment | Release Cadence Mode | What Runs |
| :--- | :--- | :--- |
| **`git` remote + authenticated `gh` + CI/CD workflows** | **Full Cloud / PR Cadence** | Local QA → branch/PR + CI checks + dev/staging probe (if configured) → Mk1 Eyeball Sign-Off → merge/tag/push → live verification → `/learn` → patch release. |
| **`git` remote only** *(no `gh` or no CI workflows)* | **Git Remote Cadence** | Local QA → local verification → Mk1 Eyeball Sign-Off → version/changelog sync → commit & annotated `git tag` → push branch/tag (with explicit user confirmation) → `/learn` → patch release. |
| **Local-only repo** *(no `git` remote or offline)* | **Local-Only Cadence** | Local QA → local diff & Mk1 Eyeball Sign-Off → version/changelog sync → clean local commit & local annotated tag (`git tag -a vX.Y.Z`) → `/learn` → local patch commit/tag. |

State the detected mode explicitly at the top of your release checklist. Never block or error out over missing `gh` or absent `.github/workflows/`.

---

## 2. The 4-Phase Delivery & Continuous Learning Lifecycle

### Phase 1: Local QA → Branch/PR & Dev Probe → Mk1 Eyeball Sign-Off
1. **Local QA Gate:** Run the discovered local test, lint, and validation commands. All checks must pass with zero unexplained warnings.
2. **Branch, PR & Dev Probe *(when remote/CI is configured)*:**
   - Push the feature branch (only with user confirmation) and open/update the PR.
   - Verify CI checks are green. If the repo has a dev/staging deployment or live health probe, execute it and record the exact output.
3. **Mk1 Eyeball Sign-Off *(Hard Human Gate)*:**
   Present a crisp sign-off package to the user:
   - Exact target version (`vX.Y.Z`) and version manifests to bump.
   - Summary of working-tree or branch diff (`git diff --stat` + key behavior changes).
   - Passing QA / probe output.
   - Merge or release risk (blast radius and rollback path).
   - **Stop and wait for explicit human sign-off** before merging, tagging, pushing, or triggering a release.

### Phase 2: Feature Version Release
1. **Clean Working Tree & Parity:** Confirm all intended edits are staged/committed cleanly (`git diff --quiet` after commit) and every detected version manifest agrees on the target version.
2. **Sync `CHANGELOG.md` and `ROADMAP.md`** (Section 3).
3. **Commit & Tag:** Create a clean release commit and annotated tag (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`).
4. **Publish & Verify *(only when remote/CI exists and user approved)*:** Push branch and tag, monitor any release workflow, and confirm live deployment health if applicable.

### Phase 3: `/learn` Retrospective
Immediately after the feature version ships, capture institutional memory while context is fresh:
1. Trigger or prepare for Antigravity's native `/learn` workflow (or write a concise `learning_proposal.md` artifact).
2. Review session corrections, recurring failure modes, missing checks, and workflow friction.
3. Prefer graduating mechanical discoveries into **fast automated tests or linters** rather than bloating prompt steering files (`AGENTS.md`).

### Phase 4: Lean Patch Release (`vX.Y.Z+1`)
Ship the codified improvements as a small, focused patch release—never mixing new product features into the learning patch:
1. Apply approved rule refinements, skill updates, and new shift-left tests.
2. Re-run the local QA suite and confirm a clean working tree.
3. Bump to the next patch version (`vX.Y.Z+1`), add a concise `CHANGELOG.md` entry, commit, tag, and ship (subject to the detected mode and user confirmation).

---

## 3. `CHANGELOG.md` vs. `ROADMAP.md` Symmetry

Keep past facts and future plans strictly separated and synchronized:

| File | Document Class | Role |
| :--- | :--- | :--- |
| **`CHANGELOG.md`** | 🏛️ **Historical Ledger** | Records **what actually shipped** in each tagged version (`Added`, `Changed`, `Fixed`, `Removed`) with release dates. Past version sections are immutable once tagged. |
| **`ROADMAP.md`** | 🟢 **Living Forward Horizon** | Tracks **planned, active, and upcoming** milestones or waves. |

### Release Boundary Symmetry Rules
- **Move, don't duplicate:** Every milestone or feature added to `CHANGELOG.md` for `vX.Y.Z` MUST simultaneously be marked completed or graduated out of `ROADMAP.md`'s upcoming backlog.
- **Zero speculative changelog entries:** Never record planned or unmerged work as shipped in `CHANGELOG.md`.
- **Graceful absence:** If the repository has only one of these files—or neither—update only what exists and do not fabricate new top-level files unless the user asks.

---

## 4. Topological Multi-Repo PR Merge Order

When a release spans multiple coupled repositories (for example: a shared schema/contract library, a standalone content/docs repository, and a downstream application or deployment pipeline that clones, pins, or builds against them):

1. **Map the Dependency DAG First:** Before merging any PR, list every repository involved and draw its directed dependency edges (`Upstream → Downstream`).
2. **Merge Strictly in Topological Order:**
   1. **Layer 1 — Upstream Contracts, Schemas & Shared Libraries:** Merge first, tag/publish if required, and verify CI passes on the default branch.
   2. **Layer 2 — Upstream Content, Taxonomies & Source Docs:** Merge next so downstream build/deploy jobs pull the updated content rather than stale refs.
   3. **Layer 3 — Downstream Applications, Portals & Deploy Pipelines:** Merge and trigger last—only after all upstream repos they clone, submodule-pin, or import have settled on their default branches/tags.
3. **Post-Merge Cross-Repo Parity Check:** Verify version pins, submodule/lockfile SHAs, and live deployed output across all coupled repos before closing the release.

> **Why this is non-negotiable:** Merging a downstream deploy pipeline PR before its upstream content or contract PR lands triggers a deploy against stale upstream commits—causing broken builds, mismatched schemas, or silent documentation drift in production.
