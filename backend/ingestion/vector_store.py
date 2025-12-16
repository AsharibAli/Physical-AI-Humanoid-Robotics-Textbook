"""
Vector store operations using Qdrant.

This module handles vector database operations for document embeddings.
"""

from typing import Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from backend.models.embedding import DocumentChunk, EmbeddingMetadata


class VectorStore:
    """Manages vector storage and retrieval using Qdrant."""

    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        collection_name: str = "textbook_chapters",
    ):
        """
        Initialize vector store.

        Args:
            url: Qdrant server URL
            api_key: Optional API key for Qdrant Cloud
            collection_name: Name of the collection to use
        """
        self.client = QdrantClient(
            url=url,
            api_key=api_key,
        )
        self.collection_name = collection_name

    def create_collection(
        self,
        vector_size: int = 1536,
        distance: Distance = Distance.COSINE,
        recreate: bool = False,
    ) -> None:
        """
        Create a collection in Qdrant.

        Args:
            vector_size: Dimension of embedding vectors
            distance: Distance metric (COSINE, EUCLID, DOT)
            recreate: If True, delete existing collection before creating
        """
        if recreate:
            try:
                self.client.delete_collection(self.collection_name)
                print(f"Deleted existing collection: {self.collection_name}")
            except Exception:
                pass

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance,
            ),
        )
        print(f"Created collection: {self.collection_name}")

    def collection_exists(self) -> bool:
        """
        Check if collection exists.

        Returns:
            True if collection exists, False otherwise
        """
        try:
            collections = self.client.get_collections()
            return any(c.name == self.collection_name for c in collections.collections)
        except Exception:
            return False

    def upsert_chunks(
        self,
        chunks: list[DocumentChunk],
        show_progress: bool = True,
    ) -> None:
        """
        Insert or update document chunks in the vector store.

        Args:
            chunks: List of DocumentChunk instances with embeddings
            show_progress: Whether to print progress updates
        """
        points = []

        for chunk in chunks:
            if chunk.embedding is None:
                raise ValueError(f"Chunk {chunk.chunk_id} has no embedding")

            # Convert metadata to dict for Qdrant payload
            payload = {
                "chapter_id": chunk.metadata.chapter_id,
                "chapter_title": chunk.metadata.chapter_title,
                "module_id": chunk.metadata.module_id,
                "section_type": chunk.metadata.section_type,
                "chunk_index": chunk.metadata.chunk_index,
                "file_path": chunk.metadata.file_path,
                "topics": chunk.metadata.topics,
                "chunk_text": chunk.metadata.chunk_text,
                "word_count": chunk.metadata.word_count,
            }

            point = PointStruct(
                id=hash(chunk.chunk_id) % (2**63),  # Convert to positive int64
                vector=chunk.embedding,
                payload=payload,
            )
            points.append(point)

        # Upsert in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i : i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch,
            )

            if show_progress:
                print(f"Upserted {min(i + batch_size, len(points))}/{len(points)} chunks")

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filter_dict: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        """
        Search for similar vectors.

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            filter_dict: Optional metadata filters

        Returns:
            List of search results with payloads and scores
        """
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=filter_dict,
            with_payload=True,
        )

        return [
            {
                "id": point.id,
                "score": point.score,
                "payload": point.payload,
            }
            for point in response.points
        ]

    def get_collection_info(self) -> dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dict with collection statistics
        """
        info = self.client.get_collection(self.collection_name)
        return {
            "name": info.config.params.vectors.size,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status,
        }

    def delete_collection(self) -> None:
        """Delete the collection."""
        self.client.delete_collection(self.collection_name)
        print(f"Deleted collection: {self.collection_name}")
