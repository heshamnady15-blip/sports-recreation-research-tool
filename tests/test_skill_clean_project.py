"""Run the scientific-research skill from a copy that has no study files.

These checks do not open the network and do not read studies/gfa-active-ageing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "scientific-research"


def _python(script: Path, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


class CleanProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.project = Path(cls.temporary.name) / "clean-project"
        cls.skill = cls.project / "scientific-research"
        shutil.copytree(
            SKILL,
            cls.skill,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_copy_contains_the_skill_and_no_study_files(self):
        names = [path.relative_to(self.project).as_posix() for path in self.project.rglob("*")]
        self.assertTrue((self.skill / "SKILL.md").is_file())
        self.assertFalse(any("gfa-active-ageing" in name for name in names))
        self.assertFalse(any(name.startswith("studies/") for name in names))
        self.assertFalse((self.project / "studies").exists())

    def test_identity_stays_compatible_with_the_technical_name(self):
        text = (self.skill / "SKILL.md").read_text(encoding="utf-8")
        identity = json.loads((self.skill / "assets" / "skill-identity.json").read_text(encoding="utf-8"))
        self.assertTrue(text.startswith("---\nname: scientific-research\n"))
        self.assertIn("display_name: El-Nady Scientific Research Assistant", text)
        self.assertIn("author: Dr. Hesham El-Nady", text)
        self.assertLessEqual(len(text.split("description:", 1)[1].split("compatibility:", 1)[0]), 1200)
        self.assertEqual(identity["technical_name"], "scientific-research")
        self.assertEqual(identity["display_name"], "El-Nady Scientific Research Assistant")
        self.assertEqual(identity["author"], "Dr. Hesham El-Nady")
        self.assertEqual(identity["orcid"], "")
        template = json.loads((self.skill / "assets" / "researcher-profile.template.json").read_text(encoding="utf-8"))
        self.assertEqual(template["name"], "")
        plugin = json.loads((ROOT / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["skills"], ".agents/skills/scientific-research")
        self.assertEqual(plugin["author"]["name"], "Dr. Hesham El-Nady")
        self.assertNotIn("license", plugin)

    def test_offline_commands_do_not_recommend_an_unverified_journal_or_doi(self):
        policy = self.skill / "scripts" / "policy.py"
        profile = _python(policy, ["profile"], self.skill)
        self.assertEqual(profile.returncode, 0, profile.stderr)
        self.assertFalse(json.loads(profile.stdout)["complete"])

        journal = _python(
            policy,
            ["journal", "--index", "scopus", "--quartile", "Q1", "--apc-mandatory", "false", "--publication-year", "2026"],
            self.skill,
        )
        decision = json.loads(journal.stdout)
        self.assertFalse(decision["recommend"])
        self.assertEqual(decision["tier"], "unverified")

        references = self.skill / "references.json"
        references.write_text(
            json.dumps([{"title": "Clean project fixture", "year": 2024, "doi": "10.5555/clean-project.fixture"}]),
            encoding="utf-8",
        )
        checked = _python(policy, ["verify-references", "--path", str(references), "--offline"], self.skill)
        self.assertEqual(checked.returncode, 1, checked.stdout)
        report = json.loads(checked.stdout)
        self.assertFalse(report["passed"])
        self.assertIn("غير متحقق منها", json.dumps(report, ensure_ascii=False))

        neutral = self.skill / "neutral.md"
        neutral.write_text("This draft names no design and reports no collected measurements.\n", encoding="utf-8")
        methods = _python(policy, ["audit-methods", "--path", str(neutral)], self.skill)
        self.assertEqual(methods.returncode, 0, methods.stderr)
        self.assertEqual(json.loads(methods.stdout)["findings"][0]["severity"], "مقبول")

        rct = self.skill / "rct.md"
        rct.write_text("This randomized controlled trial used one group and no control group.\n", encoding="utf-8")
        flagged = _python(policy, ["audit-methods", "--path", str(rct)], self.skill)
        self.assertEqual(flagged.returncode, 1)
        self.assertIn("خطأ حرج", flagged.stdout)

        stats = self.skill / "stats.md"
        stats.write_text("البيانات غير متوفرة.\n## قسم: التحليل\nThe analysis reports p < 0.05 before data collection.\n", encoding="utf-8")
        stats_report = _python(policy, ["audit-methods", "--path", str(stats)], self.skill)
        self.assertEqual(stats_report.returncode, 1)
        self.assertIn("خطأ حرج", stats_report.stdout)

        review = self.skill / "review.md"
        review.write_text(
            "\n".join(
                [
                    "## قسم: المنهج",
                    "### المنهجية",
                    "الوصف مكتمل في هذا المثال.",
                    "### التحليل الإحصائي",
                    "البيانات غير متوفرة، لذلك لا تُراجع نتيجة إحصائية.",
                    "### الأصالة",
                    "لا ادعاء أصالة غير موثق.",
                    "### الأخلاقيات",
                    "لا رقم موافقة في هذا المثال.",
                    "### الحكم",
                    "غير قابل للتحقق",
                ]
            ),
            encoding="utf-8",
        )
        reviewed = _python(policy, ["review", "--path", str(review), "--section", "المنهج"], self.skill)
        self.assertEqual(reviewed.returncode, 0, reviewed.stdout)

        probe = _python(self.skill / "scripts" / "capability_probe.py", [], self.skill)
        self.assertEqual(probe.returncode, 0, probe.stderr)
        payload = json.loads(probe.stdout)
        self.assertFalse(payload["journal_verified"])
        by_command = {item["command"]: item for item in payload["commands"]}
        self.assertFalse(by_command["audit-methods"]["network"])
        self.assertTrue(by_command["verify-references"]["network"])
        self.assertIn("api.crossref.org", by_command["verify-references"]["external_source"])
        self.assertTrue(by_command["verify-journal"]["network"])


if __name__ == "__main__":
    unittest.main()
