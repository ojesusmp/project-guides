# Claude-to-Codex Behavior Parity

## Status and deletion gate

This inventory compares the Claude-era root package at revision `297bd49` with the Codex-native package that is being promoted to the canonical plugin skill.

- **Inventory status:** complete.
- **Canonical target:** `plugins/project-guides/skills/project-guides/` (migrated from `codex/project-guides/`).
- **Deletion gate:** do not remove the root `SKILL.md`, `resources/`, or `test/quiz.txt` until a reviewer records sign-off in the final section of this document.
- **Interpretation:** "retained" means the behavior remains required, not that the old wording or provider-specific mechanism remains.

## Source mapping

| Claude-era source | Canonical Codex destination | Disposition |
|---|---|---|
| `SKILL.md` | `plugins/project-guides/skills/project-guides/SKILL.md` | Rewritten for Codex while retaining the artifact, safety, verification, and bounded-repair contracts. |
| `resources/agent-prompts.md` | `plugins/project-guides/skills/project-guides/references/authoring-prompts.md` | Condensed into capability-based, staged-file prompts with the same trust boundary. |
| `resources/developer-index-spec.md` | `plugins/project-guides/skills/project-guides/references/developer-index-spec.md` | Retained with a stronger citation and failure-behavior contract. |
| `resources/user-guide-spec.md` | `plugins/project-guides/skills/project-guides/references/user-guide-spec.md` | Retained, including the v1.7 design direction, passive HTML, accessibility, voice, and accuracy rules. |
| `test/quiz.txt` | `scripts/validate_project_guides.py` and `tests/test_validate_project_guides.py` | Replaced by deterministic validation and unit tests; the Claude CLI quiz is intentionally retired. |

Paths in the evidence column name the pre-migration Codex location (`codex/project-guides/...`) so the comparison remains auditable against revision `297bd49`. Unqualified `references/`, `scripts/`, and `tests/` paths are relative to that directory. After promotion, the same relative files live below `plugins/project-guides/skills/project-guides/`.

## Claude-era evidence map

This map anchors the grouped guarantees below to every active Claude-era source section:

| Claude-era range | Guarantees covered below |
|---|---|
| `SKILL.md:12-38` | Default pair, optional primer, applicability, and half-pipeline behavior (rows 1-6). |
| `SKILL.md:40-59` | Capability roles, scaling, and the old provider/machine mappings (rows 16-19). |
| `SKILL.md:61-77` | Untrusted-source, secret, passive-content, and trusted-placeholder boundaries (rows 7-10 and 23). |
| `SKILL.md:79-143` | Scope, coverage, author retries, source verification, rendering, bounded fixes, primer verification, and tracker logging (rows 5-12, 16-20, 27-35). |
| `SKILL.md:145-183` | Single-artifact execution and staleness fingerprint behavior (rows 2 and 13-15). |
| `SKILL.md:185-243` | Voice, mechanical HTML checks, render completeness, reduced motion, safe paths, and locked-target handling (rows 23-31). |
| `SKILL.md:245-278` | Final quality assertions, optional extras, reference authority, and the Claude quiz gate (rows 20-27 and 33-38). |
| `resources/agent-prompts.md:1-140` | Trusted placeholders, parallel authors, output ownership, design contract, source accuracy, index citations, and optional-primer content (rows 3-4, 7-10, 16-26, and 32). |
| `resources/developer-index-spec.md:1-68` | Exact identifiers, project-relative paths, secret sanitation, the 13-section outline, citations, and repair budget (rows 9-10 and 20-22). |
| `resources/user-guide-spec.md:1-108` | Passive/offline format, infographic and design rules, voice, required operator content, accuracy, troubleshooting, and safety (rows 9-10 and 23-31). |
| `test/quiz.txt` | The provider-specific regression mechanism replaced in row 37. |

## Parity inventory

