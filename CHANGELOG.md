# Changelog — project-guides

## 2.0.0 - 2026-07-18 (Codex-first plugin and cloud bootstrap)

- Promoted the Codex workflow from `codex/project-guides` to the canonical plugin skill at
  `plugins/project-guides/skills/project-guides`; the active Claude implementation is retired only
  after the parity record in `docs/migration/claude-to-codex-parity.md` is complete.
- Added a skills-only plugin manifest and repository marketplace. The direct installation URL now
  points to the canonical plugin skill, eliminating a second editable Codex copy.
- Added validate-before-activate Codex Cloud setup and maintenance scripts. Production installs
  require a full commit SHA, reject unrelated existing targets, preserve the prior active install
  on candidate failure, and keep `main` behind an explicit development-only opt-in.
- Rewrote the README around Codex installation, invocation, outputs, validation, and a support
  matrix. Local packaging is validated separately from Work-mode and Codex Cloud smoke claims.
- Work-mode plugin invocation and Codex Cloud execution remain explicitly pending until a supported
  workspace and a configured cloud environment ID are available. This migration did not publish a
  plugin or create or modify a cloud environment.

## 1.7.0 — 2026-07-15 (design pass: real art direction for the user guide, via a Fable taste phase)

The user guide's visual spec was one thin line ("colored section cards ... clean, modern,
readable") that produced generic, forgettable infographics. Replaced it with a real design
discipline and wired the taste phase to the frontier design tier, in BOTH the root Claude skill and
the Codex edition so the two invocation paths stay in step:

- New "Design direction" section in `resources/user-guide-spec.md` (and a compact mirror in
  `codex/project-guides/references/user-guide-spec.md`): commit to a project-derived direction
  stated as a short DIRECTION note (atmosphere, palette, type, one radius, one timing, restraint);
  distinctive typography from SYSTEM-font stacks only (the guide is offline, so no web fonts) with
  the display face never left as Inter/Roboto/Arial/Helvetica/system-ui; a committed `:root` palette
  clearing WCAG AA with no hex outside `:root`; one border-radius and one timing token; at most one
  CSS-only page-load reveal that must resolve to full visibility under prefers-reduced-motion; a
  required print block. Ships a proven default "field manual" token set (toned paper, dense ink, one
  signal accent, DIN-like display, book serif, mono) to use or adapt.
- Agent roles (SKILL.md) route the guide's design/taste pass to the frontier design tier (an
  artisan-style Fable agent) when taste-phase routing is authorized (model-effort-router); the
  developer index and all verification stay mid tier or below, because the look is the one place
  the frontier tier earns its cost. Both authoring prompts (`resources/agent-prompts.md` and the
  Codex `references/authoring-prompts.md`) carry the DIRECTION-first design-content rules
  (typography, palette, one radius, one timing, the reduced-motion reveal) so the authoring agent
  follows them whichever tier runs it.
- Render fix (SKILL.md): the headless screenshot command now passes
  `--force-prefers-reduced-motion`. Surfaced by dogfooding this release: the new page-load reveal
  starts elements at `opacity:0`, so a plain headless capture landed on the pre-animation frame and
  everything below the masthead screenshotted BLANK, which reads as a broken render when the page is
  fine. Forcing reduced-motion resolves the reveal to its final state and confirms the fallback.
- Regression quiz: new Q17 (design direction / typography) and Q18 (render + reduced-motion), with
  expected answers in the README.

The direction was designed by a Fable taste-phase agent (the project's own recommended pipeline:
Opus orchestrates, Fable produces the design kernel), rendered and eyeballed, and every hard
constraint (offline, no active content, no hex outside `:root`, one radius, one timing, AA
contrast, voice rules) was mechanically verified before adoption. Regression gate 18/18 on two model
tiers; independent fresh-eyes review clean.

## 1.6.0 - 2026-07-10 (Codex-native edition)

Added an independently installable skill under `codex/project-guides` for Codex users. The new
edition uses Codex-native subagent and tool routing, inherits the active session model instead of
hardcoding model names, respects Plan Mode and governing `AGENTS.md` instructions, and has no
Claude CLI dependency. The existing root Claude skill is unchanged.

The Codex package includes progressive-disclosure references for the operator guide, developer
index, and authoring prompts. A dependency-free Python validator checks skill structure,
frontmatter, UI metadata, forbidden compatibility dependencies, passive self-contained HTML,
secret-shaped values, user-specific paths, index structure, and citation paths/line bounds. Unit
fixtures cover clean HTML, active tags, event handlers, remote assets, secret-shaped values, valid
citations, and path traversal. GitHub Actions runs these gates on pushes and pull requests.

