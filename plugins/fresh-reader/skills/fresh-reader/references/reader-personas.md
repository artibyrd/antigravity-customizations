# Fresh Reader Personas & Top-Down Cascade Sieve

`fresh-reader` evaluates documentation across **four explicit reader personas** spanning two distinct axes:
* **Accessibility Gradient** (`senior-engineer` → `junior-engineer` → `vibe-coder`): how much software engineering and tooling background the reader brings.
* **Technical Rigor Lens** (`domain-expert`): deep specialist scrutiny of correctness, assumptions, notation, and edge cases.

---

## 1. The Four Reader Personas

| Persona | Assumed Background | What This Reader Actively Hunts | Expected `WON'T DO` Boundary |
| :--- | :--- | :--- | :--- |
| **`vibe-coder`** | Zero prior coding, Git, or terminal experience; just starting with AI/agentic tools. | Unexplained coding/CLI/Git jargon, missing "what exact words do I type or click?", missing high-level mental models ("why does this matter?"), intimidating setup leaps. | Deep architectural internals or edge-case theory intentionally kept behind progressive-disclosure links. |
| **`junior-engineer`** | Comfortable with at least one programming language and basic Git/terminal/dev workflows, but lacks experience with architecture patterns, testing theory, or agentic workflow conventions. | Unexplained architecture/testing/workflow jargon (e.g., *public seams*, *Deep Modules*, *ADRs*, *hermetic tests*, *tracer-bullet slices*), overly niche/advanced examples, and missing "how do I actually run/invoke this?" steps. | Basic Git/CLI literacy (`git clone`, `git diff`, JSON syntax, pull requests) or plugin-internal reference material intentionally linked out. |
| **`senior-engineer`** *(default)* | Experienced software engineer familiar with standard industry concepts (`git diff`, PRs, TDD, Mermaid, ADRs, SOLID/code smells, CI/CD) and basic Antigravity usage, with zero knowledge of *this* project. | Project-specific jargon, internal contradictions, backwards chronological steps, missing operational caveats, unstated prerequisites, and misleading claims. | Standard software engineering terms (`TDD`, `PR`, `JSON`, `SSRF`, `Mermaid`) and progressive-disclosure details owned by linked companion docs. |
| **`domain-expert`** | Deep subject-matter specialist (e.g., cryptography, formal methods, applied mathematics, distributed consensus, security protocols) reading rigorous technical documentation. | Unstated assumptions, mathematical/logical leaps, notation or definition inconsistencies, edge-case flaws, imprecise bounds, and hand-waved proofs or benchmarks. | Requests to simplify standard specialist notation or add elementary tutorials meant for general audiences. |

---

## 2. Top-Down Cascade Sieve Order

Good documentation must be **both technically accurate and accessible at its target depth**. Running a single pass directly at a novice level often buries factual contradictions under vocabulary noise; running bottom-up (`vibe-coder` → `senior-engineer`) floods higher-level docs with false positives.

Always execute the **Top-Down Cascade Sieve** down to the target persona:

| Target Persona | Required Cascade Sequence | Final Accuracy Sanity Check |
| :--- | :--- | :--- |
| **`senior-engineer`** | 1. `senior-engineer` *(converge to zero-edit)* | Built in (already verified at `senior-engineer`). |
| **`junior-engineer`** | 1. `senior-engineer` *(converge structural accuracy & project jargon)*<br>2. `junior-engineer` *(converge conceptual scaffolding, jargon bridges & relatable examples)* | If `junior-engineer` edits substantially rewrote technical claims, run 1 quick `senior-engineer` accuracy sanity check to ensure simplification introduced zero technical errors. |
| **`vibe-coder`** | 1. `senior-engineer` *(converge structural accuracy)*<br>2. `junior-engineer` *(converge engineering concepts)*<br>3. `vibe-coder` *(converge plain-English mental models & copy-paste steps)* | If `junior-engineer` / `vibe-coder` edits substantially rewrote technical claims, run 1 quick `senior-engineer` accuracy sanity check. |
| **`domain-expert`** | 1. `domain-expert` *(converge technical rigor, assumptions, notation & edge cases)*<br>2. *(Optional)* `senior-engineer` if the doc must also read cleanly for cross-team engineers outside the narrow specialty. | Built in (`domain-expert` locks correctness first; if optional `senior-engineer` rewrites technical prose, verify accuracy with 1 quick `domain-expert` check). |

*(Skip an upper sieve ONLY when the exact current document text has already converged at that upper sieve in the same run with zero subsequent edits.)*

---

## 3. Persona-Scoped Dismissal Carryover Rules

Maintain one **Cumulative Triage Ledger** across all sieves, tagging every `WON'T DO` entry with its **scope**:

1. **`scope: global`** (carries across *all* subsequent sieves):
   * Intentional progressive-disclosure boundaries (e.g., *"exact hook regex patterns belong in `plugins/foo/README.md`, not the root overview"*).
   * Intentional product/platform boundaries (e.g., *"do not duplicate unstable Antigravity IDE UI settings paths"*).
   * Anti-oscillation locks on passages already settled with the user.
2. **`scope: persona-only`** (carries *only* within the same persona—**never** suppresses a lower accessibility persona):
   * *"Expected industry term for `senior-engineer`"* (e.g., `hermetic tests`, `public seams`, `ADRs`, `Deep Modules`). When advancing from `senior-engineer` → `junior-engineer` (or `junior-engineer` → `vibe-coder`), re-evaluate those terms fresh against the new persona's baseline!

---

## 4. Cold-Start Persona Brief Snippets

Paste the matching snippet into `<persona>` in `SKILL.md` Step 2:

* **`vibe-coder`:** *"a non-programmer ('vibe coder') with zero prior coding, Git, or command-line experience who is just getting started with AI-assisted development in Google Antigravity and has zero prior context about this repository."*
* **`junior-engineer`:** *"a junior software engineer who knows a programming language and basic Git/terminal workflows, but has little experience with software architecture patterns, testing theory, or agentic workflow conventions—visiting this repository for the very first time with zero prior context."*
* **`senior-engineer`:** *"an experienced software engineer familiar with Git, terminals, testing, and basic Google Antigravity usage, visiting this repository for the very first time with zero prior context about how this project was designed or built."*
* **`domain-expert`:** *"a skeptical subject-matter domain expert in this document's technical field reading with a rigorous, discerning eye for unstated assumptions, notation or definition inconsistencies, edge cases, logical gaps, and technical inaccuracies—with zero prior context about how this document was drafted."*
