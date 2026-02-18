from __future__ import annotations

from src.modules.company_intelligence.infrastructure.sources import (
    AbrFixtureSource,
    AsicFixtureSource,
    JobsFixtureSource,
    NewsFixtureSource,
    VcFixtureSource,
)


def main() -> None:
    abr = AbrFixtureSource().fetch()
    asic = AsicFixtureSource().fetch()
    vc = VcFixtureSource().fetch()
    jobs = JobsFixtureSource().fetch()
    news = NewsFixtureSource().fetch()

    print(f"ABR records: {len(abr)}")
    print(f"ASIC records: {len(asic)}")
    print(f"VC records: {len(vc)}")
    print(f"Jobs records: {len(jobs)}")
    print(f"News records: {len(news)}")

    if abr:
        print(f"ABR sample: {abr[0].abn} | {abr[0].entity_name}")
    if vc:
        print(f"VC sample: {vc[0].abn} | {vc[0].funding_stage}")
    if jobs:
        print(f"Jobs sample: {jobs[0].abn} | open_roles={jobs[0].open_roles}")
    if news:
        print(f"News sample: {news[0].abn} | {news[0].headline[:50]}")


if __name__ == "__main__":
    main()

