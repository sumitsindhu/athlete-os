from typing import Annotated

from fastapi import APIRouter, Depends
from langgraph.graph.state import CompiledStateGraph

from app.api.deps import get_agent_graph, require_llm_configured
from app.schemas.agent import AgentRunRequest, AgentRunResponse
from app.services.agent_runner import run_agent_graph

router = APIRouter()


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(
    body: AgentRunRequest,
    graph: CompiledStateGraph = Depends(get_agent_graph),
    _: Annotated[None, Depends(require_llm_configured)] = None,
) -> AgentRunResponse:
    return await run_agent_graph(graph, message=body.message, thread_id=body.thread_id)
