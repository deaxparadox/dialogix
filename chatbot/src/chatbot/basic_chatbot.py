from typing import Annotated

from typing_extensions import TypedDict

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition

from config import setting
from llm import llm, llm_with_tools, tool_node
from log import logging
from memory import memory_saver


logger = logging.getLogger(__name__)
logging.info("Starting basic chatbot")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def route_tools(state: State):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif message := state.get("messages", []):
        ai_message = message[-1]
    else:
        raise ValueError("No message found in input state to tool_edge: {state}".format(state))
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


graph_builder = StateGraph(State)


def chatbot(state: State):
    logger.info("Function -> {0}".format(chatbot.__name__))
    return {"messages": [llm_with_tools.invoke(state['messages'])]}


graph_builder.add_node("tools", tool_node)
graph_builder.add_node('chatbot', chatbot)
#################################
# Custom conditaitons tools
#################################
# graph_builder.add_conditional_edges(
#     "chatbot",
#     route_tools,
#     {"tools": "tools", END: END}
# )
# Using prebuilt tools confition
# with Prebuilt tool node
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, 'chatbot')
graph = graph_builder.compile(checkpointer=memory_saver)


def stream_graph_update(user_input: str, /):
    logger.info("Function -> {0}".format(stream_graph_update.__name__))
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value['messages'][-1].content)


user_input: str = "What is langgraph?"
print("User:", user_input)
stream_graph_update(user_input)