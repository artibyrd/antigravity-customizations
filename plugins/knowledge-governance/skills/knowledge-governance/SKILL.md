---
name: knowledge-governance
description: >-
  Manages the 4-tier knowledge placement taxonomy, keeps AGENTS.md under an
  800-token hard ceiling via the Demotion Highway and /learn Admission Gate,
  distinguishes living invariants from historical ADRs, and conducts structured
  session retrospectives. Use when editing AGENTS.md, processing /learn
  proposals, challenging stale invariants, or auditing an agent environment.
---

# Knowledge Governance

Routes operational discoveries, rules, and retrospective findings into the lowest-cost cognitive layer so `AGENTS.md` stays sharp and attention dilution never creeps in.

When conducting a session retrospective or environment audit, read [references/retro-checklist.md](./references/retro-checklist.md) for the 7 diagnostic categories and severity-ranking workflow.

---

## 1. The 4-Tier Knowledge Placement Taxonomy

Route every new rule, pattern, or lesson to the lowest-cost tier that enforces it reliably:

| Tier | Artifact | Who Reads It | Implementer Cost | What Belongs Here |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | `AGENTS.md` *(hard ceiling: <800 tokens)* | Every agent, every turn (`always_on`) | Always-on (strictly rationed) | Universal Class α/β/γ invariants (1 sentence each) + crisp navigation pointers. Never multi-step procedures or CLI recipes. |
| **Tier 1** | Progressive Skills (`.agents/skills/<name>/SKILL.md` or plugins) | Implementer, only when triggered | Zero until activated | Subsystem-scoped runbooks, domain rules, and multi-step workflows (e.g., DB migrations, deploy ops, release procedures). |
| **Tier 1.5 *(Optional)*** | `CODING_STANDARDS.md` *(Review-Only)* | **Reviewer subagent ONLY**, never the implementer | **Zero** for implementer | Repo-wide **judgement calls** (cross-file consistency, naming idioms, error-handling style) that a linter cannot assert and that span multiple subsystems. Omit in small repos. |
| **Tier 2** | Automated Test Gates & Linters (CI, `just check`, pre-commit, governance tests) | Machine at check time (`<3s`) | **Zero** | **Every mechanical rule**: formatting, linting, typing, import shapes, manifest parity, doc links, file layout, token-budget ceilings. Default to building a Tier 2 check over writing a rule. |
| **Tier 3** | `docs/` & Architecture Blueprints | Humans & on-demand deep dives | **Zero** | Formal specifications, sequence diagrams, exhaustive references, and historical ADRs. |

### Tier 0 Cognitive Hierarchy (`AGENTS.md`)
Organize `AGENTS.md` into three concise classes so high-severity rules sit at the top:
- **Class α (Alpha — P0):** Sovereign safety, custody, security boundaries, and human authority.
- **Class β (Beta — P1):** Execution topology, delivery lifecycle, and workflow boundaries.
- **Class γ (Gamma — P2):** Interface symmetry, epistemic discipline, and navigation pointers.

### Implementation vs. Review Context Asymmetry
The **implementer** carries the highest context pressure (exploring code, editing files, debugging failures). The **reviewer** receives a focused diff and has abundant headroom. Keep `AGENTS.md` minimal for the implementer; push mechanical checks to **Tier 2** and cross-cutting style judgement calls to optional review-only **Tier 1.5 (`CODING_STANDARDS.md`)** (adding navigation pointers to `docs/` if it ever grows past ~1,000 lines).

---

## 2. The Demotion Highway & Invariant Lifecycle

> **Core Principle:** *If a machine can assert it deterministically in <0.3s, never waste prompt tokens on it.*

### Invariant Lifecycle
1. **`Proposed`** — Captured during `/learn`, a retrospective, or a post-mortem.
2. **`Active`** — Admitted to Tier 0 (`AGENTS.md`), Tier 1 (skill), Tier 1.5 (`CODING_STANDARDS.md`), or Tier 2 (automated check).
3. **`Under Review`** — Audited at milestone or minor-release boundaries.
4. **`Amended`** — Tightened, clarified, or merged with a related rule.
5. **`Demoted` (The Demotion Highway)** — Graduated out of Tier 0 `AGENTS.md` once an automated Tier 2 check, Tier 1 subsystem skill, or Tier 1.5 review standard covers it.
6. **`Retired`** — Obsolete rule removed and documented with rationale in Tier 3 docs/changelog.

