# Deep Modules, Internal Decomposition & Deepening

Shared architecture vocabulary and deepening rules for [architecture-review](../SKILL.md). Design **deep modules**: substantial behaviour behind a small interface, placed at a clean seam, testable through that interface.

---

## 1. Glossary (Use These Terms Exactly)

Consistent vocabulary prevents vague drift. Use these exact terms instead of substituting "component", "service", "unit", "API", "signature", or "boundary":

- **Module:** Anything with an interface and an implementation—scale-agnostic (a function, class, subpackage, or vertical slice). *Use instead of:* unit, component, service.
- **Interface:** Everything a caller must know to use the module correctly—types and entrypoints, plus invariants, ordering constraints, error modes, configuration, and performance characteristics. *Use instead of:* API, signature.
- **Implementation:** The body of code inside a module. Distinct from **Adapter**: a small adapter can back a large implementation (a database repo) and a large adapter can back a tiny implementation (an in-memory fake). Say *adapter* when the seam is the topic; *implementation* otherwise.
- **Depth:** Leverage at the interface—the amount of behaviour a caller or test exercises per unit of interface it must learn. **Deep** = lots of behaviour behind a small interface; **shallow** = interface nearly as complex as the implementation.
- **Seam** *(Michael Feathers)*: A place where behaviour can vary without editing the calling site; the *location* where a module's interface lives. *Use instead of:* boundary.
- **Adapter:** A concrete implementation satisfying an interface at a seam (describes *role*, not substance).
- **Leverage:** Caller gain from depth—more capability per unit of interface learned across N call sites and M tests.
- **Locality:** Maintainer gain from depth—change, bugs, knowledge, and verification concentrate in one module rather than scattering across callers.

---

## 2. Deep vs. Shallow & Core Principles

```text
Deep Module (target)                 Shallow Module (avoid)
┌──────────────────────┐             ┌──────────────────────────────────┐
│   Small Interface    │             │         Large Interface          │
├──────────────────────┤             ├──────────────────────────────────┤
│                      │             │  Thin pass-through body          │
│  Deep Implementation │             └──────────────────────────────────┘
│                      │
└──────────────────────┘
```

When shaping an interface, ask: *Can I reduce entrypoints? Simplify parameters? Hide more orchestration and invariants inside?*

1. **Depth belongs to the interface, not the file count.** A deep module can be internally composed of small, cohesive, private submodules while exposing one small external interface.
2. **The Deletion Test.** Imagine deleting the module. If complexity disappears, it was a shallow pass-through. If complexity reappears across N callers, it earns its keep.
3. **The interface is the test surface.** Callers and tests cross the same external seam. Wanting to test *past* the interface signals the wrong module shape.
4. **One adapter = hypothetical seam; two adapters = real seam.** Introduce a port/seam only when at least two concrete adapters exist (typically production + test).
5. **Designing for testability:**
   - Accept dependencies instead of constructing concrete I/O inside the module.
   - Return computed results rather than mutating caller state silently.
   - Keep the surface area small (fewer entrypoints and parameters mean simpler, stronger tests).
6. **Rejected framings:** Reject *depth as LOC ratio* (rewards padding code), *interface as type signature only* (ignores invariants and error modes), and *boundary* (collides with DDD bounded contexts).

---

## 3. Harmonizing Deep Modules with the ~500 LOC Soft Trigger

Keep **two distinct size guardrails** completely separate so they never conflict:

| Guardrail | Applies To | Purpose |
| :--- | :--- | :--- |
| **Agent Markdown Context Ceiling** (`<800` tokens for root `AGENTS.md`, concise `SKILL.md`) | Agent steering files & skills | Prevents LLM attention dilution and per-turn token bloat (governed by `knowledge-governance` / `writing-for-agents`). |
| **~500 LOC Soft Decomposition Trigger** | Source code files (`.py`, `.ts`, `.js`, `.go`, etc.) | Keeps internal implementations scannable for humans and AI tools without sacrificing external interface depth. |

**How Deep Modules and ~500 LOC reinforce each other:**
- **Deep Modules** governs the **external seam**: callers see a small, high-leverage facade.
- **~500 LOC** is a **soft internal decomposition trigger**, *never* a mandate to splinter a deep module into shallow public wrappers.
- When a deep module's implementation grows past ~500 LOC, split its **private internals** into a cohesive subpackage behind the *same* small public interface:
  - Keep shared data structures in an internal `models` module so internal imports form a strict **Directed Acyclic Graph (DAG)** with zero circular dependencies.
  - Typical clean internal splits: CLI (`main.py` parser + `dispatch.py` routing + `helpers.py` adapters); server (`app.py` assembly + `api/` + `middleware/`); domain subpackage (`__init__.py` facade exporting `__all__` + focused internal modules).
  - **Native ES Module Pitfall:** In zero-build JavaScript, `export * from './submodule.js'` re-exports symbols to outside callers but **does not bind them in the facade's local scope**—always write explicit `import { ... }` bindings for any symbol referenced locally or registered on `window`.

---

## 4. Dependency Categories for Deepening

Classify a deepening candidate's dependencies to determine how the deepened module is tested across its seam:

1. **In-process:** Pure computation or in-memory state with no I/O. Always deepenable—merge the cluster and test directly through the new interface. No adapter needed.
2. **Local-substitutable:** Dependencies with fast local test stand-ins (in-memory SQLite/PGLite, temp filesystem). Deepenable with the stand-in running in tests; keep the seam internal rather than leaking a port onto the external interface.
3. **Remote but owned (Ports & Adapters):** Services you own across a network seam. Define a **port** at the seam: the deep module owns domain logic while transport is injected (HTTP/gRPC/queue adapter in production, in-memory adapter in tests).
4. **True external (Mock):** Third-party services you do not control (payment gateways, SMS providers). Inject an explicit port; supply a mock adapter in tests.

---

## 5. Seam Discipline & Replace-Don't-Layer Testing

- **Internal seams vs. external seams:** Private internal seams help organize or verify complex internals, but keep them hidden from external callers and tests unless callers genuinely vary them.
- **Replace, do not layer tests:** Once tests exercise observable outcomes across the deepened module's external interface, **delete** the obsolete unit tests pinned to old shallow wrappers. Tests must describe behaviour across the interface so they survive internal refactors without breaking.
