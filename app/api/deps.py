from fastapi import HTTPException, Request, status
from langgraph.graph.state import CompiledStateGraph


def get_agent_graph(request: Request) -> CompiledStateGraph:
    graph = request.app.state.agent_graph
    if graph is None:
        raise RuntimeError("Agent graph is not initialized.")
    return graph


def require_llm_configured(request: Request) -> None:
    error = request.app.state.llm_config_error
    if error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=error,
        )
