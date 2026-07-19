#!/usr/bin/env python3
"""Deterministic validation for the Codex Guides skill and its outputs."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/user-guide-spec.md",
    "references/developer-index-spec.md",
    "references/authoring-prompts.md",
    "scripts/validate_codex_guides.py",
)

FORBIDDEN_PACKAGE_PATTERNS = {
    "unfinished placeholder": re.compile(r"\bTODO\b|\[TODO", re.IGNORECASE),
    "Claude CLI dependency": re.compile(r"\bclaude\s+(?:-p|--print)\b", re.IGNORECASE),
    "hardcoded model flag": re.compile(r"--model(?:=|\s)", re.IGNORECASE),
    "machine-specific MCP tool": re.compile(r"\bmcp__[a-z0-9_]+", re.IGNORECASE),
}

ACTIVE_TAGS = {"script", "iframe", "object", "embed", "base", "form"}
URL_ATTRIBUTES = {
    "action",
    "background",
    "formaction",
    "href",
    "longdesc",
    "manifest",
    "ping",
    "poster",
    "profile",
    "src",
    "xlink:href",
}
VOICE_PATTERN = re.compile(r"\u2013|\u2014|\u2015|&(?:mdash|ndash);|\b(?:leverage|robust|seamless|unlock)\b", re.IGNORECASE)
HTML_TEXT_ACTIVE_PATTERN = re.compile(
    r"srcdoc|data\s*:\s*text/html|javascript\s*:|&#x?0*106;?avascript",
    re.IGNORECASE,
)
SECRET_PATTERN = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|"
    r"github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{20,}|AIza[A-Za-z0-9_-]{30,}|"
    r"sk_(?:live|test)_[A-Za-z0-9]{20,}|"
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{20,})"
)
ABSOLUTE_USER_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/](?!<)[^\\/\s]+[\\/]"
    r"|/(?:home|Users)/(?!<)[^/\s]+/)",
    re.IGNORECASE,
)
FINGERPRINT_PATTERN = re.compile(r"codex-guides-fingerprint\s*:", re.IGNORECASE)


class PassiveHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.errors: list[str] = []
        self.tags: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.tags.add(tag)
        if tag in ACTIVE_TAGS:
            self.errors.append(f"active tag <{tag}> is forbidden")
        if tag == "link":
            self.errors.append("external stylesheet/link tags are forbidden")
        attributes = {name.lower(): value or "" for name, value in attrs}
        if tag == "meta" and attributes.get("http-equiv", "").lower() == "refresh":
            self.errors.append("meta refresh is forbidden")
        for raw_name, raw_value in attrs:
            name = raw_name.lower()
            value = raw_value or ""
            if name.startswith("on"):
                self.errors.append(f"event-handler attribute {name}= is forbidden")
            if name == "srcdoc":
                self.errors.append("srcdoc is forbidden")
            if name == "srcset":
                self.errors.append("srcset is forbidden in a self-contained guide")
            if name in URL_ATTRIBUTES and value:
                is_anchor_link = tag == "a" and name == "href" and re.match(
                    r"\s*(?:#|https?://|mailto:|tel:)", value, re.IGNORECASE
                )
                is_fragment_reference = name in {"href", "xlink:href"} and value.lstrip().startswith("#")
                is_embedded_image = name in {"src", "poster"} and re.match(
                    r"\s*data:image/(?:png|jpeg|gif|webp);base64,", value, re.IGNORECASE
                )
                if not (is_anchor_link or is_fragment_reference or is_embedded_image):
                    self.errors.append(f"external resource in {name}= is forbidden: {value[:80]}")
            if re.search(r"javascript\s*:|data\s*:\s*text/html", value, re.IGNORECASE):
                self.errors.append(f"active URL in {name}= is forbidden")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields, text[match.end() :]


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return errors
    skill_text = skill_path.read_text(encoding="utf-8")
    try:
        fields, body = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        fields, body = {}, skill_text

    if set(fields) != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")
    if fields.get("name") != root.name:
        errors.append(f"skill name must match folder name {root.name!r}")
    if len(fields.get("description", "")) < 80:
        errors.append("skill description must explain capability and trigger contexts")
    if len(body.splitlines()) > 500:
        errors.append("SKILL.md body exceeds the 500-line progressive-disclosure limit")

    package_files = [
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".yaml"}
    ]
    package_text = "\n".join(path.read_text(encoding="utf-8") for path in package_files)
    for label, pattern in FORBIDDEN_PACKAGE_PATTERNS.items():
        if pattern.search(package_text):
            errors.append(f"{label} found in Codex skill subtree")

    for reference in (
        "references/user-guide-spec.md",
        "references/developer-index-spec.md",
        "references/authoring-prompts.md",
    ):
        if reference not in skill_text:
            errors.append(f"SKILL.md does not route to {reference}")

    metadata = root / "agents/openai.yaml"
    if metadata.is_file():
        metadata_text = metadata.read_text(encoding="utf-8")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in metadata_text:
                errors.append(f"agents/openai.yaml is missing {key}")
        if "$codex-guides" not in metadata_text:
            errors.append("agents/openai.yaml default_prompt must mention $codex-guides")

    return errors


def validate_html(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    parser = PassiveHTMLParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # HTMLParser failures should become actionable output.
        errors.append(f"HTML parser failed: {exc}")
    errors.extend(parser.errors)

    if "html" not in parser.tags or "body" not in parser.tags:
        errors.append("document must contain html and body elements")
    if "style" not in parser.tags:
        errors.append("self-contained guide must include inline style")
    if "table" not in parser.tags:
        errors.append("troubleshooting table is required")
    if VOICE_PATTERN.search(text):
        errors.append("banned dash or promotional voice token found")
    if HTML_TEXT_ACTIVE_PATTERN.search(text):
        errors.append("active-content token found in HTML source")
    if re.search(r"@import\b", text, re.IGNORECASE):
        errors.append("external CSS resource is forbidden")
    for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", text, re.IGNORECASE):
        if not re.match(r"data:image/(?:png|jpeg|gif|webp);base64,", match.group(2), re.IGNORECASE):
            errors.append("non-embedded CSS resource is forbidden")
            break
    if not re.search(r"troubleshoot|diagnostic|problem|problema|diagn[oó]stic", text, re.IGNORECASE):
        errors.append("troubleshooting section is not identifiable")
    if not re.search(r"safety|limits?|security|privacy|seguridad|l[ií]mites?|privacidad", text, re.IGNORECASE):
        errors.append("safety and limits section is not identifiable")
    if not FINGERPRINT_PATTERN.search(text):
        errors.append("codex-guides fingerprint comment is missing")
    if SECRET_PATTERN.search(text):
        errors.append("possible live secret found")
    if ABSOLUTE_USER_PATH_PATTERN.search(text):
        errors.append("user-specific absolute path found")
    return errors


def validate_index(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not re.search(r"Codex-guides fingerprint\s*:", text, re.IGNORECASE):
        errors.append("developer-index fingerprint is missing")
    if SECRET_PATTERN.search(text):
        errors.append("possible live secret found")
    if ABSOLUTE_USER_PATH_PATTERN.search(text):
        errors.append("user-specific absolute path found")
    if len(re.findall(r"^#{1,3}\s+", text, re.MULTILINE)) < 4:
        errors.append("developer index has too few sections")
    return errors


def validate_citations(path: Path, source_root: Path) -> list[str]:
    errors: list[str] = []
    entries = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not entries:
        return ["citation list is empty"]
    pattern = re.compile(r"^.+?\s*->\s*(.+):(\d+)$")
    for number, entry in enumerate(entries, start=1):
        match = pattern.match(entry)
        if not match:
            errors.append(f"citation {number} does not match 'claim -> path:line'")
            continue
        relative, raw_line = match.groups()
        candidate = (source_root / relative).resolve()
        try:
            candidate.relative_to(source_root.resolve())
        except ValueError:
            errors.append(f"citation {number} escapes the source root")
            continue
        if not candidate.is_file():
            errors.append(f"citation {number} file does not exist: {relative}")
            continue
        line_number = int(raw_line)
        line_count = len(candidate.read_text(encoding="utf-8", errors="replace").splitlines())
        if line_number < 1 or line_number > line_count:
            errors.append(f"citation {number} line {line_number} is outside 1..{line_count}")
    return errors


def compute_source_fingerprint(source_root: Path, source_paths: list[Path]) -> tuple[int, int, str]:
    root = source_root.resolve()
    resolved: dict[str, Path] = {}
    for raw_path in source_paths:
        candidate = raw_path.resolve() if raw_path.is_absolute() else (root / raw_path).resolve()
        try:
            relative = candidate.relative_to(root).as_posix()
        except ValueError as exc:
            raise ValueError(f"fingerprint source escapes the source root: {raw_path}") from exc
        if not candidate.is_file():
            raise ValueError(f"fingerprint source is not a file: {raw_path}")
        resolved[relative] = candidate

    digest = hashlib.sha256()
    total_bytes = 0
    for relative in sorted(resolved):
        content = resolved[relative].read_bytes()
        total_bytes += len(content)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return len(resolved), total_bytes, digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--html", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--citations", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--fingerprint", nargs="+", type=Path, metavar="SOURCE")
    args = parser.parse_args()

    checks: list[tuple[str, list[str]]] = [("skill package", validate_package(args.skill_root.resolve()))]
    if args.html:
        checks.append((str(args.html), validate_html(args.html.resolve())))
    if args.index:
        checks.append((str(args.index), validate_index(args.index.resolve())))
    if args.citations:
        if not args.source_root:
            parser.error("--citations requires --source-root")
        checks.append((str(args.citations), validate_citations(args.citations.resolve(), args.source_root.resolve())))

    if args.fingerprint:
        if not args.source_root:
            parser.error("--fingerprint requires --source-root")
        try:
            count, total_bytes, digest = compute_source_fingerprint(args.source_root, args.fingerprint)
        except ValueError as exc:
            print(f"FAIL: fingerprint\n  - {exc}")
            return 1
        print(f"FINGERPRINT: sources={count}; bytes={total_bytes}; sha256={digest}")

    failed = False
    for label, errors in checks:
        if errors:
            failed = True
            print(f"FAIL: {label}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS: {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
