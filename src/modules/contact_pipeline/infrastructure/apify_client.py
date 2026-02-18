from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import os
import time

import requests


APIFY_API_BASE = "https://api.apify.com/v2"


@dataclass(frozen=True)
class ApifyConfig:
    api_token: str
    actor_id: str = "harvestapi~linkedin-profile-search"
    timeout_seconds: int = 60
    poll_interval_seconds: int = 3
    max_wait_seconds: int = 300

    @classmethod
    def from_env(cls) -> "ApifyConfig":
        api_token = os.getenv("APIFY_TOKEN", "").strip()
        actor_id = os.getenv("APIFY_ACTOR_ID", "harvestapi~linkedin-profile-search").strip()
        if not api_token:
            raise RuntimeError("Missing APIFY_TOKEN in environment.")
        if not actor_id:
            raise RuntimeError("Missing APIFY_ACTOR_ID in environment.")
        return cls(api_token=api_token, actor_id=actor_id)


class ApifyClient:
    def __init__(self, config: ApifyConfig) -> None:
        self._config = config

    def start_run(self, actor_input: dict[str, Any]) -> dict[str, Any]:
        url = (
            f"{APIFY_API_BASE}/acts/{self._config.actor_id}/runs"
            f"?token={self._config.api_token}"
        )
        response = requests.post(url, json=actor_input, timeout=self._config.timeout_seconds)
        response.raise_for_status()
        data = response.json().get("data", {})
        if not data:
            raise RuntimeError("Apify start_run returned empty run data.")
        return data

    def get_run(self, run_id: str) -> dict[str, Any]:
        url = f"{APIFY_API_BASE}/actor-runs/{run_id}?token={self._config.api_token}"
        response = requests.get(url, timeout=self._config.timeout_seconds)
        response.raise_for_status()
        data = response.json().get("data", {})
        if not data:
            raise RuntimeError(f"Apify get_run returned empty data for run: {run_id}")
        return data

    def wait_for_run(self, run_id: str) -> dict[str, Any]:
        waited = 0
        while waited <= self._config.max_wait_seconds:
            run = self.get_run(run_id)
            status = run.get("status")
            if status == "SUCCEEDED":
                return run
            if status in {"FAILED", "ABORTED", "TIMED-OUT"}:
                raise RuntimeError(f"Apify run failed with status: {status}")
            time.sleep(self._config.poll_interval_seconds)
            waited += self._config.poll_interval_seconds
        raise TimeoutError(
            f"Apify run did not finish within {self._config.max_wait_seconds} seconds."
        )

    def get_dataset_items(self, dataset_id: str) -> list[dict[str, Any]]:
        url = (
            f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
            f"?token={self._config.api_token}&clean=true"
        )
        response = requests.get(url, timeout=self._config.timeout_seconds)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise RuntimeError("Apify dataset items response is not a list.")
        return data

