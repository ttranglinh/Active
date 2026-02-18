from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.modules.company_intelligence.domain.company_record import CompanyRecord, SignalSource
from src.modules.company_intelligence.domain.source_records import (
    AbrRecord,
    JobsRecord,
    NewsRecord,
    VcRecord,
)


def _parse_iso_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        # Support both date-only and datetime formats.
        if "T" in value:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return datetime.fromisoformat(f"{value}T00:00:00+00:00")
    except ValueError:
        return None


def _score_hiring(jobs: JobsRecord | None) -> float:
    if not jobs:
        return 0.0
    roles = max(jobs.open_roles, jobs.roles_last_30_days)
    if roles <= 0:
        return 0.0
    if roles <= 2:
        return 20.0
    if roles <= 5:
        return 50.0
    if roles <= 10:
        return 80.0
    return 100.0


def _score_funding(vc: VcRecord | None, now: datetime) -> float:
    if not vc:
        return 0.0
    date = _parse_iso_date(vc.last_funding_date)
    if not date:
        return 20.0 if vc.vc_backed else 0.0
    months_since = max(0, (now.year - date.year) * 12 + (now.month - date.month))
    if months_since <= 3:
        return 100.0
    if months_since <= 6:
        return 80.0
    if months_since <= 12:
        return 60.0
    if months_since <= 18:
        return 30.0
    return 10.0


def _score_news(news_count: int) -> float:
    if news_count <= 0:
        return 0.0
    if news_count <= 2:
        return 40.0
    if news_count <= 5:
        return 70.0
    return 100.0


def _headcount_to_order(headcount: str | None) -> int:
    if not headcount:
        return -1
    order = [
        "1-10",
        "11-50",
        "51-200",
        "201-500",
        "501-1000",
        "1001-5000",
        "5001-10000",
        "10001+",
    ]
    return order.index(headcount) if headcount in order else -1


def _matches_input(record: AbrRecord, normalized_input: dict[str, Any] | None) -> bool:
    if not normalized_input:
        return True
    fg = normalized_input.get("firmographic", {})
    industries = {x.lower() for x in fg.get("industries", []) if isinstance(x, str)}
    regions = set(fg.get("regions", []))
    headcounts = set(fg.get("headcount_ranges", []))

    if industries:
        rec_industry = (record.industry_anzsic or "").lower()
        rec_sub_industry = (record.sub_industry or "").lower()
        matched = False
        for requested in industries:
            if requested in rec_industry or requested in rec_sub_industry:
                matched = True
                break
            # Practical synonym for MVP fixtures.
            if requested == "saas" and ("software" in rec_industry or "software" in rec_sub_industry):
                matched = True
                break
        if not matched:
            return False
    if regions and record.state not in regions and record.suburb not in regions and normalized_input.get("market") not in regions:
        # Keep Australia market as broad pass-through.
        if "Australia" not in regions:
            return False
    if headcounts and record.employee_range not in headcounts:
        return False
    return True


def build_ranked_company_records(
    *,
    abr_records: list[AbrRecord],
    vc_records: list[VcRecord],
    jobs_records: list[JobsRecord],
    news_records: list[NewsRecord],
    normalized_input: dict[str, Any] | None = None,
) -> list[CompanyRecord]:
    now = datetime.now(timezone.utc)
    vc_by_abn = {x.abn: x for x in vc_records}
    jobs_by_abn = {x.abn: x for x in jobs_records}
    news_by_abn: dict[str, list[NewsRecord]] = {}
    for n in news_records:
        news_by_abn.setdefault(n.abn, []).append(n)

    output: list[CompanyRecord] = []

    for abr in abr_records:
        if not _matches_input(abr, normalized_input):
            continue

        vc = vc_by_abn.get(abr.abn)
        jobs = jobs_by_abn.get(abr.abn)
        news = news_by_abn.get(abr.abn, [])

        hiring_score = _score_hiring(jobs)
        funding_score = _score_funding(vc, now)
        news_score = _score_news(len(news))
        signal_score = round((hiring_score * 0.6) + (funding_score * 0.3) + (news_score * 0.1), 2)

        summaries: list[str] = []
        sources: list[SignalSource] = []
        refs: list[str] = []

        if jobs:
            summaries.append(f"Hiring {jobs.open_roles} open roles ({jobs.roles_last_30_days} in last 30 days)")
            sources.append(
                SignalSource(
                    type="hiring",
                    source_name=jobs.source or "Jobs",
                    source_url=None,
                    collected_at_utc=jobs.captured_at_utc or now.isoformat(),
                    confidence=0.9,
                )
            )
            refs.append(f"jobs:{jobs.source}:{jobs.captured_at_utc}")

        if vc:
            stage = vc.funding_stage or "VC-backed"
            summaries.append(f"{stage} funding signal")
            sources.append(
                SignalSource(
                    type="funding",
                    source_name="VC Portfolio",
                    source_url=None,
                    collected_at_utc=(vc.last_funding_date + "T00:00:00Z") if vc.last_funding_date else now.isoformat(),
                    confidence=0.85,
                )
            )
            refs.append(f"vc:{','.join(vc.investor_names)}:{vc.last_funding_date}")

        if news:
            latest_news = max(news, key=lambda x: x.published_at_utc)
            summaries.append(f"{len(news)} recent news mentions")
            sources.append(
                SignalSource(
                    type="news",
                    source_name=latest_news.source_name or "News",
                    source_url=latest_news.source_url or None,
                    collected_at_utc=latest_news.published_at_utc or now.isoformat(),
                    confidence=0.75,
                )
            )
            refs.append(f"news:{latest_news.source_name}:{latest_news.published_at_utc}")

        if not summaries:
            summaries.append("No strong recent signals")

        output.append(
            CompanyRecord(
                company_id=abr.abn,
                name=abr.trading_name or abr.entity_name,
                domain=abr.website.replace("https://", "").replace("http://", "").strip("/") if abr.website else None,
                location=abr.suburb or abr.state or "Australia",
                industry=abr.sub_industry or abr.industry_anzsic or "Unknown",
                headcount_range=abr.employee_range or None,
                signal_score=signal_score,
                signal_summary=summaries,
                signal_sources=sources,
                source_refs=refs,
                updated_at_utc=now.isoformat(),
            )
        )

    output.sort(
        key=lambda x: (
            -x.signal_score,
            -_headcount_to_order(x.headcount_range),
            x.name.lower(),
        )
    )
    return output
