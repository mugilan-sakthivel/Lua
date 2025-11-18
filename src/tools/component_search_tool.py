"""Component search tool with RAG-based retrieval from website sections."""

from typing import List, Dict
from src.utils.db_manager import search_sections_sync


def search_components_rag(
    component_type: str,
    component_specification: str,
    features_list: List[str] = None,
    top_k: int = 3
) -> Dict:
    """Search for React components using RAG with vector embeddings.
    
    Uses Gemini embeddings and Supabase PostgreSQL vector store for semantic search.
    
    Args:
        component_type: Type of component (e.g., 'button', 'card', 'pricing')
        component_specification: Detailed specification of what's needed
        features_list: List of specific features the component must have
        top_k: Number of top results to return
        
    Returns:
        Dictionary with search results including code, colors, and fonts
    """
    return search_sections_sync(
        section_type=component_type,
        description=component_specification,
        top_k=top_k
    )


# Tool definition for use in agents
component_search_tool = {
    "name": "component-search",
    "description": "Search for React components using RAG with vector embeddings. Returns component code, colors, fonts, and specifications from Supabase database.",
    "parameters": {
        "type": "object",
        "properties": {
            "section_type": {
                "type": "string",
                "description": "Type of component needed (e.g., 'button', 'card', 'pricing', 'navigation', 'testimonial', 'hero', 'form')"
            },
            "description": {
                "type": "string",
                "description": "Detailed description of what the component should do and look like"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of top results to return (default: 3)",
                "default": 3
            }
        },
        "required": ["section_type", "description"]
    },
    "function": search_components_rag
}
