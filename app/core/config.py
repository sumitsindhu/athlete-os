from enum import StrEnum
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(StrEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AthleteOS"
    app_version: str = "0.1.0"
    log_level: str = "INFO"

    llm_provider: LLMProvider = LLMProvider.OPENAI

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    google_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-20250514"

    @field_validator("llm_provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    def api_key_for_provider(self, provider: LLMProvider | None = None) -> str | None:
        active = provider or self.llm_provider
        match active:
            case LLMProvider.OPENAI:
                return self.openai_api_key
            case LLMProvider.GEMINI:
                return self.google_api_key
            case LLMProvider.ANTHROPIC:
                return self.anthropic_api_key
        return None

    @property
    def llm_configured(self) -> bool:
        key = self.api_key_for_provider()
        return bool(key and key.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
