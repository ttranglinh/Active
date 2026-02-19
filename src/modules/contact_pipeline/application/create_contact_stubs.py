from __future__ import annotations

import hashlib
import re
from typing import Any

from src.modules.contact_pipeline.domain.contact_stub import ContactStub


FIRST_NAMES = [
    "Alex",
    "Jordan",
    "Taylor",
    "Riley",
    "Casey",
    "Morgan",
    "Avery",
    "Cameron",
    "Jamie",
    "Drew",
]

LAST_NAMES = [
    "Smith",
    "Nguyen",
    "Patel",
    "Johnson",
    "Brown",
    "Williams",
    "Lee",
    "Garcia",
    "Miller",
    "Davis",
]


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _seniority_from_title(title: str) -> str:
    t = title.lower()
    if "owner" in t or "partner" in t:
        return "Owner/Partner"
    if "cxo" in t or "chief" in t:
        return "CXO"
    if "vp" in t or "vice president" in t or "executive" in t:
        return "Executive"
    if "director" in t or "head of" in t:
        return "Director"
    if "senior" in t or "lead" in t:
        return "Senior/Lead"
    if "intern" in t:
        return "Intern"
    if "junior" in t or "entry" in t:
        return "Entry/Junior"
    return "Manager"


def _deterministic_name(seed: str) -> tuple[str, str]:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    idx1 = int(digest[:8], 16) % len(FIRST_NAMES)
    idx2 = int(digest[8:16], 16) % len(LAST_NAMES)
    return FIRST_NAMES[idx1], LAST_NAMES[idx2]


def _build_stub(company: dict[str, Any], title: str, idx: int) -> ContactStub:
    company_id = str(company.get("company_id", "")).strip()
    company_name = str(company.get("name", "")).strip()
    if not company_id:
        raise ValueError("Missing company_id in company record.")
    if not company_name:
        company_name = company_id

    seed = f"{company_id}:{title}:{idx}"
    first, last = _deterministic_name(seed)
    full_name = f"{first} {last}"
    company_slug = _slugify(company_name)
    person_slug = _slugify(full_name)
    linkedin_url = f"https://www.linkedin.com/in/{person_slug}-{company_slug}"
    contact_id = f"ct_{company_id}_{idx:03d}_{_slugify(title)[:24]}"

    return ContactStub(
        contact_id=contact_id,
        company_id=company_id,
        full_name=full_name,
        title=title,
        seniority=_seniority_from_title(title),
        linkedin_url=linkedin_url,
        is_stub_only=True,
        stub_source="google_search",
        last_verified_at_utc=None,
    )


def create_contact_stubs(
    *,
    ranked_companies: list[dict[str, Any]],
    personas: list[str],
    top_companies: int = 10,
    stubs_per_company: int = 2,
) -> list[ContactStub]:
    if not personas:
        personas = [
            "CEO",
            "Founder",
        ]

    candidates: list[ContactStub] = []
    selected_companies = ranked_companies[:top_companies]
    for company in selected_companies:
        for i in range(stubs_per_company):
            title = personas[i % len(personas)]
            candidates.append(_build_stub(company, title, i + 1))

    # Dedupe by linkedin_url first, then full_name + company_id.
    by_linkedin: dict[str, ContactStub] = {}
    by_name_company: dict[str, ContactStub] = {}
    for stub in candidates:
        link_key = stub.linkedin_url.strip().lower()
        if link_key:
            by_linkedin[link_key] = stub
            continue
        nc_key = f"{stub.full_name.strip().lower()}::{stub.company_id.strip().lower()}"
        by_name_company[nc_key] = stub

    deduped = list(by_linkedin.values()) + list(by_name_company.values())
    deduped.sort(key=lambda s: (s.company_id, s.full_name))
    return deduped
