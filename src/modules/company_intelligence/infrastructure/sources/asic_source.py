from __future__ import annotations

from src.modules.company_intelligence.domain.source_records import AsicRecord
from src.modules.company_intelligence.infrastructure.sources._fixture_loader import (
    load_fixture_records,
)


class AsicFixtureSource:
    file_name = "asic_fixture.json"

    def fetch(self) -> list[AsicRecord]:
        return load_fixture_records(self.file_name, AsicRecord)

