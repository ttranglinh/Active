from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from src.modules.contact_pipeline.application.create_contact_stubs import create_contact_stubs


ROOT = Path(__file__).resolve().parents[1]
COMPANY_OUTPUT_BASE = ROOT / "data" / "processed" / "company_intelligence"
CONTACT_OUTPUT_BASE = ROOT / "data" / "processed" / "contact_stubs"
DEFAULT_ICP_PERSONAS = ["CEO", "Founder"]


def _latest_company_run_file() -> Path:
    files = sorted(COMPANY_OUTPUT_BASE.glob("*.json"))
    if not files:
        raise FileNotFoundError(
            f"No company intelligence output found in: {COMPANY_OUTPUT_BASE}"
        )
    return files[-1]


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in: {path}")
    return payload


def _extract_personas(session_payload: dict[str, Any]) -> list[str]:
    normalized = session_payload.get("normalized")
    if isinstance(normalized, dict):
        icp = normalized.get("icp")
        if isinstance(icp, dict):
            personas = icp.get("personas")
            if isinstance(personas, list):
                return [str(x).strip() for x in personas if str(x).strip()]

    icp = session_payload.get("icp")
    if isinstance(icp, dict):
        personas = icp.get("personas")
        if isinstance(personas, list):
            return [str(x).strip() for x in personas if str(x).strip()]

    return []


def _resolve_path(repo_relative_path: str) -> Path:
    return ROOT / repo_relative_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create contact stubs from ranked company intelligence output."
    )
    parser.add_argument(
        "--company-run-file",
        default="",
        help=(
            "Company intelligence output JSON path relative to repo root. "
            "Default: latest in data/processed/company_intelligence/"
        ),
    )
    parser.add_argument(
        "--session-input-file",
        default="",
        help=(
            "Optional session normalized input JSON path relative to repo root. "
            "If omitted, uses input_file in company run metadata."
        ),
    )
    parser.add_argument("--top-companies", type=int, default=10)
    parser.add_argument("--stubs-per-company", type=int, default=2)
    args = parser.parse_args()

    company_path = (
        _resolve_path(args.company_run_file) if args.company_run_file else _latest_company_run_file()
    )
    company_payload = _load_json(company_path)
    ranked_companies = company_payload.get("records")
    if not isinstance(ranked_companies, list):
        raise ValueError("Company run file must contain list field: records")

    session_input_path: Path | None = None
    if args.session_input_file:
        session_input_path = _resolve_path(args.session_input_file)
    else:
        inferred = company_payload.get("input_file")
        if isinstance(inferred, str) and inferred.strip():
            session_input_path = _resolve_path(inferred.strip())

    personas: list[str] = []
    if session_input_path is not None and session_input_path.exists():
        session_payload = _load_json(session_input_path)
        personas = _extract_personas(session_payload)
    used_default_personas = False
    if not personas:
        personas = DEFAULT_ICP_PERSONAS.copy()
        used_default_personas = True

    stubs = create_contact_stubs(
        ranked_companies=ranked_companies,
        personas=personas,
        top_companies=args.top_companies,
        stubs_per_company=args.stubs_per_company,
    )

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    CONTACT_OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    out_path = CONTACT_OUTPUT_BASE / f"{run_id}.json"
    out_path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "company_run_file": str(company_path.relative_to(ROOT)).replace("\\", "/"),
                "session_input_file": (
                    str(session_input_path.relative_to(ROOT)).replace("\\", "/")
                    if session_input_path is not None and session_input_path.exists()
                    else None
                ),
                "top_companies": args.top_companies,
                "stubs_per_company": args.stubs_per_company,
                "used_default_personas": used_default_personas,
                "personas_used": personas,
                "count": len(stubs),
                "records": [s.model_dump() for s in stubs],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Run ID: {run_id}")
    print(f"Company Input: {company_path}")
    print(f"Session Input: {session_input_path if session_input_path is not None else 'None'}")
    print(f"Output: {out_path}")
    print(f"Contact stubs: {len(stubs)}")
    if stubs:
        first = stubs[0]
        print(f"Top 1: {first.full_name} | {first.title} | {first.linkedin_url}")


if __name__ == "__main__":
    main()
