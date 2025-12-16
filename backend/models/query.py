"""
Query models for RAG chatbot API.

This module defines Pydantic models for query requests and responses.
"""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """Request model for chatbot queries."""

    query_text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's question or query text",
    )
    query_mode: Literal["full-book", "selected-text"] = Field(
        default="full-book",
        description="Query mode: 'full-book' searches entire content, 'selected-text' focuses on highlighted passage",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session ID for conversation tracking",
    )
    selected_text: Optional[str] = Field(
        default=None,
        min_length=20,
        max_length=2000,
        description="Selected text context (required when query_mode='selected-text')",
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of source chunks to retrieve",
    )

    @field_validator("selected_text")
    @classmethod
    def validate_selected_text(cls, v: Optional[str], info: Any) -> Optional[str]:
        """Validate that selected_text is provided when query_mode='selected-text'."""
        if info.data.get("query_mode") == "selected-text" and not v:
            raise ValueError("selected_text is required when query_mode='selected-text'")

        # Validate word count for selected text (T088: min 20 words, max 2000 words)
        if v:
            word_count = len(v.split())
            if word_count < 20:
                raise ValueError(f"selected_text must contain at least 20 words (got {word_count})")
            if word_count > 2000:
                raise ValueError(f"selected_text must not exceed 2000 words (got {word_count})")

        return v


class SourceCitation(BaseModel):
    """Source citation with chapter and section references."""

    chapter_id: str = Field(..., description="Unique chapter identifier")
    chapter_title: str = Field(..., description="Human-readable chapter title")
    module_id: str = Field(..., description="Module identifier (e.g., 'module-01-ros2')")
    section_type: str = Field(
        ..., description="Section type (concepts, architectures, algorithms, real-world)"
    )
    file_path: str = Field(..., description="Relative path to source file")
    chunk_text: str = Field(..., description="Retrieved text chunk")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")


class QueryResponse(BaseModel):
    """Response model for chatbot queries."""

    response_text: str = Field(..., description="Generated response from RAG system")
    source_citations: list[SourceCitation] = Field(
        default_factory=list,
        description="List of source citations supporting the response",
    )
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the response quality",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversation tracking",
    )
    retrieved_chunks: int = Field(
        default=0,
        ge=0,
        description="Number of chunks retrieved from vector store",
    )
