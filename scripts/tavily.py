from langchain_tavily import TavilySearch

from log import logging


logger = logging.getLogger(__name__)


class TavilySearchLogged(TavilySearch):
    """
    Custom Tavily which include logging on `TavilySearch`.
    """
    def __init__(self, *args, **kwargs) -> None:
        logger.info("Travily Search")
        super().__init__(*args, **kwargs)
        

tavily_tool = TavilySearchLogged(max_results=2)