from typing import TypedDict


class AgentGraphState(TypedDict, total=False):
    message: str
    reply: str
