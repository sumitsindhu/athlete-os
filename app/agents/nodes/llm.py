from langchain_core.messages import AIMessage

from app.agents.state import AgentGraphState
from app.llm.runtime import get_chat_chain


async def llm_node(state: AgentGraphState) -> AgentGraphState:
    chain = get_chat_chain()
    result = await chain.ainvoke({"message": state["message"]})
    if isinstance(result, AIMessage):
        reply = result.content if isinstance(result.content, str) else str(result.content)
    else:
        reply = str(result)
    return {**state, "reply": reply}
