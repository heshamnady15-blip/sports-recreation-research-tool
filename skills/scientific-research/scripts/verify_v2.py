#!/usr/bin/env python3
"""Scientific Research Skill V2 checks.

These checks add DOI lookup, journal-evidence review, and methodology
pattern checks. They do not replace the structural helpers in policy.py,
and a passing report is not a claim that a study is scientifically valid.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from typing import Callable

SEVERITY_CRITICAL = "خطأ حرج"
SEVERITY_REVISE = "يحتاج تعديل"
SEVERITY_UNVERIFIED = "غير قابل للتحقق"
SEVERITY_OK = "مقبول"
REFERENCE_UNVERIFIED = "غير متحقق منها"
SEVERITIES = (SEVERITY_CRITICAL, SEVERITY_REVISE, SEVERITY_UNVERIFIED, SEVERITY_OK)

INDEXING_SOURCES = {"scu_digital_library_report", "scopus_sources"}
APC_SOURCES = {"publisher_journal_page", "publisher_price_list"}
PRIORITY_QUARTILES = {"Q1", "Q2"}
USER_AGENT = "scientific-research-skill/2.0"

DISCLAIMER_AR = (
    "هذا التدقيق الآلي لا يثبت الصحة العلمية الكاملة للبحث. "
    "يفحص الأدلة المعروضة والأنماط النصية فقط، ولا يجمع بيانات ولا يحكم على صدق الدراسة في الميدان."
)
DISCLAIMER_EN = (
    "This automated audit does not establish the full scientific validity of the study. "
    "It checks the supplied evidence and textual patterns only. It does not collect data "
    "and does not judge whether the study is true in the field."
)

Lookup = Callable[[str], dict]
Fetch = Callable[[str], dict]


def finding(
    *,
    severity: str,
    topic: str,
    evidence: str,
    detail_ar: str,
    detail_en: str,
) -> dict:
    if severity not in SEVERITIES:
        raise ValueError(f"unknown severity: {severity}")
    return {
        "severity": severity,
        "topic": topic,
        "evidence": evidence,
        "detail_ar": detail_ar,
        "detail_en": detail_en,
    }


def _normalize(value: str) -> str:
    text = value.casefold()
    text = text.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ى": "ي"}))
    text = re.sub(r"[^0-9a-z\u0600-\u06ff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _similar(left: str, right: str) -> float:
    a = _normalize(left)
    b = _normalize(right)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if len(a) >= 24 and len(b) >= 24 and (a in b or b in a):
        return 0.9
    return SequenceMatcher(None, a, b).ratio()


def _split_author(author: str) -> tuple[str, list[str]]:
    """Return family name and given-name parts. A comma marks Family, Given order."""
    raw = " ".join(author.replace("،", ",").split())
    if "," in raw:
        family, given = raw.split(",", 1)
        return family.strip(), [part for part in given.split() if part]
    parts = [part for part in raw.split() if part]
    if not parts:
        return "", []
    if len(parts) == 1:
        return parts[0], []
    return parts[-1], parts[:-1]


def _family_names(authors: list[str]) -> set[str]:
    names: set[str] = set()
    for author in authors:
        family, _given = _split_author(str(author))
        normalized = _normalize(family)
        if normalized:
            names.add(normalized)
    return names


def _doi_key(value: str) -> str:
    text = value.strip()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text, flags=re.I)
    return text


def _placeholder_doi(doi: str) -> bool:
    return bool(re.search(r"^10\.(?:0000|1234)/", doi, flags=re.I))


def _placeholder_url(url: str) -> bool:
    lowered = url.lower()
    return any(token in lowered for token in ("example.com", "example.org", "doi.org/10.0000", "doi.org/10.1234"))


def _http_get(url: str, timeout: float) -> tuple[int | None, str, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/html;q=0.8,*/*;q=0.5"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            raw = response.read(300_000)
            charset = "utf-8"
            content_type = response.headers.get("Content-Type", "")
            match = re.search(r"charset=([\w.-]+)", content_type, flags=re.I)
            if match:
                charset = match.group(1)
            return status, raw.decode(charset, errors="replace"), None
    except urllib.error.HTTPError as exc:
        return exc.code, "", None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, "", str(exc)


def parse_crossref_work(payload: dict) -> dict:
    message = payload.get("message") or {}
    authors = []
    for author in message.get("author") or []:
        authors.append(" ".join(part for part in (author.get("given"), author.get("family")) if part))
    year_parts = (message.get("issued") or {}).get("date-parts") or [[None]]
    year = year_parts[0][0] if year_parts and year_parts[0] else None
    doi = message.get("DOI") or ""
    return {
        "found": True,
        "source": "crossref",
        "title": ((message.get("title") or [""])[0] or ""),
        "year": year,
        "authors": [item for item in authors if item],
        "container": ((message.get("container-title") or [""])[0] or ""),
        "volume": message.get("volume") or "",
        "issue": message.get("issue") or "",
        "pages": message.get("page") or "",
        "url": message.get("URL") or (f"https://doi.org/{doi}" if doi else ""),
        "error": None,
    }


def parse_datacite_doi(payload: dict) -> dict:
    attributes = ((payload.get("data") or {}).get("attributes") or {})
    titles = attributes.get("titles") or []
    title = (titles[0].get("title") if titles else "") or ""
    authors = []
    for creator in attributes.get("creators") or []:
        name = creator.get("name") or ""
        if not name and (creator.get("givenName") or creator.get("familyName")):
            name = " ".join(part for part in (creator.get("givenName"), creator.get("familyName")) if part)
        if name:
            authors.append(name)
    container = ((attributes.get("container") or {}).get("title") or "")
    if not container:
        for item in attributes.get("relatedItems") or []:
            if item.get("relationType") in {"IsPublishedIn", "IsPartOf"}:
                related_titles = item.get("titles") or [{}]
                container = related_titles[0].get("title") or container
                if container:
                    break
    doi = attributes.get("doi") or ""
    year = attributes.get("publicationYear")
    return {
        "found": True,
        "source": "datacite",
        "title": title,
        "year": int(year) if str(year or "").isdigit() else year,
        "authors": authors,
        "container": container,
        "volume": "",
        "issue": "",
        "pages": "",
        "url": f"https://doi.org/{doi}" if doi else "",
        "error": None,
    }


def default_lookup(doi: str, *, timeout: float = 20, getter=None) -> dict:
    """Resolve a DOI from Crossref, then DataCite. Transport failure is not a match."""
    get = getter or _http_get
    key = urllib.parse.quote(_doi_key(doi))
    status, body, error = get(f"https://api.crossref.org/works/{key}", timeout)
    if status is None:
        return {"found": None, "source": "crossref", "error": error or "crossref unavailable"}
    if status == 200:
        try:
            return parse_crossref_work(json.loads(body))
        except json.JSONDecodeError as exc:
            return {"found": None, "source": "crossref", "error": f"crossref JSON: {exc}"}
    if status != 404:
        return {"found": None, "source": "crossref", "error": f"crossref HTTP {status}"}

    status, body, error = get(f"https://api.datacite.org/dois/{key}", timeout)
    if status is None:
        return {"found": None, "source": "datacite", "error": error or "datacite unavailable"}
    if status == 200:
        try:
            return parse_datacite_doi(json.loads(body))
        except json.JSONDecodeError as exc:
            return {"found": None, "source": "datacite", "error": f"datacite JSON: {exc}"}
    if status == 404:
        return {"found": False, "source": "crossref+datacite", "error": "DOI not found"}
    return {"found": None, "source": "datacite", "error": f"datacite HTTP {status}"}


def default_fetch(url: str, *, timeout: float = 20) -> dict:
    status, body, error = _http_get(url, timeout)
    if status is None:
        return {"status": None, "body": "", "error": error or "connection failed"}
    return {"status": status, "body": body, "error": None}


def format_apa7(meta: dict, doi: str = "") -> str:
    """Format a verified record in APA 7. Missing metadata is left out rather than invented."""
    authors = _apa_authors(meta.get("authors") or [])
    year = meta.get("year")
    title = (meta.get("title") or "").strip().rstrip(".")
    container = (meta.get("container") or "").strip()
    year_text = str(year) if isinstance(year, int) else "n.d."
    parts = [f"{authors} ({year_text}). {title}."]
    if container:
        citation = f"*{container}*"
        volume = str(meta.get("volume") or "").strip()
        issue = str(meta.get("issue") or "").strip()
        pages = str(meta.get("pages") or "").strip()
        if volume:
            citation += f", {volume}"
            if issue:
                citation += f"({issue})"
        if pages:
            citation += f", {pages}"
        parts.append(citation + ".")
    link = ""
    if doi:
        link = "https://doi.org/" + _doi_key(doi)
    elif meta.get("url"):
        link = str(meta["url"])
    if link:
        parts.append(link)
    return " ".join(parts)


def _apa_authors(authors: list[str]) -> str:
    if not authors:
        return "مؤلف غير مؤكد"
    formatted = [_apa_person(author) for author in authors if author.strip()]
    if not formatted:
        return "Unspecified author"
    if len(formatted) > 20:
        head = ", ".join(formatted[:19])
        return f"{head}, ... {formatted[-1]}"
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + ", & " + formatted[-1]


def _apa_person(author: str) -> str:
    family, given_parts = _split_author(author)
    if not family:
        return ""
    initials = " ".join(f"{part[0].upper()}." for part in given_parts if part)
    return f"{family}, {initials}" if initials else family


def verify_references(
    references: list[dict],
    *,
    lookup: Lookup | None = None,
    fetch: Fetch | None = None,
) -> list[dict]:
    """Check each reference. Unresolved external lookups stay unverified, never correct."""
    if not references:
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic="references",
                evidence="empty list",
                detail_ar="قائمة المراجع فارغة. لا تُستكمل بمراجع غير مسترجعة.",
                detail_en="The reference list is empty. It is not completed with unrecovered sources.",
            )
        ]
    resolver = lookup or default_lookup
    opener = fetch or default_fetch
    results = []
    for index, reference in enumerate(references, start=1):
        results.extend(_verify_one_reference(index, reference, resolver, opener))
    return results


def _verify_one_reference(index: int, reference: dict, lookup: Lookup, fetch: Fetch) -> list[dict]:
    title = str(reference.get("title") or "").strip()
    year = reference.get("year")
    doi = _doi_key(str(reference.get("doi") or ""))
    source_url = str(reference.get("source_url") or reference.get("url") or "").strip()
    topic = f"reference {index}"
    if not title or not isinstance(year, int) or (not doi and not source_url):
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic=topic,
                evidence=json.dumps({"title": title, "year": year, "doi": doi, "source_url": source_url}, ensure_ascii=False),
                detail_ar="المرجع ينقصه عنوان أو سنة رقمية أو مصدر.",
                detail_en="The reference is missing a title, a numeric year, or a source.",
            )
        ]
    if doi and _placeholder_doi(doi):
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic=topic,
                evidence=doi,
                detail_ar="معرف DOI عنصر نائب. لا يُعد مرجعًا صحيحًا.",
                detail_en="The DOI is a placeholder and is not a valid reference.",
            )
        ]
    if source_url and _placeholder_url(source_url):
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic=topic,
                evidence=source_url,
                detail_ar="رابط المرجع عنصر نائب.",
                detail_en="The reference URL is a placeholder.",
            )
        ]
    if doi:
        return [_judge_doi(topic, reference, title, year, doi, lookup)]
    return [_judge_url(topic, title, source_url, fetch)]


def _judge_doi(topic: str, reference: dict, title: str, year: int, doi: str, lookup: Lookup) -> dict:
    try:
        record = lookup(doi)
    except (urllib.error.URLError, TimeoutError, OSError, ConnectionError) as exc:
        record = {"found": None, "error": str(exc), "source": "lookup"}
    found = record.get("found") if isinstance(record, dict) else None
    if found is None:
        return finding(
            severity=SEVERITY_UNVERIFIED,
            topic=topic,
            evidence=str(record.get("error") or "lookup failed") if isinstance(record, dict) else "lookup failed",
            detail_ar=f"تعذر فحص DOI {doi}. الحالة «غير متحقق منها» وليست مرجعًا صحيحًا.",
            detail_en=f"DOI {doi} could not be checked. The status is unverified, not correct.",
        )
    if found is False:
        return finding(
            severity=SEVERITY_CRITICAL,
            topic=topic,
            evidence=doi,
            detail_ar=f"DOI {doi} غير موجود في Crossref ولا DataCite.",
            detail_en=f"DOI {doi} was not found in Crossref or DataCite.",
        )
    mismatches = []
    title_score = _similar(title, str(record.get("title") or ""))
    if title_score < 0.82:
        mismatches.append(f"title {title_score:.2f}")
    if record.get("year") != year:
        mismatches.append(f"year cited {year} / source {record.get('year')}")
    cited_authors = reference.get("authors") or []
    if cited_authors:
        cited = _family_names([str(item) for item in cited_authors])
        found_names = _family_names([str(item) for item in record.get("authors") or []])
        if not cited or not cited <= found_names:
            mismatches.append("authors")
    container = str(reference.get("container") or "").strip()
    if container and _similar(container, str(record.get("container") or "")) < 0.6:
        mismatches.append("container")
    source_name = record.get("source") or "external"
    link = f"https://doi.org/{doi}"
    apa = format_apa7(record, doi)
    evidence = f"{source_name}; {link}; match={1 - len(mismatches) / 4:.2f}"
    if mismatches:
        return finding(
            severity=SEVERITY_CRITICAL,
            topic=topic,
            evidence=evidence + "; " + ", ".join(mismatches),
            detail_ar=f"بيانات المرجع لا تطابق {source_name}. APA غير معتمد: {apa}",
            detail_en=f"The citation does not match {source_name}. Unadopted APA: {apa}",
        )
    return finding(
        severity=SEVERITY_OK,
        topic=topic,
        evidence=evidence,
        detail_ar=f"تطابقت البيانات مع {source_name}. APA 7: {apa}",
        detail_en=f"The record matches {source_name}. APA 7: {apa}",
    )


def _judge_url(topic: str, title: str, source_url: str, fetch: Fetch) -> dict:
    try:
        opened = fetch(source_url)
    except (urllib.error.URLError, TimeoutError, OSError, ConnectionError) as exc:
        opened = {"status": None, "body": "", "error": str(exc)}
    status = opened.get("status") if isinstance(opened, dict) else None
    if status is None:
        return finding(
            severity=SEVERITY_UNVERIFIED,
            topic=topic,
            evidence=str(opened.get("error") or "fetch failed"),
            detail_ar=f"تعذر فتح {source_url}. الحالة «غير متحقق منها» وليست مرجعًا صحيحًا.",
            detail_en=f"Could not open {source_url}. The status is unverified, not correct.",
        )
    if status != 200:
        return finding(
            severity=SEVERITY_CRITICAL,
            topic=topic,
            evidence=f"HTTP {status} {source_url}",
            detail_ar="رابط المصدر لا يعيد صفحة ناجحة.",
            detail_en="The source URL did not return a successful page.",
        )
    body = _normalize(str(opened.get("body") or ""))
    if _normalize(title) and _normalize(title) in body:
        return finding(
            severity=SEVERITY_OK,
            topic=topic,
            evidence=source_url,
            detail_ar=f"ظهر العنوان في الصفحة المفتوحة: {source_url}. لا توجد بيانات Crossref لهذا الرابط.",
            detail_en=f"The title appeared on the opened page: {source_url}. No Crossref record was used.",
        )
    return finding(
        severity=SEVERITY_UNVERIFIED,
        topic=topic,
        evidence=source_url,
        detail_ar="الرابط استجاب ولم يُعثر على العنوان في النص المقروء. الحالة «غير متحقق منها».",
        detail_en="The URL responded, but the title was not found in the readable text. The status is unverified.",
    )


def verify_journal_evidence(evidence: dict | None, *, fetch: Fetch | None = None) -> list[dict]:
    """Recommend a journal only when the documented Scopus and fee evidence is complete and reachable."""
    if not evidence:
        return [
            finding(
                severity=SEVERITY_UNVERIFIED,
                topic="journal",
                evidence="missing evidence record",
                detail_ar="لا يوجد سجل دليل للمجلة. لا تُوصى بها.",
                detail_en="No journal evidence record was supplied. It is not recommended.",
            )
        ]
    opener = fetch or default_fetch
    missing = _missing_journal_fields(evidence)
    if missing:
        return [
            finding(
                severity=SEVERITY_UNVERIFIED,
                topic="journal",
                evidence=", ".join(missing),
                detail_ar="دليل المجلة ناقص. لا تُعرض كخيار صالح.",
                detail_en="The journal evidence is incomplete. It is not a valid option.",
            )
        ]
    name = str(evidence.get("name") or "")
    if evidence.get("predatory") is True:
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic="journal",
                evidence=name,
                detail_ar="السجل موسوم بأن المجلة غير معتبرة. لا تُوصى بها.",
                detail_en="The record marks the journal as not credible. It is not recommended.",
            )
        ]
    if evidence.get("index") != "scopus" or evidence.get("indexing_source") not in INDEXING_SOURCES:
        return [
            finding(
                severity=SEVERITY_REVISE,
                topic="journal",
                evidence=str(evidence.get("index")),
                detail_ar="أولوية المهارة لمجلة Scopus موثقة من Scopus Sources أو تقرير المكتبة الرقمية.",
                detail_en="The skill priority is a Scopus journal documented from Scopus Sources or the digital-library report.",
            )
        ]
    quartile = str(evidence.get("quartile") or "")
    if quartile not in PRIORITY_QUARTILES | {"Q3", "Q4"}:
        return [
            finding(
                severity=SEVERITY_UNVERIFIED,
                topic="journal",
                evidence=quartile,
                detail_ar="الربع غير معروف. لا يُستبدل بتخمين.",
                detail_en="The quartile is unknown and is not replaced by a guess.",
            )
        ]
    if evidence.get("apc_source") not in APC_SOURCES:
        return [
            finding(
                severity=SEVERITY_UNVERIFIED,
                topic="journal",
                evidence=str(evidence.get("apc_source")),
                detail_ar="مصدر الرسوم ليس صفحة ناشر أو قائمة أسعار.",
                detail_en="The fee source is not a publisher page or price list.",
            )
        ]
    for label, url in (("indexing", evidence["indexing_url"]), ("apc", evidence["apc_url"])):
        if _placeholder_url(str(url)):
            return [
                finding(
                    severity=SEVERITY_CRITICAL,
                    topic="journal",
                    evidence=str(url),
                    detail_ar=f"رابط دليل {label} عنصر نائب.",
                    detail_en=f"The {label} evidence URL is a placeholder.",
                )
            ]
    if evidence.get("apc_mandatory") is True:
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic="journal",
                evidence=name,
                detail_ar="الرسوم إلزامية على المؤلف. المجلة خارج نطاق المهارة.",
                detail_en="Author fees are mandatory. The journal is outside the skill scope.",
            )
        ]
    fee_words = ("no mandatory", "no apc", "optional open access", "بلا رسوم الزامية", "بلا رسوم إلزامية")
    excerpt = _normalize(str(evidence.get("apc_excerpt") or ""))
    if not any(_normalize(word) in excerpt for word in fee_words):
        return [
            finding(
                severity=SEVERITY_REVISE,
                topic="journal",
                evidence=str(evidence.get("apc_excerpt")),
                detail_ar="مقتطف الرسوم لا ينص على مسار بلا رسوم إلزامية.",
                detail_en="The fee excerpt does not state a route without a mandatory author fee.",
            )
        ]
    if quartile not in PRIORITY_QUARTILES and not evidence.get("allow_q3_q4"):
        return [
            finding(
                severity=SEVERITY_REVISE,
                topic="journal",
                evidence=quartile,
                detail_ar="Q3 وQ4 لا يُعرضان إلا بطلب صريح وبعد اكتمال الدليل.",
                detail_en="Q3 and Q4 are shown only when explicitly requested and the evidence is complete.",
            )
        ]
    opened = []
    for label, url, excerpt_text in (
        ("indexing", evidence["indexing_url"], evidence["indexing_excerpt"]),
        ("apc", evidence["apc_url"], evidence["apc_excerpt"]),
    ):
        try:
            page = opener(str(url))
        except (urllib.error.URLError, TimeoutError, OSError, ConnectionError) as exc:
            page = {"status": None, "error": str(exc), "body": ""}
        status = page.get("status") if isinstance(page, dict) else None
        if status is None:
            return [
                finding(
                    severity=SEVERITY_UNVERIFIED,
                    topic="journal",
                    evidence=f"{label}: {page.get('error') if isinstance(page, dict) else 'failed'}",
                    detail_ar="تعذر فتح صفحة الدليل. لا تتحول المجلة إلى توصية.",
                    detail_en="The evidence page could not be opened. The journal is not treated as recommended.",
                )
            ]
        if status != 200:
            return [
                finding(
                    severity=SEVERITY_UNVERIFIED,
                    topic="journal",
                    evidence=f"{label} HTTP {status}",
                    detail_ar="صفحة الدليل لم تفتح بنجاح. التوصية موقوفة.",
                    detail_en="The evidence page did not open successfully. The recommendation stays withheld.",
                )
            ]
        body = _normalize(str(page.get("body") or ""))
        if _normalize(str(excerpt_text)) not in body:
            return [
                finding(
                    severity=SEVERITY_REVISE,
                    topic="journal",
                    evidence=f"{label} excerpt not on page",
                    detail_ar="المقتطف الموثق غير موجود في الصفحة التي فُتحت.",
                    detail_en="The documented excerpt was not present on the opened page.",
                )
            ]
        opened.append(f"{label} {url} opened {evidence.get(label + '_opened_on')}")
    indexing_body_ok = _journal_page_has_markers(evidence)
    # Markers are required inside the excerpt that was found on the page.
    if not indexing_body_ok:
        return [
            finding(
                severity=SEVERITY_REVISE,
                topic="journal",
                evidence=str(evidence.get("indexing_excerpt")),
                detail_ar="مقتطف الفهرسة لا يجمع الربع وسنة التصنيف والفئة الموضوعية.",
                detail_en="The indexing excerpt does not contain the quartile, classification year, and subject category.",
            )
        ]
    tier = "priority" if quartile in PRIORITY_QUARTILES else "fallback"
    return [
        finding(
            severity=SEVERITY_OK,
            topic="journal",
            evidence="; ".join(opened + [tier, quartile, str(evidence.get("subject_category")), str(evidence.get("classification_year"))]),
            detail_ar=(
                f"الدليل المكتوب لمجلة {name} مكتمل لسنة {evidence.get('classification_year')} "
                f"في فئة {evidence.get('subject_category')} وبالربع {quartile}، مع مسار بلا رسوم إلزامية. "
                "هذا قبول للدليل المعروض لا إثبات مستقل من قاعدة Scopus نفسها."
            ),
            detail_en=(
                f"The written evidence for {name} is complete for {evidence.get('classification_year')} "
                f"in {evidence.get('subject_category')} at {quartile}, with a route that has no mandatory fee. "
                "This accepts the supplied evidence. It is not an independent scrape of Scopus."
            ),
        )
    ]


def _missing_journal_fields(evidence: dict) -> list[str]:
    required = (
        "name",
        "index",
        "quartile",
        "subject_category",
        "classification_year",
        "indexing_source",
        "indexing_url",
        "indexing_opened_on",
        "indexing_excerpt",
        "apc_mandatory",
        "apc_source",
        "apc_url",
        "apc_opened_on",
        "apc_excerpt",
    )
    missing = []
    for field in required:
        value = evidence.get(field)
        if field == "apc_mandatory":
            if not isinstance(value, bool):
                missing.append(field)
            continue
        if field == "classification_year":
            if not isinstance(value, int):
                missing.append(field)
            continue
        if not str(value or "").strip():
            missing.append(field)
    for date_field in ("indexing_opened_on", "apc_opened_on"):
        if date_field not in missing and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(evidence.get(date_field) or "")):
            missing.append(date_field)
    return missing


def _journal_page_has_markers(evidence: dict) -> bool:
    excerpt = _normalize(str(evidence.get("indexing_excerpt") or ""))
    quartile = _normalize(str(evidence.get("quartile") or ""))
    year = str(evidence.get("classification_year") or "")
    subject = _normalize(str(evidence.get("subject_category") or ""))
    return bool(quartile and quartile in excerpt and year in excerpt and subject and subject in excerpt)


def audit_methods(text: str) -> list[dict]:
    """Flag design, statistics, ethics, and Gymnastics for All contradictions in a draft."""
    if not text or not text.strip():
        return [
            finding(
                severity=SEVERITY_UNVERIFIED,
                topic="methods",
                evidence="empty manuscript",
                detail_ar="لا يوجد نص منهجي لفحصه.",
                detail_en="There is no methods text to check.",
            )
        ]
    findings = []
    findings.extend(_design_findings(text))
    findings.extend(_statistics_findings(text))
    findings.extend(_ethics_findings(text))
    findings.extend(_domain_findings(text))
    if not findings:
        findings.append(
            finding(
                severity=SEVERITY_OK,
                topic="methods",
                evidence="no automated pattern matched",
                detail_ar="لم ترصد الأداة تعارضًا في الأنماط المفحوصة. هذا ليس حكمًا بصحة المنهج.",
                detail_en="The checker found none of the audited contradiction patterns. This is not a judgment that the methods are sound.",
            )
        )
    return findings


def _claims_rct(text: str) -> bool:
    if re.search(r"ليست تجربة عشوائية|ليس تجربة عشوائية|not an rct|not a randomized", text, flags=re.I):
        return False
    return bool(re.search(r"تجربة عشوائية|randomized controlled|randomised controlled|\bRCT\b", text, flags=re.I))


def _data_absent(text: str) -> bool:
    return bool(
        re.search(
            r"البيانات غير متوفرة|بيانات غير متوفرة|غير متوفر|لم تُجمع البيانات|لم تجمع البيانات|no data were collected|data are not available|before data collection",
            text,
            flags=re.I,
        )
    )


def _design_findings(text: str) -> list[dict]:
    results = []
    single_group = bool(re.search(r"مجموعة واحدة|مجموعه واحدة|one[- ]group|single[- ]group", text, flags=re.I))
    no_control = bool(re.search(r"بلا مجموعة مقارنة|without a control group|no control group", text, flags=re.I))
    if _claims_rct(text) and (single_group or no_control):
        results.append(
            finding(
                severity=SEVERITY_CRITICAL,
                topic="design",
                evidence="single-group or no-control text combined with an RCT label",
                detail_ar="وُصفت دراسة ذات مجموعة واحدة أو بلا مجموعة مقارنة بأنها تجربة عشوائية مضبوطة.",
                detail_en="A single-group study, or a study without a control, is described as a randomized controlled trial.",
            )
        )
    individual = bool(re.search(r"تعيين عشوائي فردي|individually randomi[sz]ed|individual[- ]level randomi", text, flags=re.I))
    cluster = bool(re.search(r"عنقودي|cluster[- ]randomi", text, flags=re.I))
    quasi = bool(re.search(r"شبه تجريب|quasi[- ]experimental|nonequivalent control", text, flags=re.I))
    labels = [name for name, present in (("individual", individual), ("cluster", cluster), ("quasi", quasi)) if present]
    alternatives = bool(re.search(r"خيار بديل|تصميم بديل|either|alternative design", text, flags=re.I))
    if len(labels) >= 2 and not alternatives:
        results.append(
            finding(
                severity=SEVERITY_REVISE,
                topic="design",
                evidence=" and ".join(labels),
                detail_ar="النص يجمع أكثر من تصميم كأنهما التصميم المنفذ نفسه: فردي، أو عنقودي، أو شبه تجريبي.",
                detail_en="The text treats more than one of individual, cluster, and quasi-experimental designs as the same executed design.",
            )
        )
    independent_t = bool(re.search(r"اختبار t المستقل|اختبار ت المستقل|independent t-test|independent-samples t", text, flags=re.I))
    cluster_analysis = bool(re.search(r"نموذج مختلط|mixed model|GEE|cluster-robust|معامل التصميم|design effect", text, flags=re.I))
    if cluster and independent_t and not cluster_analysis:
        results.append(
            finding(
                severity=SEVERITY_REVISE,
                topic="analysis",
                evidence="cluster design with an independent t-test and no cluster-aware analysis",
                detail_ar="التصميم العنقودي مذكور مع اختبار t للمستقلين من غير تحليل يراعي العنقود.",
                detail_en="A cluster design is paired with an independent t-test and no cluster-aware analysis.",
            )
        )
    return results


def _statistics_findings(text: str) -> list[dict]:
    results = []
    p_value = bool(
        re.search(
            r"p\s*[<=>]\s*0?\.\d+|p[- ]value\s*[<=>:]|القيمة الاحتمالية\s*(?:بلغت|=|تساوي)|قيمة\s*p\s*(?:=|بلغت)",
            text,
            flags=re.I,
        )
    )
    effect = bool(
        re.search(
            r"cohen(?:'s)?\s*d\s*=\s*\d|حجم الأثر\s*(?:=|بلغ)|effect size\s*(?:=|of)\s*\d|\bd\s*=\s*0?\.\d+",
            text,
            flags=re.I,
        )
    )
    count = bool(re.search(r"(?<!\d)(\d{1,5})\s+(?:المشاركين|مشاركين|مشارك|مسنين|مسن|residents|resident|participants|participant)", text, flags=re.I))
    if _data_absent(text) and (p_value or effect or count):
        bits = []
        if p_value:
            bits.append("p-value")
        if effect:
            bits.append("effect size")
        if count:
            bits.append("participant count")
        results.append(
            finding(
                severity=SEVERITY_CRITICAL,
                topic="statistics",
                evidence=", ".join(bits) + " while data are described as unavailable",
                detail_ar="ذُكرت قيمة احتمالية أو حجم أثر أو عدد مشاركين رغم أن البيانات غير متوفرة. لا تُخترع هذه الأرقام.",
                detail_en="A p-value, effect size, or participant count is stated while the data are described as unavailable. These numbers are not invented.",
            )
        )
    sample_missing = bool(re.search(r"لم يُحسب حجم العينة|حجم العينة غير محسوب|sample size was not calculated", text))
    significant = bool(re.search(r"p\s*[<=>]\s*0?\.\d+|دال إحصائي|statistically significant", text, flags=re.I))
    if sample_missing and significant:
        results.append(
            finding(
                severity=SEVERITY_REVISE,
                topic="sample-size",
                evidence="significance language without a calculated sample size",
                detail_ar="النص يذكر نتيجة دالة وحجم العينة غير محسوب.",
                detail_en="The text states a significant result while also saying the sample size was not calculated.",
            )
        )
    plural_primary = bool(re.search(r"النواتج الأولية|primary outcomes", text, flags=re.I))
    correction = bool(re.search(r"Bonferroni|تصحيح التعدد|multiplicity|family-wise", text, flags=re.I))
    if plural_primary and p_value and not correction:
        results.append(
            finding(
                severity=SEVERITY_REVISE,
                topic="analysis",
                evidence="plural primary outcomes and a p-value without a multiplicity statement",
                detail_ar="أكثر من ناتج أولي مذكور مع قيمة p ومن غير ما يبين التعامل مع تعدد المقارنات.",
                detail_en="More than one primary outcome is mentioned with a p-value and no multiplicity statement.",
            )
        )
    return results


def _ethics_findings(text: str) -> list[dict]:
    approval = re.search(
        r"(?:موافقة|ethics approval|IRB).{0,80}?(?:رقم|number|no\.)\s*(?:الموافقة|approval)?\s*[:#]?\s*([A-Za-z0-9][A-Za-z0-9/-]{2,})",
        text,
        flags=re.I | re.S,
    )
    if not approval:
        return []
    number = approval.group(1)
    if re.search(r"لا توجد موافقة|لم تُصدر موافقة|بدون موافقة|no ethics approval|approval was not obtained", text, flags=re.I):
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic="ethics",
                evidence=number,
                detail_ar="ذُكر رقم موافقة أخلاقية في نص يقول إن الموافقة غير موجودة.",
                detail_en="An ethics approval number appears in text that says approval does not exist.",
            )
        ]
    if re.search(r"مرفق|وثيقة الموافقة|approval letter|attached approval", text, flags=re.I):
        return [
            finding(
                severity=SEVERITY_OK,
                topic="ethics",
                evidence=number,
                detail_ar="رقم الموافقة مذكور مع إشارة إلى وثيقة. الأداة لا تفتح الوثيقة ولا تثبت الرقم.",
                detail_en="The approval number is cited with a document. The checker does not open that document and does not prove the number.",
            )
        ]
    return [
        finding(
            severity=SEVERITY_UNVERIFIED,
            topic="ethics",
            evidence=number,
            detail_ar="رقم موافقة مذكور بلا وثيقة مرفقة في النص. لا يُعامل كرقم صحيح.",
            detail_en="An approval number is stated without a document cited in the text. It is not treated as verified.",
        )
    ]


def _domain_findings(text: str) -> list[dict]:
    gfa = bool(re.search(r"الجمباز للجميع|gymnastics for all|\bGfA\b", text, flags=re.I))
    artistic = bool(re.search(r"درجة الصعوبة|code of points|D-score|E-score|تحكيم الجمباز الفني|artistic gymnastics", text, flags=re.I))
    if gfa and artistic:
        return [
            finding(
                severity=SEVERITY_CRITICAL,
                topic="domain",
                evidence="Gymnastics for All text combined with artistic judging language",
                detail_ar="النص يخلط الجمباز للجميع بدرجات أو تحكيم الجمباز الفني. المرجع التعريفي يبقى دليل FIG للجمباز للجميع، لا قانون التحكيم الفني.",
                detail_en="The text mixes Gymnastics for All with artistic-gymnastics scores or judging. The definition source remains the FIG Gymnastics for All manual, not the artistic code of points.",
            )
        ]
    return []


def build_audit_report(
    *,
    references: list[dict] | None = None,
    journal: dict | None = None,
    manuscript: str | None = None,
    lookup: Lookup | None = None,
    fetch: Fetch | None = None,
) -> dict:
    findings: list[dict] = []
    if references is not None:
        findings.extend(verify_references(references, lookup=lookup, fetch=fetch))
    if journal is not None:
        findings.extend(verify_journal_evidence(journal, fetch=fetch))
    if manuscript is not None:
        findings.extend(audit_methods(manuscript))
    if not findings:
        findings.append(
            finding(
                severity=SEVERITY_UNVERIFIED,
                topic="audit",
                evidence="no inputs",
                detail_ar="لم يُمرر مرجع ولا مجلة ولا نص. لا توجد نتيجة مقبولة.",
                detail_en="No references, journal evidence, or manuscript were supplied. There is no acceptable result.",
            )
        )
    counts = {severity: sum(item["severity"] == severity for item in findings) for severity in SEVERITIES}
    passed = counts[SEVERITY_CRITICAL] == 0 and counts[SEVERITY_REVISE] == 0 and counts[SEVERITY_UNVERIFIED] == 0
    report = {
        "skill": "scientific-research",
        "version": 2,
        "automated_audit_is_not_full_scientific_validation": True,
        "disclaimer_ar": DISCLAIMER_AR,
        "disclaimer_en": DISCLAIMER_EN,
        "passed": passed,
        "counts": counts,
        "findings": findings,
    }
    report["arabic"] = render_arabic(report)
    report["english"] = render_english(report)
    return report


def render_arabic(report: dict) -> str:
    lines = [
        "تقرير تدقيق مهارة البحث العلمي، الإصدار 2",
        report["disclaimer_ar"],
        f"النتيجة الآلية المغلقة: {'بلا ملاحظات حرجة أو ناقصة' if report['passed'] else 'توجد ملاحظات تمنع اعتبار الفحص ناجحًا'}.",
    ]
    for severity in SEVERITIES:
        lines.append(f"- {severity}: {report['counts'][severity]}")
    for item in report["findings"]:
        lines.append(
            f"## {item['severity']} — {item['topic']}\n{item['detail_ar']}\nالدليل: {item['evidence']}"
        )
    return "\n".join(lines)


def render_english(report: dict) -> str:
    labels = {
        SEVERITY_CRITICAL: "Critical error",
        SEVERITY_REVISE: "Needs revision",
        SEVERITY_UNVERIFIED: "Unverifiable",
        SEVERITY_OK: "Acceptable",
    }
    lines = [
        "Scientific Research Skill audit report, version 2",
        report["disclaimer_en"],
        f"Closed automated result: {'no critical, revision, or unverifiable findings' if report['passed'] else 'findings prevent treating the check as successful'}.",
    ]
    for severity in SEVERITIES:
        lines.append(f"- {labels[severity]}: {report['counts'][severity]}")
    for item in report["findings"]:
        lines.append(
            f"## {labels[item['severity']]} — {item['topic']}\n{item['detail_en']}\nEvidence: {item['evidence']}"
        )
    return "\n".join(lines)
