"""Consistency checks for the GfA Active Ageing V2.1 drafts. They do not use the network."""

from __future__ import annotations

import hashlib
import sys
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "scientific-research" / "scripts"))

from verify_v2 import SEVERITY_CRITICAL, SEVERITY_OK, SEVERITY_REVISE, audit_methods  # noqa: E402

STUDY = ROOT / "studies" / "gfa-active-ageing"
ORIGINALS = {
    "GfA_Active_Ageing_Bilingual_Intervention_Manual.docx": "bd77baa32a76e504d83f2e15bed0d151b5b52c21f544629acb40b1a5824d4b86",
    "GfA_Active_Ageing_Pilot_Protocol_Step21_AR_EN.docx": "2010c382c5f8f33d1dcf702b01b1f95c67cdf237ad1db0e3376043e04cd0c6e2",
    "GfA_Expert_Validation_Forms_AR_EN.docx": "860ee7401f07b8a2ecad8fb36dd534d3ff80e225ce0e0d14bf72cf7979704bbe",
    "GfA_Active_Ageing_SAP_Step24_AR_EN.docx": "231c9242c94cf37d9c02aa9d4317a8c47b46cb60095df81d76afb059d0fe8e11",
}
V21 = {
    "manual": STUDY / "v2.1" / "GfA_Active_Ageing_Bilingual_Intervention_Manual_v2.1.docx",
    "pilot": STUDY / "v2.1" / "GfA_Active_Ageing_Pilot_Protocol_Step21_v2.1.docx",
    "expert": STUDY / "v2.1" / "GfA_Expert_Validation_Forms_v2.1.docx",
    "sap": STUDY / "v2.1" / "GfA_Active_Ageing_SAP_Step24_v2.1.docx",
}


def document_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    lines = []
    for paragraph in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        parts = []
        for node in paragraph.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
            if node.text:
                parts.append(node.text)
        line = "".join(parts).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


class OriginalPreservationTests(unittest.TestCase):
    def test_original_bytes_match_the_supplied_package(self):
        for name, digest in ORIGINALS.items():
            path = STUDY / "original" / name
            self.assertTrue(path.is_file(), name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)


class Version21ConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {name: document_text(path) for name, path in V21.items()}

    def test_four_documents_exist_and_differ_from_the_originals(self):
        original_hashes = {
            hashlib.sha256((STUDY / "original" / name).read_bytes()).hexdigest() for name in ORIGINALS
        }
        for path in V21.values():
            self.assertTrue(path.is_file())
            self.assertNotIn(hashlib.sha256(path.read_bytes()).hexdigest(), original_hashes)
            self.assertIn("V2.1", document_text(path))

    def test_pattern_audit_finds_no_critical_or_revision_conflict(self):
        for name, text in self.texts.items():
            findings = audit_methods(text)
            severities = {item["severity"] for item in findings}
            self.assertNotIn(SEVERITY_CRITICAL, severities, name)
            self.assertNotIn(SEVERITY_REVISE, severities, name)
            self.assertIn(SEVERITY_OK, severities, name)

    def test_connectedness_claim_is_limited_to_the_instrument(self):
        for name in ("manual", "pilot", "sap"):
            text = self.texts[name]
            self.assertIn("LSNS-6", text)
            self.assertIn("within-facility social connectedness", text)
            self.assertIn("does not measure within-facility social connectedness", text)
            self.assertIn("داخل الدار", text)

    def test_executed_design_stays_unnamed_and_compared(self):
        for name in ("manual", "pilot", "sap"):
            text = self.texts[name]
            self.assertIn("Executed design: not named", text)
            self.assertIn("alternative design", text)
            self.assertIn("تصميم بديل", text)
            self.assertIn("not a randomized trial", text)
            self.assertIn("Place and time separation", text)

    def test_sessions_forms_and_denominators_remain(self):
        manual = self.texts["manual"]
        expert = self.texts["expert"]
        self.assertEqual(sum(1 for line in manual.splitlines() if line == "معلّقة / Pending"), 36)
        self.assertIn("جلسة الاستمرار", manual)
        for index in range(1, 9):
            self.assertIn(f"GFA-0{index}", manual)
        self.assertEqual(sum(1 for line in expert.splitlines() if line.isdigit()), 36)
        self.assertIn("Weeks 10–12", expert)
        self.assertIn("I-CVI", expert)
        pilot = self.texts["pilot"]
        self.assertIn("576/720", pilot)
        self.assertIn("multiplied by 36", pilot)
        self.assertIn("PILOT-R01", pilot)
        self.assertIn("PILOT-R03", pilot)
        self.assertIn("multiplied by 36", self.texts["sap"])
        self.assertIn("Assessor blinding", manual)
        self.assertIn("assessor blinding", self.texts["sap"].lower())

    def test_acceptability_dose_and_journal_are_not_overclaimed(self):
        manual = self.texts["manual"]
        pilot = self.texts["pilot"]
        self.assertIn("written notes only", manual.lower())
        self.assertIn("not an analysis outcome", manual)
        self.assertIn("ملاحظات مكتوبة فقط", pilot)
        self.assertIn("Not prescribed in this version", manual)
        self.assertIn("per-protocol analysis is not defined", self.texts["sap"].lower())
        for text in self.texts.values():
            self.assertNotIn("Co-Designed", text)
            self.assertNotIn("doi.org", text)
            self.assertNotIn("Q1", text)
            self.assertNotIn("Q2", text)
            self.assertIn("pending", text.lower())


class ClosureRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {name: document_text(path) for name, path in V21.items()}
        cls.codesign = document_text(STUDY / "v2.1" / "GfA_Active_Ageing_CoDesign_Phase_Protocol_v2.1.docx")
        cls.before = {
            path.name: document_text(path)
            for path in (STUDY / "v2.1-before-closure").glob("*.docx")
        }

    def test_design_terms_match_in_both_languages(self):
        for name in ("manual", "pilot", "sap"):
            text = self.texts[name]
            self.assertIn("تخصيص عشوائي على مستوى الشخص", text)
            self.assertIn("تخصيص عشوائي عنقودي", text)
            self.assertIn("مقارنة شبه تجريبية مضبوطة", text)
            self.assertIn("individual-level randomization", text)
            self.assertIn("cluster-randomization", text)
            self.assertIn("quasi-experimental", text)
            self.assertIn("تصميم بديل", text)
            self.assertIn("alternative design", text)
            self.assertNotIn("تصغير عدد الدور", text)
        self.assertIn("عدد قليل من الدور", self.texts["sap"])
        self.assertIn("number of facilities is small", self.texts["sap"])

    def test_assessor_blinding_covers_three_paths_and_unblinding(self):
        for name in ("manual", "pilot", "sap"):
            text = self.texts[name]
            self.assertIn("من انكشفت له المعلومة", text)
            self.assertIn("who learned the allocation", text)
            self.assertIn("could not be maintained", text)
        sap = self.texts["sap"]
        for marker in (
            "later adopted is individual-level randomization",
            "later adopted is cluster-randomization by facility",
            "later adopted is a quasi-experimental controlled comparison",
        ):
            start = sap.index(marker)
            window = sap[start : start + 500]
            self.assertIn("Outcome assessors are blinded", window, marker)

    def test_attendance_formula_is_shared_and_table_5_is_bilingual(self):
        for name in ("manual", "pilot", "sap"):
            text = self.texts[name]
            self.assertIn("الجلسات المتاحة فعلًا", text)
            self.assertIn("sessions actually available", text)
            self.assertIn("ليس تحليلًا تأكيديًا", text)
            self.assertIn("not a confirmatory analysis", text)
        manual = self.texts["manual"]
        self.assertIn("Was this session actually available?", manual)
        self.assertIn("Was the session actually available to this person?", manual)
        sap = self.texts["sap"]
        self.assertIn(
            "Attendance proportion = available sessions attended ÷ sessions actually available",
            sap,
        )
        self.assertIn("enrolled count × 36", sap)

    def test_codesign_protocol_is_separate_and_not_started(self):
        text = self.codesign
        self.assertIn("has not started", text)
        self.assertIn("المرحلة لم تبدأ", text)
        self.assertIn("Older adults", text)
        self.assertIn("staff", text)
        self.assertIn("written notes only", text.lower())
        self.assertIn("no audio recording", text)
        self.assertIn("no video recording", text)
        self.assertIn("no approval identifier", text)
        self.assertIn("36", text)
        findings = audit_methods(text)
        severities = {item["severity"] for item in findings}
        self.assertNotIn(SEVERITY_CRITICAL, severities)
        self.assertNotIn(SEVERITY_REVISE, severities)
        self.assertIn(SEVERITY_OK, severities)

    def test_previous_version_is_kept_and_originals_are_unchanged(self):
        self.assertEqual(len(self.before), 4)
        old_manual = next(text for name, text in self.before.items() if "Manual" in name)
        self.assertIn("تخصيص على مستوى الشخص، أو تخصيص على مستوى الدار", old_manual)
        self.assertNotIn("تخصيص عشوائي عنقودي", old_manual)
        for name, digest in ORIGINALS.items():
            self.assertEqual(hashlib.sha256((STUDY / "original" / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(sum(1 for line in self.texts["manual"].splitlines() if line == "معلّقة / Pending"), 36)


if __name__ == "__main__":
    unittest.main()
