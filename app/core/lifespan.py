from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.agents.graph import build_agent_graph
from app.llm.runtime import init_llm, shutdown_llm


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.llm_config_error = init_llm()
    app.state.agent_graph = build_agent_graph()
    yield
    app.state.agent_graph = None
    app.state.llm_config_error = None
    shutdown_llm()
