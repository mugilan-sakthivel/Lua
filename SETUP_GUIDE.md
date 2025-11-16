# Luna Website Builder - Setup & Configuration Guide

## Quick Start

### Prerequisites

- Python 3.10+
- Supabase account (free tier available)
- Google API key for Gemini

### Step 1: Clone & Install

```bash
# Navigate to project
cd /Users/mugilansakthivel/Developer/luna/luna\ design/luna\ py/lunapy_v2

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# You need:
# - GOOGLE_API_KEY: from Google AI Studio
# - DATABASE_URL: from Supabase
```

### Step 3: Setup Supabase

1. Go to https://supabase.com and create a project
2. In SQL Editor, enable pgvector:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Copy connection string from "Connection pooler" (at postgres://...)
4. Add to `.env`:
   ```
   DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
   ```

### Step 4: Get Google API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

### Step 5: Test Connection

```python
# test_setup.py
import os
from dotenv import load_dotenv
from src.tools.component_database import get_vector_store

load_dotenv()

try:
    vector_store = get_vector_store()
    print("✅ Database connected successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run:

```bash
python test_setup.py
```

## Architecture Overview

### Multi-Agent Orchestration

```
Website Builder Agent (Main Orchestrator)
├── Phase 1: Planner Agent
│   └── Output: website_plan.md
├── Phase 2: Component Search Agent (RAG)
│   └── Input: website_plan.md
│   └── Output: component_references.md
├── Phase 3: Design Architect Agent
│   └── Input: component_references.md
│   └── Output: design_specs.md
├── Phase 4: Code Generator Agent
│   └── Input: design_specs.md
│   └── Output: React components
├── Phase 5: Critic Agent
│   └── Input: Generated code
│   └── Output: code_review.md
└── Phase 6: Validator Agent
    └── Input: Generated code
    └── Output: validation_report.md
```

### File-Based Memory System

Each agent reads from specific files and writes to specific files:

| Agent            | Reads                   | Writes                  |
| ---------------- | ----------------------- | ----------------------- |
| Planner          | User input              | website_plan.md         |
| Component Search | website_plan.md         | component_references.md |
| Design Architect | component_references.md | design_specs.md         |
| Code Generator   | design_specs.md         | src/components/\*.jsx   |
| Critic           | src/components/\*.jsx   | code_review.md          |
| Validator        | src/components/\*.jsx   | validation_report.md    |

### Vector Embeddings & RAG

```
Component Description
    ↓
Gemini Embeddings (768-dim vectors)
    ↓
Supabase pgvector Storage
    ↓
Similarity Search (Cosine Distance)
    ↓
Top-K Components Retrieved
    ↓
Component Code + Styling Metadata
```

## Component Database Schema

### Supabase Table: `components`

```sql
CREATE TABLE IF NOT EXISTS components (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  specification TEXT NOT NULL,
  description TEXT,
  code TEXT,
  primary_color VARCHAR(7),
  secondary_color VARCHAR(7),
  font TEXT,
  tailwind_classes TEXT,
  features TEXT[],
  embedding vector(768),  -- Gemini embeddings
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB,

  -- Index for fast similarity search
  CONSTRAINT fk_embedding_dimension CHECK (dimension(embedding) = 768)
);

CREATE INDEX idx_embedding ON components USING ivfflat (embedding vector_cosine_ops);
```

**Note**: LangChain's PGVectorStore creates this automatically on first use.

## Gemini Embedding Model

### Model Details

- **Model**: `models/gemini-embedding-001`
- **Dimensions**: 768
- **Input**: Text (component descriptions)
- **Output**: Dense vector embeddings
- **Use Case**: Semantic similarity search

### Embedding Quality

The Gemini embedding model:

- ✅ Understands component semantics
- ✅ Handles variations in language
- ✅ Works with component specs and descriptions
- ✅ Produces consistent vectors for similar components

### Example

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Embed a component description
query = "primary action button with hover effect and loading state"
vector = embeddings.embed_query(query)

# vector is a 768-dimensional list
print(len(vector))  # Output: 768
print(vector[:5])   # Output: [-0.0456, 0.0234, ...]
```

## RAG Search Workflow

### How Component Search Works

1. **Planner creates website_plan.md** with required components
2. **Component Search Agent reads the plan**
3. **For each component**, the agent:
   - Embeds the component specification using Gemini
   - Searches Supabase for similar vectors
   - Retrieves top-k matching components
   - Returns code, colors, fonts, and styling

### Search Process

```python
from src.tools.component_search_tool import search_components_rag

# Agent calls this for each component in the plan
results = search_components_rag(
    component_type="button",
    component_specification="Primary action button for main CTAs with hover effect",
    features_list=["hover effect", "active state", "disabled state"],
    top_k=3  # Get 3 best matches
)

# Results include:
# - Component code (React)
# - Primary/secondary colors
# - Font family and sizing
# - Tailwind CSS classes
# - Similarity scores
```

## Adding Custom Components

### Add a New Component to Database

```python
from src.tools.component_database import add_component_to_db

new_component = {
    "id": "toast_notification",
    "type": "notification",
    "name": "Toast Notification",
    "specification": "Floating notification component that appears at screen edge",
    "features": ["auto-dismiss", "different types (success, error, warning)", "actionable"],
    "code": """
import React, { useEffect } from 'react';

export default function Toast({ message, type = 'info', onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500',
  };

  return (
    <div className={`${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg`}>
      {message}
    </div>
  );
}
    """,
    "primary_color": "#10b981",
    "secondary_color": "#ffffff",
    "font": "Inter, sans-serif",
    "tailwind_classes": "px-6 py-3 rounded-lg shadow-lg bg-green-500 text-white",
    "description": "Toast notification component with auto-dismiss"
}

# Add to database
success = add_component_to_db(new_component)
if success:
    print("✅ Component added to database")
```

### Bulk Add Components

```python
from src.tools.component_database import add_component_to_db

components = [component1, component2, component3, ...]

for component in components:
    add_component_to_db(component)
    print(f"Added: {component['name']}")
```

## Supabase Configuration Details

### Enable Vector Support

1. Go to Supabase Dashboard → SQL Editor
2. Run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

### Connection String Format

```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Example**:

```
postgresql://postgres:mypassword123@abcdefg.supabase.co:5432/postgres
```

**Where to find**:

- User: Always `postgres` (unless custom)
- Password: Set during project creation
- Host: From "Connection string" in Supabase dashboard
- Port: 5432 (default PostgreSQL)
- Database: `postgres` (default)

### Use Connection Pooler (Recommended)

1. In Supabase: Database → Connection Pooling
2. Copy "Connection pooler" string (not direct connection)
3. Add to `.env`:
   ```
   DATABASE_URL=postgresql://[user]:[password]@[pooler-host]:[port]/[database]
   ```

This provides better performance and handles concurrent connections.

## Troubleshooting

### Issue: "DATABASE_URL not found"

```
ValueError: DATABASE_URL environment variable not set
```

**Fix**:

```bash
# Verify .env file exists
ls -la .env

# Check it has DATABASE_URL
grep DATABASE_URL .env

# Reload environment
export $(cat .env | xargs)
python your_script.py
```

### Issue: "pgvector extension not available"

```
ProgrammingError: pgvector extension is not available
```

**Fix**:

1. Go to Supabase SQL Editor
2. Run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Verify:
   ```sql
   SELECT extname FROM pg_extension WHERE extname = 'vector';
   ```

### Issue: "Connection refused"

```
psycopg2.OperationalError: could not translate host name to address
```

**Fix**:

1. Verify Supabase project is running
2. Check connection string is correct
3. Ensure IP is whitelisted (usually auto in Supabase)
4. Try from different network to isolate ISP issues

### Issue: "Invalid API key"

```
ValueError: Invalid API key provided
```

**Fix**:

1. Get new key from https://makersuite.google.com/app/apikey
2. Ensure key has "Google AI for Developers" API enabled
3. No spaces in API key

### Issue: "Connection timeout"

```
TimeoutError: Connection attempt timed out
```

**Fix**:

1. Check internet connection
2. Increase timeout in connection string
3. Use connection pooler instead of direct connection
4. Check Supabase status page

## Performance Tuning

### Vector Search Optimization

```python
# Create index for faster similarity search
import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create IVFFLAT index for faster search
cursor.execute("""
CREATE INDEX idx_embedding_ivfflat ON components USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
""")

conn.commit()
cursor.close()
conn.close()
```

### Query Optimization

```python
# Use smaller top_k for faster results
results = search_components_rag(
    component_type="button",
    component_specification="...",
    top_k=3  # Smaller = faster
)

# For broader searches:
# top_k=5  # Medium
# top_k=10 # Comprehensive but slower
```

### Connection Pooling

Use Supabase connection pooler instead of direct connection:

- **Direct**: postgresql://host:5432/db (slow for many connections)
- **Pooler**: postgresql://host:6543/db (fast, handles connections)

## Monitoring & Logging

### Enable Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("luna")

# Component search logging
logger.info(f"Searching for components: {component_type}")
logger.info(f"Found {results_count} components")
```

### Monitor Database

```sql
-- View embedding statistics
SELECT
  COUNT(*) as total_components,
  COUNT(embedding) as embedded,
  COUNT(DISTINCT type) as component_types
FROM components;

-- View search performance
SELECT
  schemaname, tablename, indexname
FROM pg_indexes
WHERE tablename = 'components';
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure environment
3. ✅ Setup Supabase
4. ✅ Get Gemini API key
5. ✅ Test connection
6. ✅ Run component search agent
7. ➡️ Add custom components to database
8. ➡️ Run full website building workflow

## Getting Help

### Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Google Generative AI Docs](https://ai.google.dev/)

### Common Commands

```bash
# Verify Python installation
python --version

# Check installed packages
pip list | grep -E "langchain|supabase|pgvector"

# Test imports
python -c "from src.tools.component_database import get_vector_store; print('OK')"

# Run tests
pytest tests/

# View logs
tail -f luna.log
```

## Summary

Luna Website Builder is now configured with:

- ✅ Gemini embeddings for semantic search
- ✅ Supabase PostgreSQL for vector storage
- ✅ RAG-based component discovery
- ✅ Multi-agent orchestration
- ✅ File-based memory system

Ready to build amazing websites! 🚀
