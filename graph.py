from typing import TypedDict

from langgraph.constants import END
from langgraph.graph import StateGraph

from agents import router_agent, news_agent, scam_agent, general_agent
from guardrails import input_guardrails_node


class AgentState(TypedDict):
    input: str
    route: str
    response: str
    blocked: bool
    reason: str


def input_decision(state):
    if state.get("blocked"):
        return "end"
    return "router"



graph = StateGraph(AgentState)
graph.add_node("input_guard", input_guardrails_node)
graph.add_node("router" , router_agent)
graph.add_node("news_agent" , news_agent)
graph.add_node("scam_detection_agent" , scam_agent)
graph.add_node("general_agent", general_agent)

graph.set_entry_point("input_guard")
graph.add_conditional_edges("input_guard", input_decision,
                            {"router" : "router",
                                      "end" : END})

def router_decision(state):
    if state["route"] == "news":
        return "news"

    elif state["route"] == "scam":
        return "scam"

    else:
        return "general"

graph.add_conditional_edges("router", router_decision,
                            {"news" : "news_agent",
                                       "scam" : "scam_detection_agent",
                                       "general" : "general_agent"})

graph.add_edge("news_agent", END)
graph.add_edge("scam_detection_agent", END)
graph.add_edge("general_agent", END)

compiled_graph = graph.compile()