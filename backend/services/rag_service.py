"""
RAG (Retrieval-Augmented Generation) orchestration service.

This module orchestrates the complete RAG pipeline: retrieval + generation + citation extraction.
"""

from typing import Optional

from backend.ingestion.embedder import EmbeddingGenerator
from backend.ingestion.vector_store import VectorStore
from backend.models.query import QueryRequest, QueryResponse, SourceCitation
from backend.services.response_generator import ResponseGenerator
from backend.services.retrieval_service import RetrievalService
from backend.services.selection_handler import SelectionHandler


class RAGService:
    """Orchestrates the complete RAG pipeline."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: EmbeddingGenerator,
        response_generator: ResponseGenerator,
    ):
        """
        Initialize RAG service.

        Args:
            vector_store: VectorStore instance
            embedder: EmbeddingGenerator instance
            response_generator: ResponseGenerator instance
        """
        self.retrieval_service = RetrievalService(vector_store, embedder)
        self.response_generator = response_generator
        self.selection_handler = SelectionHandler()

    def process_query(
        self,
        request: QueryRequest,
    ) -> QueryResponse:
        """
        Process a query through the complete RAG pipeline.

        Args:
            request: QueryRequest with query details

        Returns:
            QueryResponse with answer and citations
        """
        # Step 1: Retrieve relevant chunks
        if request.query_mode == "selected-text" and request.selected_text:
            # Retrieve more chunks initially for better filtering
            initial_chunks = self.retrieval_service.retrieve_for_selected_text(
                query_text=request.query_text,
                selected_text=request.selected_text,
                max_results=request.max_results * 2,  # Get 2x for filtering
            )

            # Filter chunks using selection handler (T087)
            retrieved_chunks = self.selection_handler.filter_chunks_by_selection(
                retrieved_chunks=initial_chunks,
                selected_text=request.selected_text,
                max_results=request.max_results,
            )
        else:
            retrieved_chunks = self.retrieval_service.retrieve_relevant_chunks(
                query_text=request.query_text,
                max_results=request.max_results,
                score_threshold=0.7,
            )

        # Step 2: Format context for LLM
        base_context = self.retrieval_service.format_context_for_llm(retrieved_chunks)

        # Enhance context with selected text if in selected-text mode (T087)
        if request.query_mode == "selected-text" and request.selected_text:
            context = self.selection_handler.enhance_context_with_selection(
                base_context=base_context,
                selected_text=request.selected_text,
            )
        else:
            context = base_context

        # Step 3: Generate response
        if request.query_mode == "selected-text" and request.selected_text:
            response_text, confidence = self.response_generator.generate_response_with_selected_text(
                query=request.query_text,
                context=context,
                selected_text=request.selected_text,
            )
        else:
            response_text, confidence = self.response_generator.generate_response(
                query=request.query_text,
                context=context,
            )

        # Step 4: Extract source citations
        source_citations = self._extract_source_citations(retrieved_chunks)

        # Step 5: Build response
        return QueryResponse(
            response_text=response_text,
            source_citations=source_citations,
            confidence_score=confidence,
            session_id=request.session_id,
            retrieved_chunks=len(retrieved_chunks),
        )

    def _extract_source_citations(
        self,
        retrieved_chunks: list[dict],
    ) -> list[SourceCitation]:
        """
        Extract source citations from retrieved chunks.

        Args:
            retrieved_chunks: List of retrieved chunks with metadata

        Returns:
            List of SourceCitation objects
        """
        citations = []

        for chunk in retrieved_chunks:
            payload = chunk["payload"]
            score = chunk["score"]

            citation = SourceCitation(
                chapter_id=payload.get("chapter_id", "unknown"),
                chapter_title=payload.get("chapter_title", "Unknown Chapter"),
                module_id=payload.get("module_id", "unknown-module"),
                section_type=payload.get("section_type", "general"),
                file_path=payload.get("file_path", ""),
                chunk_text=payload.get("chunk_text", ""),
                relevance_score=score,
            )
            citations.append(citation)

        return citations

    def health_check(self) -> dict[str, str]:
        """
        Perform health check on RAG system components.

        Returns:
            Dict with health status of each component
        """
        status = {
            "vector_store": "unknown",
            "embedder": "unknown",
            "response_generator": "unknown",
        }

        # Check vector store
        try:
            if self.retrieval_service.vector_store.collection_exists():
                status["vector_store"] = "healthy"
            else:
                status["vector_store"] = "no_collection"
        except Exception as e:
            status["vector_store"] = f"error: {str(e)}"

        # Check embedder (try to generate a test embedding)
        try:
            test_embedding = self.retrieval_service.embedder.generate_embedding("test")
            if test_embedding and len(test_embedding) > 0:
                status["embedder"] = "healthy"
            else:
                status["embedder"] = "error: empty embedding"
        except Exception as e:
            status["embedder"] = f"error: {str(e)}"

        # Check response generator (simple check)
        try:
            if self.response_generator.client:
                status["response_generator"] = "healthy"
        except Exception as e:
            status["response_generator"] = f"error: {str(e)}"

        return status
