# Operational, UI/DOM & Verification Guardrails

Generalized architectural guardrails for [architecture-review](../SKILL.md). Consult this reference whenever auditing or designing developer toolchains (`Justfile`), CLI automation, production UI/web surfaces, browser verification suites, or technical specification docs.

---

## 1. Modular `Justfile` Architecture & Guidance Banners

When a repository uses `just` (or a comparable task runner) for developer and operator workflows:

- **Modular Subfiles:** Keep the root `Justfile` lean (`<80–100` LOC) as an orchestrator (`set shell`, `set dotenv-load`, `import` declarations) delegating to focused subfiles under `just/` (e.g., `preflight.just`, `quality.just`, `dev.just`, `vcs.just`, `deploy.just`, `release.just`), each well under ~300 LOC.
- **Safe vs. Gated Group Decoupling:** Never mix read-only inspection and mutating/destructive actions behind a single parameterized recipe.
  - Isolate read-only recipes (`status`, `diff`, `check`, `probe`) in safe groups (e.g., `[group('vcs: safe')]`, `[group('ops: safe')]`) so humans and agents can inspect freely.
  - Isolate mutating or destructive recipes (`commit`, `merge`, `deploy-prod`, `release`, `prune-all`) in gated groups (`[group('vcs: gated')]`, `[group('ops: gated')]`) protected by native `[confirm('...')]` guards.
- **Point-of-Action Guidance Banners:** Print concise directional beacons directly from toolchain recipes and helper scripts (showing the verified state and exact next command) rather than stuffing long procedural checklists into `AGENTS.md`.

---

## 2. Non-Interactive CLI Execution Invariant

Agent runs and CI pipelines stall indefinitely when child processes block waiting for interactive terminal input (`Proceed? [y/N]`, package download prompts, pager traps).

- Pass explicit non-interactive flags and environment variables on automated invocations:
  - `just --yes <recipe>` for `[confirm(...)]`-gated recipes (once the human has explicitly authorized the action).
  - `npx --yes` (or `-y`) to avoid interactive package-install prompts.
  - `CI=true` and `DEBIAN_FRONTEND=noninteractive` for package managers, installers, and build tools.
  - `--no-pager` / `GIT_PAGER=cat` for commands that might spawn a pager.

---

## 3. Zero-Mock Production Boundary & Fail-Closed Empty States

- **No Synthetic Data in Production Surfaces:** Production UIs, dashboards, APIs, and CLIs must never import, define, or silently fall back to hardcoded mock datasets, dummy cryptographic keys, fake trend lines, or synthetic scores. Keep simulators, chaos generators, and demo datasets strictly isolated to dedicated docs playgrounds or offline test fixtures.
- **Fail-Closed Empty States:** When an upstream endpoint is offline, uninitialized, or returns an empty collection:
  1. Surface the authentic state explicitly (`NO DATA`, `UNAVAILABLE`, `STANDALONE`, or `PENDING`).
  2. Render a clear empty-state card or status message explaining *why* data is absent and *how* to remediate or connect it.
  3. Lock or disable downstream actions (such as badge/credential export or submit controls) whenever prerequisites are unmet.

---

## 4. Safe DOM Construction (Zero Unsafe HTML / Inline Handlers)

For any client-side UI rendering API responses, query parameters, markdown metadata, or user-supplied values:

- **Construct DOM programmatically:** Build elements with `document.createElement(...)`, assign text via `.textContent` (never HTML parsing), set attributes explicitly via `setAttribute(...)`, and bind behaviour via `addEventListener(...)`.
- **Prohibited sinks for external/dynamic data:** Never interpolate API or user data into `.innerHTML`, `.outerHTML`, `insertAdjacentHTML(...)`, `document.write(...)`, or inline event attributes (`onclick="..."`, `onerror="..."`).
- **Allowlisted URLs:** Before assigning dynamic `href` or `src` attributes, validate the parsed URL scheme against an explicit allowlist (`http:` and `https:`, plus vetted root-relative `/` paths where appropriate) to block `javascript:` and `data:` injection.

---

## 5. Automated Browser Verification Gate

Pure HTTP 200 probes (`curl`, `httpx`) verify static serving and routing only—they miss ES module import errors, runtime `ReferenceError` / `TypeError` crashes, broken hydration, and unloaded assets.

Before presenting web UI, dashboard, or static documentation changes for human sign-off (Mk1 Eyeball Review), run an automated headless browser check (e.g., Playwright):

1. **Zero Uncaught Runtime Errors:** Attach `page.on("pageerror", ...)` (and check `console` error messages) across every exercised route and assert **zero** uncaught exceptions.
2. **Substantive DOM Mount:** Query the primary content root and assert meaningful rendered content (non-empty text, real mounted components—not blank shells or stuck loading spinners).
3. **Playwright Lazy-Image Scroll Verification:** Browsers defer loading `<img loading="lazy">` elements until they enter the viewport. Always scroll each target image into view (`img.scrollIntoView()` or Playwright's `locator.scrollIntoViewIfNeeded()`) and wait for load **before** asserting `img.complete && img.naturalWidth > 0`. Asserting without scrolling produces false failures or forces teams to skip image checks.
4. **Route & Viewport Sanity:** Exercise key deep-links, anchor navigation, and desktop/mobile viewports. Scope fixed-viewport app shells with container selectors (such as `body:has(.app-shell)`) so landing pages and docs retain unconstrained natural document scrolling.

---

## 6. Documentation & Spec Table Clarity

When reviewing architecture docs, RFCs, benchmarks, or operator runbooks:

- **Plain-English Companion Explanations:** Whenever a document introduces dense mathematical formulas, protocol constants, scoring equations, or multi-column parameter lattices, pair it with a concise **plain-English companion explanation** stating what the metric or constraint means in practice. Keep raw internal formulas out of top-of-funnel summaries until context is established.
- **Separate Minimum vs. Recommended Hardware Rows:** In sizing, deployment, and capacity tables, always present **Minimum Hardware** (the absolute floor required to run) and **Recommended Hardware** (the target production envelope) as **separate, explicitly labelled rows** so operators never confuse a minimum floor with a production target.
- **Genuine Schematics & Visible Captions:** Prefer concrete structural diagrams (data flows, state machines, sequence diagrams, topologies) with visible descriptive captions explaining what the graphic shows—never dump generic bullet lists into decorative boxes with arrows.