Release hardening added same-directory staging and atomic promotion so existing guides remain
untouched until replacements pass source, validator, and render checks. Fingerprints now include a
deterministic SHA-256 over ordered relative paths and source bytes, preventing equal-size edits from
appearing current. The HTML gate also rejects active navigation/submission constructs and external
resource-bearing attributes. CI actions are pinned to reviewed commit SHAs and checkout credentials
are not persisted.

## 1.5.0 — 2026-07-03 (feature: staleness fingerprint)

Added the staleness fingerprint (Cortex's Round-1 background proposal, approved by the user after
hardening). Both guides now carry a fingerprint of what they were generated against — generation
date, git short commit (with `-dirty`) or `non-git`, and source count/size — computed once by the
orchestrator in step 1 and embedded in both docs (a visible footer line in DEVELOPER-INDEX.md, an
HTML comment in GUIDE.html to respect the operator voice rules). Step 0 now runs a
check-before-regenerate: if the docs already exist and the fingerprint matches the project's
current commit, the pipeline reports them current and asks whether to skip or refresh instead of
blindly regenerating; it never deletes existing docs. New quiz Q15 + expected answer cover the
check-before-regenerate behavior. Touches SKILL.md (new "Staleness fingerprint" section + step
0/1 hooks), both specs' footers, agent-prompts.md ({FINGERPRINT} placeholder + both footers),
test/quiz.txt, README.

