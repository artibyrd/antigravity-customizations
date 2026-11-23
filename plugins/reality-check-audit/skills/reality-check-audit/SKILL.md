---
name: reality-check-audit
description: >-
  Conducts a structured, evidence-backed cross-model "Outsider's Honest
  Assessment" across a whole repository, milestone, dashboard, or documentation
  suite—structured as What's Genuinely Good, What's Concerning, What's
  Aspirational vs. Real, and Concrete Remediation Plans. Actively hunts mocked
  or hardcoded telemetry, doc-vs-code drift, and governance bloat. Use at
  milestone boundaries, before major releases, or to break single-model echo
  chambers.
---

# Reality Check Audit

Performs an adversarial, whole-system **"Outsider's Honest Assessment"** to break author and single-model confirmation bias. Every claim—praise or criticism—must be backed by direct inspection of source code, tests, configs, and data files.

> **Cross-Model Tip:** This audit delivers its highest signal when executed by a **different model family** than the one that authored the codebase (or in a fresh read-only context via `invoke_subagent`) with zero prior conversational loyalty.

---

## 1. Scoping & Evidence Verification Protocol

Before writing a single sentence of the assessment:

1. **Read the claims first:** Inspect the root `README.md`, key architecture/docs pages, `AGENTS.md` (if present), and any user-facing dashboards or CLI help output to inventory what the project *claims* to do.
2. **Verify against actual shipped code:** Trace each major claim directly into the implementation, entrypoints, tests, and data artifacts. Measure concrete facts (file sizes, line counts, test coverage of real paths vs. mocks, governance-to-feature ratios).
3. **Never accuse from filenames or surface greps alone:** Before labeling anything "stubbed", "vaporware", "untested", or "coupled", read the full module and its tests.
4. **Track self-corrections honestly:** If deeper inspection disproves an initial suspicion, drop or narrow the concern rather than defending a weak critique—and summarize major disproved hypotheses in an optional closing appendix so the user sees what held up under scrutiny.

---

## 2. Active Hunt Targets

Probe these four failure modes systematically:

1. **Mocked, Hardcoded, or Synthetic Reality**
   - Hardcoded metrics, fake dashboard numbers, static JSON fixtures served as "live telemetry", or stubbed adapters pretending to be real integrations.
   - Silent fallback paths that fabricate plausible outputs without labeling them degraded/offline.
   - Dead no-op functions, bypassed abstraction layers, or tests asserting behavior against local test-file stand-ins instead of production code.
2. **Documentation-vs-Code Drift & Aspirational Framing**
   - Theoretical math projections or lab-only simulation numbers presented as observed production metrics.
   - README badges, CLI flags, API endpoints, or feature tables that no longer match shipped code.
   - Fragmented or inconsistent implementations of the same documented rule, scoring formula, or invariant across multiple modules.
3. **Over-Engineering & Governance Bloat**
   - Disproportionate ratio of meta-rules, steering files, process docs, or scaffolding relative to actual product code ("the tail wagging the dog").
   - Redundant rules duplicated across `AGENTS.md`, skills, and docs—or governance checks enforced on one language/directory (e.g., `*.py`) while silently missing another (e.g., `*.js` or `*.ts`).
   - Premature abstractions, empty extension layers, or contributor friction that optimizes for internal rule consistency over user value.
4. **Structural & Trust-Boundary Weaknesses**
   - Subtle abuse/capture vectors in heuristics, consensus rules, or permission gates.
   - Un-decomposed monolith files hiding behind clean top-level architecture diagrams.
   - Unverified external assumptions (network, credentials, build steps) that fail silently or dangerously in real environments.

---

## 3. Required Report Structure

Save the assessment as a point-in-time **Historical Artifact** (e.g., `<appDataDir>/brain/<conversation-id>/reality_check_audit.md`) or present it directly in chat if the user asks for an inline review. Use this exact progression:

```markdown
# An Outsider's Honest Assessment of <Project / Scope>

> [!IMPORTANT]
> **Classification:** 🏛️ **Historical Artifact** (*"That belongs in a museum!"*)
> **Status:** Immutable Snapshot | **Recorded:** YYYY-MM-DD
> **Auditor:** <Model / Fresh Subagent> | **Scope:** <Exact repos, branches/commits, and areas read>

## TL;DR Verdict
[One blunt, fair paragraph: is this a real working system or vaporware? What is its strongest asset, and what is its biggest real risk?]

## I. What's Genuinely Good
[Concrete engineering strengths verified directly in code/tests—cite exact files and line ranges. Zero hollow flattery; omit anything not earned.]

## II. What's Concerning
[Ranked, substantiated risks—governance bloat, mocked/hardcoded reality, fragmented logic, structural/security flaws, asymmetric enforcement. Cite exact file paths, measurements, and cross-reference the matching Remediation Plan number.]

## III. What's Aspirational vs. Real

| Feature / Claim | Documentation Claim | Shipped Reality |
| :--- | :--- | :--- |
| <Capability> | ✅ <What docs/README promise> | **Real and working** (backed by `<file>`) |
| <Metric / Subsystem> | ⚠️ <What docs imply> | **Projected / Partial / Fragmented** — <exact gap> |
| <Unwired Feature> | ❌ <What docs claim> | **Aspirational / Mocked** — <exact evidence> |

## IV. Concrete Remediation Plans
[Numbered, self-contained remediation plans—**Plan 1**, **Plan 2**, etc.—directly addressing Sections II and III. Each plan specifies: target files, exact change, and deterministic verification check. Never give vague advice like "clean up docs."]

## V. Final Assessment
- **Is it conceptually sound?** [Direct answer + why]
- **Is it realistically applicable today?** [Direct answer + boundaries]
- **What is the real risk?** [The 1–2 risks that actually matter]

## Appendix: Hypotheses Tested & Retracted (Optional)
[Brief table of initial skepticisms that deeper code inspection disproved—proves the audit was thorough rather than superficial.]
```

---

## 4. Tone & Calibration Guardrails

- **Respect earned engineering, expose real gaps:** Never manufacture fake flaws to look "critical", and never soften a real defect to be polite.
- **Distinguish deliberate trade-offs from bugs:** Check `docs/adr/` or architecture docs before faulting an unusual design—if a trade-off was intentional and honestly documented, evaluate its consequences rather than treating it as an oversight.
- **Separate diff review from system audit:** If the user only wants a review of uncommitted changes or a single PR diff, recommend diff-level code review instead of a whole-repository reality check.
