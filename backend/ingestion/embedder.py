"""
Embedding generation using OpenAI API.

This module generates vector embeddings for text chunks.
"""

import asyncio
from typing import Optional

from openai import AsyncOpenAI, OpenAI


class EmbeddingGenerator:
    """Generates embeddings using OpenAI's embedding models."""

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-ada-002",
        batch_size: int = 100,
    ):
        """
        Initialize embedding generator.

        Args:
            api_key: OpenAI API key
            model: Embedding model to use (default: text-embedding-ada-002)
            batch_size: Number of texts to embed in a single API call
        """
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.batch_size = batch_size

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        # Replace newlines with spaces (recommended by OpenAI)
        text = text.replace("\n", " ")

        response = self.client.embeddings.create(
            input=[text],
            model=self.model,
        )

        return response.data[0].embedding

    async def generate_embeddings_async(
        self,
        texts: list[str],
        show_progress: bool = True,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts asynchronously.

        Args:
            texts: List of input texts
            show_progress: Whether to print progress updates

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]

            # Clean texts
            cleaned_batch = [text.replace("\n", " ") for text in batch]

            # Generate embeddings for batch
            response = await self.async_client.embeddings.create(
                input=cleaned_batch,
                model=self.model,
            )

            # Extract embeddings
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

            if show_progress:
                print(f"Embedded {len(all_embeddings)}/{len(texts)} texts")

        return all_embeddings

    def generate_embeddings_sync(
        self,
        texts: list[str],
        show_progress: bool = True,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts synchronously.

        Args:
            texts: List of input texts
            show_progress: Whether to print progress updates

        Returns:
            List of embedding vectors
        """
        return asyncio.run(self.generate_embeddings_async(texts, show_progress))

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings for the current model.

        Returns:
            Embedding dimension
        """
        # OpenAI text-embedding-ada-002 produces 1536-dimensional embeddings
        if self.model == "text-embedding-ada-002":
            return 1536
        elif self.model.startswith("text-embedding-3-small"):
            return 1536
        elif self.model.startswith("text-embedding-3-large"):
            return 3072
        else:
            # Default fallback
            return 1536
