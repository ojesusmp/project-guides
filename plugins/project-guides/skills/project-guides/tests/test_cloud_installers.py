from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


def find_repository_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".github" / "workflows" / "codex-skill.yml").is_file():
            return candidate
    raise RuntimeError("repository root was not found")


ROOT = find_repository_root()
SKILL_ROOT = ROOT / "plugins" / "project-guides" / "skills" / "project-guides"
CLOUD_ROOT = ROOT / "integrations" / "codex-cloud"
SETUP_SCRIPT = CLOUD_ROOT / "setup.sh"
MAINTENANCE_SCRIPT = CLOUD_ROOT / "maintenance.sh"


@unittest.skipUnless(shutil.which("bash") and shutil.which("git"), "bash and git are required")
class CloudInstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="project guides ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.fixture_repository = self.root / "fixture repository"
        self.home = self.root / "home directory"
        self.cache = self.root / "cache directory"
        self.skills = self.home / ".agents" / "skills"
        self.fixture_skill = (
            self.fixture_repository / "plugins" / "project-guides" / "skills" / "project-guides"
        )

        shutil.copytree(
            SKILL_ROOT,
            self.fixture_skill,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        self.git("init")
        self.git("config", "user.email", "project-guides-tests@example.invalid")
        self.git("config", "user.name", "Project Guides Tests")
        self.git("add", ".")
        self.git("commit", "-m", "valid fixture")
        self.good_sha = self.git("rev-parse", "HEAD").stdout.strip()

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.fixture_repository,
            check=True,
            capture_output=True,
            text=True,
        )

    def run_installer(
        self,
        script: Path,
        ref: str | None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": self.home.as_posix(),
                "PROJECT_GUIDES_REPOSITORY": self.fixture_repository.as_posix(),
                "PROJECT_GUIDES_CACHE_DIR": self.cache.as_posix(),
                "PROJECT_GUIDES_SKILLS_DIR": self.skills.as_posix(),
            }
        )
        arguments = ["bash", script.as_posix()]
        if script == SETUP_SCRIPT:
            if ref is None:
                environment.pop("PROJECT_GUIDES_COMMIT", None)
            else:
                environment["PROJECT_GUIDES_COMMIT"] = ref
        else:
            environment.pop("PROJECT_GUIDES_COMMIT", None)
            if ref is not None:
                arguments.append(ref)
        return subprocess.run(
            arguments,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )

    @property
    def active_skill(self) -> Path:
        return self.skills / "project-guides"

    def test_setup_is_idempotent_with_paths_containing_spaces(self) -> None:
        first = self.run_installer(SETUP_SCRIPT, self.good_sha)
        self.assertEqual(0, first.returncode, first.stdout + first.stderr)
        first_skill = (self.active_skill / "SKILL.md").read_bytes()

        second = self.run_installer(SETUP_SCRIPT, self.good_sha)
        self.assertEqual(0, second.returncode, second.stdout + second.stderr)
        self.assertEqual(first_skill, (self.active_skill / "SKILL.md").read_bytes())

    def test_setup_rejects_unrelated_existing_target(self) -> None:
        self.active_skill.mkdir(parents=True)
        sentinel = self.active_skill / "unrelated.txt"
        sentinel.write_text("do not replace", encoding="utf-8")

        result = self.run_installer(SETUP_SCRIPT, self.good_sha)

        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("do not replace", sentinel.read_text(encoding="utf-8"))

    def test_failed_maintenance_preserves_active_install(self) -> None:
        setup = self.run_installer(SETUP_SCRIPT, self.good_sha)
        self.assertEqual(0, setup.returncode, setup.stdout + setup.stderr)
        active_before = (self.active_skill / "SKILL.md").read_bytes()

        required_reference = self.fixture_skill / "references" / "user-guide-spec.md"
        required_reference.unlink()
        self.git("add", "-A")
        self.git("commit", "-m", "invalid fixture")
        bad_sha = self.git("rev-parse", "HEAD").stdout.strip()

        update = self.run_installer(MAINTENANCE_SCRIPT, bad_sha)

        self.assertNotEqual(0, update.returncode, update.stdout + update.stderr)
        self.assertEqual(active_before, (self.active_skill / "SKILL.md").read_bytes())
        self.assertTrue((self.active_skill / "references" / "user-guide-spec.md").is_file())

    def test_production_ref_must_be_a_full_commit_sha(self) -> None:
        for ref in (None, self.good_sha[:12], "main", "v1.0.0", "f" * 40):
            with self.subTest(ref=ref):
                result = self.run_installer(SETUP_SCRIPT, ref)
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertFalse(self.active_skill.exists())


if __name__ == "__main__":
    unittest.main()
