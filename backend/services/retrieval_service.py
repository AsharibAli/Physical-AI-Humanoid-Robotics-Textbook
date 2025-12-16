"""
Retrieval service for RAG system.

This module handles vector similarity search using Qdrant.
"""

from typing import Any, Optional

from backend.ingestion.embedder import EmbeddingGenerator
from backend.ingestion.vector_store import VectorStore


class RetrievalService:
    """Handles document retrieval from vector store."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: EmbeddingGenerator,
    ):
        """
        Initialize retrieval service.

        Args:
            vector_store: VectorStore instance
            embedder: EmbeddingGenerator instance
        """
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve_relevant_chunks(
        self,
        query_text: str,
        max_results: int = 5,
        score_threshold: float = 0.7,
        filter_dict: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve relevant document chunks for a query.

        Args:
            query_text: User's query text
            max_results: Maximum number of chunks to retrieve
            score_threshold: Minimum similarity score (0-1)
            filter_dict: Optional metadata filters

        Returns:
            List of retrieved chunks with metadata and scores
        """
        # Generate query embedding
        query_embedding = self.embedder.generate_embedding(query_text)

        # Search vector store
        results = self.vector_store.search(
            query_vector=query_embedding,
            limit=max_results,
            score_threshold=score_threshold,
            filter_dict=filter_dict,
        )

        return results

    def retrieve_for_selected_text(
        self,
        query_text: str,
        selected_text: str,
        max_results: int = 3,
    ) -> list[dict[str, Any]]:
        """
        Retrieve chunks relevant to both query and selected text context.

        Args:
            query_text: User's query
            selected_text: Highlighted text from document
            max_results: Maximum results to return

        Returns:
            List of retrieved chunks filtered by context
        """
        # Generate embedding for selected text
        selected_embedding = self.embedder.generate_embedding(selected_text)

        # Generate embedding for query
        query_embedding = self.embedder.generate_embedding(query_text)

        # Average the two embeddings to balance relevance
        combined_embedding = [
            (q + s) / 2 for q, s in zip(query_embedding, selected_embedding)
        ]

        # Search with combined embedding
        results = self.vector_store.search(
            query_vector=combined_embedding,
            limit=max_results,
            score_threshold=0.6,  # Lower threshold for context-aware search
        )

        # Filter results to prefer chunks that contain similar content to selected text
        filtered_results = []
        for result in results:
            chunk_text = result["payload"].get("chunk_text", "")

            # Simple heuristic: check if any significant words from selected text appear
            selected_words = set(selected_text.lower().split())
            chunk_words = set(chunk_text.lower().split())
            overlap = len(selected_words & chunk_words)

            if overlap > 3:  # At least 3 words overlap
                filtered_results.append(result)

        return filtered_results[:max_results]

    def format_context_for_llm(
        self,
        retrieved_chunks: list[dict[str, Any]],
    ) -> str:
        """
        Format retrieved chunks into context string for LLM.

        Args:
            retrieved_chunks: List of retrieved chunks with metadata

        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return ""

        context_parts = []

        for i, chunk in enumerate(retrieved_chunks, 1):
            payload = chunk["payload"]
            score = chunk["score"]

            chapter_title = payload.get("chapter_title", "Unknown")
            section_type = payload.get("section_type", "Unknown")
            chunk_text = payload.get("chunk_text", "")

            context_parts.append(
                f"[Source {i}: {chapter_title} - {section_type} (relevance: {score:.2f})]\n{chunk_text}\n"
            )

        return "\n---\n".join(context_parts)
