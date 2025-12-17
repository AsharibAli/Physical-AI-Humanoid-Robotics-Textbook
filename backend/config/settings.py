"""
Application settings and configuration.

This module loads configuration from environment variables.
"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-ada-002"

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_chapters"

    # Application Configuration
    environment: str = "development"
    debug: bool = True

    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # API Configuration
    api_v1_prefix: str = "/api/v1"

    def get_allowed_origins_list(self) -> list[str]:
        """Get list of allowed CORS origins."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Singleton settings instance
settings = Settings()
