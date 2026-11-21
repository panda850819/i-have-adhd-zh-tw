from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("check_repo", ROOT / "scripts/check_repo.py")
assert SPEC and SPEC.loader
check_repo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_repo)


class RepositoryTests(unittest.TestCase):
    def test_repository_contracts(self):
        self.assertEqual([], check_repo.check_repository(ROOT))

    def test_literal_python_version_in_workflow_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".python-version").write_text("3.12\n", encoding="utf-8")
            (root / ".github/workflows/validate.yml").write_text(
                "      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.12'\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_repo.check_ci_python(root, errors)
        self.assertTrue(any(".python-version: must hold" in error for error in errors))
        self.assertTrue(any("not python-version:" in error for error in errors))
        self.assertTrue(any("ci-python" in error for error in errors))

    def test_duplicate_case_ids_are_rejected(self):
        row = {
            "id": "duplicate",
            "category": "filler",
            "prompt": "test",
            "risk": "low",
            "criteria": ["works"],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.jsonl"
            path.write_text("\n".join(json.dumps(row) for _ in range(2)), encoding="utf-8")
            _, errors = check_repo.load_cases(path)
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_missing_case_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.jsonl"
            path.write_text(json.dumps({"id": "incomplete"}), encoding="utf-8")
            _, errors = check_repo.load_cases(path)
        self.assertTrue(any("missing fields" in error for error in errors))

    def test_invalid_risk_is_rejected(self):
        row = {
            "id": "bad-risk",
            "category": "safety",
            "prompt": "test",
            "risk": "critical",
            "criteria": ["works"],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "cases.jsonl"
            path.write_text(json.dumps(row), encoding="utf-8")
            _, errors = check_repo.load_cases(path)
        self.assertTrue(any("unsupported risk" in error for error in errors))

    def test_missing_local_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = Path("README.md")
            (root / path).write_text("[missing](./not-here.md)", encoding="utf-8")
            errors: list[str] = []
            check_repo.check_local_links(root, path, errors)
        self.assertTrue(any("local link target does not exist" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
