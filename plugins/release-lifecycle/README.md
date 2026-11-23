# Release Lifecycle

An Antigravity plugin that codifies a disciplined **4-phase delivery and continuous learning release cadence**—from local QA and human **Mk1 Eyeball Sign-Off** through feature release, `/learn` retrospective, and lean learning patch release—while adapting cleanly to any repository's real tooling via **Self-Contained Graceful Preflight**.

## Why Use It?

- **Self-Contained Graceful Preflight:** Probes `git` remotes, `gh auth status`, `.github/workflows/`, `Justfile`/`Makefile`, `CHANGELOG.md`, `ROADMAP.md`, and version manifests first—never assumes GitHub Actions, `gh` CLI, or cloud staging exists, and degrades smoothly to a local-only release cadence when they are absent.
- **4-Phase Delivery & Continuous Learning Cadence:** Separates feature delivery (`vX.Y.0`) from post-release process/governance hardening (`vX.Y.1`) via a structured **Local QA → PR/Dev Probe → Mk1 Eyeball Sign-Off → Feature Release → `/learn` Retrospective → Lean Patch Release** loop.
- **`CHANGELOG.md` vs. `ROADMAP.md` Symmetry:** Keeps historical shipped reality (`CHANGELOG.md`) and the living forward backlog (`ROADMAP.md`) strictly synchronized at every release boundary.
- **Topological Multi-Repo PR Merge Order:** Prevents stale clones and broken deploy pipelines by ordering merges strictly from upstream content/contract/library repos to downstream deploy pipelines and portals.

## Included Files

- [`skills/release-lifecycle/SKILL.md`](./skills/release-lifecycle/SKILL.md) — Graceful preflight matrix, 4-phase delivery & `/learn` cadence, Mk1 Eyeball gate, `CHANGELOG.md` vs. `ROADMAP.md` symmetry rules, and Topological Multi-Repo PR Merge Order.

## Example Prompts

- *"Run `release-lifecycle` preflight on this repository and assemble the Mk1 Eyeball sign-off package for `v1.4.0`."*
- *"Verify version parity and `CHANGELOG.md` vs. `ROADMAP.md` symmetry before we tag the release."*
- *"Order our open PRs across these coupled repositories using Topological Multi-Repo PR Merge Order."*

## Origin & Attribution

- **Provenance:** `Original`
- **Author:** Authored natively for Google Antigravity by Arthur Davis (`https://github.com/artibyrd`), generalized from multi-repository continuous-learning release workflows into a standalone, zero-assumption plugin.
