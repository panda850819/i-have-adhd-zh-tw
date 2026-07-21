#!/usr/bin/env python3
"""Dependency-free repository contract checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


PLUGIN_NAME = "i-have-adhd-zh-tw"
MARKETPLACE_NAME = "panda850819"
REPOSITORY = "https://github.com/panda850819/i-have-adhd-zh-tw"
UPSTREAM = "https://github.com/ayghri/i-have-adhd"
PLUGIN_ROOT = Path("plugins/i-have-adhd-zh-tw")
SKILL_PATH = PLUGIN_ROOT / "skills/i-have-adhd-zh-tw/SKILL.md"
CASES_PATH = Path("evals/cases.jsonl")
REQUIRED_FILES = (
    Path(".agents/plugins/marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
    PLUGIN_ROOT / ".claude-plugin/plugin.json",
    PLUGIN_ROOT / ".codex-plugin/plugin.json",
    SKILL_PATH,
    PLUGIN_ROOT / "skills/i-have-adhd-zh-tw/agents/openai.yaml",
    PLUGIN_ROOT / "LICENSE",
    Path("README.md"),
    Path("INSTALL.md"),
    CASES_PATH,
    Path("evals/rubric.md"),
    Path(".github/workflows/validate.yml"),
)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level JSON must be an object")
        return {}
    return value


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

    legacy_skill = root / "skills/i-have-adhd"
    if legacy_skill.exists() and any(path.is_file() for path in legacy_skill.rglob("*")):
        errors.append("legacy skill files still exist under skills/i-have-adhd")

    frontmatter = parse_frontmatter(root / SKILL_PATH, errors)
    if frontmatter.get("name") != PLUGIN_NAME:
        errors.append(f"{SKILL_PATH}: name must be {PLUGIN_NAME}")
    description = frontmatter.get("description", "")
    for phrase in ("每一則回覆", "台灣繁體中文", "agent 能完成的工作"):
        if phrase not in description:
            errors.append(f"{SKILL_PATH}: description missing always-on signal: {phrase}")

    agents = load_json(root / ".agents/plugins/marketplace.json", errors)
    if agents.get("name") != MARKETPLACE_NAME:
        errors.append(".agents marketplace name mismatch")
    agents_plugins = agents.get("plugins", [])
    if not agents_plugins or agents_plugins[0].get("name") != PLUGIN_NAME:
        errors.append(".agents plugin name mismatch")
    else:
        source = agents_plugins[0].get("source", {})
        if source != {"source": "local", "path": "./plugins/i-have-adhd-zh-tw"}:
            errors.append(".agents plugin must resolve from its marketplace subdirectory")

    claude_market = load_json(root / ".claude-plugin/marketplace.json", errors)
    if claude_market.get("name") != MARKETPLACE_NAME:
        errors.append("Claude marketplace name mismatch")
    claude_plugins = claude_market.get("plugins", [])
    if not claude_plugins or claude_plugins[0].get("name") != PLUGIN_NAME:
        errors.append("Claude marketplace plugin name mismatch")

    claude_plugin = load_json(root / PLUGIN_ROOT / ".claude-plugin/plugin.json", errors)
    if claude_plugin.get("name") != PLUGIN_NAME:
        errors.append("Claude plugin name mismatch")
    if claude_plugin.get("version") != "0.1.3":
        errors.append("Claude plugin version mismatch")
    if claude_plugin.get("author", {}).get("url") != "https://github.com/panda850819":
        errors.append("Claude plugin author mismatch")

    codex = load_json(root / PLUGIN_ROOT / ".codex-plugin/plugin.json", errors)
    if codex.get("name") != PLUGIN_NAME:
        errors.append("Codex plugin name mismatch")
    if codex.get("version") != "0.1.3":
        errors.append("Codex plugin version mismatch")
    if codex.get("repository") != REPOSITORY:
        errors.append("Codex repository URL mismatch")
    if codex.get("skills") != "./skills/":
        errors.append("Codex skills path mismatch")

    openai_yaml = (root / PLUGIN_ROOT / "skills/i-have-adhd-zh-tw/agents/openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation: true" not in openai_yaml:
        errors.append("OpenAI metadata must allow implicit invocation")
    if "$i-have-adhd-zh-tw" not in openai_yaml:
        errors.append("OpenAI default prompt must name the zh-TW skill")

    for relative in (Path("README.md"), Path("INSTALL.md")):
        text = (root / relative).read_text(encoding="utf-8")
        if REPOSITORY.removeprefix("https://github.com/") not in text:
            errors.append(f"{relative}: repository install target missing")
        if "i-have-adhd-zh-tw" not in text:
            errors.append(f"{relative}: plugin name missing")

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
