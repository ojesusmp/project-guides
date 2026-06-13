---
name: project-guides
description: Generate two companion guides for any project: a visual infographic HTML user guide in plain human voice (learn it, know what to expect, troubleshoot) and an exhaustive developer index (every file, path, variable, function, endpoint, config option, and script internal, enough to modify or rebuild). Use after building a program, app, feature, or toolkit when the user wants documentation, onboarding material, a rebuild reference, or durable context for future AI sessions, or when they ask for "the two guides", a user guide, a developer index or technical reference, or to document a project. Authors both via source-reading agents in parallel, verifies the technical doc against the real code, and renders the infographic to confirm it looks right.
---

# Project Guides

Produce a documentation pair (optionally a trio) for a finished program, app, or feature.
The same pipeline every time: author from the real source with parallel agents, verify the
technical doc against the code, render the infographic to confirm it is right, then hand over.

## What this produces

1. **User guide** — a self-contained infographic HTML file. Audience: the operator. Plain human
   voice. Teaches the program, sets expectations, and troubleshoots. Section spec:
   `resources/user-guide-spec.md`.
2. **Developer index** — an exhaustive Markdown technical reference. Audience: anyone modifying or
   rebuilding the program, including a future AI session with no context. Section spec:
   `resources/developer-index-spec.md`.
3. **AI context primer (optional, recommended for future-session work)** — a one-page fast
   orientation. Produce it when the user wants quick future-session onboarding, not a full rebuild
   reference. Spec lives at the bottom of `resources/agent-prompts.md`.

## When to use

- A program, app, feature, or script collection was just built or substantially changed and the
  user wants it documented.
- The user asks for "the two guides", a user guide, a developer index / technical reference, an
  onboarding doc, or durable context for future sessions.

## When NOT to use

- A throwaway snippet or a single tiny script (a header comment is enough).
- The user wants only ONE of the two; then run just that half.

## The pipeline (follow in order)

**0. Scope it.** Identify the project root, the actual source files to document (list them
explicitly), the tech stack, and where the outputs go. Default output location: a `docs/` folder
in the project, or alongside the code (for a single-folder tool, next to it). If the location is
ambiguous, ask once. Note any standing constraints (voice rules, things that must not be named).

**1. Author both in parallel.** The two guides are independent, so spawn BOTH agents in the same
batch. Each MUST read the real source files for exactness (do not let them work from your summary
alone). Use the fill-in templates in `resources/agent-prompts.md`:
- Agent A: a design-capable agent (e.g. a designer subagent) builds the user guide HTML. Pass the
  voice rules and the user-guide spec.
- Agent B: a strong technical writer (opus tier) builds the developer index. Pass the
  developer-index spec and tell it to quote real identifiers, not invent.

**2. Verify the developer index against the real code.** This doc gets trusted by future sessions,
so accuracy is the bar. If you wrote the code, cross-check it yourself (paths, identifiers,
endpoints, option names, output filenames). If you did NOT write it, have a verifier that did not
author the doc read the key files and confirm. Fix every mismatch before shipping.

**3. Render and eyeball the infographic.** Screenshot the HTML headless and look at it. Confirm it
renders, looks professional, is self-contained, and the facts match. Fix layout or content issues.
Render command is below.

**4. (Optional) Produce the AI context primer** if the user wants future-session onboarding.

**5. Log it** if the user keeps a project tracker or shared memory: one line noting the guides
exist and where, so the next session finds them.

## Voice rules for the user guide (non-negotiable)

Plain human voice. Empathetic, neutral, confident. NO em dashes. NO arrows or checkmark/emoji
bullets. None of "leverage", "robust", "seamless", "unlock", or other AI-tell phrasing. Uneven
natural sentence rhythm. The file must be self-contained: inline CSS (and inline SVG if useful), no
CDN, no JS framework, no external assets, one scrollable page that opens by double-click. (The
developer index is technical and neutral; these voice rules are for the user guide.)

## Rendering the infographic to verify it

- Windows (Edge): `msedge --headless=new --disable-gpu --hide-scrollbars --screenshot="<out>.png" --window-size=1300,5200 "file:///<absolute-html-path-url-encoded>"`
- macOS/Linux: `chrome`/`chromium --headless --screenshot=<out>.png --window-size=1300,5200 "file://..."`, or `wkhtmltoimage in.html out.png`.
- Then open the PNG and read it. Do not delete files on protected or cloud-synced paths; the
  screenshot overwrites in place.

## Quality gates (do not finish until all hold)

- Developer index: every path, identifier, endpoint, and option is traceable to the real source
  (spot-checked, not assumed).
- User guide: renders cleanly, no em dashes, no AI tells, fully self-contained, includes a
  troubleshooting table and a safety/limits note where relevant.
- Both: a future session could pick up the project cold from these alone.

## Optional extra artifacts (advice to offer)

- **AI context primer** (recommended when future sessions will continue the work): one page, what
  the project is, where things live, how to run it, the next steps, and links to the two guides.
- **Quickstart cheat-sheet**: one page, only the daily-driver actions. Good for a tool the user
  operates often.
- **CHANGELOG**: only for a project that will keep evolving.
Keep the default to the two core guides. Add others only when asked or clearly useful; do not pad.

## Reference files

- `resources/user-guide-spec.md` — required sections + visual and voice rules for the infographic.
- `resources/developer-index-spec.md` — the full section structure for the technical reference.
- `resources/agent-prompts.md` — fill-in-the-blank prompt templates for Agent A, Agent B, and the
  optional primer.
