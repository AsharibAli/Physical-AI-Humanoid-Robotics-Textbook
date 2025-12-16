"""
Embedding models for document ingestion and vector storage.

This module defines Pydantic models for document metadata and embeddings.
"""

from typing import Optional

from pydantic import BaseModel, Field


class EmbeddingMetadata(BaseModel):
    """Metadata for document chunks stored in vector database."""

    chapter_id: str = Field(
        ...,
        description="Unique chapter identifier (e.g., 'module-01-chapter-01')",
    )
    chapter_title: str = Field(
        ...,
        description="Human-readable chapter title",
    )
    module_id: str = Field(
        ...,
        description="Module identifier (e.g., 'module-01-ros2')",
    )
    section_type: str = Field(
        ...,
        description="Section type: concepts, architectures, algorithms, or real-world",
    )
    chunk_index: int = Field(
        ...,
        ge=0,
        description="Index of this chunk within the chapter (0-based)",
    )
    file_path: str = Field(
        ...,
        description="Relative path to source file from frontend/docs/",
    )
    topics: list[str] = Field(
        default_factory=list,
        description="List of topic tags extracted from content",
    )
    chunk_text: str = Field(
        ...,
        min_length=1,
        description="The actual text content of this chunk",
    )
    word_count: Optional[int] = Field(
        default=None,
        ge=0,
        description="Word count of this chunk",
    )


class DocumentChunk(BaseModel):
    """Represents a chunk of document with its embedding."""

    chunk_id: str = Field(
        ...,
        description="Unique identifier for this chunk (chapter_id + chunk_index)",
    )
    text: str = Field(
        ...,
        min_length=1,
        description="Text content of the chunk",
    )
    embedding: Optional[list[float]] = Field(
        default=None,
        description="Vector embedding (populated after embedding generation)",
    )
    metadata: EmbeddingMetadata = Field(
        ...,
        description="Metadata for this chunk",
    )
