from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_codex_guides.py"
SPEC = importlib.util.spec_from_file_location("codex_guides_validator", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


VALID_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><style>body { color: #111; }</style></head>
<body><main><h1>Tool guide</h1><section><h2>Problem solving</h2>
<table><tr><th>Problem</th><th>Fix</th></tr><tr><td>No output</td><td>Read the log.</td></tr></table>
</section><section><h2>Safety and limits</h2><p>Keep credentials private.</p></section></main>
<!-- codex-guides-fingerprint: generated=2026-01-01; commit=abc123; sources=1; bytes=10 -->
</body></html>"""


class ValidatorTests(unittest.TestCase):
    def write_temp(self, name: str, content: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        path = directory / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_html_passes(self) -> None:
        path = self.write_temp("GUIDE.html", VALID_HTML)
        self.assertEqual([], VALIDATOR.validate_html(path))

    def test_active_content_fails(self) -> None:
        path = self.write_temp("GUIDE.html", VALID_HTML.replace("</main>", "<script>alert(1)</script></main>"))
        self.assertTrue(any("active tag" in error for error in VALIDATOR.validate_html(path)))

    def test_event_handler_fails(self) -> None:
        path = self.write_temp("GUIDE.html", VALID_HTML.replace("<main>", '<main onclick="run()">'))
        self.assertTrue(any("event-handler" in error for error in VALIDATOR.validate_html(path)))

    def test_external_asset_fails(self) -> None:
        path = self.write_temp("GUIDE.html", VALID_HTML.replace("<main>", '<main><img src="https://example.test/a.png">'))
        self.assertTrue(any("external resource" in error for error in VALIDATOR.validate_html(path)))

    def test_active_navigation_and_resource_attributes_fail(self) -> None:
        payloads = (
            '<meta http-equiv="refresh" content="0;url=https://example.test">',
            '<img srcset="https://example.test/a.png 1x">',
            '<svg><use href="https://example.test/icons.svg#x"></use></svg>',
            '<form action="https://example.test/collect"></form>',
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                path = self.write_temp("GUIDE.html", VALID_HTML.replace("<main>", f"{payload}<main>"))
                self.assertTrue(VALIDATOR.validate_html(path))

    def test_secret_fails(self) -> None:
        token = "sk-" + ("a" * 24)
        path = self.write_temp("GUIDE.html", VALID_HTML.replace("Keep credentials private.", token))
        self.assertTrue(any("secret" in error for error in VALIDATOR.validate_html(path)))

    def test_additional_secret_and_user_paths_fail(self) -> None:
        payloads = (
            "github_pat_" + ("a" * 30),
            "C:/Users/alice/project/config.json",
            "/Users/alice/project/config.json",
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                path = self.write_temp("GUIDE.html", VALID_HTML.replace("Keep credentials private.", payload))
                self.assertTrue(VALIDATOR.validate_html(path))

    def test_citations_accept_valid_relative_line(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / "app.py"
        source.write_text("one\ntwo\n", encoding="utf-8")
        citations = root / "citations.txt"
        citations.write_text("Entry point -> app.py:2\n", encoding="utf-8")
        self.assertEqual([], VALIDATOR.validate_citations(citations, root))

    def test_citations_reject_escape(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        citations = root / "citations.txt"
        citations.write_text("Bad -> ../outside.py:1\n", encoding="utf-8")
        self.assertTrue(any("escapes" in error for error in VALIDATOR.validate_citations(citations, root)))

    def test_fingerprint_detects_equal_byte_content_changes(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / "app.py"
        source.write_text("alpha", encoding="utf-8")
        first = VALIDATOR.compute_source_fingerprint(root, [Path("app.py")])
        source.write_text("bravo", encoding="utf-8")
        second = VALIDATOR.compute_source_fingerprint(root, [Path("app.py")])
        self.assertEqual(first[:2], second[:2])
        self.assertNotEqual(first[2], second[2])

    def test_fingerprint_is_path_order_independent(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "a.txt").write_text("a", encoding="utf-8")
        (root / "b.txt").write_text("b", encoding="utf-8")
        first = VALIDATOR.compute_source_fingerprint(root, [Path("a.txt"), Path("b.txt")])
        second = VALIDATOR.compute_source_fingerprint(root, [Path("b.txt"), Path("a.txt")])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
