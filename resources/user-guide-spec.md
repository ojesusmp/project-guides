# User guide spec (the infographic HTML)

The user guide is one self-contained HTML page for the person who OPERATES the program. It teaches,
sets expectations, and troubleshoots. It is visual, not a wall of text.

## Format and visual rules

- One self-contained `.html` file. Inline CSS, optional inline SVG. No CDN, no JS framework, no
  external assets. Opens by double-click. One scrollable page.
- Genuine infographic: colored section cards, numbered steps, at least one simple flow diagram,
  and a troubleshooting table. Clean, modern, readable. A print-friendly `@media print` block is a
  nice touch.
- Match the house style if the project already has one (read any existing manual for palette/tone).

## Voice rules (non-negotiable)

Plain human voice. Empathetic, neutral, confident. NO em dashes. NO arrows or checkmark/emoji
bullets (use plain dots or numbered circles). None of "leverage", "robust", "seamless", "unlock",
or AI-tell phrasing. Natural, uneven sentence rhythm.

## Required sections (adapt names to the project)

1. **The big picture.** One small diagram of how the parts connect, one sentence each.
2. **First-time setup and launch.** Exact steps to start it, what the first run looks like, what is
   normal, how to stop it. Name prerequisites.
3. **The screen / interface explained.** Every region the operator sees, what each control does,
   what the status indicators mean.
4. **Each major feature or component, one block each.** What it does, what to expect, where its
   output goes, and any gotcha. Use the real names from the code.
5. **Any configuration the operator edits, explained field by field**, using a real loaded example.
   Include a short "how to figure out X" tip where a step needs judgment.
6. **The money/value workflow** if there is one (the path from action to the result that matters).
7. **A typical end-to-end task** ("when X happens, do these steps").
8. **What to expect.** Timings, where files land, fixed vs variable outputs.
9. **A troubleshooting TABLE.** Columns: problem, what it means, fix. Cover the realistic failures
   (will not start, nothing happens, an error appears, a dependency missing, a save/lock issue, a
   long run that looks frozen, a port or path problem).
10. **Safety / limits box.** What it does and does not do, privacy/exposure, secrets handling, and
    any domain constraints the operator must respect.
11. **Footer line** noting the guide is also usable as context for a future session.

## Accuracy

The authoring agent MUST read the real source so names, paths, outputs, and behavior are correct.
Do not invent features. Validate the HTML is well-formed (balanced tags) before finishing.
