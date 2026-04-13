import os
from typing import Sequence

import chromadb
from openai import OpenAI

from knowledge_matchmaker_relationship_engine.domain.service.corpus_query import CorpusQuery


class ChromaCorpusQuery(CorpusQuery):
    def __init__(self) -> None:
        self._chroma_client = chromadb.EphemeralClient()
        self._openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self._collection = self._chroma_client.get_or_create_collection(name="corpus")

    def query(self, thinking_summary: str, top_k: int = 5) -> list[dict]:
        response = self._openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=thinking_summary,
        )
        embedding: Sequence[float] = response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["metadatas"],
        )

        items = []
        if results["metadatas"]:
            for metadata in results["metadatas"][0]:
                items.append(
                    {
                        "title": metadata.get("title", ""),
                        "source_url": metadata.get("source_url", ""),
                        "chunk_text": metadata.get("chunk_text", ""),
                    }
                )

        return items
