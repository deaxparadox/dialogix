from langchain_core.tools import tool
from langgraph.types import Command, interrupt

from log import logging


logger = logging.getLogger(__name__)


@tool
def human_assistance(query: str) -> str:
    """Request assistance from human"""
    human_response = interrupt({"query": query})
    logger.info("Human assistance tool called with query: {0}".format(human_assistance))
    return human_response['data']