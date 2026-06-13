# Developer index spec (the technical reference)

The developer index is an exhaustive Markdown reference for anyone modifying or rebuilding the
program, including a future AI session with no prior context. Accuracy is the first requirement:
every identifier is quoted from the real source, never inferred.

## Principles

- Read every relevant file. Quote real function names, variables, constants, route paths, config
  keys, and output filenames. If something is a known limitation, label it as such.
- Prefer tables for APIs, config schemas, and file trees.
- State versions and exact values, not "roughly" or "a number".

## Required sections (adapt to the project's nature)

1. **Overview and architecture.** What the program is, the core model in one paragraph, an ASCII
   architecture diagram, and the one or two load-bearing design principles.
2. **Tech stack and versions.** Every dependency with its version and why it is there. Build/run
   tooling and any compiler/runtime config, annotated.
3. **Full file tree** of every relevant directory, one-line purpose per file.
4. **Source reference, file by file.** For each source file: its exported types/interfaces (every
   field), every function (signature + behavior), and every module-level constant/variable.
5. **Complete API / command reference** (if the program has one). One subsection per
   endpoint/command: method/usage, params, request body shape, success response shape (with a
   realistic example), and every error/status code. Note any asymmetries.
6. **Frontend / UI reference** (if applicable): element ids, the client functions, and the
   update/polling model.
7. **Configuration reference.** Every config file and option (type, meaning, how to change it), and
   the full schema of any data the program reads or writes, including the exact current values and
   the validation rules enforced.
8. **External scripts / subprocess reference** (if the program drives other scripts or binaries):
   one subsection each covering purpose, key constants, functions, inputs (args, env, config it
   reads), exact output paths and filename patterns (fixed vs generated), runtime notes, and
   dependencies.
9. **Launch and run flow.** The exact chain from start command to running, plus the manual
   commands (install, start, type-check/test).
10. **Security model.** Network binding, any access guards, secret handling, and the auth posture
    (and why, if "none by design").
11. **How to modify (cookbook).** Concrete recipes for the common changes (change a setting, add a
    new unit/route/script, wire a deferred feature), naming the exact files and lines/identifiers.
12. **Known caveats and limitations.** Every sharp edge: in-memory vs persisted state, crash
    recovery, concurrency limits, platform quirks, placeholder values that must be replaced, and
    anything that surprised the author.
13. **Footer / durable context.** State that the document is durable context for future sessions,
    and point to companion files (the user guide, any plan/ADR, any project memory or tracker).

## Verification (the orchestrator does this after the agent finishes)

Spot-check the produced index against the real source: pick several paths, identifiers, endpoints,
option names, and output filenames and confirm each exists exactly as documented. Fix any
mismatch. If you did not author the code, use a verifier that did not author the doc.
