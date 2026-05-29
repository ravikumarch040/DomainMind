from pydantic_settings import BaseSettings, SettingsConfigDict


class RetrievalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    qdrant_url: str = "http://localhost:6333"
    tei_embed_url: str = "http://localhost:8081"
    tei_rerank_url: str = "http://localhost:8082"
    embed_model: str = "BAAI/bge-large-en-v1.5"
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    database_url: str = "postgresql://domainmind:domainmind@localhost:5432/domainmind"
    redis_url: str = "redis://localhost:6379/0"


settings = RetrievalSettings()
