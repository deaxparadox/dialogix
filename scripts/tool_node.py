import json

from langchain_core.messages import ToolMessage

from log import logging


logger = logging.getLogger(__name__)

class BasicToolNode:
    """A node that run the tools request in the last AI messsage."""
    
    def __init__(self, tools: list) -> None:
        self.tool_by_name = {tool.name: tool for tool in tools}
        
    def __call__(self, inputs: dict):
        logger.info("Auto tool calling function called")
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in the input.")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tool_by_name[tool_call['name']].invoke(
                tool_call['args']
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call['name'],
                    tool_call_id=tool_call['id']
                )
            )
        return {"messages": outputs}