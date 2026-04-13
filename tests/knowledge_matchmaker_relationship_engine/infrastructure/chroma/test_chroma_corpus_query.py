from unittest.mock import patch, MagicMock

from assertpy import assert_that

from knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query import (
    ChromaCorpusQuery,
)


class TestChromaCorpusQuery:
    @patch("knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.OpenAI")
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.chromadb.EphemeralClient"
    )
    def test_should_return_items_from_query_results(self, mock_chroma_client_class, mock_openai_class):
        mock_embedding_response = MagicMock()
        mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_openai_instance = MagicMock()
        mock_openai_instance.embeddings.create.return_value = mock_embedding_response
        mock_openai_class.return_value = mock_openai_instance

        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "metadatas": [
                [
                    {"title": "Paper A", "source_url": "http://a.com", "chunk_text": "some text"},
                ]
            ]
        }
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.get_or_create_collection.return_value = mock_collection
        mock_chroma_client_class.return_value = mock_chroma_instance

        corpus_query = ChromaCorpusQuery()
        result = corpus_query.query("user thinking")

        assert_that(result).is_length(1)

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.OpenAI")
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.chromadb.EphemeralClient"
    )
    def test_should_return_title_from_metadata(self, mock_chroma_client_class, mock_openai_class):
        mock_embedding_response = MagicMock()
        mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_openai_instance = MagicMock()
        mock_openai_instance.embeddings.create.return_value = mock_embedding_response
        mock_openai_class.return_value = mock_openai_instance

        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "metadatas": [
                [
                    {"title": "Paper A", "source_url": "http://a.com", "chunk_text": "some text"},
                ]
            ]
        }
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.get_or_create_collection.return_value = mock_collection
        mock_chroma_client_class.return_value = mock_chroma_instance

        corpus_query = ChromaCorpusQuery()
        result = corpus_query.query("user thinking")

        assert_that(result[0]["title"]).is_equal_to("Paper A")

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.OpenAI")
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.chromadb.EphemeralClient"
    )
    def test_should_return_empty_list_when_no_metadatas(self, mock_chroma_client_class, mock_openai_class):
        mock_embedding_response = MagicMock()
        mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_openai_instance = MagicMock()
        mock_openai_instance.embeddings.create.return_value = mock_embedding_response
        mock_openai_class.return_value = mock_openai_instance

        mock_collection = MagicMock()
        mock_collection.query.return_value = {"metadatas": []}
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.get_or_create_collection.return_value = mock_collection
        mock_chroma_client_class.return_value = mock_chroma_instance

        corpus_query = ChromaCorpusQuery()
        result = corpus_query.query("user thinking")

        assert_that(result).is_empty()

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.OpenAI")
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.chromadb.EphemeralClient"
    )
    def test_should_use_text_embedding_model(self, mock_chroma_client_class, mock_openai_class):
        mock_embedding_response = MagicMock()
        mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_openai_instance = MagicMock()
        mock_openai_instance.embeddings.create.return_value = mock_embedding_response
        mock_openai_class.return_value = mock_openai_instance

        mock_collection = MagicMock()
        mock_collection.query.return_value = {"metadatas": []}
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.get_or_create_collection.return_value = mock_collection
        mock_chroma_client_class.return_value = mock_chroma_instance

        corpus_query = ChromaCorpusQuery()
        corpus_query.query("user thinking")

        call_kwargs = mock_openai_instance.embeddings.create.call_args.kwargs
        assert_that(call_kwargs["model"]).is_equal_to("text-embedding-3-small")

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.OpenAI")
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.chromadb.EphemeralClient"
    )
    def test_should_pass_top_k_as_n_results(self, mock_chroma_client_class, mock_openai_class):
        mock_embedding_response = MagicMock()
        mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_openai_instance = MagicMock()
        mock_openai_instance.embeddings.create.return_value = mock_embedding_response
        mock_openai_class.return_value = mock_openai_instance

        mock_collection = MagicMock()
        mock_collection.query.return_value = {"metadatas": []}
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.get_or_create_collection.return_value = mock_collection
        mock_chroma_client_class.return_value = mock_chroma_instance

        corpus_query = ChromaCorpusQuery()
        corpus_query.query("user thinking", top_k=3)

        assert_that(mock_collection.query.call_args.kwargs["n_results"]).is_equal_to(3)

    @patch("knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.OpenAI")
    @patch(
        "knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query.chromadb.EphemeralClient"
    )
    def test_should_default_missing_metadata_fields_to_empty_string(self, mock_chroma_client_class, mock_openai_class):
        mock_embedding_response = MagicMock()
        mock_embedding_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_openai_instance = MagicMock()
        mock_openai_instance.embeddings.create.return_value = mock_embedding_response
        mock_openai_class.return_value = mock_openai_instance

        mock_collection = MagicMock()
        mock_collection.query.return_value = {"metadatas": [[{}]]}
        mock_chroma_instance = MagicMock()
        mock_chroma_instance.get_or_create_collection.return_value = mock_collection
        mock_chroma_client_class.return_value = mock_chroma_instance

        corpus_query = ChromaCorpusQuery()
        result = corpus_query.query("user thinking")

        assert_that(result[0]["title"]).is_equal_to("")
