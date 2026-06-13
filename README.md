# project-guides

A reusable skill that documents any finished program, app, feature, or toolkit by producing a
matched pair of guides, the same way every time.

## What it makes

1. **GUIDE.html** — a visual, self-contained infographic user guide in plain human voice. For the
   operator: learn it, know what to expect, troubleshoot.
2. **DEVELOPER-INDEX.md** — an exhaustive technical reference (files, paths, variables, functions,
   endpoints, options, script internals) good enough to modify or rebuild from scratch, by a person
   or a future AI session.
3. **AI-CONTEXT.md** (optional) — a one-page fast orientation for a fresh session.

## How it works

It runs a fixed pipeline: scope the project, spawn two agents in parallel that READ the real source
for exactness (a designer for the HTML, a technical writer for the index), verify the technical doc
against the actual code, render the infographic headless and eyeball it, then optionally add the
primer and log where the guides live.

## Use it

Say `/project-guides`, or just ask to "document this project", for "the two guides", a "user guide",
or a "developer index". The skill carries the section specs and the agent prompt templates so the
output is consistent across projects.

## Files

- `SKILL.md` — the pipeline, when to use, voice rules, render command, quality gates.
- `resources/user-guide-spec.md` — required sections + visual/voice rules for the infographic.
- `resources/developer-index-spec.md` — the full section structure for the technical reference.
- `resources/agent-prompts.md` — fill-in-the-blank prompts for both agents and the optional primer.
