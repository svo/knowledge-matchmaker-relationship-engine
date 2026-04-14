from abc import ABC, abstractmethod


class ThinkingExtractorClient(ABC):
    @abstractmethod
    def extract(self, draft_text: str) -> dict[str, list[str]]:
        raise NotImplementedError
