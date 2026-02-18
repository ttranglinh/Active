from __future__ import annotations

from src.modules.company_intelligence.domain.source_records import NewsRecord
from src.modules.company_intelligence.infrastructure.sources._fixture_loader import (
    load_fixture_records,
)


class NewsFixtureSource:
    file_name = "news_fixture.json"

    def fetch(self) -> list[NewsRecord]:
        return load_fixture_records(self.file_name, NewsRecord)

