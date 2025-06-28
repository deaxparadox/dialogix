from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

from config import setting
from log import logging

logger = logging.getLogger(__name__)


llm = init_chat_model(
    "{platform}:{model}".format(
        platform=setting.PLATFORM,
        model=setting.LLM_MODEL
    )
)

logger.info("LLM initialized with model: {0}".format(llm))


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    logger.info("Human assistance tool called with query: {0}".format(query))
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}


def stream_graph_update(graph: CompiledStateGraph, user_input: str, config: dict, /):
    logger.info("Function -> {0}".format(stream_graph_update.__name__))
    
    events = graph.stream(
        {"messages": {"role": "user", "content": user_input}},
        config,
        stream_mode="values"
    )
    
    for event in events:
        event['messages'][-1].pretty_print()


# def generate_human_response(graph: CompiledStateGraph, config, /):
#     human_response = (
#         "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
#         " It's much more reliable and extensible than simple autonomous agents."
#     )
    
#     human_command = Command(resume={"data": human_response})
    
#     events = graph.stream(
#         human_command,
#         config,
#         stream_mode="values"
#     )
    
#     for event in events:
#         event['messages'][-1].pretty_print()
    
    


with PostgresSaver.from_conn_string(setting.DATABASE_URL) as saver:
    saver.setup()

    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    graph = graph_builder.compile(checkpointer=saver)

    config = {'configurable': {'thread_id': '1'}}
    
    
    # user_input = input("#>> ").strip()
    user_input = "My name is Alex."
    stream_graph_update(graph, user_input, config)
    
    user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
    stream_graph_update(graph, user_input, config)
    # generate_human_response(graph, config)
    
    user_input = "What is my name?"
    stream_graph_update(graph, user_input, config)