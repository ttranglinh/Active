from __future__ import annotations

from pydantic import BaseModel


class ContactStub(BaseModel):
    contact_id: str
    company_id: str
    full_name: str
    title: str
    seniority: str
    linkedin_url: str
    is_stub_only: bool = True
    stub_source: str = "apify"
    last_verified_at_utc: str | None = None

