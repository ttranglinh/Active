from __future__ import annotations

from pydantic import BaseModel, Field


class FirmographicInput(BaseModel):
    industries: list[str] = Field(default_factory=list)
    headcount_ranges: list[str] = Field(default_factory=list)
    regions: list[str] = Field(default_factory=list)
    revenue_ranges: list[str] = Field(default_factory=list)


class IcpInput(BaseModel):
    company_types: list[str] = Field(default_factory=list)
    personas: list[str] = Field(default_factory=list)
    seniority: list[str] = Field(default_factory=list)


class UserInputContract(BaseModel):
    input_id: str
    created_at_utc: str
    market: str
    services: list[str] = Field(default_factory=list)
    firmographic: FirmographicInput = Field(default_factory=FirmographicInput)
    icp: IcpInput = Field(default_factory=IcpInput)
    signals: list[str] = Field(default_factory=list)
    notes: str = ""
    session_name: str = ""


class NormalizationReport(BaseModel):
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    dropped_fields: list[str] = Field(default_factory=list)
    normalized_at_utc: str


class NormalizationResult(BaseModel):
    normalized: UserInputContract
    report: NormalizationReport

