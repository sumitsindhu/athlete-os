from langgraph.graph.state import CompiledStateGraph

from app.agents.state import AgentGraphState
from app.core.config import LLMProvider, settings
from app.schemas.agent import AgentRunResponse


def _model_name_for_provider(provider: LLMProvider) -> str:
    match provider:
        case LLMProvider.OPENAI:
            return settings.openai_model
        case LLMProvider.GEMINI:
            return settings.gemini_model
        case LLMProvider.ANTHROPIC:
            return settings.anthropic_model
    return "unknown"


async def run_agent_graph(
    graph: CompiledStateGraph,
    *,
    message: str,
    thread_id: str | None = None,
) -> AgentRunResponse:
    _ = thread_id
    initial: AgentGraphState = {"message": message}
    final = await graph.ainvoke(initial)
    return AgentRunResponse(
        reply=final.get("reply", ""),
        provider=settings.llm_provider.value,
        model=_model_name_for_provider(settings.llm_provider),
    )
