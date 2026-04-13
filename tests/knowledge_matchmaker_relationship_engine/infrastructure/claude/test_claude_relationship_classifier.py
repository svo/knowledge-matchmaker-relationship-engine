from unittest.mock import patch, MagicMock

from assertpy import assert_that

from knowledge_matchmaker_relationship_engine.domain.model.relationship import RelationshipType
from knowledge_matchmaker_relationship_engine.infrastructure.claude.claude_relationship_classifier import (
    ClaudeRelationshipClassifier,
)


class TestClaudeRelationshipClassifier:
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.claude.claude_relationship_classifier.anthropic.Anthropic"
    )
    def test_should_return_relationship_type_from_tool_use(self, mock_anthropic_class):
        mock_tool_use_block = MagicMock()
        mock_tool_use_block.type = "tool_use"
        mock_tool_use_block.input = {
            "relationship_type": "RESONANCE",
            "reason": "aligns with the user's argument",
        }

        mock_response = MagicMock()
        mock_response.content = [mock_tool_use_block]

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client

        classifier = ClaudeRelationshipClassifier()
        relationship_type, _ = classifier.classify("thinking", "Title", "excerpt")

        assert_that(relationship_type).is_equal_to(RelationshipType.RESONANCE)

    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.claude.claude_relationship_classifier.anthropic.Anthropic"
    )
    def test_should_return_reason_from_tool_use(self, mock_anthropic_class):
        mock_tool_use_block = MagicMock()
        mock_tool_use_block.type = "tool_use"
        mock_tool_use_block.input = {
            "relationship_type": "CONFLICT",
            "reason": "contradicts the user's claim",
        }

        mock_response = MagicMock()
        mock_response.content = [mock_tool_use_block]

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client

        classifier = ClaudeRelationshipClassifier()
        _, reason = classifier.classify("thinking", "Title", "excerpt")

        assert_that(reason).is_equal_to("contradicts the user's claim")

    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.claude.claude_relationship_classifier.anthropic.Anthropic"
    )
    def test_should_call_anthropic_with_haiku_model(self, mock_anthropic_class):
        mock_tool_use_block = MagicMock()
        mock_tool_use_block.type = "tool_use"
        mock_tool_use_block.input = {
            "relationship_type": "BLIND_SPOT",
            "reason": "user overlooked this",
        }

        mock_response = MagicMock()
        mock_response.content = [mock_tool_use_block]

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client

        classifier = ClaudeRelationshipClassifier()
        classifier.classify("thinking", "Title", "excerpt")

        call_kwargs = mock_client.messages.create.call_args.kwargs
        assert_that(call_kwargs["model"]).is_equal_to("claude-haiku-4-5-20251001")

    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.claude.claude_relationship_classifier.anthropic.Anthropic"
    )
    def test_should_classify_open_space_relationship(self, mock_anthropic_class):
        mock_tool_use_block = MagicMock()
        mock_tool_use_block.type = "tool_use"
        mock_tool_use_block.input = {
            "relationship_type": "OPEN_SPACE",
            "reason": "an unexplored area",
        }

        mock_response = MagicMock()
        mock_response.content = [mock_tool_use_block]

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client

        classifier = ClaudeRelationshipClassifier()
        relationship_type, _ = classifier.classify("thinking", "Title", "excerpt")

        assert_that(relationship_type).is_equal_to(RelationshipType.OPEN_SPACE)
