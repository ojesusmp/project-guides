# codex-guides

> **OpenAI Codex only.** Install this package in Codex skill/plugin locations. Do not install it in
> `.claude/skills`, and do not treat it as a generic ChatGPT custom GPT. A Claude edition must live
> in a separately named package such as `project-guides-claude`.

`codex-guides` is a Codex-native skill that reads a real repository and creates verified project
documentation. By default it produces a self-contained operator guide at `docs/GUIDE.html` and a
cited maintainer reference at `docs/DEVELOPER-INDEX.md`. `docs/AI-CONTEXT.md` is opt-in.

Version: 3.0.0. See [CHANGELOG.md](CHANGELOG.md) for migration notes.

## Install for Codex

### Plugin from this repository

Add the repository marketplace, install the plugin, then start a new Codex session so discovery is
reloaded:

```bash
codex plugin marketplace add ojesusmp/codex-guides
codex plugin add codex-guides@codex-guides
```

For local development, clone the repository and replace `ojesusmp/codex-guides` in the first
command with the clone path. The marketplace entry resolves to
`plugins/codex-guides`, which bundles the one canonical skill at
`plugins/codex-guides/skills/codex-guides`.

### Direct skill installation

For local experimentation without the plugin, ask Codex:

```text
Use $skill-installer to install codex-guides from
https://github.com/ojesusmp/codex-guides/tree/main/plugins/codex-guides/skills/codex-guides
```

Pin a release or full commit SHA instead of `main` for a reproducible installation.

## Use it

Invoke `$codex-guides`, or ask Codex to document a project, create a user guide, or build a
developer index. A single-artifact request runs only the matching half-pipeline. The skill:

1. scopes and fingerprints the source repository;
2. authors requested artifacts independently when agent capacity is available;
3. verifies facts and citations against source;
4. validates passive, self-contained HTML and scans for secrets and user-specific paths;
5. renders the staged HTML when a browser is available; and
6. promotes outputs only after the requested checks pass.

If browser rendering is unavailable, the skill reports that verification gap rather than claiming
visual verification. Agent-phase internet is not required.

## Delivery and verification status

| Surface | Delivery path | Status |
|---|---|---|
| Codex CLI, app, and IDE | Repository plugin or direct skill | Package validation and local tests are the merge gate |
| Work mode on web or desktop | Installed, shared, or published plugin through a supported workspace path | End-to-end workspace smoke pending; the repo marketplace alone does not prove web availability |
| Codex Cloud | Environment bootstrap in [`integrations/codex-cloud`](integrations/codex-cloud/README.md) | Bootstrap documented; end-to-end smoke pending because no environment ID is available |
| Claude Code, Claude Desktop, and claude.ai | Not supported | Use a separately named Claude package; never copy this package into `.claude/skills` |
| Generic ChatGPT chats/custom GPTs | Not a direct install target | This package requires a Codex skill or plugin runtime |

The migration does not publish a plugin, change a Codex Cloud environment, or infer online support
from local validation.

## Package layout

```text
.agents/plugins/marketplace.json
plugins/codex-guides/
  .codex-plugin/plugin.json
  skills/codex-guides/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
    tests/
integrations/codex-cloud/
  README.md
  setup.sh
  maintenance.sh
```

## Validate

From the repository root:

```bash
python plugins/codex-guides/skills/codex-guides/scripts/validate_codex_guides.py
python -m unittest discover -s plugins/codex-guides/skills/codex-guides/tests -v
python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-guides
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/codex-guides/skills/codex-guides
python -m json.tool plugins/codex-guides/.codex-plugin/plugin.json
python -m json.tool .agents/plugins/marketplace.json
bash -n integrations/codex-cloud/setup.sh integrations/codex-cloud/maintenance.sh
```

The Python package validator has no third-party dependencies. Optional browser rendering is used
only for visual inspection of generated `GUIDE.html` files.

## License

[MIT](LICENSE)
