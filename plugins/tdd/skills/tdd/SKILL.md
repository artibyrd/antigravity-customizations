---
name: tdd
description: >-
  Two-phase vertical-slice test-driven development at pre-agreed public seams
  with hermetic offline testing boundaries. Use during planning (/plan) to lock
  in testable seams and vertical behavioral slices before coding or /teamwork
  swarms, and during implementation to drive red-green-refactor cycles, fix bugs
  test-first, or audit seam-based integration tests.
---

# Test-Driven Development

TDD spans **two coordinated phases**—**seam & vertical-slice design during planning** and the **red → green loop during implementation**. This skill governs what makes every cycle produce tests worth keeping: observable behavior, pre-agreed seams, hermetic boundaries, anti-patterns to reject, and loop discipline. Apply every section *before* and *during* the loop—never bolted on after implementation.

When exploring the codebase, read `GLOSSARY.md` (if present) so test names and interface vocabulary match the domain language, and respect any `docs/adr/` decisions in the area you touch; skip quietly if neither exists.

> **Project overlay (optional):** If `.agents/overrides/tdd.md` exists in the workspace or repository root, read it first and apply its `Overrides`, `Extensions`, and `Disabled / Not Applicable` deltas on top of this skill.

---

## 1. What a Good Test Is

Tests verify **observable behavior through public interfaces**, never internal structure. Code can be rewritten completely while behavior stays intact; good tests survive refactors untouched. A good test reads like a specification (`"user can checkout with valid cart"`) rather than a wiring diagram.

Read [references/tests.md](./references/tests.md) for concrete good/bad examples and [references/mocking.md](./references/mocking.md) for boundary-mocking guidelines.

---

## 2. Phase A — Planning-Time Seam & Vertical-Slice Design (With `/plan`)

A **seam** is the public boundary where you observe behavior without reaching inside—callers and tests cross the same interface. Tests live at seams, never against private internals.

**Lock seams and vertical slices during planning whenever creating an `implementation_plan.md`.** Doing this during Stage 2 (before coding or launching autonomous `/teamwork` swarm workers) prevents implementers from fighting a horizontal plan ("build all models → build all services → add tests at the end") and eliminates mid-swarm stalls waiting for human seam approval:

1. **List candidate public seams** for the planned feature, with a one-line note on **what each catches** and **what it misses**, and confirm with the user: *"What is the public interface, and which seams should we test?"*
2. **Check three interface invariants** before locking the plan:
   - **Depth over pass-throughs:** A deep module hides complexity behind a small, caller-friendly interface; if a test has to reach past the interface to assert behavior, the seam is in the wrong place.
   - **Real variance:** Introduce an adapter seam only when something genuinely varies across it (e.g., production gateway vs. in-memory fake), not for hypothetical future swaps.
   - **Pure return values & injected dependencies:** Accept external dependencies as parameters and return explicit results instead of mutating hidden state.
3. **Structure the plan as vertical behavioral slices:** Record the agreed seam(s) and ordered vertical tracer-bullet behaviors (thin end-to-end slices: one failing test → minimal code → next behavior) directly in `implementation_plan.md`.

*(Ad-hoc / planless fallback: When fixing a quick bug or building a small change without a formal plan, run this seam-agreement step inline before writing the first test—never write tests against unconfirmed seams.)*

---

## 3. Hermetic Testing Boundary

Keep unit and seam tests **fast, deterministic, and offline**:
- **Deterministic by construction:** Pin clocks, seed RNG, isolate temporary directories, and prefer real in-memory stores or local test databases over network services.
- **Zero internal mocking:** Never mock your own modules or internal collaborators. Exercise real local boundaries whenever they can run locally and deterministically.
- **Boundary-only doubles:** Inject narrow, SDK-style adapters strictly at true external system boundaries (third-party HTTP APIs, payment/email providers, LLM endpoints, non-deterministic clocks). Never replace core domain logic under test with hardcoded synthetic stubs.

---

## 4. Anti-Patterns to Reject

- **Implementation-coupled:** Mocks internal collaborators, invokes private methods, asserts call counts/order, or verifies via a side channel (querying internal DB tables instead of calling the public read interface). *Tell:* the test breaks during a behavior-preserving refactor.
- **Tautological:** Recomputes the expected value using the same formula as the production code (`expect(add(a, b)).toBe(a + b)` or mirroring logic in the test), so it passes by construction. Expected values must come from an independent source of truth: a known-good literal, a worked example, or the specification.
- **Test-file stand-ins:** Re-implements production validation, parsing, or handler logic as local helper functions inside the test file instead of calling the actual production seam. Security, parser, and integration tests must exercise real production handlers and validators directly.
- **Horizontal slicing:** Writing all tests upfront, then writing all implementation. Bulk upfront tests assert *imagined* shapes instead of real behavior and lock in rigid structure before learning from the code. Use **vertical slices** instead: one failing test → one minimal implementation → repeat, letting each tracer-bullet cycle inform the next.

---

## 5. Phase B — Execution-Time Rules of the Loop

- **Start from pre-agreed seams:** If `implementation_plan.md` already pins the approved seams and vertical slices from Phase A, confirm them briefly and enter red → green immediately (including inside `/teamwork` workers). If no seams were agreed during planning, complete Phase A with the user before writing the first test.
- **Red before green:** Write one failing test first, run it to observe the expected failure, then write only enough production code to make it pass. Do not anticipate future tests or add speculative abstractions.
- **One slice at a time:** One agreed seam, one behavior, one minimal implementation per cycle.
- **Keep refactoring in the review stage:** Do not interleave speculative refactors into the red → green cycle—address structural cleanup during the dedicated review stage once behavior is locked green.
