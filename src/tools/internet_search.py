"""Internet search tool using Tavily API."""

import os
from typing import Literal
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize the Tavily client once and reuse it
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search using Tavily API.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        topic: Search topic type (general, news, finance)
        include_raw_content: Whether to include raw content
        
    Returns:
        Search results from Tavily
    """
    search_docs = tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
    return search_docs
