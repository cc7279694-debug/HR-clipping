#!/usr/bin/env python3
"""Lightweight repository checks; deliberately not a general YAML/Markdown parser."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKILL = ".agents/skills/hr-clipping"
REQUIRED_FILES = (
    "README.md", "AGENTS.md", ".gitignore", "STATUS.md",
    f"{SKILL}/SKILL.md",
    f"{SKILL}/references/production-baseline-v1.md",
    f"{SKILL}/references/reference-analysis.md",
    f"{SKILL}/references/validation.md",
    f"{SKILL}/templates/episode-brief.md",
    f"{SKILL}/templates/edit-plan.md",
    f"{SKILL}/templates/review.md",
    f"{SKILL}/examples/openfilm-episode.md",
    "tests/skill-scenarios.md", "docs/V1_INTEGRATION_REVIEW.md",
    "docs/V1_INTEGRATION_PLAN.md", "docs/SOURCE_PROVENANCE.md",
    "docs/source-package-checks.json",
    "tests/evidence/baseline-responses.md",
    "tests/evidence/with-skill-responses.md",
    "tests/evidence/implicit-route-response.md",
    "tests/evidence/negative-route-response.md",
    "tests/evidence/behavior-assessment.md",
    "tests/evidence/verification-log.md",
)
FIELDS = {
    "templates/episode-brief.md": ("本期主题", "素材位置", "本次任务", "特别要求", "事实表"),
    "templates/edit-plan.md": ("素材ID", "源入点", "源出点", "成片入点", "成片出点", "P/D/E/R", "事实依据", "字幕时间轴", "TBD"),
    "templates/review.md": ("完整画面复看", "完整声音复听", "可编辑工程", "原素材", "平台预览"),
}
LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\((<[^>\n]+>|[^)\s]+)\)")


def validate(root: Path) -> list[str]:
    """Return human-readable violations without modifying the repository."""
    root = root.resolve()
    errors = []
    contents = {}
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing: {relative}")
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f"escape: {relative}")
            continue
        try:
            contents[relative] = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"UTF-8: {relative}")

    entry = contents.get(f"{SKILL}/SKILL.md", "")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", entry, re.DOTALL)
    if not match:
        errors.append("frontmatter: expected opening and closing delimiters")
    else:
        # This skill uses only two single-line scalar fields. Other YAML is unsupported.
        fields = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if not separator or key in fields or key not in {"name", "description"}:
                errors.append("frontmatter: only unique name/description scalar fields supported")
            fields[key] = value.strip()
        if fields.get("name") != "hr-clipping":
            errors.append("name: expected hr-clipping")
        description = fields.get("description", "")
        if not description or len(description) > 1024 or description.startswith(("|", ">", "[", "{")):
            errors.append("description: expected nonempty single-line scalar, at most 1024 characters")

    entries = sorted(p.relative_to(root).as_posix() for p in (root / ".agents/skills").glob("*/SKILL.md"))
    if entries != [f"{SKILL}/SKILL.md"]:
        errors.append("unique: repository must contain exactly one Skill at the canonical path")

    for relative, content in contents.items():
        if "$xiaoyang-tech-vlog" in content:
            errors.append(f"legacy: old invocation in {relative}")
        if not relative.endswith(".md"):
            continue
        for target in LINK.findall(content):
            target = target.strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme in {"https", "http", "mailto"} or not parsed.path:
                continue
            if parsed.scheme or parsed.netloc or "\\" in target:
                errors.append(f"escape: non-relative local link in {relative}")
                continue
            path = Path(unquote(parsed.path))
            resolved = (root / relative).parent.joinpath(path).resolve()
            if path.is_absolute() or not resolved.is_relative_to(root):
                errors.append(f"escape: {relative} -> {target}")
            elif not resolved.exists():
                errors.append(f"link: {relative} -> {target}")

    for relative, fields in FIELDS.items():
        content = contents.get(f"{SKILL}/{relative}", "")
        for field in fields:
            if field not in content:
                errors.append(f"field: {relative} missing {field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        return 1
    print(f"PASS: {len(REQUIRED_FILES)} required files; UTF-8, identity, local file targets, template fields")
    print("Scope: limited scalar-field checks; link targets only, not anchors; no host/behavior/media validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
