from pydantic_settings import BaseSettings, SettingsConfigDict


class EvalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://domainmind:domainmind@localhost:5432/domainmind"
    gateway_url: str = "http://localhost:8080"
    retrieval_url: str = "http://localhost:8001"
    judge_model: str = "gpt-4o-2024-08-06"
    openai_api_key: str = ""
    faithfulness_threshold: float = 0.75
    golden_set_path: str = "evals/golden_set.jsonl"


settings = EvalSettings()
