-- Enable pgvector extension (only once per database)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create your table
CREATE TABLE website_sections (
    id BIGSERIAL PRIMARY KEY,
    section_type TEXT,
    website_name TEXT,
    website_url TEXT,
    theme TEXT,
    code TEXT,
    description TEXT,
    font_url TEXT,
    document TEXT,
    document_vectors VECTOR(3072)   -- adjust dimension if needed
);
