from abc import ABC, abstractmethod


class CorpusQuery(ABC):
    @abstractmethod
    def query(self, thinking_summary: str, top_k: int = 5) -> list[dict]:
        pass
