from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode

from tavily import tavily_tool
from tool_node import BasicToolNode
from hil import human_assistance


llm = init_chat_model("openai:gpt-4.1")
"""LLM instance"""

tools = [tavily_tool, human_assistance]
"""Tools lists"""

# tool_node = BasicToolNode(tools=tools)
"""Tool node for automatic calling of tools"""

tool_node = ToolNode(tools=tools)

llm_with_tools = llm.bind_tools(tools)
"""LLM with tools binded"""