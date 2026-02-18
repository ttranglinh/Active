from __future__ import annotations

from pydantic import BaseModel, Field


class AbrRecord(BaseModel):
    abn: str
    entity_name: str
    trading_name: str = ""
    entity_type: str = ""
    status: str = ""
    state: str = ""
    suburb: str = ""
    postcode: str = ""
    industry_anzsic: str = ""
    sub_industry: str = ""
    employee_range: str = ""
    revenue_range: str = ""
    website: str = ""
    linkedin_url: str = ""
    founded_year: int | None = None


class AsicRecord(BaseModel):
    abn: str
    incorporation_date: str = ""
    director_names: list[str] = Field(default_factory=list)
    entity_status: str = ""


class VcRecord(BaseModel):
    abn: str
    domain: str = ""
    vc_backed: bool = False
    investor_names: list[str] = Field(default_factory=list)
    funding_stage: str = ""
    last_funding_date: str = ""
    funding_amount_aud: int | float | None = None


class JobsRecord(BaseModel):
    abn: str
    domain: str = ""
    source: str = ""
    open_roles: int = 0
    roles_last_30_days: int = 0
    captured_at_utc: str = ""


class NewsRecord(BaseModel):
    abn: str
    domain: str = ""
    headline: str = ""
    source_name: str = ""
    source_url: str = ""
    published_at_utc: str = ""

