from __future__ import annotations

from src.modules.company_intelligence.domain.source_records import AbrRecord
from src.modules.company_intelligence.infrastructure.sources._fixture_loader import (
    load_fixture_records,
)


class AbrFixtureSource:
    file_name = "abr_fixture.json"

    def fetch(self) -> list[AbrRecord]:
        return load_fixture_records(self.file_name, AbrRecord)

