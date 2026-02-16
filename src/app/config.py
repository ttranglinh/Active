from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    environment: str = 'dev'

