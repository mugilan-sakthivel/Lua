# Phase 3: Component Search Agent Implementation

## Overview

Phase 3 implements the **Component Discovery & Search Agent** using RAG (Retrieval Augmented Generation) with Gemini embeddings and Supabase PostgreSQL vector store. This agent searches for relevant React components that match the website plan created in Phase 2.

## Architecture

### System Flow

```
Planner Agent Output (website_plan.md)
            ↓
Component Search Agent
    ├── Reads website_plan.md
    ├── Extracts component inventory
    ├── Uses component-search tool (RAG)
    ├── Queries Supabase vector store
    └── Writes component_references.md
            ↓
Design Architect Agent (Phase 4)
    └── Reads component_references.md
```

### Technology Stack

| Component         | Technology          | Details                                             |
| ----------------- | ------------------- | --------------------------------------------------- |
| **LLM**           | Google Gemini       | `gemini-2.5-flash` for orchestration                |
| **Embeddings**    | Gemini Embeddings   | `models/gemini-embedding-001` for vector embeddings |
| **Vector Store**  | Supabase PostgreSQL | PGVector extension for similarity search            |
| **RAG Framework** | LangChain           | For retrieval and generation                        |
| **Database**      | PostgreSQL          | With pgvector extension                             |

## Implementation Details

### 1. Gemini Embeddings Configuration

**File**: `src/tools/component_database.py`

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
```

**Key Points**:

- Uses the latest Gemini embedding model
- 768-dimensional embeddings
- Semantic understanding of component descriptions
- Supports vector similarity search

### 2. Supabase/PostgreSQL Vector Store

**File**: `src/tools/component_database.py`

```python
from langchain_postgres import PGVectorStore

def get_vector_store():
    """Initialize connection to Supabase PostgreSQL vector store."""
    connection_string = os.environ.get("DATABASE_URL")

    vector_store = PGVectorStore.from_connection_string(
        connection_string=connection_string,
        embedding_function=embeddings,
        table_name="components",
        pre_delete_collection=False,
    )
    return vector_store
```

**Database Requirements**:

- PostgreSQL 12+ with pgvector extension
- Supabase project with vector support enabled
- Table: `components` with vector column

### 3. Component Search Tool

**File**: `src/tools/component_search_tool.py`

The tool searches for components using semantic similarity:

```python
def search_components_rag(
    component_type: str,
    component_specification: str,
    features_list: List[str] = None,
    top_k: int = 3
) -> Dict:
    """Search components using RAG with Gemini embeddings."""
    # Queries: "{component_type}: {component_specification}"
    # Returns: Top k matching components with code and styling
```

**Tool Parameters**:

- `component_type`: Type of component (button, card, pricing, etc.)
- `component_specification`: Detailed requirements
- `features_list`: Specific features needed
- `top_k`: Number of results to return (default: 3)

**Returns**:

- Component code (copy-paste ready)
- Primary and secondary colors
- Font/typography information
- Tailwind CSS classes
- Similarity scores

### 4. Component Search Agent

**File**: `src/subagents/component_search_agent.py`

Dictionary-style sub-agent definition:

```python
component_search_agent = {
    "name": "component-search-agent",
    "description": "Search for React components using RAG...",
    "system_prompt": sub_component_search_prompt,
    "tools": [component_search_tool],
}
```

**Workflow**:

1. Reads `website_plan.md` from planner agent
2. Extracts component inventory
3. For each component, uses component-search tool
4. Collects results with React code and styling
5. Writes findings to `component_references.md`

### 5. File-Based Memory System

**Input File**: `website_plan.md`

- Created by planner agent
- Contains component inventory with specifications

**Output File**: `component_references.md`

- Component code snippets
- Design system (colors, fonts)
- Styling information
- Integration notes

**Example Output Structure**:

```markdown
# Component Reference Guide

## Design System

### Colors

- Primary Color: #1e3a8a (blue-900)
- Secondary Color: #0ea5e9 (sky-500)

### Typography

- Font Family: Inter, sans-serif
- Font Sizes: h1(36px), h2(28px), h3(24px), p(16px)

## Components Found

### 1. Primary Button

- Type: button
- Purpose: Main action button
- React Code: [...]
- Styling: [...]

...more components...
```

## Environment Configuration

**File**: `.env` (copy from `.env.example`)

```bash
# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Supabase PostgreSQL Connection String
# Format: postgresql://[user]:[password]@[host]:[port]/[database]
DATABASE_URL=postgresql://postgres:password@host.supabase.co:5432/postgres

# Optional: LangSmith Tracing
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=your_langsmith_key_here
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key packages**:

- `langchain-google-genai`: Gemini integration
- `langchain-postgres`: PostgreSQL/pgvector support
- `langchain-text-splitters`: Text chunking
- `pgvector`: Vector operations
- `psycopg2-binary`: PostgreSQL driver

### 2. Configure Supabase

1. Create a Supabase project: https://supabase.com
2. Enable pgvector extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Create components table (auto-created by LangChain if using PGVectorStore)
4. Get connection string from Supabase dashboard
5. Set `DATABASE_URL` in `.env`

### 3. Set Gemini API Key

