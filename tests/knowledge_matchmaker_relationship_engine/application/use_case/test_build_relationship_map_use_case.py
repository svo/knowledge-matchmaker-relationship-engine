from unittest.mock import Mock

import pytest
from assertpy import assert_that

from knowledge_matchmaker_relationship_engine.application.use_case.build_relationship_map_use_case import (
    BuildRelationshipMapUseCase,
)
from knowledge_matchmaker_relationship_engine.domain.model.relationship import RelationshipMap, RelationshipType
from knowledge_matchmaker_relationship_engine.domain.service.corpus_query import CorpusQuery
from knowledge_matchmaker_relationship_engine.domain.service.relationship_classifier import RelationshipClassifier
from knowledge_matchmaker_relationship_engine.domain.service.thinking_extractor_client import ThinkingExtractorClient


class TestBuildRelationshipMapUseCase:
    @pytest.fixture
    def mock_thinking_extractor_client(self) -> Mock:
        mock = Mock(spec=ThinkingExtractorClient)
        mock.extract.return_value = {"claims": ["distributed cognition is key"], "assumptions": [], "framings": []}
        return mock

    @pytest.fixture
    def mock_corpus_query(self) -> Mock:
        mock = Mock(spec=CorpusQuery)
        mock.query.return_value = [
            {"title": "Being and Time", "source_url": "https://example.com/being", "chunk_text": "Readiness-to-hand..."}
        ]
        return mock

    @pytest.fixture
    def mock_relationship_classifier(self) -> Mock:
        mock = Mock(spec=RelationshipClassifier)
        mock.classify.return_value = (RelationshipType.CONFLICT, "Challenges your claim about distributed cognition.")
        return mock

    @pytest.fixture
    def use_case(
        self, mock_thinking_extractor_client, mock_corpus_query, mock_relationship_classifier
    ) -> BuildRelationshipMapUseCase:
        return BuildRelationshipMapUseCase(
            thinking_extractor_client=mock_thinking_extractor_client,
            corpus_query=mock_corpus_query,
            relationship_classifier=mock_relationship_classifier,
        )

    def test_should_call_thinking_extractor_with_draft_text(self, use_case, mock_thinking_extractor_client):
        use_case.execute("My draft about cognition.")

        mock_thinking_extractor_client.extract.assert_called_once_with("My draft about cognition.")

    def test_should_call_corpus_query_with_thinking_summary(self, use_case, mock_corpus_query):
        use_case.execute("My draft about cognition.")

        mock_corpus_query.query.assert_called_once_with("distributed cognition is key", top_k=5)

    def test_should_return_relationship_map(self, use_case):
        result = use_case.execute("My draft about cognition.")

        assert_that(result).is_instance_of(RelationshipMap)

    def test_should_return_empty_map_when_corpus_empty(self, use_case, mock_corpus_query):
        mock_corpus_query.query.return_value = []

        result = use_case.execute("My draft about cognition.")

        assert_that(result.pointers).is_empty()
