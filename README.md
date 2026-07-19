# project-guides

`project-guides` is a Codex-native skill that reads a real repository and creates verified project
documentation. By default it produces a self-contained operator guide at `docs/GUIDE.html` and a
cited maintainer reference at `docs/DEVELOPER-INDEX.md`. `docs/AI-CONTEXT.md` is opt-in.

Version: 2.0.0. See [CHANGELOG.md](CHANGELOG.md) for migration notes.

## Install for Codex

### Plugin from this repository

Add the repository marketplace, install the plugin, then start a new Codex session so discovery is
reloaded:

```bash
codex plugin marketplace add ojesusmp/project-guides
codex plugin add project-guides@project-guides
```

For local development, clone the repository and replace `ojesusmp/project-guides` in the first
command with the clone path. The marketplace entry resolves to
`plugins/project-guides`, which bundles the one canonical skill at
`plugins/project-guides/skills/project-guides`.

### Direct skill installation

For local experimentation without the plugin, ask Codex:

```text
Use $skill-installer to install project-guides from
https://github.com/ojesusmp/project-guides/tree/main/plugins/project-guides/skills/project-guides
```

Pin a release or full commit SHA instead of `main` for a reproducible installation.

## Use it

Invoke `$project-guides`, or ask Codex to document a project, create a user guide, or build a
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
| Claude | Historical implementation | Retired from the active package after parity review; see `docs/migration/claude-to-codex-parity.md` |

The migration does not publish a plugin, change a Codex Cloud environment, or infer online support
from local validation.

## Package layout

```text
.agents/plugins/marketplace.json
plugins/project-guides/
  .codex-plugin/plugin.json
  skills/project-guides/
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
python plugins/project-guides/skills/project-guides/scripts/validate_project_guides.py
python -m unittest discover -s plugins/project-guides/skills/project-guides/tests -v
python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/project-guides
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/project-guides/skills/project-guides
python -m json.tool plugins/project-guides/.codex-plugin/plugin.json
python -m json.tool .agents/plugins/marketplace.json
bash -n integrations/codex-cloud/setup.sh integrations/codex-cloud/maintenance.sh
```

The Python package validator has no third-party dependencies. Optional browser rendering is used
only for visual inspection of generated `GUIDE.html` files.

## License

[MIT](LICENSE)
