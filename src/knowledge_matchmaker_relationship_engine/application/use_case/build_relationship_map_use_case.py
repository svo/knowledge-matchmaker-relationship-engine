from knowledge_matchmaker_relationship_engine.domain.model.relationship import Pointer, RelationshipMap
from knowledge_matchmaker_relationship_engine.domain.service.corpus_query import CorpusQuery
from knowledge_matchmaker_relationship_engine.domain.service.relationship_classifier import RelationshipClassifier
from knowledge_matchmaker_relationship_engine.domain.service.thinking_extractor_client import ThinkingExtractorClient


class BuildRelationshipMapUseCase:
    def __init__(
        self,
        thinking_extractor_client: ThinkingExtractorClient,
        corpus_query: CorpusQuery,
        relationship_classifier: RelationshipClassifier,
    ) -> None:
        self._thinking_extractor_client = thinking_extractor_client
        self._corpus_query = corpus_query
        self._relationship_classifier = relationship_classifier

    def execute(self, draft_text: str) -> RelationshipMap:
        extracted = self._thinking_extractor_client.extract(draft_text)
        all_positions = extracted["claims"] + extracted["assumptions"] + extracted["framings"]
        thinking_summary = " ".join(all_positions)

        results = self._corpus_query.query(thinking_summary, top_k=5)

        pointers = []
        for result in results:
            relationship_type, reason = self._relationship_classifier.classify(
                thinking_summary, result["title"], result["chunk_text"]
            )
            pointers.append(
                Pointer(
                    title=result["title"],
                    source_url=result["source_url"],
                    relationship_type=relationship_type,
                    reason=reason,
                )
            )

        return RelationshipMap(pointers=pointers)
