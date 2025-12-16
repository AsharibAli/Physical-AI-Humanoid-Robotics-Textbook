"""
Text chunking for document ingestion.

This module splits documents into overlapping chunks for embedding.
"""

import re
from typing import Optional


class TextChunker:
    """Splits text into overlapping chunks with section boundary awareness."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap_size: int = 100,
        respect_boundaries: bool = True,
    ):
        """
        Initialize chunker.

        Args:
            chunk_size: Target chunk size in words
            overlap_size: Overlap between chunks in words
            respect_boundaries: If True, avoid breaking at Markdown section boundaries
        """
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.respect_boundaries = respect_boundaries

    def chunk_text(
        self,
        text: str,
        section_type: Optional[str] = None,
    ) -> list[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Input text to chunk
            section_type: Optional section type for metadata

        Returns:
            List of text chunks
        """
        if not text.strip():
            return []

        # Split into words
        words = text.split()

        if len(words) <= self.chunk_size:
            # Text is small enough, return as single chunk
            return [text]

        chunks = []
        start_idx = 0

        while start_idx < len(words):
            # Calculate end index for this chunk
            end_idx = min(start_idx + self.chunk_size, len(words))

            # Extract chunk
            chunk_words = words[start_idx:end_idx]
            chunk_text = " ".join(chunk_words)

            # If respecting boundaries, try to end at sentence or paragraph boundary
            if self.respect_boundaries and end_idx < len(words):
                chunk_text = self._adjust_to_boundary(chunk_text)

            chunks.append(chunk_text)

            # Move start index forward (with overlap)
            if end_idx >= len(words):
                break
            start_idx = end_idx - self.overlap_size

        return chunks

    def _adjust_to_boundary(self, text: str) -> str:
        """
        Adjust chunk to end at a natural boundary (sentence, paragraph).

        Args:
            text: Input text to adjust

        Returns:
            Adjusted text ending at a boundary
        """
        # Try to end at paragraph break
        paragraph_match = re.search(r"\n\n", text)
        if paragraph_match and paragraph_match.start() > len(text) * 0.5:
            return text[: paragraph_match.start()]

        # Try to end at sentence boundary
        sentence_matches = list(re.finditer(r"[.!?]\s+", text))
        if sentence_matches:
            # Find last sentence break in the latter half of the chunk
            for match in reversed(sentence_matches):
                if match.end() > len(text) * 0.5:
                    return text[: match.end()].strip()

        # No good boundary found, return original
        return text

    def chunk_document_sections(
        self,
        sections: dict[str, str],
    ) -> list[tuple[str, str, int]]:
        """
        Chunk multiple document sections.

        Args:
            sections: Dict mapping section types to content

        Returns:
            List of tuples (section_type, chunk_text, chunk_index)
        """
        all_chunks = []

        for section_type, content in sections.items():
            chunks = self.chunk_text(content, section_type)
            for idx, chunk in enumerate(chunks):
                all_chunks.append((section_type, chunk, idx))

        return all_chunks

    def get_word_count(self, text: str) -> int:
        """
        Count words in text.

        Args:
            text: Input text

        Returns:
            Word count
        """
        return len(text.split())
