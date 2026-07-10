# User Guide Specification

Create one self-contained `GUIDE.html` for the person operating the project. Teach actual workflows, expected results, recovery steps, and boundaries without assuming development knowledge.

## Format

- Use semantic HTML with inline CSS. Optional inline SVG is allowed when it is passive and accessible.
- Do not use JavaScript, external files, CDNs, remote fonts, iframes, embeds, objects, event-handler attributes, or active URLs.
- Make the page responsive and print-friendly. Use visible focus styles when links are present and respect `prefers-reduced-motion` if animation is used.
- Use project-relative example paths and replace secrets with descriptive placeholders.
- Match an established project visual language when one exists. Otherwise choose a restrained palette with WCAG AA text contrast.
- Use a diagram, numbered flow, or compact visual model that clarifies how the real parts connect. Do not add decoration that obscures the workflow.

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
<!-- project-guides-fingerprint: {FINGERPRINT} -->
```

Omit a money/value workflow only when the project has none. For headless projects, replace the visual interface tour with commands, files, logs, and process lifecycle.

## Accuracy Gate

- Ground every command, path, feature name, state, output, and failure in inspected source.
- Do not invent controls, automation, guarantees, or integrations.
- Ensure the HTML parses, the required table and limits section exist, and the passive-content validator passes.
- Render desktop and narrow views when a renderer is available. A screenshot supplements source checks; it cannot prove textual accuracy or safety.
