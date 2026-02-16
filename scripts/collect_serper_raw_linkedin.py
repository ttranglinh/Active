from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urlunparse

from dotenv import load_dotenv

from src.modules.ingestion.infrastructure.serper_client import SerperClient, SerperConfig


ROOT = Path(__file__).resolve().parents[1]
TEST_DATA_DIR = ROOT / "data" / "test-data"
RAW_BASE_DIR = ROOT / "data" / "raw" / "serper" / "linkedin_search"
PROCESSED_BASE_DIR = ROOT / "data" / "processed" / "ingestion" / "linkedin_profile_urls"
PROFILE_URL_RE = re.compile(r"^https?://(www\.)?linkedin\.com/in/", re.IGNORECASE)

# Load environment variables from repository-level .env for consistent local runs.
load_dotenv(ROOT / ".env")


def load_test_input(file_name: str) -> dict[str, Any]:
    path = TEST_DATA_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Test input not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_queries(payload: dict[str, Any], limit: int = 12) -> list[str]:
    icp = payload.get("icp", {})
    firmographic = payload.get("firmographic", {})

    personas = icp.get("personas", [])[:4] or ["Founder", "CEO"]
    regions = firmographic.get("regions", [])[:3] or [payload.get("market", "Australia")]
    services = payload.get("services", [])[:3]
    industries = firmographic.get("industries", [])[:3]
    signals = payload.get("signals", [])[:3]

    geography = " OR ".join(f'"{region}"' for region in regions if region)
    geography_group = f"({geography})" if geography else "(Australia)"
    niche_keywords = [kw for kw in (services + industries) if kw][:4]
    if not niche_keywords:
        niche_keywords = ["B2B", "SaaS"]

    queries: list[str] = []
    seen: set[str] = set()

    # Query pattern: [Operator] + [Geography] + [Core Title] + [1-2 Niche Keywords] (+ optional Signal)
    for persona in personas:
        for i, keyword1 in enumerate(niche_keywords):
            for j, keyword2 in enumerate(niche_keywords):
                if i == j:
                    continue
                for signal in [None] + signals:
                    signal_part = f' ("{signal}")' if signal else ""
                    query = (
                        f'site:linkedin.com/in {geography_group} ("{persona}") '
                        f'("{keyword1}") ("{keyword2}"){signal_part} -jobs -job'
                    )
                    query = " ".join(query.split())
                    if query in seen:
                        continue
                    seen.add(query)
                    queries.append(query)
                    if len(queries) >= limit:
                        return queries

    return queries


def normalize_linkedin_profile(url: str) -> str | None:
    if not PROFILE_URL_RE.search(url):
        return None
    parsed = urlparse(url)
    clean = urlunparse(
        (
            parsed.scheme or "https",
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            "",
            "",
            "",
        )
    )
    return clean


def extract_profile_urls(serper_response: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for item in serper_response.get("organic", []):
        link = item.get("link", "")
        normalized = normalize_linkedin_profile(link)
        if normalized:
            urls.append(normalized)
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Call Serper search and store raw JSON + extracted LinkedIn profile URLs."
    )
    parser.add_argument(
        "--input-file",
        default="fi_au_saas_security_001.json",
        help="File inside data/test-data/ to generate search queries from.",
    )
    parser.add_argument(
        "--target-count",
        type=int,
        default=50,
        help="Stop when this many unique LinkedIn profile URLs are collected.",
    )
    args = parser.parse_args()

    input_payload = load_test_input(args.input_file)
    queries = build_queries(input_payload)
    if not queries:
        raise RuntimeError("No queries generated from test input.")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RAW_BASE_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    PROCESSED_BASE_DIR.mkdir(parents=True, exist_ok=True)

    client = SerperClient(SerperConfig.from_env())
    unique_urls: set[str] = set()

    for index, query in enumerate(queries, start=1):
        response_json = client.search(query=query, gl="au", hl="en", num=10, page=1)
        raw_record = {
            "meta": {
                "run_id": run_id,
                "query_id": f"query_{index:03d}",
                "query": query,
                "source": "serper",
                "collected_at_utc": datetime.now(timezone.utc).isoformat(),
            },
            "response": response_json,
        }
        (run_dir / f"query_{index:03d}.json").write_text(
            json.dumps(raw_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        unique_urls.update(extract_profile_urls(response_json))
        if len(unique_urls) >= args.target_count:
            break

    manifest = {
        "run_id": run_id,
        "input_file": args.input_file,
        "query_count": min(len(queries), index),
        "queries": queries[:index],
        "target_count": args.target_count,
        "unique_profile_urls": len(unique_urls),
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    output_json = {
        "run_id": run_id,
        "target_count": args.target_count,
        "unique_count": len(unique_urls),
        "urls": sorted(unique_urls)[: args.target_count],
    }
    (PROCESSED_BASE_DIR / f"{run_id}.json").write_text(
        json.dumps(output_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    csv_path = PROCESSED_BASE_DIR / f"{run_id}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url"])
        for url in output_json["urls"]:
            writer.writerow([url])

    print(f"Run ID: {run_id}")
    print(f"Raw Serper JSON dir: {run_dir}")
    print(f"Processed URL JSON: {PROCESSED_BASE_DIR / f'{run_id}.json'}")
    print(f"Processed URL CSV: {csv_path}")
    print(f"Unique LinkedIn profiles: {output_json['unique_count']}")


if __name__ == "__main__":
    main()
