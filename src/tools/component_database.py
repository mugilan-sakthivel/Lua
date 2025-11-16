"""Component database with Supabase vector store for RAG-based retrieval."""

import os
from typing import List, Dict
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVectorStore
from langchain_core.documents import Document

# Initialize Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Initialize Supabase/PostgreSQL vector store
def get_vector_store():
    """Get or create the vector store connection.
    
    Returns:
        PGVectorStore instance connected to Supabase
    """
    connection_string = os.environ.get("DATABASE_URL")
    
    if not connection_string:
        raise ValueError(
            "DATABASE_URL environment variable not set. "
            "Please provide your Supabase connection string."
        )
    
    vector_store = PGVectorStore.from_connection_string(
        connection_string=connection_string,
        embedding_function=embeddings,
        table_name="components",  # Table name in Supabase
        pre_delete_collection=False,  # Don't delete existing data
    )
    
    return vector_store


# Mock component database for initial setup
MOCK_COMPONENTS = [
    {
        "id": "button_primary",
        "type": "button",
        "name": "Primary Button",
        "specification": "A primary action button with emphasis for main CTAs",
        "features": ["hover effect", "active state", "disabled state", "ripple animation"],
        "code": """import React from 'react';

export default function PrimaryButton({ children, onClick, disabled = false }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
    >
      {children}
    </button>
  );
}
""",
        "primary_color": "#1e3a8a",
        "secondary_color": "#0ea5e9",
        "font": "Inter, sans-serif",
        "tailwind_classes": "px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200",
        "description": "A primary action button suitable for main CTAs",
    },
    {
        "id": "card_feature",
        "type": "card",
        "name": "Feature Card",
        "specification": "Card component for displaying features with icon and description",
        "features": ["icon support", "title", "description", "hover effect"],
        "code": """import React from 'react';

export default function FeatureCard({ icon: Icon, title, description }) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border border-gray-100">
      <Icon className="w-12 h-12 text-blue-600 mb-4" />
      <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm leading-relaxed">{description}</p>
    </div>
  );
}
""",
        "primary_color": "#1e3a8a",
        "secondary_color": "#f3f4f6",
        "font": "Inter, sans-serif",
        "tailwind_classes": "p-6 bg-white rounded-lg shadow-md hover:shadow-lg hover:-translate-y-1",
        "description": "Feature showcase card with icon, title, and description",
    },
    {
        "id": "pricing_card",
        "type": "pricing",
        "name": "Pricing Tier Card",
        "specification": "Card for displaying pricing plans with features list and CTA button",
        "features": ["plan name", "price", "features list", "CTA button", "highlight option"],
        "code": """import React from 'react';

export default function PricingCard({ planName, price, features, isHighlighted = false, onSelect }) {
  return (
    <div className={`p-8 rounded-lg transition-all duration-300 ${
      isHighlighted 
        ? 'bg-gradient-to-b from-blue-600 to-blue-700 text-white shadow-2xl scale-105' 
        : 'bg-white border border-gray-200 text-gray-900'
    }`}>
      <h3 className="text-2xl font-bold mb-2">{planName}</h3>
      <div className="text-4xl font-bold mb-6">${price}<span className="text-lg">/mo</span></div>
      <ul className="mb-8 space-y-3">
        {features.map((feature, idx) => (
          <li key={idx} className="flex items-center gap-2">
            <span className="text-2xl">✓</span> {feature}
          </li>
        ))}
      </ul>
      <button onClick={onSelect} className={`w-full py-3 font-semibold rounded-lg transition-all ${
        isHighlighted 
          ? 'bg-white text-blue-600 hover:bg-gray-100' 
          : 'bg-blue-600 text-white hover:bg-blue-700'
      }`}>
        Get Started
      </button>
    </div>
  );
}
""",
        "primary_color": "#1e3a8a",
        "secondary_color": "#ffffff",
        "font": "Inter, sans-serif",
        "tailwind_classes": "p-8 rounded-lg bg-gradient-to-b from-blue-600 to-blue-700",
        "description": "Pricing plan card with features and call-to-action",
    },
]


def initialize_component_database():
    """Initialize the component database with mock components.
    
    Should be run once to populate the database with initial components.
    """
    vector_store = get_vector_store()
    
    # Convert mock components to Document objects for vector store
    documents = []
    for component in MOCK_COMPONENTS:
        doc = Document(
            page_content=component["specification"],
            metadata={
                "id": component["id"],
                "type": component["type"],
                "name": component["name"],
                "features": component["features"],
                "code": component["code"],
                "primary_color": component["primary_color"],
                "secondary_color": component["secondary_color"],
                "font": component["font"],
                "tailwind_classes": component["tailwind_classes"],
                "description": component["description"],
            }
        )
        documents.append(doc)
    
    # Add documents to vector store
    vector_store.add_documents(documents)
    print(f"✅ Initialized database with {len(documents)} components")


def search_components(
    component_type: str,
    component_specification: str,
    top_k: int = 3
) -> Dict:
    """Search for components using vector similarity (RAG).
    
    Args:
        component_type: Type of component (e.g., 'button', 'card', 'pricing')
        component_specification: Description of what's needed
        top_k: Number of top results to return
        
    Returns:
        Dictionary with search results and component details
    """
    vector_store = get_vector_store()
    
    # Search by similarity
    search_query = f"{component_type}: {component_specification}"
    
    try:
        results = vector_store.similarity_search(search_query, k=top_k)
        
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "id": doc.metadata.get("id"),
                "name": doc.metadata.get("name"),
                "type": doc.metadata.get("type"),
                "specification": doc.page_content,
                "features": doc.metadata.get("features", []),
                "code": doc.metadata.get("code"),
                "primary_color": doc.metadata.get("primary_color"),
                "secondary_color": doc.metadata.get("secondary_color"),
                "font": doc.metadata.get("font"),
                "tailwind_classes": doc.metadata.get("tailwind_classes"),
                "description": doc.metadata.get("description"),
            })
        
        return {
            "status": "success",
            "component_type": component_type,
            "specification": component_specification,
            "results_count": len(formatted_results),
            "top_k": top_k,
            "results": formatted_results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "component_type": component_type,
            "message": str(e),
            "results": []
        }


def add_component_to_db(component_dict: Dict) -> bool:
    """Add a new component to the database.
    
    Args:
        component_dict: Component definition dictionary
        
    Returns:
        True if successful, False otherwise
    """
    vector_store = get_vector_store()
    
    doc = Document(
        page_content=component_dict["specification"],
        metadata={
            "id": component_dict["id"],
            "type": component_dict["type"],
            "name": component_dict["name"],
            "features": component_dict.get("features", []),
            "code": component_dict.get("code", ""),
            "primary_color": component_dict.get("primary_color", ""),
            "secondary_color": component_dict.get("secondary_color", ""),
            "font": component_dict.get("font", ""),
            "tailwind_classes": component_dict.get("tailwind_classes", ""),
            "description": component_dict.get("description", ""),
        }
    )
    
    try:
        vector_store.add_documents([doc])
        return True
    except Exception as e:
        print(f"❌ Error adding component: {e}")
        return False
