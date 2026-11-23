# UI Prototype

Generate **several radically different UI variations** switchable from a floating bottom bar. The user flips between variants in the browser, picks a winner (or combines elements across variants), and discards the rest before committing.

If the question is about business logic or state transitions rather than visual layout/interaction, switch to [references/logic.md](./logic.md).

---

## When This Is the Right Shape

- *"What should this page or panel look like?"*
- *"Show me a few genuinely different options for this dashboard before we commit."*
- *"Try alternative layouts for the settings screen."*
- Any time debating vague mental mockups is slower than clicking through 3 real layouts.

---

## Choosing the Host Shape

### Sub-Shape A: Adjustment to an Existing Page *(Strongly Preferred for Live Web Apps)*

A UI prototype is far easier to judge when it butts up against the rest of the app: real header, real sidebar, real data density. An isolated canvas hides layout friction.

- Render variants **on the existing route**, gated by a `?variant=` URL search parameter (`?variant=A`, `?variant=B`, `?variant=C`).
- Keep existing data fetching, auth, and route params intact; swap only the rendered UI subtree.
- Even for a new section, card, or step that naturally lives inside an existing page, mount the variants inside that host page.

### Sub-Shape B: Standalone Throwaway Surface *(When No Host Page Exists)*

Use this only when the surface genuinely has no existing home (an entirely new top-level app/surface, or a repository without a running frontend yet):

- **In an existing web app:** create a clearly marked throwaway route obeying the project's existing routing convention (include `prototype` in the path or filename, e.g. `/prototype/<name>`). Never invent a new top-level folder architecture.
- **Without a running frontend (or for fast isolated concept sketches):** build a **single self-contained HTML file** in the session scratch/artifact directory (`<appDataDir>/brain/<conversation-id>/scratch/prototype-<slug>.html`)—or render interactively via Antigravity's `generative_ui` skill—using the exact same `?variant=` URL param (or hash/state) and floating bottom switcher bar so the repo root stays completely clean.

In all shapes, the floating bottom switcher bar is identical.

---

## Process

### 1. State the Question and Pick N

Default to **3 variants**. Cap at **5** (more than 5 turns radical options into noise).

Write a one-line scope note at the top of the prototype or route comment:
> *"Three structurally different variants of the settings page, switchable via `?variant=`, on `/settings`."*

### 2. Generate Radically Different Variants

Hold every variant to:
- the surface's real purpose and available data,
- the project's existing component library / styling system (or clean zero-dependency CSS for standalone HTML),
- a clear exported or named identifier (`VariantA`, `VariantB`, `VariantC` with short descriptive labels like `Sidebar layout`, `Split workbench`, `Guided wizard`).

Variants must be **structurally different**: different layout, different information hierarchy, different primary affordance—not color swaps or minor spacing tweaks. Three slight variations of the same card grid is wallpaper, not a UI prototype. If two drafts converge, discard one and regenerate with an explicit structural constraint (e.g. *"do not use a card grid"*).

### 3. Wire the Switcher

Mount one clean switcher around the variants:

```tsx
// Conceptual sketch — adapt to the project's framework or plain JS
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A', 'B', 'C']} current={variant} />
  </>
);
```

Keep read-only data above the switcher; stub any mutating actions so exploring variants never mutates real backend state.

### 4. Build the Floating Bottom Switcher Bar

Render a compact fixed-position bar at the bottom-center of the viewport with three elements:
- **Left arrow (`←`):** cycles to the previous variant (wraps around).
- **Variant label:** shows the current key and short descriptive name (e.g. `B · Split workbench`).
- **Right arrow (`→`):** cycles to the next variant (wraps around).

Required switcher behaviors:
- **Reload-stable URL:** clicking an arrow updates `?variant=` via the framework router (`router.replace`, `navigate`, or `history.replaceState`) so any variant can be reloaded or linked directly.
- **Keyboard navigation:** `←` and `→` arrow keys cycle variants, **except** when focus is inside `<input>`, `<textarea>`, `<select>`, or `[contenteditable]`.
- **Visually distinct:** style as a high-contrast floating pill with subtle shadow so nobody mistakes it for part of the UI under evaluation.
- **Hidden in production builds:** for in-app prototypes, gate rendering on a non-production environment check (`process.env.NODE_ENV !== 'production'` or framework equivalent) so a stray merge can never expose the bar to end users.

### 5. Hand It Over

Share the exact preview URL and `?variant=` keys (or clickable `file://` link / browser preview / `generative_ui` widget for standalone HTML—never assume `open` or `xdg-open`). Expect hybrid feedback like *"keep the navigation from B with the detail pane from C"*; that synthesis is usually the real design.

### 6. Capture the Answer and Clean Up Before Committing

Once a direction wins, follow [SKILL.md](../SKILL.md):
- **Rewrite the winner properly** into production code (real error handling, accessibility, safe DOM construction, tests—never ship raw prototype code straight to production).
- **Sub-shape A:** fold the production implementation into the existing route; delete every losing variant component and the `PrototypeSwitcher` from the working tree before committing.
- **Sub-shape B (in-app route):** promote the production implementation to its real route; delete the throwaway `/prototype/...` route and `PrototypeSwitcher` before committing.
- **Sub-shape B (scratch HTML):** keep the scratch HTML outside the repo (or optionally archive on a separate throwaway git branch) so `git status` contains zero throwaway artifacts.

---

## Anti-Patterns

- **Variants that differ only in colors, fonts, or copy.** Real variants disagree on structure and workflow.
- **Sharing a rigid `<Layout>` across all variants.** A shared top header is fine; sharing the page layout prevents genuine structural exploration.
- **Wiring variants to real backend mutations.** Stub writes; the question is layout and UX, not backend persistence.
- **Shipping raw prototype components or the switcher bar to main.** Rewrite the winning design cleanly and delete all prototype scaffolding before committing.
