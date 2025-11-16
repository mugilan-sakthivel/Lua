"""Component search tool with RAG-based retrieval from Supabase."""

from typing import List, Dict
from src.tools.component_database import search_components


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
    return search_components(
        component_type=component_type,
        component_specification=component_specification,
        top_k=top_k
    )


# Tool definition for use in agents
component_search_tool = {
    "name": "component-search",
    "description": "Search for React components using RAG with vector embeddings. Returns component code, colors, fonts, and specifications from Supabase database.",
    "parameters": {
        "type": "object",
        "properties": {
            "component_type": {
                "type": "string",
                "description": "Type of component needed (e.g., 'button', 'card', 'pricing', 'navigation', 'testimonial', 'hero', 'form')"
            },
            "component_specification": {
                "type": "string",
                "description": "Detailed specification of what the component should do and look like"
            },
            "features_list": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of specific features the component must have"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of top results to return (default: 3)",
                "default": 3
            }
        },
        "required": ["component_type", "component_specification"]
    },
    "function": search_components_rag
}
