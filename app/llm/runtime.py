from langchain_core.runnables import Runnable

from app.chains.chat import build_chat_chain_from_model
from app.llm.factory import get_chat_model, llm_configuration_error

_config_error: str | None = None
_chat_chain: Runnable | None = None


def init_llm() -> str | None:
    global _config_error, _chat_chain
    _config_error = llm_configuration_error()
    _chat_chain = None
    if _config_error is None:
        _chat_chain = build_chat_chain_from_model(get_chat_model())
    return _config_error


def shutdown_llm() -> None:
    global _config_error, _chat_chain
    _config_error = None
    _chat_chain = None


def llm_boot_error() -> str | None:
    return _config_error


def get_chat_chain() -> Runnable:
    if _config_error is not None:
        raise RuntimeError(_config_error)
    if _chat_chain is None:
        raise RuntimeError("LLM is not initialized.")
    return _chat_chain
