from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[2]
SESSIONS_DIR = ROOT / "data" / "sessions"
PIPELINE_SCRIPT = ROOT / "scripts" / "collect_apify_raw_linkedin.py"


class MarketFiltersPayload(BaseModel):
    services: list[str] = Field(default_factory=list)
    valueProp: str = ""
    targetPersonas: list[str] = Field(default_factory=list)
    seniority: list[str] = Field(default_factory=list)
    regions: list[str] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)
    headcount: list[str] = Field(default_factory=list)
    signals: list[str] = Field(default_factory=list)


class CreateSessionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    market: str = "Australia"
    filters: MarketFiltersPayload


class RunSessionRequest(BaseModel):
    target_count: int = 200


app = FastAPI(title="Active Session API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def to_pipeline_input(session_id: str, payload: CreateSessionRequest) -> dict:
    return {
        "input_id": f"session_{session_id}",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "market": payload.market,
        "services": payload.filters.services,
        "firmographic": {
            "industries": payload.filters.industries,
            "headcount_ranges": payload.filters.headcount,
            "regions": payload.filters.regions,
            "revenue_ranges": [],
        },
        "icp": {
            "company_types": [],
            "personas": payload.filters.targetPersonas,
            "seniority": payload.filters.seniority,
        },
        "signals": payload.filters.signals,
        "notes": payload.filters.valueProp,
        "session_name": payload.name,
    }


def session_dir(session_id: str) -> Path:
    return SESSIONS_DIR / session_id


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/sessions")
def create_session(req: CreateSessionRequest) -> dict:
    sid = f"s_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    sdir = session_dir(sid)
    sdir.mkdir(parents=True, exist_ok=False)

    user_input = to_pipeline_input(sid, req)
    (sdir / "user_input.json").write_text(json.dumps(user_input, ensure_ascii=False, indent=2), encoding="utf-8")
    (sdir / "meta.json").write_text(
        json.dumps(
            {
                "session_id": sid,
                "name": req.name,
                "market": req.market,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "session_id": sid,
        "name": req.name,
        "user_input_path": str((sdir / "user_input.json").relative_to(ROOT)),
    }


@app.post("/api/sessions/{session_id}/run")
def run_session(session_id: str, req: RunSessionRequest) -> dict:
    sdir = session_dir(session_id)
    if not (sdir / "user_input.json").exists():
        raise HTTPException(status_code=404, detail="Session not found.")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    cmd = [
        sys.executable,
        str(PIPELINE_SCRIPT),
        "--session-id",
        session_id,
        "--target-count",
        str(req.target_count),
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Pipeline run failed.",
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            },
        )

    run_id = ""
    for line in proc.stdout.splitlines():
        if line.startswith("Run ID: "):
            run_id = line.replace("Run ID: ", "").strip()
            break

    summary_path = sdir / "runs" / f"{run_id}.json"
    summary = {}
    if run_id and summary_path.exists():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))

    return {
        "session_id": session_id,
        "run_id": run_id,
        "summary": summary,
        "stdout": proc.stdout,
    }

