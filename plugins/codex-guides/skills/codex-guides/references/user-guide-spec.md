# User Guide Specification

Create one self-contained `GUIDE.html` for the person operating the project. Teach actual workflows, expected results, recovery steps, and boundaries without assuming development knowledge.

## Format

- Use semantic HTML with inline CSS. Optional inline SVG is allowed when it is passive and accessible.
- Do not use JavaScript, external files, CDNs, remote fonts, iframes, embeds, objects, event-handler attributes, or active URLs.
- Make the page responsive and print-friendly. Use visible focus styles when links are present and respect `prefers-reduced-motion` if animation is used.
- Use project-relative example paths and replace secrets with descriptive placeholders.
- Match an established project visual language when one exists. Otherwise follow the Design Direction below.
- Use a diagram, numbered flow, or compact visual model that clarifies how the real parts connect. Do not add decoration that obscures the workflow.

## Design Direction

"Clean, modern, readable" is the absence of a direction and produces generic guides. Before writing markup, commit to a direction derived from what the tool is (a backup tool is a field manual, a dashboard is an instrument panel) and hold it consistently: atmosphere, palette, type, one radius, one motion timing, and what the design will not do.

- Typography: distinctive SYSTEM-font stacks only. The file is offline, so no web fonts, no `@import`, no font links. Never leave the visible display face as Inter, Roboto, Arial, Helvetica, or `system-ui`. A strong display face, a readable body face, and a monospace for commands.
- Color: a committed palette as CSS variables in one `:root`, a tonal ramp plus at most one accent, not a timid even gray. Body text on its background clears WCAG AA 4.5:1. No hex values outside `:root`.
- One radius token and one transition duration+easing token, used everywhere.
- Motion: at most one CSS-only page-load reveal. It must resolve to full visibility under `prefers-reduced-motion` (renderers screenshot that state, so an entrance starting at `opacity:0` would otherwise capture blank). Include a print block that flattens to ink-on-white.

Proven default when the project has no house style: toned technical paper, dense ink, one signal accent; a DIN-like condensed display face, a book serif, monospace commands. Tokens:

```css
:root{
  --paper:#F2EFE6; --paper-deep:#E4DFD0; --stone:#9A9382; --field:#4A463C; --ink:#23211B;
  --signal:#A63C0D;                 /* one accent, 5.6:1 on paper */
  --radius:2px; --speed:200ms; --ease:cubic-bezier(0.33,0,0.2,1);
  --font-display:Bahnschrift,'DIN Alternate','Franklin Gothic Medium','Nimbus Sans Narrow',sans-serif;
  --font-text:Charter,'Bitstream Charter','Sitka Text',Cambria,Georgia,serif;
  --font-mono:'Cascadia Mono','Segoe UI Mono',Consolas,'SF Mono',Menlo,monospace;
}
```

Body `--ink` on `--paper` is 13.7:1 (AA clear). Adapt per project; do not make every guide identical.

## Voice

Use plain, direct, human language. Avoid em dashes, arrows as bullets, emoji bullets, and promotional filler. Do not use the words `leverage`, `robust`, `seamless`, or `unlock`. State uncertainty and limitations explicitly.

## Required Content

1. Purpose and a small system/workflow diagram.
2. Prerequisites, first setup, exact launch steps, normal first-run state, and shutdown.
3. Interface or command-line tour, including controls, status indicators, inputs, outputs, and logs that actually exist.
4. One block for each major feature: purpose, action, result location, timing, and caveat.
5. Operator-editable configuration, field by field, with a sanitized real-shaped example and validation rules.
6. A representative end-to-end task.
7. Expected timings and fixed versus variable outputs.
8. A troubleshooting table with problem, meaning, evidence to inspect, and fix.
9. A clearly labeled safety and limits section covering privacy, secrets, network exposure, destructive actions, and domain-specific constraints.
10. A footer saying the guide can orient a future session.
11. An HTML fingerprint comment in this exact shape:

```html
<!-- codex-guides-fingerprint: {FINGERPRINT} -->
```

Omit a money/value workflow only when the project has none. For headless projects, replace the visual interface tour with commands, files, logs, and process lifecycle.

## Accuracy Gate

- Ground every command, path, feature name, state, output, and failure in inspected source.
- Do not invent controls, automation, guarantees, or integrations.
- Ensure the HTML parses, the required table and limits section exist, and the passive-content validator passes.
- Render desktop and narrow views when a renderer is available. A screenshot supplements source checks; it cannot prove textual accuracy or safety.