### The `/learn` Admission Gate
Before admitting any new rule into Tier 0 `AGENTS.md`, prove all three gates:
1. **"Why not a test?" (Tier 2 Gate):** Prove no linter rule, pre-commit hook, or fast governance test can assert it deterministically. If a machine can check it, build the check and stop—never add prose to `AGENTS.md`.
2. **"Why not a skill or `CODING_STANDARDS.md`?" (Tier 1 / 1.5 Gate):** Prove the rule applies to *every turn* across the whole repo. If it is subsystem-scoped, route to a Tier 1 skill. If it is a repo-wide judgement call enforced at review time, route to optional Tier 1.5 `CODING_STANDARDS.md`.
3. **Token Budget Impact (<800-Token Gate):** Estimate `AGENTS.md` tokens (`word_count * 1.33`). If adding the rule would exceed 800 tokens, identify an existing rule to demote, compress, or retire first.

---

## 3. The Invariant Challenger

When auditing `AGENTS.md` (or reviewing user-global steering files such as `~/.gemini/GEMINI.md`), challenge every rule and assign exactly one disposition:

- **`PRESERVE`** — Requires active cognitive judgment or P0 human safety custody on every turn; stays in Tier 0.
- **`DEMOTE`** — Mechanically verifiable (graduate to Tier 2 test/linter), subsystem-scoped (move to Tier 1 skill), or review-only judgement call (move to Tier 1.5 `CODING_STANDARDS.md`).
- **`AMEND`** — Still valid, but wordy, ambiguous, or scoped too broadly; sharpen into a single actionable sentence.
- **`NULLIFY`** — No-op (does not alter agent behavior), superseded by architecture changes, or obsolete; delete and note why.

---

## 4. Living Invariants vs. Historical ADRs

Invariants and Architecture Decision Records (ADRs) are complementary—never conflate them:

| Dimension | **Living Invariants** (`AGENTS.md` / Skills / Tests) | **Historical ADRs** (`docs/adr/NNNN-*.md`) |
| :--- | :--- | :--- |
| **Lifecycle Class** | Living rule (*continuously updated*) | Historical artifact (*immutable point-in-time record*) |
| **Question Answered** | **"WHAT must always hold true right now?"** | **"WHY did we choose X over Y at time *t*?"** |
| **Mutability** | Mutable: `Proposed → Active → Amended → Demoted → Retired`. | Immutable once accepted; never edited in place—only superseded by a newer ADR. |
| **Admission Gate** | 3-part `/learn` Gate (not a test + universal + <800-token budget). | 3-part ADR Gate (all required): **hard to reverse** + **surprising without context** + **result of a real trade-off**. |
| **Agent Context Cost** | Paid per turn (Tier 0), on trigger (Tier 1), or at check time (Tier 2). | Zero on normal turns; consulted when exploring that area so agents do not re-litigate settled trade-offs. |

*Example:* An ADR records *why* a repo chose a zero-bundler frontend and what trade-offs were accepted; the enforceable rule ("no bundler manifest or `node_modules`") is demoted to a Tier 2 governance test instead of consuming Tier 0 tokens.

---

## 5. Session Retrospectives

When asked to run a retrospective or improve the agent environment after a session:
1. Read [references/retro-checklist.md](./references/retro-checklist.md).
2. Inspect the primary sources for the specified session (defaulting to the current session; inspect session logs/transcripts if the user points to an earlier run).
3. Inspect the repo's existing check/lint/CI configuration before proposing new automated checks.
4. Classify each candidate across the 7 diagnostic categories, route every proposed rule through the **4-Tier Taxonomy** and **`/learn` Admission Gate**, and present findings **ranked by severity**.
