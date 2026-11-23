---
name: domain-modeling
description: >-
  Actively builds and sharpens a project's domain model: checks the codebase
  first, challenges fuzzy terminology, maintains a lazy implementation-free
  GLOSSARY.md (or multi-context GLOSSARY-MAP.md) inline, and gates immutable
  Historical ADRs behind a 3-criteria trade-off check separate from Living
  Invariants. Pairs naturally with Antigravity's native /grill-me. Use when
  discussing domain terminology, editing GLOSSARY.md, or recording an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is an *active* discipline: exploring code first, challenging fuzzy terms, stress-testing boundaries with edge-case scenarios, and recording glossary terms and architectural decisions the moment they crystallise.

> **Pairs with native `/grill-me`:** During interactive design sessions, use Antigravity's native `/grill-me` workflow to interview through open design decisions while applying this skill to lock down ubiquitous language in `GLOSSARY.md` and gate Historical ADRs.

---

## 1. Explore First, Ask Second

Before asking the user how a concept works or what a term means in the current system:
1. Check for `GLOSSARY-MAP.md`, `GLOSSARY.md`, and `docs/adr/` to load existing language and settled decisions.
2. Inspect the relevant source code, schemas, and tests directly.
3. Never ask the user a factual question the repository can answer. When the user's description contradicts the code, surface the mismatch concretely: *"The code cancels entire Orders, but you just described partial cancellation. Which behavior is canonical?"*

---

## 2. Lazy File Structure

Create domain files **lazily**—only when you have something concrete to write. Never pre-scaffold empty glossaries or empty `docs/adr/` directories.

### Single Context (Most Repos)
```text
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

### Multi-Context Repos (`GLOSSARY-MAP.md`)
When a repo spans distinct bounded contexts, place a `GLOSSARY-MAP.md` at the root pointing to each context's glossary and context-specific ADRs (keeping system-wide ADRs at root `docs/adr/`):

```text
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                  ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/         ← context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

---

## 3. Active Session Habits

### Challenge Against the Glossary
When the user uses a term that conflicts with `GLOSSARY.md`, call it out immediately: *"Your glossary defines 'Cancellation' as X, but you seem to mean Y. Which is it?"*

### Sharpen Fuzzy Language
When the user uses overloaded or vague words, propose a canonical term and capture rejected synonyms under `_Avoid_`: *"You're saying 'account'—do you mean the Customer or the User? Those are different concepts."*

### Stress-Test with Concrete Scenarios
Probe domain boundaries by inventing sharp edge cases that force crisp definitions (e.g., partial refunds, split shipments, revoked memberships, re-opened records).

### Update `GLOSSARY.md` Inline (Zero Implementation Details)
The moment a term is resolved, update `GLOSSARY.md` right there—do not batch terms up for the end of the session. Follow [references/glossary-format.md](./references/glossary-format.md).

- **`GLOSSARY.md` must stay strictly devoid of implementation details.** No database columns, API endpoints, class names, file paths, or design notes. It is a domain glossary and nothing else.
- If no `GLOSSARY.md` exists yet, create it lazily when the first term is resolved.

---

## 4. Offer Historical ADRs Sparingly (3-Criteria Gate)

Create `docs/adr/` lazily on the first qualifying decision, and follow [references/adr-format.md](./references/adr-format.md). Offer to write an ADR **only when ALL three criteria hold**:

1. **Hard to reverse:** Changing direction later carries meaningful migration or rewrite cost.
2. **Surprising without context:** A future reader will look at the codebase and ask *"why did they do it this way?"*
3. **Result of a real trade-off:** Genuine alternatives existed, and you chose one for specific reasons worth preserving.

If any single criterion is missing, skip the ADR.

---

## 5. Historical ADRs vs. Living Invariants

ADRs and enforceable project invariants are complementary—never conflate them:

| Dimension | **Historical ADRs** (`docs/adr/NNNN-*.md`) | **Living Invariants** (`AGENTS.md`, Skills, Automated Tests) |
| :--- | :--- | :--- |
| **Lifecycle Class** | 🏛️ **Historical Artifact** (*immutable point-in-time record*) | 🟢 **Living Rule** (*continuously maintained*) |
| **Question Answered** | **"WHY did we choose X over Y at time *t*?"** | **"WHAT must always hold true right now?"** |
| **Mutability** | Immutable once accepted; never edited in place—only superseded by a newer ADR (e.g., `superseded by ADR-0014`). | Mutable: proposed, active, amended, demoted to automated checks, or retired. |
| **Agent Context Cost** | Zero on normal turns; consulted during exploration/design so agents stop re-litigating settled trade-offs. | Paid per turn (if in `AGENTS.md`), on skill trigger, or at test/CI time (zero prompt cost). |

*Example:* An ADR explains **why** a frontend rejected build-time bundlers in favor of vanilla ES modules and what trade-offs were accepted; the enforceable rule (*"no bundler manifest or `node_modules` directory"*) belongs in an automated governance test—not duplicated as mutable prose inside the ADR.
