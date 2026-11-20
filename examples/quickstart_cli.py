#!/usr/bin/env python3
"""Zero-dependency Python starter CLI for Official Open-Data Apify Actors.

Supports:
  - french-companies : SIRENE/RNE + BODACC KYC + BOAMP (France)
  - eu-tenders       : EU TED v3 (27 countries) + BOAMP public procurement
  - clinical-trials  : NIH ClinicalTrials.gov REST API v2

Usage:
  export APIFY_TOKEN="apify_api_..."
  python3 examples/quickstart_cli.py clinical-trials --condition diabetes --mode count
  python3 examples/quickstart_cli.py french-companies --postal-code 75008 --qualiopi --mode count
  python3 examples/quickstart_cli.py eu-tenders --countries FRA,DEU --cpv 72 --max 5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any

ACTORS = {
    "french-companies": "yannabadie~french-company-intelligence-mcp",
    "eu-tenders": "yannabadie~eu-public-tenders-ted-boamp",
    "clinical-trials": "yannabadie~clinical-trials-api-mcp",
}


def build_payload(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    actor_slug = ACTORS[args.command]
    if args.command == "french-companies":
        payload: dict[str, Any] = {
            "mode": args.mode,
            "maxResults": args.max,
        }
        if args.query:
            payload["query"] = args.query
        if args.postal_code:
            payload["postalCode"] = args.postal_code
        if args.department:
            payload["department"] = args.department
        if args.qualiopi:
            payload["estQualiopi"] = True
        if args.rge:
            payload["estRge"] = True
        if args.include_bodacc:
            payload["includeBodacc"] = True
        return actor_slug, payload

    if args.command == "eu-tenders":
        payload = {
            "sources": ["ted", "boamp"],
            "countries": [c.strip() for c in args.countries.split(",") if c.strip()],
            "cpvCodes": [c.strip() for c in args.cpv.split(",") if c.strip()],
            "scope": "ACTIVE",
            "maxResultsPerSource": args.max,
        }
        if args.keywords:
            payload["keywords"] = [k.strip() for k in args.keywords.split(",") if k.strip()]
        return actor_slug, payload

    # clinical-trials
    payload = {
        "mode": args.mode,
        "condition": args.condition,
        "overallStatus": ["RECRUITING"],
        "maxResults": args.max,
    }
    if args.sponsor:
        payload["sponsor"] = args.sponsor
    if args.location:
        payload["location"] = args.location
    if args.phases:
        payload["phases"] = [p.strip().upper() for p in args.phases.split(",") if p.strip()]
    return actor_slug, payload


def call_apify(actor_slug: str, payload: dict[str, Any], token: str) -> list[dict[str, Any]]:
    url = (
        f"https://api.apify.com/v2/acts/{actor_slug}/run-sync-get-dataset-items?"
        + urllib.parse.urlencode({"token": token})
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Starter CLI for Official Open-Data Apify Actors.")
    parser.add_argument("--dry-run", action="store_true", help="Print request payload without calling Apify.")
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("french-companies", help="Query French SIRENE/RNE + BODACC + BOAMP.")
    p1.add_argument("--mode", default="count", choices=["count", "search_companies", "watch_bodacc", "search_boamp"])
    p1.add_argument("--query", default="")
    p1.add_argument("--postal-code", default="")
    p1.add_argument("--department", default="")
    p1.add_argument("--qualiopi", action="store_true")
    p1.add_argument("--rge", action="store_true")
    p1.add_argument("--include-bodacc", action="store_true")
    p1.add_argument("--max", type=int, default=10)

    p2 = sub.add_parser("eu-tenders", help="Query EU TED v3 + French BOAMP tenders.")
    p2.add_argument("--countries", default="FRA,DEU")
    p2.add_argument("--cpv", default="72")
    p2.add_argument("--keywords", default="")
    p2.add_argument("--max", type=int, default=10)

    p3 = sub.add_parser("clinical-trials", help="Query NIH ClinicalTrials.gov API v2.")
    p3.add_argument("--mode", default="count", choices=["count", "search"])
    p3.add_argument("--condition", default="diabetes")
    p3.add_argument("--sponsor", default="")
    p3.add_argument("--location", default="")
    p3.add_argument("--phases", default="")
    p3.add_argument("--max", type=int, default=10)

    args = parser.parse_args(argv)
    actor_slug, payload = build_payload(args)

    if args.dry_run:
        print(json.dumps({"actor": actor_slug, "input": payload}, indent=2))
        return 0

    token = os.environ.get("APIFY_TOKEN", "").strip()
    if not token:
        print("Error: set APIFY_TOKEN environment variable (free $5/mo Apify account).", file=sys.stderr)
        return 2

    items = call_apify(actor_slug, payload, token)
    print(json.dumps(items, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
