#!/usr/bin/env python3
"""Show which skill commands run offline and which need an external source.

The live DOI mode prints the record returned by Crossref or DataCite.
It does not verify a journal and it does not treat a connection failure
as a match.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_v2 import default_lookup  # noqa: E402


COMMANDS = [
    {
        "command": "profile",
        "network": False,
        "external_source": None,
        "note": "Reads the local researcher profile or the empty template.",
    },
    {
        "command": "similarity",
        "network": False,
        "external_source": None,
        "note": "The promotion numbers come from references/official-snapshot.json, a dated local copy. They are not a live council page.",
    },
    {
        "command": "journal",
        "network": False,
        "external_source": None,
        "note": "Decides from the fields you pass. Missing indexing or fee sources stay unverified and are not a recommendation.",
    },
    {
        "command": "references",
        "network": False,
        "external_source": None,
        "note": "Checks that a reference has a title, a year, and a DOI or an opened URL. It does not resolve the DOI.",
    },
    {
        "command": "review",
        "network": False,
        "external_source": None,
        "note": "Checks the four section criteria: methods, statistical analysis, originality, and ethics.",
    },
    {
        "command": "audit-methods",
        "network": False,
        "external_source": None,
        "note": "Pattern check for design, statistics, ethics, and domain contradictions. A pass is not proof that the methods are sound.",
    },
    {
        "command": "verify-references",
        "network": True,
        "external_source": "https://api.crossref.org then https://api.datacite.org",
        "note": "A connection failure or an unconfirmed title is unverified, not accepted.",
    },
    {
        "command": "verify-journal",
        "network": True,
        "external_source": "the indexing URL and the publisher fee URL written in the evidence file",
        "note": "The checker does not query Scopus by itself. A page that does not open stays unverified.",
    },
    {
        "command": "audit",
        "network": True,
        "external_source": "same sources as the attached reference and journal records",
        "note": "Methods text in the same report can be checked offline. Reference and journal parts need the network.",
    },
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report skill network requirements")
    parser.add_argument("--live-doi", help="Resolve this DOI and print the external record")
    args = parser.parse_args(argv)
    if args.live_doi:
        record = default_lookup(args.live_doi)
        json.dump({"doi": args.live_doi, "record": record, "journal_verified": False}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        if record.get("found") is True:
            return 0
        if record.get("found") is False:
            return 1
        return 2
    json.dump({"commands": COMMANDS, "journal_verified": False}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