| # | Claude-era guarantee | Disposition | Canonical Codex behavior and evidence |
|---:|---|---|---|
| 1 | Produce `GUIDE.html` and `DEVELOPER-INDEX.md` as the default pair. | **Retained** | The Codex skill selects both by default and writes them under `docs/` (`codex/project-guides/SKILL.md:10-22`). |
| 2 | Allow a user to request only one guide and run only that artifact's authoring and verification path. | **Retained** | Artifact selection is explicit; a single requested artifact runs only its applicable stages (`codex/project-guides/SKILL.md:10-22`). |
| 3 | Offer `AI-CONTEXT.md` only as an optional third artifact. | **Retained** | The context primer is created only when explicitly requested (`codex/project-guides/SKILL.md:10-22`; `references/authoring-prompts.md:25-27`). |
| 4 | Skip a separate primer when the project uses the external `faro` convention and its `PROJECT.md`. | **Intentionally dropped** | `faro` is provider/ecosystem-specific and is not a dependency of the canonical skill. The general rule remains: do not create `AI-CONTEXT.md` unless requested, and do not invent work status (`references/authoring-prompts.md:25-27`). Existing project memory can be linked as inspected operator documentation rather than treated as a required integration. |
| 5 | Avoid generating guides for throwaway or unstable work unless the user explicitly wants current-state documentation. | **Changed** | The canonical trigger remains documentation of a project or substantial feature, but Codex follows the active user request and governing mode rather than embedding an interactive confirmation protocol (`codex/project-guides/SKILL.md:6-8,24-29`). Staleness is reported through the fingerprint contract. |
| 6 | Default output to `{PROJECT_ROOT}/docs`; do not write to the root without explicit authorization. | **Retained and simplified** | The Codex skill defaults to `docs/` and permits another location only when the user explicitly requests it and governing instructions allow it (`codex/project-guides/SKILL.md:10-22,24-29`). |
| 7 | Treat repository contents, including embedded AI instructions, as untrusted data rather than governing instructions. | **Retained and strengthened** | The active `AGENTS.md` and session instructions govern; target code, comments, docs, and configuration are data. Commands found in target files are not run merely because the files request them (`codex/project-guides/SKILL.md:24-37`; `references/authoring-prompts.md:3-7`). |
| 8 | Populate constraint/style placeholders only from trusted session or user context, not target-file prose. | **Retained** | Author prompts require placeholders from user/session context and independently verified facts, and prohibit copying untrusted target prose into `{CONSTRAINTS}` (`references/authoring-prompts.md:3-7`). |
| 9 | Never reproduce live secrets; document the setting with a placeholder. | **Retained and broadened** | Keys, tokens, passwords, cookies, private keys, recovery codes, and credentialed connection strings are prohibited; artifacts use placeholders and identify the configuration location (`codex/project-guides/SKILL.md:31-37`; both canonical specifications). |
| 10 | Use project-relative paths and avoid leaking absolute user-specific paths. | **Retained and mechanically enforced** | Both canonical specifications require project-relative paths, and the bundled validator rejects absolute user paths (`references/developer-index-spec.md:7-12`; `references/user-guide-spec.md:7-12`; `tests/test_validate_project_guides.py`). |
| 11 | Enumerate the real source explicitly, read every relevant file, split large scopes into bounded groups, and never silently omit coverage. | **Retained and clarified** | Scope uses read-only enumeration, excludes generated/vendor/cache/binary content by default, records unresolved coverage, and merges bounded groups (`codex/project-guides/SKILL.md:41-47`). |
| 12 | Inspect manifests, entry points, configuration, tests, and existing operator documentation before authoring. | **Retained** | These sources are named explicitly in the Codex scope stage (`codex/project-guides/SKILL.md:43-46`). |
| 13 | Compute one shared staleness fingerprint containing generation date, repository state, source count, and byte total. | **Retained and strengthened** | The Codex fingerprint adds a deterministic SHA-256 over ordered relative paths and exact bytes, so equal-size edits cannot appear current (`codex/project-guides/SKILL.md:49-63`; `tests/test_validate_project_guides.py:96-119`). |
| 14 | Distinguish `non-git` from `git-unavailable`, preserve the dirty marker, and compare existing fingerprints before regenerating. | **Retained** | Commit state remains `short commit`, `non-git`, or `git-unavailable`, with `-dirty`; current docs are not overwritten unless refresh was requested (`codex/project-guides/SKILL.md:47-63`). Generation time is correctly informational rather than a currentness field. |
| 15 | Compute the fingerprint once and embed the same value in every generated artifact. | **Retained** | One fingerprint is reused in all requested artifacts (`codex/project-guides/SKILL.md:49-63`; both canonical author prompts and specifications). |
| 16 | Prefer two independent authors that each inspect real source instead of relying on a shared summary. | **Retained with Codex-native routing** | When native subagents and capacity are available, guide and index authors run as bounded independent tasks and own disjoint staged files (`codex/project-guides/SKILL.md:65-75`). |
| 17 | Scale down safely when the project is small or agents are unavailable. | **Retained** | Direct authoring is allowed for small projects or unavailable subagents (`codex/project-guides/SKILL.md:73-75`). |
| 18 | Retry a malformed/failed author once, then author directly or report the artifact blocked. | **Retained** | An unusable author result receives one concrete retry before direct authoring or a blocked report (`codex/project-guides/SKILL.md:73-75`). |
| 19 | Route authors/verifiers by capability rather than scattering model names through the workflow. | **Retained and made provider-neutral** | The canonical skill inherits the active session model and never hardcodes model names (`codex/project-guides/SKILL.md:65-75`). The old Claude model aliases, `alfred`, and machine-specific router references are intentionally removed. |
| 20 | Verify the developer index against source, check every citation, and independently spot-check behavior plus validation/failure handling. | **Retained** | The verifier checks every `path:line` citation, at least one behavior claim, at least one validation/failure claim, applicable sections, secrets, and paths (`codex/project-guides/SKILL.md:77-87`; `references/developer-index-spec.md:36-46`). |
| 21 | Require an exhaustive but project-adapted developer index: architecture, versions, files, source reference, interfaces, config/data, processes, commands, security, modification recipes, and caveats. | **Retained and clarified** | The canonical 13-part outline preserves all surfaces and explicitly permits omission only when a surface is genuinely absent and the omission is reported (`references/developer-index-spec.md:14-34`). |
| 22 | Quote exact identifiers and versions, distinguish fact from inference, and do not fabricate missing surfaces. | **Retained and strengthened** | The canonical spec requires real identifiers, labels inference, documents side effects and failure behavior, and prohibits invented sections (`references/developer-index-spec.md:5-12,14-34`). |
| 23 | Produce a self-contained, offline, passive HTML guide with no script, handlers, active URLs, frames/embeds, or remote assets. | **Retained and mechanically strengthened** | The canonical spec keeps the passive HTML contract; the validator rejects active tags, handlers, navigation/submission constructs, external resource attributes, remote assets, and dangerous URL schemes (`codex/project-guides/SKILL.md:31-37,88-97`; `references/user-guide-spec.md:5-12`; validator unit tests). |
| 24 | Use a deliberate project-derived visual direction rather than generic styling. | **Retained** | The v1.7 direction contract remains: project-derived atmosphere, system-font typography, a committed `:root` palette, WCAG AA contrast, one radius, one motion token, reduced-motion handling, and print styling (`references/user-guide-spec.md:14-36`; `references/authoring-prompts.md:9-13`). |
| 25 | Use plain human voice and reject em dashes, arrow/emoji bullets, and promotional filler such as `leverage`, `robust`, `seamless`, and `unlock`. | **Retained** | The canonical guide specification keeps these exact voice constraints (`references/user-guide-spec.md:38-40`). |
| 26 | Cover setup, launch/stop, real controls or commands, features, configuration, an end-to-end task, timings/outputs, troubleshooting, and safety/limits. | **Retained** | The canonical guide preserves the operator content contract, including troubleshooting and a labeled safety/limits section (`references/user-guide-spec.md:42-60`). |
| 27 | Validate guide facts against source; a screenshot cannot prove textual accuracy or safety. | **Retained** | Commands, paths, states, outputs, limitations, and required sections are source-checked before visual inspection; rendering supplements rather than replaces validation (`codex/project-guides/SKILL.md:88-107`; `references/user-guide-spec.md:62-67`). |
| 28 | Bound repairs to two fix cycles per artifact and report remaining failures precisely. | **Retained** | The Codex skill defines the same repair-all-known-failures plus recheck cycle and caps it at two (`codex/project-guides/SKILL.md:95-97,99-107`). |
| 29 | Render the full guide, do not certify a truncated/blank capture, and report when visual verification is unavailable. | **Retained and broadened** | The canonical flow inspects desktop and narrow/mobile views, full-page/footer coverage, text fit, contrast, tables, and print behavior. If no renderer exists, it reports a verification gap rather than claiming visual success (`codex/project-guides/SKILL.md:99-107`). |
| 30 | Keep render paths shell-safe and encode local file URLs. | **Retained without machine-specific browser paths** | The canonical skill requires shell-safe paths and a properly encoded `file:///` URL but delegates browser discovery to available Codex/browser tools (`codex/project-guides/SKILL.md:101-107`). Hardcoded Windows browser locations are intentionally dropped as non-portable delivery detail. |
| 31 | Re-run the HTML gate after layout edits. | **Retained** | Every HTML repair re-runs the bundled validator (`codex/project-guides/SKILL.md:101-107`). |
| 32 | Never destroy the last known-good guide before replacement validation succeeds. | **Retained and strengthened** | Authors write same-directory staged artifacts; final files are promoted with same-filesystem atomic replace, with backups restored if any promotion fails (`codex/project-guides/SKILL.md:65-75,99-110`). |
| 33 | Cross-check shared commands, paths, names, and configuration between the two guides. | **Retained** | Shared facts are cross-checked when both artifacts are produced (`codex/project-guides/SKILL.md:95-97,132-137`). |
| 34 | Report artifact paths, source scope, verification outcomes, cleared false positives, visual gaps, unresolved coverage, and refresh/current status. | **Retained and formalized** | The Codex handoff contract enumerates these fields and forbids completion claims while required checks fail (`codex/project-guides/SKILL.md:111-130`). |
| 35 | Optionally log guide locations to an already-declared tracker, but do not hunt for one. | **Intentionally dropped** | Tracker mutation is outside the documentation-generation contract and can create unrelated writes. Governing project instructions may separately require logging; the canonical skill does not invent that side effect. |
| 36 | Suggest a quickstart or changelog when useful, without padding the default output. | **Intentionally dropped** | The canonical skill keeps exactly two default outputs plus the explicitly requested context primer. Extra deliverables require an ordinary user request rather than an embedded upsell. |
| 37 | Use an LLM quiz piped to `claude -p --model ...` as a regression gate. | **Replaced** | The provider-specific nondeterministic quiz is removed. A dependency-free validator and 11 unit tests cover package structure, passive HTML, active navigation/resources, secrets, user paths, citations, and fingerprint determinism (`scripts/validate_project_guides.py`; `tests/test_validate_project_guides.py`). |
| 38 | Preserve history even after the active Claude package is removed. | **Retained** | Git history and `CHANGELOG.md` preserve the Claude-era releases and the later Codex-native edition. This inventory records the migration decision; no second active workflow copy is retained. |

