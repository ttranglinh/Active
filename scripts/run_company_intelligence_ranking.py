from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from src.modules.company_intelligence.application.build_ranked_companies import (
    build_ranked_company_records,
)
from src.modules.company_intelligence.infrastructure.sources import (
    AbrFixtureSource,
    JobsFixtureSource,
    NewsFixtureSource,
    VcFixtureSource,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_BASE = ROOT / "data" / "processed" / "company_intelligence"


def load_input(path: str) -> dict | None:
    if not path:
        return None
    full = ROOT / path
    if not full.exists():
        raise FileNotFoundError(f"Input file not found: {full}")
    payload = json.loads(full.read_text(encoding="utf-8"))
    if "normalized" in payload and isinstance(payload["normalized"], dict):
        return payload["normalized"]
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ranked company output from fixture sources.")
    parser.add_argument(
        "--input-file",
        default="",
        help="Optional normalized input JSON path relative to repo root for filtering.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top records to keep in output.",
    )
    parser.add_argument(
        "--fallback-unfiltered",
        action="store_true",
        help="If filtered output is empty, rerun ranking without input filters.",
    )
    args = parser.parse_args()

    normalized_input = load_input(args.input_file)
    abr = AbrFixtureSource().fetch()
    vc = VcFixtureSource().fetch()
    jobs = JobsFixtureSource().fetch()
    news = NewsFixtureSource().fetch()

    ranked = build_ranked_company_records(
        abr_records=abr,
        vc_records=vc,
        jobs_records=jobs,
        news_records=news,
        normalized_input=normalized_input,
    )
    fallback_used = False
    if not ranked and normalized_input and args.fallback_unfiltered:
        ranked = build_ranked_company_records(
            abr_records=abr,
            vc_records=vc,
            jobs_records=jobs,
            news_records=news,
            normalized_input=None,
        )
        fallback_used = True

    top_records = ranked[: args.top]

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_BASE / f"{run_id}.json"
    out_path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "input_file": args.input_file or None,
                "fallback_unfiltered_used": fallback_used,
                "count": len(top_records),
                "records": [r.model_dump() for r in top_records],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Run ID: {run_id}")
    print(f"Output: {out_path}")
    print(f"Records: {len(top_records)}")
    if top_records:
        print(f"Top 1: {top_records[0].name} | signal_score={top_records[0].signal_score}")


if __name__ == "__main__":
    main()
