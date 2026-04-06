import os

import httpx

from knowledge_matchmaker_relationship_engine.domain.service.thinking_extractor_client import ThinkingExtractorClient


class ThinkingExtractorHttpClient(ThinkingExtractorClient):
    def __init__(self) -> None:
        self._base_url = os.environ.get("THINKING_EXTRACTOR_URL", "http://localhost:8001")

    def extract(self, draft_text: str) -> list[dict]:
        with httpx.Client() as client:
            response = client.post(
                f"{self._base_url}/extract",
                json={"text": draft_text},
            )
            response.raise_for_status()
            return response.json()["positions"]
