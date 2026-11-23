# Session Retrospective Checklist (7 Diagnostic Categories)

Use this checklist when auditing a coding session to improve the agent's **environment** for future runs. Always read the primary sources for the session (defaulting to the current session, or inspecting prior session logs/transcripts if the user specifies one) and check the repo's existing lint/test/CI setup before proposing new checks.

Present candidate improvements to the user **in order of severity** (highest impact first), routing each recommendation through the 4-Tier Knowledge Taxonomy in [../SKILL.md](../SKILL.md).

---

## The 7 Diagnostic Categories

1. **Navigation**
   - *Ask:* How easy was it for the agent to find the right files? Are there hidden dependencies between files or directories? Would a crisp **navigation pointer** in `AGENTS.md` or a Tier 1 skill eliminate wasted search turns?
   - *Use when:* The session spent excessive turns hunting for files, entrypoints, or conventions.

2. **Automated checks (Tier 2 — Highest Leverage)**
   - *Ask:* Could a deterministic check have caught an error the agent made (linting, typechecking, unit/governance tests, filesystem/manifest linters)?
   - *Preflight first:* Read the repo's own check command (`Justfile`, `Makefile`, `package.json`, `pyproject.toml`, CI workflows) before suggesting anything new—an existing check that sits unwired or silently broken is the real finding, not a reinvention.
   - *Standing finding:* A repo with **no guardrail at all** (no pre-commit hook and no CI job running lint/typecheck/test) is itself a high-severity finding, not a neutral default.
   - *Use when:* The agent made a mechanical mistake a check could catch, or the repo lacks basic automated guardrails.

3. **Coding standards (Tier 2 vs. Optional Review-Only Tier 1.5)**
   - *Ask:* Should the **reviewer** enforce a new rule, or should an existing rule be sharpened or removed?
   - *Classify first:*
     - **Mechanical violation** (fixed syntactic pattern, banned API, import shape, file-location rule) → **Tier 2 deterministic check, full stop** (custom linter rule, pre-commit hook, governance test, or CI job—whichever the repo's stack makes cheapest). Default to building the check over writing prose.
     - **Genuine judgement call** (cross-file consistency, "matches surrounding idioms", architectural taste no linter can assert) → **Optional Tier 1.5 `CODING_STANDARDS.md`** (read by the reviewer agent, not the implementer).
   - *Use when:* Review failed to catch a recurring mistake or a standard was vague/unenforced.

4. **Global `AGENTS.md` (Tier 0 Bloat Audit)**
   - *Ask:* Are steering instructions bloating `AGENTS.md` (or user-global `~/.gemini/GEMINI.md`) that should ride the **Demotion Highway** into Tier 2 checks, Tier 1 subsystem skills, or Tier 1.5 `CODING_STANDARDS.md`?
   - *Use when:* `AGENTS.md` approaches or exceeds the 800-token ceiling, or global rules accumulate project-specific clutter.

5. **Tool economy**
   - *Ask:* Did the agent make expensive, repetitive, or high-token tool calls that could be streamlined? Are custom CLIs, scripts, or MCP servers returning noisy output that wastes context?
   - *Use when:* The session burned disproportionate tokens or turns on clunky tool invocations.

6. **No-ops**
   - *Ask:* Are there instructions in `AGENTS.md`, skills, or rules that never actually change agent behavior (obvious platitudes like "write clean code", duplicated advice, or stale rules for deleted modules)?
   - *Action:* Mark `NULLIFY` under the Invariant Challenger and delete them.
   - *Use when:* Steering files feel long, generic, or unwieldy.

7. **Information access**
   - *Ask:* Was a crucial signal invisible to the agent—e.g., dev server logs not teed to a readable file, missing read-only access to diagnostics, or opaque build output?
   - *Use when:* The agent had to guess or ask the user for runtime state it could safely observe with better plumbing.

---

## Implementation vs. Review Context Reminder

- **Implementation agents** operate under maximum context pressure (exploring code, editing, debugging). Keep their always-on context (`AGENTS.md`) minimal and high-signal.
- **Review agents** operate on a bounded diff with minimal exploration. Place cross-cutting judgement-call standards in optional `CODING_STANDARDS.md` so reviewers enforce them at **zero implementer context cost**.
- Add navigation pointers from `CODING_STANDARDS.md` to `docs/` if it ever grows beyond ~1,000 lines.
