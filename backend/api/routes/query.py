"""
Query endpoint for RAG chatbot.

This module handles user queries and returns AI-generated responses with source citations.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.dependencies import get_rag_service
from backend.models.query import QueryRequest, QueryResponse
from backend.services.rag_service import RAGService

router = APIRouter(tags=["query"])


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
)
async def process_query(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Process a user query through the RAG system.

    This endpoint:
    1. Retrieves relevant document chunks from the vector database
    2. Generates a response using OpenAI's completion API
    3. Returns the response with source citations

    Args:
        request: QueryRequest with user's question and options
        rag_service: RAG service instance (injected)

    Returns:
        QueryResponse with answer and source citations

    Raises:
        HTTPException: 400 for invalid requests, 500 for internal errors
    """
    try:
        # Validate selected text requirement
        if request.query_mode == "selected-text" and not request.selected_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="selected_text is required when query_mode='selected-text'",
            )

        # Process query through RAG pipeline
        response = rag_service.process_query(request)

        return response

    except ValueError as e:
        # Validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Internal errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
