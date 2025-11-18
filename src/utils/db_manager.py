"""Database utilities for website_sections using Prisma ORM."""

import json
import asyncio
from typing import Dict, Optional
from dotenv import load_dotenv
from prisma import Prisma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


async def create_website_section(
    section_type: str,
    website_name: str,
    website_url: str,
    theme: str,
    code: str,
    description: str,
    font_url: Optional[str] = None,
) -> Dict:
    """Create a new website section with vector embeddings using Prisma.
    
    Args:
        section_type: Type of section (e.g., 'header', 'hero', 'footer')
        website_name: Name of the website
        website_url: URL of the website
        theme: Theme/style of the section
        code: HTML/CSS/JS code for the section
        description: Description of the section
        font_url: Optional font URL
    
    Returns:
        Dict: Created record with success status
    """
    try:
        # Create document string dynamically
        document = f"""Section Type: {section_type}
Theme: {theme}
Description: {description}"""
        
        # Generate embeddings from the document
        vector = embeddings.embed_query(document)
        
        # Connect to database via Prisma
        prisma = Prisma()
        await prisma.connect()
        
        try:
            # Use raw SQL to insert since Prisma has issues with pgvector
            query = """
            INSERT INTO website_sections (section_type, website_name, website_url, theme, code, description, font_url, document, document_vectors)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id, section_type, website_name, website_url, theme, description
            """
            
            result = await prisma.query_raw(
                query,
                section_type, website_name, website_url, theme, code, description, font_url, document, vector
            )
            
            section = result[0] if result else None
            
            return {
                "success": True,
                "message": "Website section created successfully",
                "data": {
                    "id": section['id'],
                    "section_type": section['section_type'],
                    "website_name": section['website_name'],
                    "website_url": section['website_url'],
                    "theme": section['theme'],
                    "description": section['description'],
                    "document": document,
                    "vector_dimensions": len(vector)
                }
            }
            
        finally:
            await prisma.disconnect()
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to create website section: {str(e)}",
            "data": None
        }


def store_section_sync(
    section_type: str,
    website_name: str, 
    website_url: str,
    theme: str,
    code: str,
    description: str,
    font_url: Optional[str] = None,
) -> Dict:
    """Synchronous wrapper for create_website_section."""
    return asyncio.run(
        create_website_section(
            section_type, website_name, website_url, theme,
            code, description, font_url
        )
    )


async def search_website_sections(
    section_type: str,
    description: str,
    top_k: int = 3
) -> Dict:
    """Search for website sections using cosine similarity with vector embeddings.
    
    Args:
        section_type: Type of section to search for
        description: Description to search against
        top_k: Number of top results to return
        
    Returns:
        Dictionary with search results
    """
    try:
        # Create search query document (focus on description since we filter by section_type)
        search_document = description
        
        # Generate embeddings for search query
        search_vector = embeddings.embed_query(search_document)
        
        # Connect to database via Prisma
        prisma = Prisma()
        await prisma.connect()
        
        try:
            # Use raw SQL for cosine similarity search with pgvector
            # Convert search vector to proper format for pgvector
            vector_str = f"[{','.join(map(str, search_vector))}]"
            
            query = """
            SELECT 
                id, section_type, website_name, website_url, theme, 
                code, description, font_url, document,
                (document_vectors <=> $1::vector) as similarity_distance
            FROM website_sections 
            WHERE section_type = $2
            ORDER BY document_vectors <=> $1::vector
            LIMIT $3
            """
            
            # Execute similarity search - filter by exact section_type match
            results = await prisma.query_raw(
                query,
                vector_str,
                section_type,  # Exact match instead of ILIKE
                top_k
            )
            
            # Format results
            formatted_results = []
            for row in results:
                formatted_results.append({
                    "id": row['id'],
                    "section_type": row['section_type'],
                    "website_name": row['website_name'],
                    "website_url": row['website_url'],
                    "theme": row['theme'],
                    "code": row['code'],
                    "description": row['description'],
                    "font_url": row['font_url'],
                    "document": row['document'],
                    "similarity_score": 1 - row['similarity_distance']  # Convert distance to similarity
                })
            
            return {
                "status": "success",
                "section_type": section_type,
                "search_description": description,
                "results_count": len(formatted_results),
                "top_k": top_k,
                "results": formatted_results
            }
            
        finally:
            await prisma.disconnect()
            
    except Exception as e:
        return {
            "status": "error",
            "section_type": section_type,
            "message": str(e),
            "results": []
        }


def search_sections_sync(
    section_type: str,
    description: str,
    top_k: int = 3
) -> Dict:
    """Synchronous wrapper for search_website_sections."""
    return asyncio.run(
        search_website_sections(section_type, description, top_k)
    )