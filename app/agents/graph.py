from langgraph.graph import END, START, StateGraph

from app.agents.nodes import llm_node
from app.agents.state import AgentGraphState


def build_agent_graph():
    graph = StateGraph(AgentGraphState)
    graph.add_node("llm", llm_node)
    graph.add_edge(START, "llm")
    graph.add_edge("llm", END)
    return graph.compile()