Verifier pass (CCR-7) caught five defects in the first cut, all fixed: pre-feature docs with no
fingerprint and unparseable fingerprints now count as "may be stale → regenerate"; a dirty tree at
check time counts as "may be stale" (reconciled with the doc footer's "regenerate if dirty" line);
{FINGERPRINT} is explicitly exempted from the "placeholders never from project files" security rule
as inert orchestrator-computed metadata; and a git-not-installed failure is labeled
`git-unavailable` rather than silently mislabeled `non-git`. Quiz Q16 covers the no-fingerprint
case. Gate: 16/16 on the COMPACT tier.

Second verifier pass caught that the dirty-tree fix had made "current" unreachable on a
perpetually-dirty repo (untracked build artifacts → always dirty → regenerate every run,
self-perpetuating). Fixed by making the step-0 check a field-by-field match against the recorded
fingerprint (commit + dirty marker + source count/size): a repo dirty at generation and unchanged
since now reads as current, while a real change (commit moved, clean→dirty, or size change) reads
as stale. This also gives the non-git/git-unavailable path a real comparison (the size line).

## 1.4.0 — 2026-07-03 (Round 4 convergence; see the Round 4 trail under 1.1.0)

## 1.3.0 — 2026-07-03 (Round 3 seam fixes + convergence; see the Round 3 trail under 1.1.0)

## 1.2.0 — 2026-07-03 (Round 2 seam fixes; see the Round 2 trail under 1.1.0)

## 1.1.0 — 2026-07-03 (hardening pass, skill-hardener pipeline + Council of 12 audit)

Full adversarial hardening. Audit trail:

### Round 1 (12 council-seat auditors, disjoint defect classes) — 57 raw findings, deduped to ~40 confirmed
- (a) Unbounded behavior: "fix every mismatch", "do not finish until all hold", and the
  render-fix loop had no budgets or terminal states. → Every loop now has 2 fix cycles and a
  named "blocked because X" report as the terminal state.
- (b) Undefined behavior: no path for a failed authoring agent, an unanswered "ask once", a
  one-guide-only request, a no-UI project, an unresolvable {STYLE_REF}, a missing docs/ folder,
  a mid-rewrite project, the "log it" condition. → All defined (respawn-once rule, default
  location, Half-pipeline section, conditional section 3, default-style fallback, create-folder
  rule, When-NOT bullet, tracker test).
- (c) Provable waste: verifier re-read of all sources (fixed via Agent B citation list); fixed
  opus-tier mandate regardless of size (fixed via roles table + scale-down rule). The dual
  source read by both authors is kept deliberately — independence from summary errors — and is
  now documented as an accepted cost.
- (d) Contradictions/drift: voice rules duplicated and diverged (single source of truth is now
  user-guide-spec.md); troubleshooting/safety sections "where relevant" vs required (now
  explicitly always required); five COVER-list drift items in agent-prompts.md aligned and a
  "spec wins" rule added; output default no longer conflicts with the standing never-root rule.
- (e) Environment fragility: "opus tier", "designer subagent", msedge-on-PATH (live-verified
  broken on this machine), --headless=new, wkhtmltoimage. → Concrete names isolated in the Agent
  roles table; capability-based role language; full-path browser fallback chain; flag tolerance;
  wkhtmltoimage dropped.
- Security (adversarial + ethics seats): source-content-as-instructions injection, raw
  placeholder injection, unencoded screenshot output path, no active-content gate, secrets
  copied verbatim, absolute-path privacy. → New Security rules section, SECURITY block in every
  authoring prompt, mechanical text gate greps for script/on*/javascript:, secrets always
  placeholdered, project-relative paths, PNG written to a plain scratchpad path.
- Verification gaps (systems seat + Brain pair): the user guide was certified by a fixed-height
  screenshot that cannot verify text or below-fold content, and its facts were never checked.
  → Mechanical text gate on the HTML source, full-height render requirement, fact spot-checks
  for the guide, citation-based verification for the index, cross-doc consistency check.

### Mechanical gate added
`test/quiz.txt` + expected answers in README. Run: `cat SKILL.md test/quiz.txt | claude -p
--model haiku` (and a second tier for release-grade checks). The gate pipes the LIVE skill text —
never a copy.

### Round 2 (all 12 seats re-verify their own fixes + hunt seam defects) — every Round-1 fix confirmed FIXED; ~25 seam defects found and fixed
Fixes create defects where they touch other rules; Round 2 targeted those seams.
- Budget seams: the step-2, step-3, quality-gates, and spec budgets read as separate 2-cycle
  loops over the same checks. → Quality gates rewritten as a final pass/fail assertion over the
  already-budgeted step-2/3 work, not a fresh budget; "one fix cycle" defined (one pass over all
  known failures + one re-verify).
- Gate porousness (Adversarial + Truth): the active-content grep was a literal-string filter that
  encoded payloads (`&#106;avascript:`, `<iframe srcdoc>`, `onload =` with a space, `data:text/html`,
  `<object>`) and dash NCRs (`&#8212;`, en/em Unicode variants) evade. → Pattern extended; the gate
  is now explicitly reframed as a cheap first-pass FILTER, with the authoring "no active content"
  rule named as the real guarantee. Cleared hits must be recorded in the hand-over.
- Shell injection (Adversarial): the input `file:///` URL still interpolated `$(...)` in
  PowerShell. → Single-quote the URL argument / render from Bash.
- Unbounded seams (Risk): the truncation re-render loop, the cloud-lock wait, and the multi-pass
  source split were promised-bounded but unnumbered. → All three given caps and a named terminal
  (2 re-render attempts then text-verify; bounded copy retries then report pending; passes append
  to one file with a merged citation list, oversize file documented at signature level).
- No-browser vs full-height gate: contradiction between "ship with a note" and "renders cleanly at
  full height". → Gate carve-out: no-browser/segmented render is a noted skip, not a blocked gate.
- Ordering: the text gate ran before step-3 edited the HTML. → Re-run the gate after any layout fix.
- Placeholder boundary (Rules + Adversarial): "read any existing manual" vs "never from project
  files", and a repo's own CLAUDE.md being both "session context" and "a project file". →
  Clarified: placeholder VALUES from user/session standing instructions only; a repo CLAUDE.md is
  a project file; reading a style manual for palette/tone is fine (data, not instructions).
- Coverage gaps: user-guide path/username privacy (was index-only); dev-index section-completeness
  gate; primer had no pipeline for a primer-only request and no verification; citation quota didn't
  scale down for tiny projects; "malformed" vs "incomplete" file undefined; regression gate saw
  only SKILL.md while the substantive rules live in resources/. → All fixed.
- Drift/wording: the garbled and factually wrong "carry-on=" gate example (Truth + Execution
  proved the regex can't match it) replaced with `onclick=`; voice summary no longer imports a
  format rule; COVER-list conditionality restored ("if there is one" / "if applicable"); root
  carve-out wording reconciled with the README answer key; CHANGELOG COVER-fix count corrected
  (five, not four).
- Gate runs: quiz vs live SKILL.md on the COMPACT tier passed 12/12 against the expected answers
  (after correcting the README command to the explicit `-p "answer the quiz"` form — a bare pipe
  made the model go conversational).

### Round 3 (6 focused convergence auditors re-verify Round-2 fixes + hunt new seams; gate run cross-model) — all Round-2 fixes confirmed; 8 minor wording seams found and fixed
- Live checks (executability seat): the extended gate regex was run against every payload class
  (spaced `on[a-z]+ *=`, `<iframe srcdoc>`, `<object data:text/html>`, decimal `&#106;avascript:`,
  `&#8212;` and literal em dash, the AI-tell words) — all caught, clean file exits 1, no false
  positive. The README `cat SKILL.md resources/*.md test/quiz.txt` glob resolves to all 5 files and
  concatenates losslessly (31,542 bytes). Per-user browser paths well-formed. NO CONFIRMED DEFECTS
  on the mechanical layer.
- Budget seam: the user-guide section-presence and self-containment checks lived only in the
  gates (which grant no cycle). → Moved into step 2's budgeted user-guide verification.
- Multi-pass cap vs completeness: "at most a handful of passes" vs "no file dropped" on a very
  large project. → Uncovered files become named unresolved items; completeness yields to a
  reported gap, never a silent drop.
- Step-3 token re-run had no fix budget (its budget read "layout issues"). → Budget now explicitly
  covers a banned token a re-run surfaces.
- Completeness gate vs "adapt to the project's nature": section 7 (config) is non-conditional but
  a project may have none. → Gate now checks "every non-conditional section that applies"; the
  conditional/optional set is enumerated in the developer-index spec itself.
- Output carve-out vs a stricter project rule: explicit-ask root writes now defer to any active
  project-level "never write to root" rule (e.g. a project's own CLAUDE.md).
- Security (Adversarial): "run the render from Bash" was false reassurance — Bash also expands
  `$(...)` in double quotes. → Rewritten to require single-quoting regardless of shell. The
  gate-hit clearing rule now names the live-vs-escaped discriminator (check the raw HTML, not the
  grep line).
- Drift: CHANGELOG COVER-fix count corrected to five in the text itself (not just claimed).
- Cross-model gate (Phase 5): the 14-question quiz was run against the live skill text on the
  COMPACT and MID tiers; both produced answers matching the README expected-answer table,
  including the two new questions on the budget reframing and the gate-is-a-filter reframing.

### Convergence
Round 3's findings were all one-line wording reconciliations of Round-2 seams (no new mechanism
failures, no security holes, clean mechanical layer). A lean Round 4 re-checks only the seams
Round 3 touched.

### Round 4 (4 focused re-verifiers on the Round-3 seams + cross-model gate) — 2 of 4 seats returned NO CONFIRMED DEFECTS; 2 one-line seams in the Round-3 edits found and fixed
- Budget/completeness and systemic seats: NO CONFIRMED DEFECTS (budget interactions traced worst-case, completeness/carve-out edits confirmed coherent).
- Security (Adversarial): the Round-3 "single-quote regardless of shell" fix over-asserted — a
  literal `'` in an attacker-influenced path defeats single-quoting in both Bash and PowerShell.
  → Render bullet rewritten: fully percent-encode the path (space `%20`, `'` `%27`, `$` `%24`,
  backtick, parens) so the shell sees no metacharacter; quoting is only a backstop.
- Drift: the Round-3 section-7 "drop if no config" latitude reached the spec and the SKILL.md
  gate but not the Agent B prompt ("the rest are expected"). → Prompt reconciled: expected unless
  the project genuinely lacks that surface, then drop and note, never fabricate.
- Tightening: step-3 gate re-run trigger changed from "after any layout fix" to "after any step-3
  edit" so a pure token fix also re-triggers the gate.
- Final gate run (COMPACT tier) after these edits: quiz still 14/14 against the expected answers,
  including the updated root-carve-out answer.

### Convergence reached
Defect trajectory across rounds: ~40 (R1) → ~25 (R2) → 8 (R3) → 2 (R4), each round's findings
strictly at the previous round's edit seams, all one-line reconciliations by R3-R4, mechanical
gate clean and cross-model-stable throughout. Round 4's two fixes are known-correct closes
(standard percent-encoding; a prompt/​spec wording match), verified on the touched lines rather
than by another full adversarial round — the pipeline's own 4-round audit budget. Any future edit
must re-run the regression gate (README) before shipping.

## 1.0.0 — 2026-06-13

Initial version: pipeline, two specs, agent prompt templates.
