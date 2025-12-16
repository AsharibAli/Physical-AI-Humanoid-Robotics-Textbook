"""
ChatKit session management endpoints.

This module provides endpoints for creating and refreshing ChatKit sessions.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from openai import OpenAI
import logging

from backend.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chatkit", tags=["chatkit"])

# OpenAI client for ChatKit
openai_client = OpenAI(api_key=settings.openai_api_key)


class SessionResponse(BaseModel):
    """ChatKit session response with client secret."""

    client_secret: str
    session_id: str | None = None
    expires_at: int | None = None


class SessionRefreshRequest(BaseModel):
    """Request to refresh an existing ChatKit session."""

    existing_session_id: str


@router.post("/session", response_model=SessionResponse)
async def create_chatkit_session():
    """
    Create a new ChatKit session configuration.

    Returns a client_secret (OpenAI API key) that ChatKit can use.
    For production, you should use a proxy or session-based authentication.

    Returns:
        SessionResponse with client_secret for ChatKit initialization

    Raises:
        HTTPException: 500 if session creation fails
    """
    try:
        # For now, return the OpenAI API key
        # In production, you would create ephemeral keys or use a proxy
        return SessionResponse(
            client_secret=settings.openai_api_key,
            session_id=None,
            expires_at=None,
        )

    except Exception as e:
        logger.error(f"Failed to create ChatKit session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat session: {str(e)}",
        )


@router.post("/refresh", response_model=SessionResponse)
async def refresh_chatkit_session(request: SessionRefreshRequest):
    """
    Refresh an existing ChatKit session.

    Returns the same API key for continued access.

    Args:
        request: SessionRefreshRequest with existing session ID

    Returns:
        SessionResponse with refreshed client_secret

    Raises:
        HTTPException: 500 if session refresh fails
    """
    try:
        # Return the same API key
        return SessionResponse(
            client_secret=settings.openai_api_key,
            session_id=request.existing_session_id,
            expires_at=None,
        )

    except Exception as e:
        logger.error(f"Failed to refresh ChatKit session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh chat session: {str(e)}",
        )
