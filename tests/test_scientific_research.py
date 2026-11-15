"""Tests for the scientific-research skill rules and package layout."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "scientific-research"
sys.path.insert(0, str(SKILL / "scripts"))

import policy  # noqa: E402
from package_skill import build_zip, included  # noqa: E402


def setUpModule():
    patcher = patch("urllib.request.urlopen", side_effect=AssertionError("tests must not open a network connection"))
    patcher.start()


class JournalTests(unittest.TestCase):
    def test_priority_q1_without_mandatory_fee(self):
        decision = policy.journal_decision(
            index="scopus",
            quartile="Q1",
            apc_mandatory=False,
            indexing_source="scopus_sources",
            apc_source="publisher_journal_page",
            publication_year=2026,
        )
        self.assertTrue(decision["recommend"])
        self.assertEqual(decision["tier"], "priority")

    def test_q2_is_priority_and_q4_needs_explicit_fallback(self):
        q2 = policy.journal_decision(
            index="scopus",
            quartile="Q2",
            apc_mandatory=False,
            indexing_source="scu_digital_library_report",
            apc_source="publisher_price_list",
            publication_year=2025,
        )
        q4 = policy.journal_decision(
            index="scopus",
            quartile="Q4",
            apc_mandatory=False,
            indexing_source="scopus_sources",
            apc_source="publisher_journal_page",
            publication_year=2025,
        )
        q4_allowed = policy.journal_decision(
            index="scopus",
            quartile="Q4",
            apc_mandatory=False,
            indexing_source="scopus_sources",
            apc_source="publisher_journal_page",
            publication_year=2025,
            allow_q3_q4=True,
        )
        self.assertEqual(q2["tier"], "priority")
        self.assertFalse(q4["recommend"])
        self.assertEqual(q4_allowed["tier"], "fallback")

    def test_mandatory_fee_and_unverified_records_are_not_recommended(self):
        fee = policy.journal_decision(
            index="scopus",
            quartile="Q1",
            apc_mandatory=True,
            indexing_source="scopus_sources",
            apc_source="publisher_journal_page",
            publication_year=2026,
        )
        unknown = policy.journal_decision(
            index="scopus",
            quartile="Q1",
            apc_mandatory=False,
            indexing_source=None,
            apc_source=None,
            publication_year=None,
        )
        predatory = policy.journal_decision(
            index="scopus",
            quartile="Q1",
            apc_mandatory=False,
            indexing_source="scopus_sources",
            apc_source="publisher_journal_page",
            predatory=True,
            publication_year=2026,
        )
        self.assertFalse(fee["recommend"])
        self.assertEqual(unknown["tier"], "unverified")
        self.assertEqual(predatory["tier"], "rejected")

    def test_non_scopus_index_does_not_meet_the_priority_rule(self):
        decision = policy.journal_decision(
            index="web_of_science",
            quartile="Q1",
            apc_mandatory=False,
            indexing_source="scu_digital_library_report",
            apc_source="publisher_journal_page",
            publication_year=2026,
        )
        self.assertFalse(decision["recommend"])


class SimilarityTests(unittest.TestCase):
    def test_promotion_snapshot_stays_inside_promotion_scope(self):
        limit = policy.load_promotion_snapshot()
        promotion = policy.similarity_guidance(product="promotion", official_limit=limit)
        article = policy.similarity_guidance(product="original", official_limit=limit)
        thesis = policy.similarity_guidance(product="thesis", official_limit=limit)
        missing = policy.similarity_guidance(product="promotion", official_limit=None)
        self.assertTrue(promotion["apply_numeric_limit"])
        self.assertEqual(promotion["single_paper_max"], 0.2)
        self.assertEqual(promotion["aggregate_max"], 0.4)
        self.assertIn("scu.eg", promotion["source_url"])
        self.assertEqual(promotion["checked_on"], "2026-11-13")
        self.assertFalse(article["apply_numeric_limit"])
        self.assertFalse(thesis["apply_numeric_limit"])
        self.assertFalse(missing["apply_numeric_limit"])
        self.assertNotIn("single_paper_max", article)

    def test_journal_limit_applies_only_with_its_own_source(self):
        guided = policy.similarity_guidance(
            product="thesis_to_article",
            official_limit={
                "scope": "journal",
                "single_paper_max": 0.15,
                "aggregate_max": 0.15,
                "source_url": "https://publisher.example.edu/author-guidelines",
                "checked_on": "2026-11-13",
            },
        )
        self.assertTrue(guided["apply_numeric_limit"])
        self.assertEqual(guided["scope"], "journal")
        self.assertNotEqual(guided["single_paper_max"], 0.2)


class ProfileReferenceReviewTests(unittest.TestCase):
    def test_template_profile_is_incomplete(self):
        template = json.loads(policy.PROFILE_TEMPLATE.read_text(encoding="utf-8"))
        status = policy.profile_status(template)
        self.assertFalse(status["complete"])
        self.assertEqual(status["missing"], list(policy.PROFILE_FIELDS))

    def test_completed_profile_accepts_orcid_and_warns_on_public_email(self):
        status = policy.profile_status(
            {
                "name": "اسم للتجربة",
                "university": "جامعة للتجربة",
                "department": "قسم للتجربة",
                "institutional_email": "person@gmail.com",
                "orcid": "https://orcid.org/0000-0002-1825-0097",
            }
        )
        self.assertTrue(status["complete"])
        self.assertTrue(status["warnings"])

    def test_real_reference_passes_and_placeholder_fails(self):
        real = json.loads((ROOT / "tests/fixtures/real-reference.json").read_text(encoding="utf-8"))
        invented = json.loads((ROOT / "tests/fixtures/invented-reference.json").read_text(encoding="utf-8"))
        self.assertEqual(policy.validate_references(real), [])
        self.assertTrue(policy.validate_references(invented))
        self.assertTrue(policy.validate_references([{"title": "بلا مصدر", "year": 2020}]))

    def test_section_review_requires_four_criteria(self):
        complete = (ROOT / "tests/fixtures/methods-review.md").read_text(encoding="utf-8")
        incomplete = (ROOT / "tests/fixtures/incomplete-review.md").read_text(encoding="utf-8")
        self.assertEqual(policy.review_issues(complete, ["المنهج"]), [])
        issues = policy.review_issues(incomplete, ["المنهج"])
        self.assertTrue(any("التحليل الإحصائي" in issue for issue in issues))
        invented_stats = complete.replace(
            "البيانات غير متوفرة، لذلك لا تُراجع نتيجة إحصائية.",
            "البيانات غير متوفرة.\np < 0.05",
        )
        self.assertTrue(any("نتيجة إحصائية" in issue for issue in policy.review_issues(invented_stats, ["المنهج"])))

    def test_profile_command_reads_the_default_file_and_still_accepts_path(self):
        default = policy.PROFILE_PATH
        other = SKILL / "assets" / "profile-cli-other.json"
        complete = {
            "name": "اسم للتجربة",
            "university": "جامعة للتجربة",
            "department": "قسم للتجربة",
            "institutional_email": "person@univ.edu.eg",
            "orcid": "0000-0002-1825-0097",
        }
        backup = default.read_text(encoding="utf-8") if default.exists() else None
        try:
            if default.exists():
                default.unlink()
            missing = self._profile_cli([])
            self.assertFalse(missing["complete"])
            self.assertEqual(missing["missing"], list(policy.PROFILE_FIELDS))
            default.write_text(json.dumps(complete, ensure_ascii=False), encoding="utf-8")
            loaded = self._profile_cli([])
            self.assertTrue(loaded["complete"])
            self.assertEqual(loaded["missing"], [])
            other.write_text(
                json.dumps({**complete, "name": ""}, ensure_ascii=False),
                encoding="utf-8",
            )
            overridden = self._profile_cli(["--path", str(other)])
            self.assertFalse(overridden["complete"])
            self.assertIn("name", overridden["missing"])
            absent = self._profile_cli(["--path", str(SKILL / "assets" / "no-such-profile.json")])
            self.assertFalse(absent["complete"])
            self.assertEqual(absent["missing"], list(policy.PROFILE_FIELDS))
        finally:
            if other.exists():
                other.unlink()
            if backup is None and default.exists():
                default.unlink()
            elif backup is not None:
                default.write_text(backup, encoding="utf-8")

    def _profile_cli(self, extra: list[str]) -> dict:
        buffer = StringIO()
        with patch("sys.stdout", buffer):
            code = policy.main(["profile", *extra])
        self.assertEqual(code, 0)
        return json.loads(buffer.getvalue())


class PackageTests(unittest.TestCase):
    def test_skill_layout_and_platforms(self):
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill_md.startswith("---\nname: scientific-research\n"))
        self.assertNotIn("20%", skill_md)
        self.assertNotIn("40%", skill_md)
        for link in (
            ROOT / ".cursor/skills/scientific-research",
            ROOT / ".claude/skills/scientific-research",
        ):
            self.assertTrue(link.is_symlink())
            self.assertEqual((link / "SKILL.md").resolve(), (SKILL / "SKILL.md").resolve())
        for guide in ("cursor.md", "claude.md", "chatgpt.md", "gemini.md"):
            text = (ROOT / "platforms" / guide).read_text(encoding="utf-8")
            self.assertIn("scientific-research", text)
        snapshot = json.loads((SKILL / "references/official-snapshot.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["product_scope"], "promotion_dossier")
        self.assertTrue(snapshot["not_a_universal_manuscript_limit"])
        points = json.loads((SKILL / "references/cycle15-journal-points.json").read_text(encoding="utf-8"))
        self.assertEqual(points["specialized"]["web_of_science"]["Q1"], 10.0)
        self.assertEqual(points["specialized"]["scopus"]["Q1"], 9.0)
        self.assertEqual(points["non_specialized"]["scopus"]["Q4"], 7.0)

    def test_zip_has_skill_md_at_its_root(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = build_zip(Path(directory) / "scientific-research.zip")
            with zipfile.ZipFile(archive) as zipped:
                names = set(zipped.namelist())
                identity = json.loads(zipped.read("assets/skill-identity.json"))
                template = json.loads(zipped.read("assets/researcher-profile.template.json"))
                citation = zipped.read("CITATION.cff").decode("utf-8")
            self.assertIn("SKILL.md", names)
            self.assertIn("references/official-snapshot.json", names)
            self.assertIn("references/applied-example.md", names)
            self.assertNotIn("assets/researcher-profile.json", names)
            joined = "\n".join(names)
            self.assertNotIn("researcher-profile.json", joined)
            self.assertNotIn("gfa-active-ageing", joined.lower())
            self.assertNotIn("studies/", joined)
            self.assertEqual(identity["version"], "2.0.0")
            self.assertEqual(identity["author"], "Dr. Hesham El-Nady")
            self.assertEqual(identity["orcid"], "")
            self.assertEqual(identity["institutional_email"], "")
            self.assertEqual(template["name"], "")
            self.assertEqual(template["institutional_email"], "")
            self.assertEqual(template["orcid"], "")
            self.assertIn("version: 2.0.0\n", citation)

    def test_package_filter_drops_profile_and_study_files_and_keeps_the_note(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            study = root / "studies" / "gfa-active-ageing" / "draft.md"
            study.parent.mkdir(parents=True)
            study.write_text("study file", encoding="utf-8")
            profile = root / "assets" / "researcher-profile.json"
            profile.parent.mkdir()
            profile.write_text("{}", encoding="utf-8")
            skill = root / "SKILL.md"
            skill.write_text("ok", encoding="utf-8")
            note = root / "references" / "applied-example.md"
            note.parent.mkdir()
            note.write_text("The GfA Active Ageing study stays outside the skill.", encoding="utf-8")
            self.assertFalse(included(study, root))
            self.assertFalse(included(profile, root))
            self.assertTrue(included(skill, root))
            self.assertTrue(included(note, root))


if __name__ == "__main__":
    unittest.main()
