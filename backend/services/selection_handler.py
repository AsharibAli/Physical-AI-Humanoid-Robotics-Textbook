"""
Selection handler for context-aware text selection queries.

This module filters retrieved chunks to focus on selected text context.
"""

from typing import Optional


class SelectionHandler:
    """Handles filtering and context extraction for selected text queries."""

    def __init__(self, similarity_threshold: float = 0.3):
        """
        Initialize selection handler.

        Args:
            similarity_threshold: Minimum word overlap ratio to consider a chunk relevant
        """
        self.similarity_threshold = similarity_threshold

    def filter_chunks_by_selection(
        self,
        retrieved_chunks: list[dict],
        selected_text: str,
        max_results: int = 3,
    ) -> list[dict]:
        """
        Filter retrieved chunks to focus on those most relevant to selected text.

        Args:
            retrieved_chunks: List of chunks from vector search
            selected_text: User's highlighted text
            max_results: Maximum chunks to return

        Returns:
            Filtered list of chunks sorted by relevance to selected text
        """
        if not selected_text or not retrieved_chunks:
            return retrieved_chunks[:max_results]

        # Extract keywords from selected text (simple word-based approach)
        selected_words = self._extract_keywords(selected_text)

        # Score each chunk based on overlap with selected text
        scored_chunks = []
        for chunk in retrieved_chunks:
            chunk_text = chunk.get("payload", {}).get("chunk_text", "")
            overlap_score = self._calculate_overlap_score(chunk_text, selected_words)

            # Combine vector similarity score with text overlap score
            vector_score = chunk.get("score", 0.0)
            combined_score = (vector_score * 0.6) + (overlap_score * 0.4)

            scored_chunks.append({
                **chunk,
                "combined_score": combined_score,
                "text_overlap": overlap_score,
            })

        # Sort by combined score
        scored_chunks.sort(key=lambda x: x["combined_score"], reverse=True)

        # Filter chunks that meet the similarity threshold
        filtered_chunks = [
            chunk for chunk in scored_chunks
            if chunk["text_overlap"] >= self.similarity_threshold
        ]

        # If filtering is too aggressive, fall back to top chunks
        if not filtered_chunks and scored_chunks:
            filtered_chunks = scored_chunks[:max_results]

        return filtered_chunks[:max_results]

    def _extract_keywords(self, text: str) -> set[str]:
        """
        Extract keywords from text.

        Args:
            text: Input text

        Returns:
            Set of lowercase keywords
        """
        # Simple keyword extraction (can be enhanced with NLP)
        words = text.lower().split()

        # Remove common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "can", "this", "that", "these",
            "those", "i", "you", "he", "she", "it", "we", "they", "what", "which",
            "who", "when", "where", "why", "how",
        }

        keywords = {word for word in words if word not in stop_words and len(word) > 2}

        return keywords

    def _calculate_overlap_score(self, chunk_text: str, selected_keywords: set[str]) -> float:
        """
        Calculate overlap score between chunk and selected text keywords.

        Args:
            chunk_text: Text chunk to score
            selected_keywords: Keywords from selected text

        Returns:
            Overlap score (0-1)
        """
        if not selected_keywords:
            return 0.0

        chunk_words = set(chunk_text.lower().split())

        # Calculate Jaccard similarity
        intersection = len(chunk_words & selected_keywords)
        union = len(chunk_words | selected_keywords)

        if union == 0:
            return 0.0

        return intersection / union

    def enhance_context_with_selection(
        self,
        base_context: str,
        selected_text: str,
    ) -> str:
        """
        Enhance the context string with selected text information.

        Args:
            base_context: Base context from retrieved chunks
            selected_text: User's selected text

        Returns:
            Enhanced context string
        """
        enhanced_context = f"""HIGHLIGHTED PASSAGE (User's Focus):
{selected_text}

---

RELATED CONTENT FROM TEXTBOOK:
{base_context}"""

        return enhanced_context

    def validate_selection_focus(
        self,
        response_text: str,
        selected_text: str,
    ) -> float:
        """
        Validate that the response focuses on the selected text.

        Args:
            response_text: Generated response
            selected_text: User's selected text

        Returns:
            Focus score (0-1), where 1.0 means response is highly focused on selection
        """
        selected_keywords = self._extract_keywords(selected_text)
        response_words = set(response_text.lower().split())

        # Check what percentage of selected keywords appear in the response
        if not selected_keywords:
            return 0.5

        keywords_in_response = len(selected_keywords & response_words)
        focus_score = keywords_in_response / len(selected_keywords)

        return min(1.0, focus_score)
