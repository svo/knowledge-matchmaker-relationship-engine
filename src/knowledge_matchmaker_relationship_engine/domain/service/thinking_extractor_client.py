from abc import ABC, abstractmethod


class ThinkingExtractorClient(ABC):
    @abstractmethod
    def extract(self, draft_text: str) -> list[dict]:
        pass
