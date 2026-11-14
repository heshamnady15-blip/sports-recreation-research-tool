"""V2 checks use synthetic fixtures only. They do not call Crossref, DataCite, or journal sites."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "scientific-research" / "scripts"))

import verify_v2  # noqa: E402
from verify_v2 import (  # noqa: E402
    SEVERITY_CRITICAL,
    SEVERITY_OK,
    SEVERITY_REVISE,
    SEVERITY_UNVERIFIED,
    audit_methods,
    build_audit_report,
    default_lookup,
    format_apa7,
    parse_crossref_work,
    parse_datacite_doi,
    verify_journal_evidence,
    verify_references,
)

def setUpModule():
    patcher = patch("urllib.request.urlopen", side_effect=AssertionError("tests must not open a network connection"))
    patcher.start()


DOI = "10.5555/fixture.v2.match"
TITLE = "Synthetic movement study for fixture residents"
AUTHORS = ["Ada Lovelace", "Grace Hopper"]
CONTAINER = "Journal of Fixture Studies"


def matched_record(doi: str) -> dict:
    if doi != DOI:
        raise AssertionError(f"unexpected lookup for {doi}")
    return {
        "found": True,
        "source": "crossref",
        "title": TITLE,
        "year": 2024,
        "authors": AUTHORS,
        "container": CONTAINER,
        "volume": "4",
        "issue": "2",
        "pages": "10-12",
        "url": f"https://doi.org/{DOI}",
        "error": None,
    }


def offline_lookup(doi: str) -> dict:
    return {"found": None, "source": "fixture", "error": f"connection reset while asking about {doi}"}


def missing_lookup(doi: str) -> dict:
    return {"found": False, "source": "crossref+datacite", "error": "DOI not found"}


class ReferenceVerificationTests(unittest.TestCase):
    def test_matching_synthetic_doi_is_acceptable_and_uses_apa7(self):
        findings = verify_references(
            [
                {
                    "title": TITLE,
                    "year": 2024,
                    "doi": DOI,
                    "authors": AUTHORS,
                    "container": CONTAINER,
                }
            ],
            lookup=matched_record,
        )
        self.assertEqual(findings[0]["severity"], SEVERITY_OK)
        self.assertIn("https://doi.org/10.5555/fixture.v2.match", findings[0]["detail_en"])
        self.assertIn("Lovelace, A., & Hopper, G. (2024).", findings[0]["detail_en"])
        self.assertIn("*Journal of Fixture Studies*, 4(2), 10-12.", findings[0]["detail_en"])

    def test_inverted_datacite_names_match_natural_order_and_apa7(self):
        def lookup(doi: str) -> dict:
            record = matched_record(doi)
            record["source"] = "datacite"
            record["authors"] = ["Lovelace, Ada", "Hopper, Grace"]
            return record

        finding = verify_references(
            [
                {
                    "title": TITLE,
                    "year": 2024,
                    "doi": DOI,
                    "authors": ["Ada Lovelace", "Grace Hopper"],
                    "container": CONTAINER,
                }
            ],
            lookup=lookup,
        )[0]
        self.assertEqual(finding["severity"], SEVERITY_OK)
        self.assertIn("Lovelace, A., & Hopper, G. (2024).", finding["detail_en"])
        self.assertIn(f"https://doi.org/{DOI}", finding["detail_en"])
        self.assertNotIn("Ada, L.", finding["detail_en"])
        self.assertIn("*Journal of Fixture Studies*, 4(2), 10-12.", finding["detail_en"])

    def test_title_year_author_and_container_mismatches_are_critical(self):
        for reference, evidence in (
            ({"title": "A different invented title about Cairo homes", "year": 2024, "doi": DOI, "authors": AUTHORS}, "title"),
            ({"title": TITLE, "year": 1999, "doi": DOI, "authors": AUTHORS}, "year"),
            ({"title": TITLE, "year": 2024, "doi": DOI, "authors": ["Mary Seacole"]}, "authors"),
            ({"title": TITLE, "year": 2024, "doi": DOI, "authors": AUTHORS, "container": "Unrelated Fixture Proceedings"}, "container"),
        ):
            with self.subTest(evidence=evidence):
                finding = verify_references([reference], lookup=matched_record)[0]
                self.assertEqual(finding["severity"], SEVERITY_CRITICAL)
                self.assertIn(evidence, finding["evidence"])

    def test_unknown_doi_is_critical_and_connection_failure_is_not_success(self):
        missing = verify_references(
            [{"title": TITLE, "year": 2024, "doi": "10.5555/fixture.v2.missing"}],
            lookup=missing_lookup,
        )[0]
        offline = verify_references(
            [{"title": TITLE, "year": 2024, "doi": DOI}],
            lookup=offline_lookup,
        )[0]
        self.assertEqual(missing["severity"], SEVERITY_CRITICAL)
        self.assertEqual(offline["severity"], SEVERITY_UNVERIFIED)
        self.assertNotEqual(offline["severity"], SEVERITY_OK)
        self.assertIn("غير متحقق منها", offline["detail_ar"])

    def test_placeholder_doi_never_calls_lookup(self):
        def explode(doi: str) -> dict:
            raise AssertionError(doi)

        finding = verify_references(
            [{"title": "Placeholder fixture", "year": 2024, "doi": "10.1234/fixture.fake"}],
            lookup=explode,
        )[0]
        self.assertEqual(finding["severity"], SEVERITY_CRITICAL)

    def test_url_outcomes_stay_distinct(self):
        def fetch(url: str) -> dict:
            if url.endswith("/down"):
                return {"status": None, "body": "", "error": "timed out"}
            if url.endswith("/missing"):
                return {"status": 404, "body": "", "error": None}
            if url.endswith("/title"):
                return {"status": 200, "body": f"page about {TITLE}", "error": None}
            return {"status": 200, "body": "unrelated fixture page", "error": None}

        rows = verify_references(
            [
                {"title": TITLE, "year": 2024, "source_url": "https://fixture.local/title"},
                {"title": TITLE, "year": 2024, "source_url": "https://fixture.local/blank"},
                {"title": TITLE, "year": 2024, "source_url": "https://fixture.local/missing"},
                {"title": TITLE, "year": 2024, "source_url": "https://fixture.local/down"},
            ],
            fetch=fetch,
        )
        self.assertEqual([item["severity"] for item in rows], [SEVERITY_OK, SEVERITY_UNVERIFIED, SEVERITY_CRITICAL, SEVERITY_UNVERIFIED])

    def test_lookup_order_uses_datacite_after_crossref_404_and_transport_is_unverified(self):
        calls = []

        def getter(url: str, timeout: float):
            calls.append(url)
            if "crossref.org" in url and url.endswith("transport"):
                return None, "", "network down"
            if "crossref.org" in url:
                return 404, "", None
            if "datacite.org" in url and url.endswith("absent"):
                return 404, "", None
            if "datacite.org" in url and url.endswith("down"):
                return None, "", "datacite down"
            if "datacite.org" in url:
                body = json.dumps(
                    {
                        "data": {
                            "attributes": {
                                "doi": "10.5555/fixture.v2.datacite",
                                "titles": [{"title": TITLE}],
                                "publicationYear": "2024",
                                "creators": [{"name": "Lovelace, Ada"}],
                                "container": {"title": CONTAINER},
                            }
                        }
                    }
                )
                return 200, body, None
            raise AssertionError(url)

        found = default_lookup("10.5555/fixture.v2.datacite", getter=getter)
        self.assertTrue(found["found"])
        self.assertEqual(found["source"], "datacite")
        self.assertEqual(found["year"], 2024)
        self.assertEqual(calls[0].startswith("https://api.crossref.org/"), True)
        self.assertIn("api.datacite.org", calls[1])

        absent = default_lookup("10.5555/fixture.v2.absent", getter=getter)
        self.assertFalse(absent["found"])
        transport = default_lookup("10.5555/fixture.v2.transport", getter=getter)
        self.assertIsNone(transport["found"])
        datacite_down = default_lookup("10.5555/fixture.v2.down", getter=getter)
        self.assertIsNone(datacite_down["found"])

    def test_parsers_read_synthetic_payloads_without_adding_fields(self):
        crossref = parse_crossref_work(
            {
                "message": {
                    "DOI": DOI,
                    "title": [TITLE],
                    "author": [{"given": "Ada", "family": "Lovelace"}],
                    "issued": {"date-parts": [[2024]]},
                    "container-title": [CONTAINER],
                    "volume": "4",
                    "issue": "2",
                    "page": "10-12",
                }
            }
        )
        self.assertEqual(crossref["authors"], ["Ada Lovelace"])
        self.assertEqual(crossref["url"], f"https://doi.org/{DOI}")
        datacite = parse_datacite_doi(
            {"data": {"attributes": {"doi": DOI, "titles": [{"title": TITLE}], "publicationYear": "2024", "creators": []}}}
        )
        self.assertEqual(datacite["year"], 2024)
        apa = format_apa7({"authors": [f"Author {index} Example" for index in range(1, 22)], "year": 2024, "title": "Long fixture"}, DOI)
        self.assertIn("... Example, A.", apa)
        self.assertNotIn("Author 20", apa)


class JournalEvidenceTests(unittest.TestCase):
    def evidence(self, **overrides) -> dict:
        record = {
            "name": "Fixture Ageing Journal",
            "index": "scopus",
            "quartile": "Q1",
            "subject_category": "Physiotherapy",
            "classification_year": 2026,
            "indexing_source": "scopus_sources",
            "indexing_url": "https://fixture.local/scopus-sources",
            "indexing_opened_on": "2026-11-14",
            "indexing_excerpt": "Scopus Q1 2026 Physiotherapy",
            "apc_mandatory": False,
            "apc_source": "publisher_journal_page",
            "apc_url": "https://fixture.local/publisher-fees",
            "apc_opened_on": "2026-11-14",
            "apc_excerpt": "No mandatory author fee. Optional open access is separate.",
        }
        record.update(overrides)
        return record

    def fetch(self, url: str) -> dict:
        pages = {
            "https://fixture.local/scopus-sources": "Catalogue Scopus Q1 2026 Physiotherapy for the fixture.",
            "https://fixture.local/publisher-fees": "No mandatory author fee. Optional open access is separate.",
        }
        if url == "https://fixture.local/down":
            return {"status": None, "body": "", "error": "connection failed"}
        if url not in pages:
            return {"status": 404, "body": "", "error": None}
        return {"status": 200, "body": pages[url], "error": None}

    def test_complete_q1_evidence_is_acceptable_only_as_supplied_evidence(self):
        finding = verify_journal_evidence(self.evidence(), fetch=self.fetch)[0]
        self.assertEqual(finding["severity"], SEVERITY_OK)
        self.assertIn("not an independent scrape", finding["detail_en"])

        def fetch_q2(url: str) -> dict:
            if "fees" in url:
                return {"status": 200, "body": "No mandatory author fee. Optional open access is separate.", "error": None}
            return {"status": 200, "body": "Indexed as Scopus Q2 2026 Physiotherapy.", "error": None}

        q2 = verify_journal_evidence(
            self.evidence(quartile="Q2", indexing_excerpt="Scopus Q2 2026 Physiotherapy"),
            fetch=fetch_q2,
        )[0]
        self.assertEqual(q2["severity"], SEVERITY_OK)
        self.assertIn("Q2", q2["evidence"])

    def test_incomplete_unreachable_paid_and_mismatched_evidence_are_not_recommendations(self):
        incomplete = verify_journal_evidence(self.evidence(subject_category="", indexing_excerpt=""), fetch=self.fetch)[0]
        paid = verify_journal_evidence(self.evidence(apc_mandatory=True), fetch=self.fetch)[0]
        down = verify_journal_evidence(
            self.evidence(indexing_url="https://fixture.local/down"),
            fetch=self.fetch,
        )[0]
        mismatch = verify_journal_evidence(
            self.evidence(indexing_excerpt="Scopus Q1 2026 Physiotherapy extra clause"),
            fetch=self.fetch,
        )[0]
        self.assertEqual(incomplete["severity"], SEVERITY_UNVERIFIED)
        self.assertEqual(paid["severity"], SEVERITY_CRITICAL)
        self.assertEqual(down["severity"], SEVERITY_UNVERIFIED)
        self.assertEqual(mismatch["severity"], SEVERITY_REVISE)
        for finding in (incomplete, paid, down, mismatch):
            self.assertNotEqual(finding["severity"], SEVERITY_OK)


class MethodsAuditTests(unittest.TestCase):
    def test_single_group_rct_unsupported_numbers_and_artistic_judging_are_critical(self):
        text = """
        This single-group study is a randomized controlled trial of Gymnastics for All.
        البيانات غير متوفرة.
        p < 0.05 and Cohen's d = 0.80.
        القيمة الاحتمالية بلغت 0.03.
        شارك 30 مشارك.
        لا توجد موافقة، ورقم الموافقة SYNTH-14.
        استُخدمت D-score من تحكيم الجمباز الفني.
        """
        severities = {item["topic"]: item["severity"] for item in audit_methods(text)}
        self.assertEqual(severities["design"], SEVERITY_CRITICAL)
        self.assertEqual(severities["statistics"], SEVERITY_CRITICAL)
        self.assertEqual(severities["ethics"], SEVERITY_CRITICAL)
        self.assertEqual(severities["domain"], SEVERITY_CRITICAL)

    def test_designs_stay_distinct_and_an_unattached_approval_number_is_unverifiable(self):
        conflict = audit_methods(
            "The executed design is individually randomized and also cluster-randomized. "
            "The analysis is an independent t-test. Primary outcomes were both function and quality of life, p = 0.20."
        )
        topics = {item["topic"] for item in conflict if item["severity"] == SEVERITY_REVISE}
        self.assertIn("design", topics)
        self.assertIn("analysis", topics)
        approval = audit_methods("Ethics approval number SYNTH-77 is listed in the draft.")
        self.assertEqual(approval[0]["severity"], SEVERITY_UNVERIFIED)
        self.assertNotEqual(approval[0]["severity"], SEVERITY_OK)

    def test_clean_quasi_experimental_text_has_no_critical_pattern(self):
        findings = audit_methods(
            "التصميم شبه تجريبي بمجموعة مقارنة غير متكافئة. البيانات غير متوفرة، لذلك لا تُكتب نتيجة."
        )
        self.assertEqual(findings[0]["severity"], SEVERITY_OK)
        self.assertIn("ليس حكمًا بصحة المنهج", findings[0]["detail_ar"])


class ReportTests(unittest.TestCase):
    def test_report_is_bilingual_and_does_not_treat_offline_as_success(self):
        report = build_audit_report(
            references=[{"title": TITLE, "year": 2024, "doi": DOI}],
            journal={"name": "Fixture Ageing Journal"},
            manuscript="",
            lookup=offline_lookup,
        )
        self.assertFalse(report["passed"])
        self.assertTrue(report["automated_audit_is_not_full_scientific_validation"])
        self.assertIn("لا يثبت الصحة العلمية الكاملة", report["arabic"])
        self.assertIn("does not establish the full scientific validity", report["english"])
        self.assertGreater(report["counts"][SEVERITY_UNVERIFIED], 0)
        self.assertEqual(report["counts"][SEVERITY_OK], 0)

    def test_cli_offline_reference_check_exits_with_failure(self):
        import subprocess

        script = ROOT / ".agents/skills/scientific-research/scripts/policy.py"
        completed = subprocess.run(
            [sys.executable, str(script), "verify-references", "--path", str(Path(__file__).with_name("fixtures") / "v2-reference.json"), "--offline"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual(payload["findings"][0]["severity"], SEVERITY_UNVERIFIED)


if __name__ == "__main__":
    unittest.main()
