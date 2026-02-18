from __future__ import annotations

from src.modules.company_intelligence.domain.source_records import VcRecord
from src.modules.company_intelligence.infrastructure.sources._fixture_loader import (
    load_fixture_records,
)


class VcFixtureSource:
    file_name = "vc_fixture.json"

    def fetch(self) -> list[VcRecord]:
        return load_fixture_records(self.file_name, VcRecord)

