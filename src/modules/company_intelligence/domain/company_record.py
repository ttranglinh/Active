from __future__ import annotations

from pydantic import BaseModel, Field


class SignalSource(BaseModel):
    type: str
    source_name: str
    source_url: str | None = None
    collected_at_utc: str
    confidence: float | None = None


class CompanyRecord(BaseModel):
    company_id: str
    name: str
    domain: str | None = None
    location: str
    industry: str
    headcount_range: str | None = None
    signal_score: float = Field(ge=0, le=100)
    signal_summary: list[str] = Field(default_factory=list)
    signal_sources: list[SignalSource] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    updated_at_utc: str

