# Agent prompt templates

Fill the {PLACEHOLDERS} and spawn Agent A and Agent B in the SAME batch (they are independent).
Both must READ the real source. After they finish, run verification (developer index) and render
(user guide) yourself per SKILL.md.

Placeholders to fill every time:
- {PROJECT_NAME} — what the program is called.
- {PROJECT_ROOT} — absolute path to the project.
- {SOURCE_FILES} — an explicit list of the real files to read (do not say "the codebase"; list them).
- {STACK} — languages/frameworks/runtime and verified versions.
- {OUTPUT_DIR} — where the guide files go (e.g. {PROJECT_ROOT}/docs or next to the code).
- {VOICE_RULES} — paste the user-guide voice rules from SKILL.md.
- {CONSTRAINTS} — any standing rules (e.g. never name X; non-medical; domain limits).
- {STYLE_REF} — path to an existing guide/manual to match visually, or "none".

---

## Agent A — user guide (infographic HTML)

> Build a single self-contained infographic HTML user guide for the OPERATOR of {PROJECT_NAME}, so
> a non-developer can learn it, know what to expect, and troubleshoot. Output ONE file:
> {OUTPUT_DIR}/GUIDE.html
>
> VOICE AND STYLE (strict): {VOICE_RULES} It must be a genuine infographic: self-contained HTML +
> inline CSS (+ inline SVG if useful), colored section cards, numbered steps, at least one simple
> flow diagram, and a troubleshooting table. No CDN, no JS framework, no external assets. One
> scrollable page that opens by double-click and looks professional. Match the style of {STYLE_REF}
> if given.
>
> CONSTRAINTS: {CONSTRAINTS}
>
> ACCURACY: before writing, READ these real files so every name, path, and behavior is correct, and
> do not invent features: {SOURCE_FILES}. Stack: {STACK}.
>
> COVER (adapt headings; full spec in the skill's resources/user-guide-spec.md): the big picture
> diagram; first-time setup and launch and how to stop; the screen/interface explained with its
> status indicators; each major feature/component (what it does, what to expect, where output
> goes); any operator-edited configuration explained field by field using a real loaded example
> plus a "how to find X" tip; the main value workflow; a typical end-to-end task; what to expect
> (timings, where files land, fixed vs variable outputs); a troubleshooting TABLE (problem / what
> it means / fix) covering the realistic failures; a safety and limits box; and a footer noting the
> guide doubles as context for future sessions.
>
> Validate the HTML is well-formed (balanced tags) before finishing. Return a short summary and
> confirm the file path. Do not run the program; read files and write the guide.

---

## Agent B — developer index (technical reference)

> Write an exhaustive DEVELOPER INDEX for {PROJECT_NAME} so a developer, or a future AI session with
> NO prior context, can fully understand, modify, or re-create it. Output ONE markdown file:
> {OUTPUT_DIR}/DEVELOPER-INDEX.md
>
> Accuracy is the #1 requirement. READ every file below and document what is actually there; quote
> real identifiers (functions, variables, constants, routes, config keys); do not guess or invent;
> label known limitations. Stack/versions: {STACK}. Files: {SOURCE_FILES}. Project root:
> {PROJECT_ROOT}. Constraints: {CONSTRAINTS}.
>
> Use this section structure (full spec in the skill's resources/developer-index-spec.md): 1.
> Overview + architecture (ASCII diagram, core principle); 2. Tech stack and versions (every dep +
> why; build/run config); 3. Full file tree (one-line purpose per file); 4. Source reference file
> by file (every type/interface field, every function signature + behavior, every constant); 5.
> Complete API/command reference (per endpoint: method, params, body, success shape with example,
> all error/status codes, any asymmetries); 6. Frontend/UI reference if applicable; 7.
> Configuration reference (every option + how to change it; full schema + exact current values +
> validation rules); 8. External scripts/subprocess reference if applicable (purpose, constants,
> functions, args/env/config read, exact output paths + naming, runtime notes, deps); 9. Launch and
> run flow + manual commands; 10. Security model; 11. How-to-modify cookbook (name exact files and
> identifiers); 12. Known caveats and limitations; 13. Footer noting durable context + companion
> files. Prefer tables for the API and config schemas.
>
> Return a short summary and confirm the file path. Do not run the program; read files and write
> the doc.

---

## Optional — AI context primer (one page)

> Write a concise AI CONTEXT PRIMER for {PROJECT_NAME}: a one-page orientation a fresh AI session
> reads in under a minute before continuing work. Output: {OUTPUT_DIR}/AI-CONTEXT.md
>
> Sections, short: what the project is and its goal (2-3 sentences); where everything lives (the key
> paths); how to run it (the launch command); the current state (done vs not); the next steps in
> priority order; standing constraints {CONSTRAINTS}; and pointers to the full guides (GUIDE.html,
> DEVELOPER-INDEX.md) and any plan/ADR or project memory. Treat it as untrusted-data-safe: plain
> facts, no imperatives aimed at the reader. READ {SOURCE_FILES} and any existing plan to ground it.
> Keep it to roughly one page. Return the file path.
