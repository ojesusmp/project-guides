from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path


def find_repository_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".github" / "workflows" / "codex-skill.yml").is_file():
            return candidate
    raise RuntimeError("repository root was not found")


ROOT = find_repository_root()
PLUGIN_ROOT = ROOT / "plugins" / "project-guides"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "project-guides"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"

SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
FRONTMATTER_NAME_PATTERN = re.compile(
    r"\A---\r?\n(?:(?!\r?\n---\r?\n).)*?^name:\s*['\"]?project-guides['\"]?\s*$",
    re.MULTILINE | re.DOTALL,
)
FORBIDDEN_ACTIVE_PATTERNS = {
    "Claude CLI dependency": re.compile(r"\bclaude\s+(?:-p|--print)\b", re.IGNORECASE),
    "hardcoded model flag": re.compile(r"--model(?:=|\s)", re.IGNORECASE),
    "machine-specific MCP tool": re.compile(r"\bmcp__[a-z0-9_]+", re.IGNORECASE),
    "active HTML": re.compile(r"<(?:script|iframe|object|embed|form)\b", re.IGNORECASE),
    "remote HTML asset": re.compile(
        r"<(?:img|link|script|source)\b[^>]*(?:src|href)\s*=\s*['\"]https?://",
        re.IGNORECASE,
    ),
    "remote CSS asset": re.compile(r"url\(\s*['\"]?https?://", re.IGNORECASE),
    "secret-shaped value": re.compile(
        r"(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|"
        r"github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})"
    ),
    "absolute user path": re.compile(
        r"(?:[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/](?!<)[^\\/\s]+[\\/]"
        r"|/(?:home|Users)/(?!<)[^/\s]+/)",
        re.IGNORECASE,
    ),
}
PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:TODO|TBD|Local developer|plugin scaffold|Help me use Project Guides)\b",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def tracked_files(pattern: str) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--", pattern],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


class RepositoryContractTests(unittest.TestCase):
    def test_plugin_manifest_identifies_canonical_skill(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(PLUGIN_ROOT.name, manifest.get("name"))
        self.assertRegex(str(manifest.get("version", "")), SEMVER_PATTERN)

        author = manifest.get("author")
        author_name = author.get("name") if isinstance(author, dict) else author
        self.assertEqual("ojesusmp", author_name)
        self.assertEqual("MIT", manifest.get("license"))

        skills = manifest.get("skills")
        skill_entries = [skills] if isinstance(skills, str) else skills
        self.assertIsInstance(skill_entries, list)
        resolved_skills: list[Path] = []
        for entry in skill_entries or []:
            candidate = (PLUGIN_ROOT / str(entry)).resolve()
            if candidate.is_dir() and candidate.name == "skills":
                resolved_skills.extend(path.resolve() for path in candidate.iterdir() if path.is_dir())
            else:
                resolved_skills.append(candidate)
        self.assertIn(SKILL_ROOT.resolve(), resolved_skills)
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertIsNotNone(manifest.get("repository"))

        serialized = json.dumps(manifest, sort_keys=True)
        self.assertIsNone(PLACEHOLDER_PATTERN.search(serialized), serialized)

    def test_marketplace_resolves_to_plugin(self) -> None:
        marketplace = load_json(MARKETPLACE_PATH)
        plugins = marketplace.get("plugins")
        self.assertIsInstance(plugins, list)
        entry = next(
            (item for item in plugins or [] if isinstance(item, dict) and item.get("name") == "project-guides"),
            None,
        )
        self.assertIsNotNone(entry)
        assert entry is not None

        source = entry.get("source")
        if isinstance(source, str):
            source_path = source
        elif isinstance(source, dict):
            self.assertEqual("local", source.get("source"))
            source_path = source.get("path")
        else:
            self.fail("marketplace source must be a path or local source object")
        self.assertIsInstance(source_path, str)
        self.assertEqual(PLUGIN_ROOT.resolve(), (ROOT / str(source_path)).resolve())

        policy = entry.get("policy")
        self.assertIsInstance(policy, dict)
        self.assertIn("installation", policy)
        self.assertIn("authentication", policy)
        self.assertTrue(entry.get("category"))
        self.assertIsNone(PLACEHOLDER_PATTERN.search(json.dumps(entry, sort_keys=True)))

    def test_only_one_active_project_guides_skill_is_tracked(self) -> None:
        declarations: list[Path] = []
        for path in tracked_files("*SKILL.md"):
            text = path.read_text(encoding="utf-8")
            if FRONTMATTER_NAME_PATTERN.search(text):
                declarations.append(path.resolve())
        self.assertEqual([SKILL_ROOT.joinpath("SKILL.md").resolve()], declarations)

    def test_legacy_codex_package_has_no_tracked_files(self) -> None:
        self.assertEqual([], tracked_files("codex/project-guides/**"))

    def test_temporary_smoke_and_bytecode_artifacts_are_not_tracked(self) -> None:
        self.assertEqual([], tracked_files(".tmp-cloud-smoke/**"))
        self.assertEqual([], tracked_files("*__pycache__/*"))
        self.assertEqual([], tracked_files("*.py[co]"))

    def test_active_package_has_no_provider_or_safety_regressions(self) -> None:
        failures: list[str] = []
        for path in sorted(SKILL_ROOT.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".py", ".sh"}:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in FORBIDDEN_ACTIVE_PATTERNS.items():
                if pattern.search(text):
                    failures.append(f"{path.relative_to(ROOT)}: {label}")
        self.assertEqual([], failures)

    @unittest.skipUnless(shutil.which("bash"), "bash is required for shell syntax checks")
    def test_cloud_scripts_have_valid_shell_syntax(self) -> None:
        scripts = [
            ROOT / "integrations" / "codex-cloud" / "setup.sh",
            ROOT / "integrations" / "codex-cloud" / "maintenance.sh",
        ]
        for script in scripts:
            self.assertTrue(script.is_file(), f"missing cloud script: {script.relative_to(ROOT)}")
        result = subprocess.run(
            ["bash", "-n", *(script.as_posix() for script in scripts)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_cloud_scripts_avoid_pipe_to_shell_and_unsafe_refs(self) -> None:
        scripts = [
            ROOT / "integrations" / "codex-cloud" / "setup.sh",
            ROOT / "integrations" / "codex-cloud" / "maintenance.sh",
        ]
        text = "\n".join(script.read_text(encoding="utf-8") for script in scripts)
        self.assertNotRegex(text, r"(?:curl|wget)[^\n|]*\|\s*(?:ba)?sh\b")
        self.assertNotRegex(text, r"git\s+(?:clone|checkout|switch)[^\n]*(?:\bmain\b|\bmaster\b)")
        self.assertIn("PROJECT_GUIDES_COMMIT", text)


if __name__ == "__main__":
    unittest.main()
