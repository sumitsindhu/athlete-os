from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import LLMProvider, settings


def llm_configuration_error(provider: LLMProvider | None = None) -> str | None:
    active = provider or settings.llm_provider
    if settings.api_key_for_provider(active):
        return None
    match active:
        case LLMProvider.OPENAI:
            return "Set OPENAI_API_KEY for LLM_PROVIDER=openai."
        case LLMProvider.GEMINI:
            return "Set GOOGLE_API_KEY for LLM_PROVIDER=gemini."
        case LLMProvider.ANTHROPIC:
            return "Set ANTHROPIC_API_KEY for LLM_PROVIDER=anthropic."
    return "Unknown LLM provider."


def get_chat_model(*, provider: LLMProvider | None = None) -> BaseChatModel:
    active = provider or settings.llm_provider
    match active:
        case LLMProvider.OPENAI:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0,
            )
        case LLMProvider.GEMINI:
            from app.llm.gemini_http import GeminiHttpChatModel

            model = settings.gemini_model.removeprefix("models/")
            return GeminiHttpChatModel(
                model=model,
                api_key=settings.google_api_key or "",
                temperature=0,
            )
        case LLMProvider.ANTHROPIC:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=settings.anthropic_model,
                api_key=settings.anthropic_api_key,
                temperature=0,
            )

    raise RuntimeError(f"Unsupported LLM provider: {active!r}")
