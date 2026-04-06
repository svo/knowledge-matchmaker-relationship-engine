from abc import ABC, abstractmethod

from knowledge_matchmaker_relationship_engine.domain.model.relationship import RelationshipType


class RelationshipClassifier(ABC):
    @abstractmethod
    def classify(self, thinking_summary: str, title: str, chunk_text: str) -> tuple[RelationshipType, str]:
        pass
