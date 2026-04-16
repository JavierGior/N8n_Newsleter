-- Habilitar extensión de vectores (para deduplicación semántica futura)
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal de noticias
CREATE TABLE IF NOT EXISTS news_archive (
    id SERIAL PRIMARY KEY,
    url_hash VARCHAR(64) UNIQUE NOT NULL, -- MD5 de la URL para deduplicación rápida
    content_hash VARCHAR(64),             -- MD5 del texto limpio (Trafilatura) para evitar re-publicaciones
    title TEXT,
    url TEXT,
    published_date DATE,
    source VARCHAR(100),
    analysis_json JSONB,                  -- Guardamos el análisis completo de AI
    embedding vector(1536),               -- Para búsqueda semántica
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para velocidad
CREATE INDEX idx_url_hash ON news_archive(url_hash);
CREATE INDEX idx_content_hash ON news_archive(content_hash);
CREATE INDEX idx_date ON news_archive(published_date);