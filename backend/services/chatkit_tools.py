"""
ChatKit tool handlers for search_textbook function.

This module handles tool calls from ChatKit sessions and integrates with the RAG service.
"""

import logging
from typing import Dict, Any, Optional

from backend.models.query import QueryRequest
from backend.services.rag_service import RAGService

logger = logging.getLogger(__name__)


class ChatKitToolHandler:
    """Handles tool calls from ChatKit sessions."""

    def __init__(self, rag_service: RAGService):
        """
        Initialize tool handler.

        Args:
            rag_service: RAGService instance for processing queries
        """
        self.rag_service = rag_service

    async def handle_search_textbook(
        self,
        query: str,
        selected_text: Optional[str] = None,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Handle search_textbook tool call from ChatKit.

        Args:
            query: User's search query
            selected_text: Optional highlighted text for context-aware search
            max_results: Maximum number of chunks to retrieve

        Returns:
            Formatted tool response with textbook content and citations
        """
        try:
            # Determine query mode based on selected_text
            query_mode = "selected-text" if selected_text else "full-book"

            # Create QueryRequest
            request = QueryRequest(
                query_text=query,
                query_mode=query_mode,
                selected_text=selected_text,
                max_results=max_results
            )

            # Call RAG service (reuse Phase 5 infrastructure)
            result = self.rag_service.process_query(request)

            # Format for ChatKit tool response
            formatted_result = {
                "status": "success",
                "content": result.response_text,
                "citations": [
                    {
                        "source": f"{cite.module_id}/{cite.chapter_id}",
                        "title": cite.chapter_title,
                        "section": cite.section_type,
                        "relevance": round(cite.relevance_score, 2),
                        "file_path": cite.file_path,
                        "text_preview": cite.chunk_text[:200] + "..." if len(cite.chunk_text) > 200 else cite.chunk_text
                    }
                    for cite in result.source_citations
                ],
                "confidence": round(result.confidence_score, 2),
                "chunks_retrieved": result.retrieved_chunks
            }

            logger.info(f"Successfully processed search_textbook query: '{query[:50]}...'")
            return formatted_result

        except Exception as e:
            logger.error(f"Error in search_textbook tool: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to search textbook. Please try rephrasing your question or try again later."
            }

    async def route_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Route tool calls to appropriate handlers.

        Args:
            tool_name: Name of the tool being called
            arguments: Tool arguments from ChatKit

        Returns:
            Tool execution result
        """
        if tool_name == "search_textbook":
            return await self.handle_search_textbook(**arguments)
        else:
            logger.warning(f"Unknown tool called: {tool_name}")
            return {
                "status": "error",
                "error": f"Unknown tool: {tool_name}",
                "message": "This tool is not supported."
            }
