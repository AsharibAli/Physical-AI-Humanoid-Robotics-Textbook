"""
Response generation service using OpenAI API.

This module generates responses using retrieved context.
"""

from typing import Optional

from openai import OpenAI


class ResponseGenerator:
    """Generates responses using OpenAI's completion API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
    ):
        """
        Initialize response generator.

        Args:
            api_key: OpenAI API key
            model: Model to use for completion
            temperature: Temperature for sampling (lower = more focused)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def generate_response(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
    ) -> tuple[str, float]:
        """
        Generate a response based on query and retrieved context.

        Args:
            query: User's query
            context: Retrieved context from vector store
            system_prompt: Optional custom system prompt

        Returns:
            Tuple of (response_text, confidence_score)
        """
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt()

        # Build user message with context and query
        user_message = self._build_user_message(query, context)

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=self.temperature,
            max_tokens=1000,
        )

        response_text = response.choices[0].message.content or ""

        # Estimate confidence based on response characteristics
        confidence = self._estimate_confidence(response_text, context)

        return response_text, confidence

    def _get_default_system_prompt(self) -> str:
        """
        Get the default system prompt for RAG.

        Returns:
            System prompt string
        """
        return """You are an AI assistant helping students learn about Physical AI and Humanoid Robotics.

Your task is to answer questions based STRICTLY on the provided context from the textbook. Follow these rules:

1. ONLY use information from the provided context sources
2. If the context doesn't contain enough information to answer, say "I don't have enough information in the textbook to answer this question."
3. DO NOT make up information or use external knowledge
4. When citing information, reference the source number (e.g., "According to Source 1...")
5. Be clear, concise, and educational
6. If the user's question is ambiguous, ask for clarification
7. Format your answers with proper structure (paragraphs, lists when appropriate)

Remember: Accuracy is more important than completeness. It's better to say "I don't know" than to hallucinate information."""

    def _build_user_message(self, query: str, context: str) -> str:
        """
        Build the user message with context and query.

        Args:
            query: User's query
            context: Retrieved context

        Returns:
            Formatted user message
        """
        if not context:
            return f"""Question: {query}

Context: No relevant information found in the textbook.

Please answer based on the available context."""

        return f"""Context from textbook:

{context}

---

Question: {query}

Please answer the question using ONLY the information from the context above. Cite specific sources when possible."""

    def _estimate_confidence(self, response: str, context: str) -> float:
        """
        Estimate confidence score for the response.

        Args:
            response: Generated response
            context: Retrieved context

        Returns:
            Confidence score (0-1)
        """
        # Simple heuristic-based confidence estimation

        confidence = 0.5  # Base confidence

        # Increase confidence if response contains source citations
        if "Source" in response or "According to" in response:
            confidence += 0.2

        # Decrease confidence if response indicates uncertainty
        uncertainty_phrases = [
            "I don't have enough information",
            "I'm not sure",
            "unclear",
            "cannot answer",
        ]
        if any(phrase.lower() in response.lower() for phrase in uncertainty_phrases):
            confidence -= 0.3

        # Increase confidence if context is substantial
        if context and len(context) > 500:
            confidence += 0.1

        # Ensure confidence is in [0, 1]
        return max(0.0, min(1.0, confidence))

    def generate_response_with_selected_text(
        self,
        query: str,
        context: str,
        selected_text: str,
    ) -> tuple[str, float]:
        """
        Generate a response focused on selected text.

        Args:
            query: User's query
            context: Retrieved context
            selected_text: User's highlighted text

        Returns:
            Tuple of (response_text, confidence_score)
        """
        system_prompt = """You are an AI assistant helping students understand specific passages from a Physical AI and Humanoid Robotics textbook.

The user has highlighted a specific passage and is asking a question about it. Your task is to:

1. Focus your answer on the highlighted passage
2. Use the additional context ONLY to provide supporting information
3. Stay within the scope of the highlighted text
4. Be concise and directly address the question
5. If the question cannot be answered from the highlighted passage, say so clearly

Remember: The highlighted passage is the primary source."""

        user_message = f"""Highlighted passage:
{selected_text}

---

Additional context from textbook:
{context}

---

Question: {query}

Please answer the question focusing primarily on the highlighted passage above."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=self.temperature,
            max_tokens=800,
        )

        response_text = response.choices[0].message.content or ""
        confidence = self._estimate_confidence(response_text, context)

        return response_text, confidence
