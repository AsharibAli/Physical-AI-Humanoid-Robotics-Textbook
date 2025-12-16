"""
Health check endpoint.

This module provides health monitoring for the RAG backend.
"""

from fastapi import APIRouter, Depends

from backend.api.dependencies import get_rag_service
from backend.services.rag_service import RAGService

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Health check endpoint.

    Checks connectivity to:
    - Qdrant vector database
    - OpenAI API (embeddings)
    - OpenAI API (completions)

    Returns:
        Dict with health status of each component
    """
    health_status = rag_service.health_check()

    # Determine overall status
    all_healthy = all(status == "healthy" for status in health_status.values())

    return {
        "status": "healthy" if all_healthy else "degraded",
        "components": health_status,
    }


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Physical AI Textbook RAG API",
        "version": "1.0.0",
        "description": "RAG-powered backend for Physical AI & Humanoid Robotics textbook",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
