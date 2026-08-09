#!/usr/bin/env python3
"""Dependency-free repository contract checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SKILL_NAME = "i-have-adhd-zh-tw"
REPOSITORY = "https://github.com/panda850819/i-have-adhd-zh-tw"
UPSTREAM = "https://github.com/ayghri/i-have-adhd"
SKILL_PATH = Path("skills/i-have-adhd-zh-tw/SKILL.md")
CASES_PATH = Path("evals/cases.jsonl")
REQUIRED_FILES = (
    SKILL_PATH,
    SKILL_PATH.parent / "LICENSE",
    Path("LICENSE"),
    Path("README.md"),
    Path("INSTALL.md"),
    CASES_PATH,
    Path("evals/rubric.md"),
    Path(".github/workflows/validate.yml"),
)
FORBIDDEN_PLUGIN_PATHS = (
    Path(".agents/plugins"),
    Path(".claude-plugin"),
    Path(".codex-plugin"),
    Path(".cursor"),
    Path("plugins/i-have-adhd-zh-tw"),
)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        return {}
    values: dict[str, str] = {}
    for number, line in enumerate(match.group(1).splitlines(), start=2):
        key, separator, raw_value = line.partition(":")
        if not separator:
            errors.append(f"{path}:{number}: unsupported frontmatter line")
            continue
        values[key.strip()] = raw_value.strip().strip("\"'")
    return values


def load_cases(path: Path) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    errors: list[str] = []
    seen: set[str] = set()
    required = {"id", "category", "prompt", "risk", "criteria"}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{number}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{path}:{number}: row must be an object")
            continue
        missing = sorted(required - set(row))
        if missing:
            errors.append(f"{path}:{number}: missing fields: {', '.join(missing)}")
            continue
        case_id = row["id"]
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{path}:{number}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{path}:{number}: duplicate id: {case_id}")
        else:
            seen.add(case_id)
        if row["risk"] not in {"low", "medium", "high"}:
            errors.append(f"{path}:{number}: unsupported risk: {row['risk']}")
        if not isinstance(row["criteria"], list) or not row["criteria"]:
            errors.append(f"{path}:{number}: criteria must be a non-empty list")
        rows.append(row)
    return rows, errors


def check_local_links(root: Path, path: Path, errors: list[str]) -> None:
    text = (root / path).read_text(encoding="utf-8")
    for target in re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", text):
        target = target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        resolved = (root / path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path}: local link target does not exist: {target}")


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        return errors

    for relative in FORBIDDEN_PLUGIN_PATHS:
        if (root / relative).exists():
            errors.append(f"host-specific plugin packaging must not exist: {relative}")

    legacy_skill = root / "skills/i-have-adhd"
    if legacy_skill.exists() and any(path.is_file() for path in legacy_skill.rglob("*")):
        errors.append("legacy skill files still exist under skills/i-have-adhd")

    if (root / "LICENSE").read_bytes() != (root / SKILL_PATH.parent / "LICENSE").read_bytes():
        errors.append(f"{SKILL_PATH.parent / 'LICENSE'}: must match root LICENSE")

    frontmatter = parse_frontmatter(root / SKILL_PATH, errors)
    if frontmatter.get("name") != SKILL_NAME:
        errors.append(f"{SKILL_PATH}: name must be {SKILL_NAME}")
    description = frontmatter.get("description", "")
    for phrase in ("每一則回覆", "台灣繁體中文", "agent 能完成的工作"):
        if phrase not in description:
            errors.append(f"{SKILL_PATH}: description missing always-on signal: {phrase}")
    if frontmatter.get("license") != "MIT":
        errors.append(f"{SKILL_PATH}: license must be MIT")

    skill_text = (root / SKILL_PATH).read_text(encoding="utf-8")
    for phrase in ("最少步驟", "一次只維持一個 `in_progress`", "慣用語與比喻"):
        if phrase not in skill_text:
            errors.append(f"{SKILL_PATH}: missing upstream behavior: {phrase}")

    for relative in (Path("README.md"), Path("INSTALL.md")):
        text = (root / relative).read_text(encoding="utf-8")
        if REPOSITORY.removeprefix("https://github.com/") not in text:
            errors.append(f"{relative}: repository install target missing")
        if "npx skills add" not in text:
            errors.append(f"{relative}: standard Skill install command missing")
        if SKILL_NAME not in text:
            errors.append(f"{relative}: Skill name missing")

    readme = (root / "README.md").read_text(encoding="utf-8")
    attribution_signals = {
        UPSTREAM: "upstream repository",
        "Ayoub Ghriss": "upstream author",
        "非官方繁體中文衍生版本": "unofficial derivative status",
        "不以此專案營利": "maintainer non-profit statement",
        "不是額外的授權限制": "MIT non-restriction clarification",
    }
    for signal, label in attribution_signals.items():
        if signal not in readme:
            errors.append(f"README.md: missing {label}")

    for relative in root.rglob("*.md"):
        if ".git" not in relative.parts:
            check_local_links(root, relative.relative_to(root), errors)

    cases, case_errors = load_cases(root / CASES_PATH)
    errors.extend(case_errors)
    if len(cases) < 15:
        errors.append(f"{CASES_PATH}: expected at least 15 cases, found {len(cases)}")
    required_categories = {
        "agent-autonomy",
        "natural-zh-tw",
        "terminology",
        "safety",
        "filler",
        "banned-phrases",
        "calibration",
    }
    missing_categories = sorted(required_categories - {row.get("category") for row in cases})
    if missing_categories:
        errors.append(f"{CASES_PATH}: missing categories: {', '.join(missing_categories)}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors = check_repository(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("repository contracts: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
