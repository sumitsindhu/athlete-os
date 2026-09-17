from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=32000)
    thread_id: str | None = None


class AgentRunResponse(BaseModel):
    reply: str
    provider: str
    model: str
