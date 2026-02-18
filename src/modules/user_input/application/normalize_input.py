from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.modules.user_input.domain.constants import (
    ALLOWED_HEADCOUNT_RANGES,
    ALLOWED_SENIORITY,
    DEFAULT_MARKET,
)
from src.modules.user_input.domain.contracts import (
    IcpInput,
    FirmographicInput,
    NormalizationReport,
    NormalizationResult,
    UserInputContract,
)


def _clean_str(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _clean_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for item in values:
        cleaned = _clean_str(item)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            out.append(cleaned)
    return out


def normalize_user_input(payload: dict[str, Any], strict: bool = False) -> NormalizationResult:
    warnings: list[str] = []
    errors: list[str] = []
    dropped_fields: list[str] = []

    input_id = _clean_str(payload.get("input_id"))
    if not input_id:
        errors.append("Missing required field: input_id")

    created_at_utc = _clean_str(payload.get("created_at_utc"))
    if not created_at_utc:
        created_at_utc = datetime.now(timezone.utc).isoformat()
        warnings.append("created_at_utc missing; defaulted to current UTC time.")

    market = _clean_str(payload.get("market")) or DEFAULT_MARKET
    if not _clean_str(payload.get("market")):
        warnings.append(f"market missing; defaulted to {DEFAULT_MARKET}.")

    services = _clean_list(payload.get("services", []))
    signals = _clean_list(payload.get("signals", []))
    notes = _clean_str(payload.get("notes"))
    session_name = _clean_str(payload.get("session_name"))

    firmographic_raw = payload.get("firmographic", {}) if isinstance(payload.get("firmographic"), dict) else {}
    icp_raw = payload.get("icp", {}) if isinstance(payload.get("icp"), dict) else {}

    industries = _clean_list(firmographic_raw.get("industries", []))
    headcount_ranges_raw = _clean_list(firmographic_raw.get("headcount_ranges", []))
    regions = _clean_list(firmographic_raw.get("regions", []))
    revenue_ranges = _clean_list(firmographic_raw.get("revenue_ranges", []))

    headcount_ranges: list[str] = []
    for value in headcount_ranges_raw:
        if value in ALLOWED_HEADCOUNT_RANGES:
            headcount_ranges.append(value)
        else:
            warnings.append(f"Ignored invalid headcount range: {value}")
            dropped_fields.append(f"firmographic.headcount_ranges:{value}")

    personas = _clean_list(icp_raw.get("personas", []))
    if not personas:
        errors.append("Missing required field: icp.personas")

    seniority_raw = _clean_list(icp_raw.get("seniority", []))
    seniority: list[str] = []
    for value in seniority_raw:
        if value in ALLOWED_SENIORITY:
            seniority.append(value)
        else:
            warnings.append(f"Ignored invalid seniority value: {value}")
            dropped_fields.append(f"icp.seniority:{value}")

    company_types = _clean_list(icp_raw.get("company_types", []))

    if not regions:
        regions = [market]
        warnings.append("firmographic.regions missing; defaulted to market.")

    if strict and errors:
        report = NormalizationReport(
            warnings=warnings,
            errors=errors,
            dropped_fields=dropped_fields,
            normalized_at_utc=datetime.now(timezone.utc).isoformat(),
        )
        # Build a minimal object for strict-mode errors.
        normalized = UserInputContract(
            input_id=input_id or "invalid",
            created_at_utc=created_at_utc,
            market=market,
            services=services,
            firmographic=FirmographicInput(),
            icp=IcpInput(),
            signals=signals,
            notes=notes,
            session_name=session_name,
        )
        return NormalizationResult(normalized=normalized, report=report)

    normalized = UserInputContract(
        input_id=input_id or "generated_missing_id",
        created_at_utc=created_at_utc,
        market=market,
        services=services,
        firmographic=FirmographicInput(
            industries=industries,
            headcount_ranges=headcount_ranges,
            regions=regions,
            revenue_ranges=revenue_ranges,
        ),
        icp=IcpInput(
            company_types=company_types,
            personas=personas,
            seniority=seniority,
        ),
        signals=signals,
        notes=notes,
        session_name=session_name,
    )

    report = NormalizationReport(
        warnings=warnings,
        errors=errors,
        dropped_fields=dropped_fields,
        normalized_at_utc=datetime.now(timezone.utc).isoformat(),
    )
    return NormalizationResult(normalized=normalized, report=report)

