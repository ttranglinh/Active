from __future__ import annotations

from src.modules.company_intelligence.domain.source_records import JobsRecord
from src.modules.company_intelligence.infrastructure.sources._fixture_loader import (
    load_fixture_records,
)


class JobsFixtureSource:
    file_name = "jobs_fixture.json"

    def fetch(self) -> list[JobsRecord]:
        return load_fixture_records(self.file_name, JobsRecord)

