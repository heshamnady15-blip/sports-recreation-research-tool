#!/usr/bin/env python3
"""Executable rules for the scientific-research skill.

The functions decide whether a journal may be recommended, whether a numeric
similarity limit may be applied, and whether a reference or a section review
is complete. They do not invent bibliographic records or measurements.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = SKILL_ROOT / "references" / "official-snapshot.json"
PROFILE_TEMPLATE = SKILL_ROOT / "assets" / "researcher-profile.template.json"

PROFILE_FIELDS = (
    "name",
    "university",
    "department",
    "institutional_email",
    "orcid",
)

PRODUCTS = {
    "original",
    "promotion",
    "thesis",
    "systematic_review",
    "meta_analysis",
    "thesis_to_article",
}

DESIGNS = {
    "quantitative",
    "qualitative",
    "mixed",
    "experimental",
    "descriptive",
    "correlational",
    "systematic_review",
    "meta_analysis",
}

INDEXING_SOURCES = {"scu_digital_library_report", "scopus_sources"}
APC_SOURCES = {"publisher_journal_page", "publisher_price_list"}
PRIORITY_QUARTILES = {"Q1", "Q2"}
FALLBACK_QUARTILES = {"Q3", "Q4"}
PUBLIC_EMAIL_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com"}
ORCID_RE = re.compile(r"^(?:https?://orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$")
PLACEHOLDER_DOI_RE = re.compile(r"^10\.(?:0000|1234)/", re.I)
REVIEW_CRITERIA = ("المنهجية", "التحليل الإحصائي", "الأصالة", "الأخلاقيات")
REVIEW_VERDICTS = {"مقبول", "يحتاج تعديل", "غير قابل للتحقق"}

PRODUCT_SIMILARITY_SCOPE = {
    "promotion": "promotion_dossier",
    "thesis": "university_thesis",
    "original": "journal",
    "systematic_review": "journal",
    "meta_analysis": "journal",
    "thesis_to_article": "journal",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def journal_decision(
    *,
    index: str,
    quartile: str,
    apc_mandatory: bool,
    indexing_source: str | None,
    apc_source: str | None,
    predatory: bool = False,
    allow_q3_q4: bool = False,
    publication_year: int | None = None,
) -> dict:
    """Decide whether a journal meets the skill's publication rule.

    A recommendation requires a Scopus quartile verified from Scopus Sources or
    from the Supreme Council digital-library report, plus an author-fee status
    verified from the publisher. Unverified records are not recommended.
    """
    reasons: list[str] = []
    if predatory:
        reasons.append("السجل موسوم بأنه مجلة مزيفة أو غير معتبرة، والمادة 17 من قواعد الدورة 15 لا تعتد بالأبحاث المنشورة في المجلات المزيفة.")
        return _journal_result(False, "rejected", reasons, publication_year)
    if indexing_source not in INDEXING_SOURCES:
        reasons.append("تصنيف الفهرسة غير موثق من Scopus Sources أو من تقرير وحدة المكتبات الرقمية بالمجلس الأعلى للجامعات.")
    if apc_source not in APC_SOURCES:
        reasons.append("حالة رسوم النشر غير موثقة من صفحة الناشر أو قائمة أسعاره الرسمية.")
    if index != "scopus":
        reasons.append("أولوية هذه المهارة للمجلات المفهرسة في Scopus. وجود قاعدة أخرى لا يغني عن تحقق Scopus.")
    if quartile not in PRIORITY_QUARTILES | FALLBACK_QUARTILES:
        reasons.append("الربع غير معروف. لا يُستبدل بتخمين.")
    if apc_mandatory:
        reasons.append("توجد رسوم نشر إلزامية على المؤلف، وهذا يخرج المجلة من نطاق المهارة.")
    if publication_year is None:
        reasons.append("سنة النشر أو سنة التصنيف غير محددة. التصنيف يُؤخذ لسنة النشر.")

    verified = not any(
        item.startswith("تصنيف") or item.startswith("حالة رسوم") or item.startswith("سنة")
        for item in reasons
    )
    if not verified or index != "scopus" or apc_mandatory or predatory:
        tier = "unverified" if not verified else "rejected"
        recommend = False
        if not reasons:
            reasons.append("السجل لا يستوفي شرط التوصية.")
        return _journal_result(recommend, tier, reasons, publication_year)

    if quartile in PRIORITY_QUARTILES:
        reasons.append(f"مجلة Scopus {quartile} بلا رسوم نشر إلزامية موثقة، ضمن الأولوية.")
        return _journal_result(True, "priority", reasons, publication_year)
    if allow_q3_q4:
        reasons.append(f"مجلة Scopus {quartile} بلا رسوم إلزامية. القبول احتياطي لأن الأولوية تبقى لـ Q1 وQ2.")
        return _journal_result(True, "fallback", reasons, publication_year)
    reasons.append(f"مجلة Scopus {quartile} بلا رسوم إلزامية، ولا تُعرض إلا إذا طُلب صراحة دعم Q3 أو Q4.")
    return _journal_result(False, "rejected", reasons, publication_year)


def _journal_result(recommend: bool, tier: str, reasons: list[str], publication_year: int | None) -> dict:
    return {
        "recommend": recommend,
        "tier": tier,
        "publication_year": publication_year,
        "reasons": reasons,
    }


def similarity_guidance(*, product: str, official_limit: dict | None) -> dict:
    """Return a numeric similarity limit only when an official source matches the product scope."""
    if product not in PRODUCTS:
        return {
            "apply_numeric_limit": False,
            "blocked_reason": "نوع المنتج غير معروف، لذلك لا يُفرض حد تشابه.",
        }
    expected_scope = PRODUCT_SIMILARITY_SCOPE[product]
    if not official_limit:
        return {
            "apply_numeric_limit": False,
            "scope": expected_scope,
            "blocked_reason": "لا يوجد حد رسمي محمّل لهذه الجلسة. لا تضع نسبة من عندك.",
        }
    source_url = str(official_limit.get("source_url") or "").strip()
    checked_on = str(official_limit.get("checked_on") or "").strip()
    scope = str(official_limit.get("scope") or "").strip()
    if not source_url or not checked_on:
        return {
            "apply_numeric_limit": False,
            "scope": expected_scope,
            "blocked_reason": "الحد الرسمي ناقص المصدر أو تاريخ التحقق.",
        }
    if scope != expected_scope:
        return {
            "apply_numeric_limit": False,
            "scope": expected_scope,
            "blocked_reason": (
                f"الحد المحمّل خاص بنطاق {scope or 'غير محدد'} ولا يُطبّق على {product}. "
                "حد ملف الترقية لا يُنسخ إلى المقال أو الرسالة إلا إذا نص مصدر ذلك المنتج على الحد نفسه."
            ),
        }
    single = official_limit.get("single_paper_max")
    aggregate = official_limit.get("aggregate_max")
    if not isinstance(single, (int, float)) or not isinstance(aggregate, (int, float)):
        return {
            "apply_numeric_limit": False,
            "scope": expected_scope,
            "blocked_reason": "المصدر الرسمي لا يعطي حدًا رقميًا قابلًا للتطبيق.",
        }
    return {
        "apply_numeric_limit": True,
        "scope": expected_scope,
        "single_paper_max": single,
        "aggregate_max": aggregate,
        "source_url": source_url,
        "checked_on": checked_on,
        "tool": official_limit.get("tool"),
        "exemption": official_limit.get("exemption"),
        "statement": (
            "يُستخدم هذا الحد فقط داخل نطاقه الرسمي، مع ذكر المصدر وتاريخ التحقق. "
            "ليس حدًا ثابتًا للمهارة ولا يُدرج في متن البحث كسياسة داخلية."
        ),
    }


def load_promotion_snapshot() -> dict:
    raw = load_json(SNAPSHOT_PATH)
    return {
        "scope": raw["product_scope"],
        "single_paper_max": raw["single_paper_highest_similarity_max"],
        "aggregate_max": raw["aggregate_max"],
        "source_url": raw["sources"][0]["url"],
        "checked_on": raw["checked_on"],
        "tool": raw.get("tool"),
        "exemption": raw.get("exemption"),
    }


def profile_status(profile: dict | None) -> dict:
    if profile is None:
        return {
            "complete": False,
            "missing": list(PROFILE_FIELDS),
            "warnings": ["انسخ قالب الباحث واملأ الحقول. لا تخترع الاسم أو الجامعة أو ORCID."],
        }
    missing = [field for field in PROFILE_FIELDS if not str(profile.get(field) or "").strip()]
    warnings: list[str] = []
    email = str(profile.get("institutional_email") or "").strip()
    if email:
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            missing.append("institutional_email")
            warnings.append("البريد غير صالح.")
        else:
            domain = email.rsplit("@", 1)[1].lower()
            if domain in PUBLIC_EMAIL_DOMAINS:
                warnings.append("البريد ليس على نطاق مؤسسة. الحقل مخصص للبريد المؤسسي.")
    orcid = str(profile.get("orcid") or "").strip()
    if orcid and not ORCID_RE.match(orcid):
        missing.append("orcid")
        warnings.append("ORCID لا يطابق الصيغة 0000-0000-0000-0000.")
    # A field can be both empty and invalid; keep the list stable.
    missing = list(dict.fromkeys(missing))
    return {"complete": not missing, "missing": missing, "warnings": warnings}


def validate_references(references: list[dict]) -> list[str]:
    issues: list[str] = []
    if not references:
        return ["قائمة المراجع فارغة. لا تُستكمل بمراجع غير مسترجعة."]
    for index, ref in enumerate(references, start=1):
        title = str(ref.get("title") or "").strip()
        year = ref.get("year")
        doi = str(ref.get("doi") or "").strip()
        source_url = str(ref.get("source_url") or "").strip()
        if not title:
            issues.append(f"المرجع {index}: العنوان مفقود.")
        if not isinstance(year, int):
            issues.append(f"المرجع {index}: سنة النشر مفقودة أو غير رقمية.")
        if not doi and not source_url:
            issues.append(f"المرجع {index}: لا DOI ولا رابط مصدر. لا يُكتب المرجع.")
        if doi and PLACEHOLDER_DOI_RE.search(doi):
            issues.append(f"المرجع {index}: DOI عنصر نائب وليس معرفًا مسترجعًا.")
        if source_url and _placeholder_url(source_url):
            issues.append(f"المرجع {index}: الرابط عنصر نائب.")
    return issues


def _placeholder_url(url: str) -> bool:
    lowered = url.lower()
    return any(token in lowered for token in ("example.com", "example.org", "doi.org/10.0000", "doi.org/10.1234"))


def review_issues(text: str, sections: list[str]) -> list[str]:
    issues: list[str] = []
    if not text.strip():
        return ["تقرير المراجعة فارغ."]
    for section in sections:
        marker = f"## قسم: {section}"
        start = text.find(marker)
        if start < 0:
            issues.append(f"القسم '{section}' بلا مراجعة مستقلة.")
            continue
        next_heading = text.find("\n## قسم:", start + len(marker))
        block = text[start:] if next_heading < 0 else text[start:next_heading]
        for criterion in REVIEW_CRITERIA:
            if f"### {criterion}" not in block:
                issues.append(f"قسم {section}: معيار '{criterion}' غير موجود.")
        verdict_line = ""
        for line in block.splitlines():
            if line.startswith("### الحكم"):
                continue
            if line.strip() in REVIEW_VERDICTS and "### الحكم" in block:
                verdict_line = line.strip()
                break
        if "### الحكم" not in block or verdict_line not in REVIEW_VERDICTS:
            issues.append(f"قسم {section}: الحكم يجب أن يكون أحد {sorted(REVIEW_VERDICTS)}.")
        if "غير متوفر" in block and re.search(r"p\s*[<=>]", block, flags=re.I):
            issues.append(f"قسم {section}: يذكر نتيجة إحصائية بينما البيانات غير متوفرة.")
    return issues


def _print_json(payload: dict) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="قواعد مهارة البحث العلمي")
    sub = parser.add_subparsers(dest="command", required=True)

    journal = sub.add_parser("journal")
    journal.add_argument("--index", required=True)
    journal.add_argument("--quartile", required=True)
    journal.add_argument("--apc-mandatory", required=True, choices=("true", "false"))
    journal.add_argument("--indexing-source")
    journal.add_argument("--apc-source")
    journal.add_argument("--predatory", action="store_true")
    journal.add_argument("--allow-q3-q4", action="store_true")
    journal.add_argument("--publication-year", type=int)

    similarity = sub.add_parser("similarity")
    similarity.add_argument("--product", required=True)
    similarity.add_argument("--snapshot", action="store_true")
    similarity.add_argument("--limit-json")

    profile = sub.add_parser("profile")
    profile.add_argument("--path")

    references = sub.add_parser("references")
    references.add_argument("--path", required=True)

    review = sub.add_parser("review")
    review.add_argument("--path", required=True)
    review.add_argument("--section", action="append", required=True)

    verify_refs = sub.add_parser("verify-references")
    verify_refs.add_argument("--path", required=True)
    verify_refs.add_argument("--offline", action="store_true")

    verify_journal = sub.add_parser("verify-journal")
    verify_journal.add_argument("--path", required=True)
    verify_journal.add_argument("--offline", action="store_true")

    audit_methods_cmd = sub.add_parser("audit-methods")
    audit_methods_cmd.add_argument("--path", required=True)

    audit = sub.add_parser("audit")
    audit.add_argument("--references")
    audit.add_argument("--journal")
    audit.add_argument("--manuscript")
    audit.add_argument("--offline", action="store_true")

    args = parser.parse_args(argv)
    if args.command == "journal":
        _print_json(
            journal_decision(
                index=args.index,
                quartile=args.quartile,
                apc_mandatory=args.apc_mandatory == "true",
                indexing_source=args.indexing_source,
                apc_source=args.apc_source,
                predatory=args.predatory,
                allow_q3_q4=args.allow_q3_q4,
                publication_year=args.publication_year,
            )
        )
        return 0
    if args.command == "similarity":
        limit = None
        if args.snapshot:
            limit = load_promotion_snapshot()
        elif args.limit_json:
            limit = json.loads(args.limit_json)
        _print_json(similarity_guidance(product=args.product, official_limit=limit))
        return 0
    if args.command == "profile":
        path = Path(args.path) if args.path else None
        data = load_json(path) if path and path.is_file() else None
        _print_json(profile_status(data))
        return 0
    if args.command == "references":
        payload = load_json(Path(args.path))
        issues = validate_references(payload)
        _print_json({"ok": not issues, "issues": issues})
        return 0 if not issues else 1
    if args.command == "review":
        text = Path(args.path).read_text(encoding="utf-8")
        issues = review_issues(text, args.section)
        _print_json({"ok": not issues, "issues": issues})
        return 0 if not issues else 1
    if args.command in {"verify-references", "verify-journal", "audit-methods", "audit"}:
        from verify_v2 import build_audit_report

        def unreachable(doi: str) -> dict:
            return {"found": None, "source": "offline", "error": "offline"}

        def unreachable_fetch(url: str) -> dict:
            return {"status": None, "body": "", "error": "offline"}

        lookup = unreachable if getattr(args, "offline", False) else None
        fetch = unreachable_fetch if getattr(args, "offline", False) else None
        references = journal = manuscript = None
        if args.command == "verify-references":
            references = load_json(Path(args.path))
        elif args.command == "verify-journal":
            journal = load_json(Path(args.path))
        elif args.command == "audit-methods":
            manuscript = Path(args.path).read_text(encoding="utf-8")
        else:
            if args.references:
                references = load_json(Path(args.references))
            if args.journal:
                journal = load_json(Path(args.journal))
            if args.manuscript:
                manuscript = Path(args.manuscript).read_text(encoding="utf-8")
        report = build_audit_report(
            references=references,
            journal=journal,
            manuscript=manuscript,
            lookup=lookup,
            fetch=fetch,
        )
        _print_json(report)
        return 0 if report["passed"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
