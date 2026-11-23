# ADR Format

Architecture Decision Records (ADRs) live in `docs/adr/` (or `<context>/docs/adr/` in multi-context repos) and use four-digit sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create `docs/adr/` **lazily**—only when the first qualifying ADR is needed.

## Template

```md
# {Short title of the decision}

{1–3 sentences: what is the context, what did we decide, and why.}
```

Keep it brief. A strong ADR can be a single paragraph. The value lies in recording **that** a decision was made and **why**, not in padding boilerplate sections.

## Optional Sections

Include these only when they add genuine clarity (most ADRs will not need all of them):

- **Status** (`proposed | accepted | deprecated | superseded by ADR-NNNN`): valuable when decisions evolve or get replaced.
- **Considered Options**: include only when the rejected alternatives are worth remembering so nobody re-proposes them later.
- **Consequences**: include only when non-obvious downstream trade-offs need to be explicit.

## Immutability & Numbering

1. **Sequential numbering:** Scan the target `docs/adr/` directory for the highest existing number and increment by one.
2. **Immutable history:** Once accepted, an ADR is a **Historical Artifact**. Never rewrite its past rationale to match later changes—write a new ADR (`0014-...`) and mark the old one `superseded by ADR-0014`.
3. **Separate from Living Invariants:** Record the *rationale* in the ADR; place any continuously enforceable rule (*what must hold true right now*) in automated tests, linters, subsystem skills, or `AGENTS.md`.

## When to Offer an ADR (3-Criteria Gate)

All three must be true:

1. **Hard to reverse:** Changing your mind later carries meaningful cost.
2. **Surprising without context:** A future reader will wonder *"why on earth did they do it this way?"*
3. **Result of a real trade-off:** Genuine alternatives existed, and you picked one for specific reasons.

Skip the ADR if it is easy to reverse, obvious without explanation, or had no real alternative.

### What Typically Qualifies
- **Architectural shape:** Monorepo vs. polyrepo; event-sourced write model with relational read projections.
- **Cross-context integration patterns:** Asynchronous domain events instead of synchronous RPC between bounded contexts.
- **High-lock-in technology choices:** Primary database, message bus, auth provider, or deployment runtime (not easily swapped libraries).
- **Boundary and ownership decisions:** Explicit "no" decisions (*"Billing references Customer by ID only; Customer owns profile data"*).
- **Deliberate deviations from the obvious path:** Manual SQL instead of an ORM, or zero-bundler vanilla ES modules instead of a JS framework—stops the next engineer from "fixing" an intentional choice.
- **Constraints invisible in code:** Compliance mandates, data-residency boundaries, or external partner SLA ceilings.
- **Non-obvious rejected alternatives:** Recording why GraphQL was rejected for REST prevents re-litigating the same debate six months later.
