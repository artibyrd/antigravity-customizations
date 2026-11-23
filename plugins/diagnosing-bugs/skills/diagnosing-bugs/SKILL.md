---
name: diagnosing-bugs
description: >-
  Structured 6-phase diagnosis loop for hard bugs and performance regressions:
  tight red-capable feedback loop first, reproduce and minimise, 3-5 ranked
  falsifiable hypotheses, targeted [DEBUG-xxxx] instrumentation, seam regression
  test, and cleanup. Use when the user says "diagnose" or "debug this", or
  reports something broken, throwing, failing, flaky, or slow.
---

# Diagnosing Bugs

A 6-phase discipline for hard bugs and performance regressions. Skip phases only when explicitly justified.

When exploring the codebase, read `GLOSSARY.md` (if present) for domain vocabulary and check `docs/adr/` or local ADRs (if present) in the area you are touching; skip quietly if neither exists.

## Redact Secrets First

This workflow prints commands, outputs, and captured artifacts. **Redact every secret first**: replace credentials, tokens, cookies, and keys with `<REDACTED>`. Build loops against environment variables so secrets stay in the environment rather than in commands or logs. Captured artifacts often carry auth headers—quote only the lines carrying the signal.

If the redacted output is not enough to diagnose the bug, say so explicitly and ask the user.

---

## Phase 1: Build a Tight, Red-Capable Feedback Loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal that goes red on *this* bug, bisection, hypothesis-testing, and instrumentation all consume it cleanly. Without one, staring at code leads to guessing.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to Construct a Loop (Rough Priority Order)

1. **Failing test** at whatever seam reaches the bug: unit, integration, or e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer / browser tool) driving the UI and asserting on DOM, console, or network state.
5. **Replay a captured trace:** save a real network request, payload, or event log to disk and replay it through the code path in isolation.
6. **Throwaway harness:** spin up a minimal subset of the system that exercises the bug code path with a single call.
7. **Property / fuzz loop:** for "sometimes wrong output" bugs, run 1,000 random inputs and isolate the failure mode.
8. **Bisection harness:** if the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" for `git bisect run`.
9. **Differential loop:** run the same input through old-version vs. new-version (or two configs) and diff outputs.
10. **HITL bash script (last resort):** when a human must click or authenticate, drive them with [scripts/hitl-loop.template.sh](./scripts/hitl-loop.template.sh) so the loop stays structured and captured observations feed back to you.

### Tighten the Loop

Treat the loop as a product. Once you have *a* loop, **tighten** it:
- **Faster:** cache setup, skip unrelated init, narrow test scope.
- **Sharper signal:** assert on the user's specific symptom, not "didn't crash".
- **More deterministic:** pin time, seed RNG, isolate filesystem, freeze network.

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### Non-Deterministic Bugs

Aim for a **higher reproduction rate**, not a pristine single repro. Loop the trigger 100×, parallelise, add stress, narrow timing windows, or inject controlled delays. A 50%-flake bug is debuggable; a 1% flake is not—raise the rate until it is reliably observable.

### When You Genuinely Cannot Build a Loop

Stop and say so explicitly. List what you tried. Ask the user for:
- (a) access to an environment that reproduces the bug,
- (b) a redacted captured artifact (HAR file, log dump, core dump, timestamped trace), or
- (c) permission to add temporary production instrumentation.

**Do not hypothesise without a loop.**

### Phase 1 Completion Gate

Phase 1 is complete only when you can name **one command** you have **already run at least once** (showing the redacted invocation and output) that is:
- [ ] **Red-capable:** exercises the real bug code path and asserts the **user's exact symptom**, so it goes red on this bug and green once fixed.
- [ ] **Deterministic:** same verdict across runs (or a pinned, high reproduction rate for flakes).
- [ ] **Fast:** seconds, not minutes.
- [ ] **Agent-runnable:** runs unattended (human-in-the-loop only via [scripts/hitl-loop.template.sh](./scripts/hitl-loop.template.sh)).

If you catch yourself reading code to form a theory before this command exists, **stop**: jumping straight to hypotheses is the exact failure this discipline prevents. No red-capable command, no Phase 2.

---

## Phase 2: Reproduce + Minimise

Run the loop and watch it go red. Confirm:
- [ ] The loop produces the exact failure mode the **user** described, not a different nearby failure.
- [ ] The failure reproduces reliably across runs (or at a high, measured flake rate).
- [ ] The exact symptom (error message, wrong output, latency measurement) is captured so later phases verify the real fix.

### Minimise

Once red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut, keeping only what is load-bearing.

A minimal repro shrinks the hypothesis space in Phase 3 and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**: removing any one of them turns the loop green. Do not proceed until you have reproduced **and** minimised.

---

## Phase 3: Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible guess.

Every hypothesis must be **falsifiable** with an explicit prediction:
> Format: `"If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."`

If you cannot state the prediction, it is a vibe—discard or sharpen it.

**Show the ranked list to the user before testing.** Their domain context often re-ranks instantly or eliminates ruled-out hypotheses. Do not block on a reply if the user is unavailable—proceed down your ranking.

---

## Phase 4: Instrument

Every probe must test a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:
1. **Debugger / REPL inspection** if supported—one breakpoint beats ten logs.
2. **Targeted logs** at the exact boundaries that distinguish competing hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix such as `[DEBUG-a4f2]`. Cleanup becomes a single `grep`. Untagged logs survive; tagged logs die.

**Performance branch:** For performance regressions, logs usually distort timings. Establish a repeatable baseline measurement first (timing harness, profiler, query plan), then bisect or isolate. Measure first, fix second.

---

## Phase 5: Fix + Regression Test

Write the regression test **before the fix**, provided a **correct seam** exists.

A correct seam exercises the **real bug pattern** as it occurs at the call site. A shallow test (single-caller test when the bug requires concurrent callers, or a unit test that mocks away the triggering chain) gives false confidence.

**If no correct seam exists, that itself is a finding.** Document that the architecture prevented locking down the bug and carry that note into Phase 6.

If a correct seam exists:
1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail. (If you forced the red state by mutating code or a fixture, `diff` against a pristine copy to confirm the mutation landed before trusting it.)
3. Apply the fix.
4. Watch the regression test pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

---

## Phase 6: Cleanup

Verify every item before declaring done:
- [ ] Original Phase 1 repro loop re-run and confirmed green.
- [ ] Regression test passes (or absence of a clean seam is documented).
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` confirms zero remaining hits).
- [ ] Throwaway harnesses/prototypes deleted (or moved to a clearly-marked scratch/debug location).
- [ ] The confirmed root-cause hypothesis is stated in the commit or PR message so future debuggers learn from it.
