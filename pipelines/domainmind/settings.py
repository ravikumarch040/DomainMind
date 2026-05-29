"""Shared configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # AWS
    aws_region: str = "us-east-1"
    s3_data_bucket: str = "domainmind-dev-data"
    s3_model_bucket: str = "domainmind-dev-models"

    # Model
    base_model_name: str = "mistralai/Mistral-7B-Instruct-v0.3"
    domain: str = "compliance and legal"
    system_prompt: str = (
        "You are a compliance and legal expert specializing in SOC 2, HIPAA, and HITECH."
    )

    # OpenAI (ZDR-enrolled key via Secrets Manager in prod)
    openai_api_key: str = ""
    openai_model_labeler: str = "gpt-4o"
    openai_model_judge: str = "gpt-4o-2024-08-06"

    # W&B
    wandb_project: str = "domainmind-qlora"
    wandb_entity: str = ""

    # Paths
    data_dir: str = "data"
    output_dir: str = "./outputs"

    # DVC / SageMaker
    dvc_remote: str = "s3://domainmind-dev-data/dvc"
    sagemaker_role_arn: str = ""
    training_instance_type: str = "ml.g5.2xlarge"
    sweep_instance_type: str = "ml.g5.12xlarge"


settings = Settings()
