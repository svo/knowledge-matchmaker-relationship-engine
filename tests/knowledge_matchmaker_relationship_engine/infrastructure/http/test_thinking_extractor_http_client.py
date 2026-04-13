from unittest.mock import patch, MagicMock

from assertpy import assert_that

from knowledge_matchmaker_relationship_engine.infrastructure.http.thinking_extractor_http_client import (
    ThinkingExtractorHttpClient,
)


class TestThinkingExtractorHttpClient:
    @patch.dict("os.environ", {"THINKING_EXTRACTOR_URL": "http://test-host:9999"})
    def test_should_use_configured_base_url(self):
        client = ThinkingExtractorHttpClient()

        assert_that(client._base_url).is_equal_to("http://test-host:9999")

    @patch.dict("os.environ", {}, clear=True)
    def test_should_use_default_base_url_when_env_not_set(self):
        client = ThinkingExtractorHttpClient()

        assert_that(client._base_url).is_equal_to("http://localhost:8001")

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.http.thinking_extractor_http_client.httpx.Client")
    def test_should_return_positions_from_response(self, mock_client_class):
        mock_response = MagicMock()
        mock_response.json.return_value = {"positions": [{"text": "some thinking"}]}
        mock_client_instance = MagicMock()
        mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
        mock_client_instance.__exit__ = MagicMock(return_value=False)
        mock_client_instance.post.return_value = mock_response
        mock_client_class.return_value = mock_client_instance

        client = ThinkingExtractorHttpClient()
        result = client.extract("my draft text")

        assert_that(result).is_equal_to([{"text": "some thinking"}])

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.http.thinking_extractor_http_client.httpx.Client")
    def test_should_post_draft_text_as_json(self, mock_client_class):
        mock_response = MagicMock()
        mock_response.json.return_value = {"positions": []}
        mock_client_instance = MagicMock()
        mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
        mock_client_instance.__exit__ = MagicMock(return_value=False)
        mock_client_instance.post.return_value = mock_response
        mock_client_class.return_value = mock_client_instance

        client = ThinkingExtractorHttpClient()
        client.extract("test draft")

        mock_client_instance.post.assert_called_once_with(
            "http://localhost:8001/extract",
            json={"text": "test draft"},
        )

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.http.thinking_extractor_http_client.httpx.Client")
    def test_should_call_raise_for_status_on_response(self, mock_client_class):
        mock_response = MagicMock()
        mock_response.json.return_value = {"positions": []}
        mock_client_instance = MagicMock()
        mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
        mock_client_instance.__exit__ = MagicMock(return_value=False)
        mock_client_instance.post.return_value = mock_response
        mock_client_class.return_value = mock_client_instance

        client = ThinkingExtractorHttpClient()
        client.extract("test draft")

        assert_that(mock_response.raise_for_status.called).is_true()
