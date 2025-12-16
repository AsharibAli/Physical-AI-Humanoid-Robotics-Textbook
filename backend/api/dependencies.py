"""
Dependency injection for FastAPI endpoints.

This module provides singleton instances of services for API endpoints.
"""

from functools import lru_cache

from backend.config.settings import settings
from backend.ingestion.embedder import EmbeddingGenerator
from backend.ingestion.vector_store import VectorStore
from backend.services.rag_service import RAGService
from backend.services.response_generator import ResponseGenerator


@lru_cache()
def get_vector_store() -> VectorStore:
    """
    Get singleton VectorStore instance.

    Returns:
        VectorStore instance
    """
    return VectorStore(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        collection_name=settings.qdrant_collection_name,
    )


@lru_cache()
def get_embedder() -> EmbeddingGenerator:
    """
    Get singleton EmbeddingGenerator instance.

    Returns:
        EmbeddingGenerator instance
    """
    return EmbeddingGenerator(
        api_key=settings.openai_api_key,
        model=settings.openai_embedding_model,
    )


@lru_cache()
def get_response_generator() -> ResponseGenerator:
    """
    Get singleton ResponseGenerator instance.

    Returns:
        ResponseGenerator instance
    """
    return ResponseGenerator(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )


@lru_cache()
def get_rag_service() -> RAGService:
    """
    Get singleton RAGService instance.

    Returns:
        RAGService instance
    """
    return RAGService(
        vector_store=get_vector_store(),
        embedder=get_embedder(),
        response_generator=get_response_generator(),
    )
