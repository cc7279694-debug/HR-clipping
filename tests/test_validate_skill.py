"""Exercise the validator against broken copies, using only the standard library."""

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skill.py"
SKILL = Path(".agents/skills/hr-clipping")


class BootstrapTests(unittest.TestCase):
    def test_validator_exists(self):
        self.assertTrue(SCRIPT.is_file(), "validator not implemented")


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SCRIPT.is_file():
            raise unittest.SkipTest("validator not implemented")
        spec = importlib.util.spec_from_file_location("skill_validator", SCRIPT)
        cls.validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.validator)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hr-clipping-validator-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in self.validator.REQUIRED_FILES:
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    def edit(self, relative, transform):
        path = self.root / relative
        path.write_text(transform(path.read_text(encoding="utf-8")), encoding="utf-8")

    def errors(self):
        return self.validator.validate(self.root)

    def test_valid_repository(self):
        self.assertEqual([], self.errors())

    def test_missing_required_file(self):
        (self.root / SKILL / "templates/review.md").unlink()
        self.assertTrue(any("missing:" in e for e in self.errors()))

    def test_wrong_identifier(self):
        self.edit(SKILL / "SKILL.md", lambda s: s.replace("name: hr-clipping", "name: other"))
        self.assertTrue(any("name:" in e for e in self.errors()))

    def test_empty_description(self):
        self.edit(SKILL / "SKILL.md", lambda s: "\n".join(
            "description:" if line.startswith("description:") else line for line in s.splitlines()))
        self.assertTrue(any("description:" in e for e in self.errors()))

    def test_broken_relative_link(self):
        self.edit(SKILL / "SKILL.md", lambda s: s + "\n[missing](references/missing.md)\n")
        self.assertTrue(any("link:" in e for e in self.errors()))

    def test_link_cannot_escape_repository(self):
        self.edit(SKILL / "SKILL.md", lambda s: s + "\n[escape](../../../../../../outside.md)\n")
        self.assertTrue(any("escape:" in e for e in self.errors()))

    def test_invalid_utf8(self):
        (self.root / SKILL / "templates/review.md").write_bytes(b"\xff")
        self.assertTrue(any("UTF-8:" in e for e in self.errors()))

    def test_missing_timeline_field(self):
        self.edit(SKILL / "templates/edit-plan.md", lambda s: s.replace("成片入点", "入点"))
        self.assertTrue(any("field:" in e for e in self.errors()))

    def test_duplicate_skill(self):
        other = self.root / ".agents/skills/duplicate"
        other.mkdir(parents=True)
        shutil.copyfile(self.root / SKILL / "SKILL.md", other / "SKILL.md")
        self.assertTrue(any("unique:" in e for e in self.errors()))

    def test_old_invocation_is_rejected(self):
        self.edit(Path("README.md"), lambda s: s + "\n使用 $xiaoyang-tech-vlog\n")
        self.assertTrue(any("legacy:" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
