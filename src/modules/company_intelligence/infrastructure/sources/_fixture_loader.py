from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel


ROOT = Path(__file__).resolve().parents[5]
FIXTURE_BASE = ROOT / "data" / "raw" / "company_sources"

T = TypeVar("T", bound=BaseModel)


def load_fixture_records(file_name: str, model: type[T]) -> list[T]:
    path = FIXTURE_BASE / file_name
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError(f"Fixture must be a JSON array: {path}")

    return [model.model_validate(item) for item in payload]
