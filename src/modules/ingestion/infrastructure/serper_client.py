from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import os

import requests


SERPER_SEARCH_URL = "https://google.serper.dev/search"


@dataclass(frozen=True)
class SerperConfig:
    api_key: str
    timeout_seconds: int = 30

    @classmethod
    def from_env(cls) -> "SerperConfig":
        api_key = os.getenv("SERPER_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("Missing SERPER_API_KEY in environment.")
        return cls(api_key=api_key)


class SerperClient:
    def __init__(self, config: SerperConfig) -> None:
        self._config = config

    def search(
        self,
        *,
        query: str,
        gl: str = "au",
        hl: str = "en",
        num: int = 10,
        page: int = 1,
    ) -> dict[str, Any]:
        payload = {
            "q": query,
            "gl": gl,
            "hl": hl,
            "num": num,
            "page": page,
        }
        headers = {
            "X-API-KEY": self._config.api_key,
            "Content-Type": "application/json",
        }
        response = requests.post(
            SERPER_SEARCH_URL,
            json=payload,
            headers=headers,
            timeout=self._config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