1. Get API key from Google AI Studio: https://makersuite.google.com/app/apikey
2. Set `GOOGLE_API_KEY` in `.env`

### 4. Initialize Component Database (Optional)

```python
from src.tools.component_database import initialize_component_database

# Populate with mock components (first time only)
initialize_component_database()
```

## Workflow Integration

### How It Fits in the Full Pipeline

```
1. User Input
    ↓
2. Website Builder Agent (Orchestrator)
    ├── Planner Agent → website_plan.md
    ├── Component Search Agent → component_references.md
    ├── Design Architect Agent → design_specs.md
    ├── Code Generator Agent → React code
    ├── Critic Agent → code_review.md
    └── Validator Agent → validation_report.md
    ↓
3. Final Website Output
```

### Phase 3 in Context

- **Input**: Website plan with component inventory
- **Process**: RAG-based semantic search for matching components
- **Output**: Curated component references with code and styling
- **Next Phase**: Design architect refines the components and styling

## Mock Components

The system comes with mock components for testing:

1. **Primary Button**

   - Type: button
   - Features: hover, active, disabled states
   - Styling: Blue theme with Tailwind

2. **Feature Card**

   - Type: card
   - Features: icon support, title, description
   - Styling: White with shadow effects

3. **Pricing Card**
   - Type: pricing
   - Features: plan name, price, features list, CTA
   - Styling: Highlighted option support

These can be extended with real components from your Supabase database.

## RAG Search Process

### How Vector Embeddings Work

1. **Component Description Embedding**:

   - Gemini embedding model converts text to 768-dim vector
   - "Primary action button with hover effect" → [0.123, -0.456, ...]

2. **Query Embedding**:

   - User search query converted to same vector space
   - "button: primary action button" → [0.125, -0.450, ...]

3. **Similarity Search**:

   - Supabase calculates cosine similarity
   - Returns components with highest similarity scores

4. **Metadata Retrieval**:
   - Returns full component code, colors, fonts
   - Ready for integration

### Advantages

- ✅ Semantic understanding (not keyword-based)
- ✅ Handles variations in language
- ✅ Finds components by intent, not exact match
- ✅ Fast similarity search with pgvector
- ✅ Scalable to thousands of components

## Testing & Validation

### Manual Testing

```python
from src.tools.component_search_tool import search_components_rag

# Test component search
results = search_components_rag(
    component_type="button",
    component_specification="Primary action button with hover effects",
    top_k=3
)

print(f"Found {results['results_count']} components")
for component in results['results']:
    print(f"- {component['name']}: {component['description']}")
```

### Expected Output

```
Found 3 components
- Primary Button: A primary action button suitable for main CTAs
- Secondary Button: A secondary action button for less prominent actions
- Icon Button: A compact button with icon only
```

## Common Issues & Solutions

### Issue 1: "DATABASE_URL not set"

```
Error: DATABASE_URL environment variable not set
```

**Solution**: Ensure `.env` file has valid `DATABASE_URL`

### Issue 2: "pgvector extension not found"

```
Error: pgvector extension not available
```

**Solution**: Run `CREATE EXTENSION IF NOT EXISTS vector;` in Supabase SQL editor

### Issue 3: "Connection refused"

```
Error: Connection to database failed
```

**Solution**: Check Supabase is running and connection string is correct

### Issue 4: "API key not set"

```
Error: GOOGLE_API_KEY environment variable not set
```

**Solution**: Get key from https://makersuite.google.com/app/apikey

## Performance Considerations

- **Vector Search**: pgvector is optimized for similarity search
- **Embedding Caching**: Consider caching embeddings for frequently searched components
- **Connection Pooling**: Use connection pooling for database efficiency
- **Top-K Results**: Adjust `top_k` parameter based on accuracy vs latency needs

## Next Steps

After Phase 3 (Component Search):

1. **Phase 4**: Design Architect Agent

   - Reads `component_references.md`
   - Creates design specifications
   - Outputs `design_specs.md`

2. **Phase 5**: Code Generator Agent

   - Reads `design_specs.md`
   - Generates React components
   - Creates project structure

3. **Phase 6**: Critic Agent

   - Reviews generated code
   - Suggests improvements
   - Outputs `code_review.md`

4. **Phase 7**: Validator Agent
   - Validates design fidelity
   - Checks accessibility
   - Outputs `validation_report.md`

## References

### Documentation

- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/rag/)
- [Supabase Vector Guide](https://supabase.com/docs/guides/ai-guides)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Google Generative AI Embeddings](https://ai.google.dev/docs)

### Key Files

- `src/tools/component_database.py` - Database initialization and search
- `src/tools/component_search_tool.py` - RAG search tool
- `src/subagents/component_search_agent.py` - Agent definition
- `src/services/agent_service.py` - Main orchestrator

## Summary

Phase 3 implements a sophisticated RAG-based component discovery system:

✅ Uses Gemini embeddings for semantic understanding
✅ Stores components in Supabase PostgreSQL with pgvector
✅ Provides similarity-based search for component discovery
✅ Integrates seamlessly with file-based memory (website_plan.md → component_references.md)
✅ Prepares data for design refinement in next phase

The system is production-ready and can be extended with additional components in your Supabase database.
