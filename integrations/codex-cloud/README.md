# Codex Cloud bootstrap

This adapter installs the same canonical skill shipped by the repository plugin. It does not carry
a separate cloud workflow. Run it in the environment setup phase, where network access is allowed,
then keep agent-phase internet disabled.

## Production setup

Choose and review a repository commit, then record its complete 40-character SHA in the Codex Cloud
environment setup command:

```bash
export PROJECT_GUIDES_COMMIT=0123456789abcdef0123456789abcdef01234567
bash integrations/codex-cloud/setup.sh
```

`setup.sh` stages that exact commit, runs the bundled package validator, and activates the validated
skill at `$HOME/.agents/skills/project-guides`. Activation uses an installer-owned symlink and does
not replace an unrelated file or directory. A failed fetch or validation leaves the previous active
installation untouched. Re-running setup for the same commit validates the active copy and exits
successfully.

The default source is `https://github.com/ojesusmp/project-guides.git`. Set
`PROJECT_GUIDES_REPOSITORY` only when testing a trusted fork. Set `PROJECT_GUIDES_CACHE_DIR` or
`PROJECT_GUIDES_SKILLS_DIR` when the environment requires different cache or discovery locations.

## Maintenance

Update only to another reviewed full commit SHA:

```bash
bash integrations/codex-cloud/maintenance.sh fedcba9876543210fedcba9876543210fedcba98
```

Using a moving branch is unsafe for production. For an explicitly temporary development environment,
`main` may be resolved and recorded as a full SHA with:

```bash
PROJECT_GUIDES_ALLOW_DEVELOPMENT_REF=1 \
  bash integrations/codex-cloud/maintenance.sh main
```

## Smoke task

Start a fresh task after setup, disable agent internet, and use this prompt against a small fixture
repository:

```text
Use $project-guides to create only docs/DEVELOPER-INDEX.md. Verify every citation and report the
source fingerprint and all skipped checks.
```

Confirm the task diff contains only the expected documentation output. Repeat setup with the same
SHA, then try an invalid candidate and confirm the prior skill remains active.

Codex Cloud support is currently **bootstrap documented; end-to-end smoke pending**. No environment
was created or changed as part of this repository migration, and no environment ID is recorded yet.