## Provider- and machine-specific removals

The following removals are intentional compatibility cleanup rather than lost product behavior:

- Claude CLI invocation (`claude -p`) and concrete Claude model flags.
- Named local agents such as `alfred`, provider tiers, and machine-specific routing plugins.
- Root `CLAUDE.md` terminology as a privileged workflow concept; target `CLAUDE.md`, `AGENTS.md`, and similar files remain untrusted project data unless they are governing instructions supplied by the active Codex environment.
- Hardcoded browser installation paths and shell-specific screenshot recipes.
- The LLM-scored `test/quiz.txt` gate.
- `faro`-specific primer suppression, tracker mutation, and unsolicited extra-artifact suggestions.

None of these removals weakens the canonical requirements for factual source coverage, passive output, secret sanitation, citations, bounded repair, render-gap reporting, or last-known-good preservation.

## Review checklist and sign-off

The reviewer must complete this section before the Claude-era active files are deleted.

- [ ] Every root `SKILL.md` guarantee is represented above as retained, changed, replaced, or intentionally dropped.
- [ ] Every behavior in `resources/agent-prompts.md`, `resources/developer-index-spec.md`, and `resources/user-guide-spec.md` has a canonical destination or an explicit removal rationale.
- [ ] The canonical package validator and all migrated unit tests pass.
- [ ] Exactly one tracked `SKILL.md` declares `name: project-guides` after migration.
- [ ] Root `SKILL.md`, `resources/`, and `test/quiz.txt` are removed only after this checklist is signed.

**Reviewer:** _pending_

**Review commit:** _pending_

**Date:** _pending_

**Verdict:** **PENDING**
