"""SageMaker training job launcher."""

import os
from pathlib import Path

from domainmind.settings import settings


def launch_training_job(
    *,
    train_data_s3: str,
    val_data_s3: str,
    output_s3: str,
    hyperparameters: dict | None = None,
    instance_type: str | None = None,
    max_runtime_seconds: int = 86400,
):
    """Launch SageMaker training job (requires AWS credentials + role)."""
    import sagemaker
    from sagemaker.huggingface import HuggingFace

    instance_type = instance_type or settings.training_instance_type
    role = settings.sagemaker_role_arn or os.environ.get("SAGEMAKER_ROLE_ARN")
    if not role:
        raise ValueError("Set SAGEMAKER_ROLE_ARN or settings.sagemaker_role_arn")

    hyperparameters = hyperparameters or {
        "model_name": settings.base_model_name,
        "lora_r": "16",
        "lora_alpha": "32",
        "learning_rate": "2e-4",
        "num_train_epochs": "3",
    }

    huggingface_estimator = HuggingFace(
        entry_point="sagemaker_train.py",
        source_dir=str(Path(__file__).parent.parent.parent),
        instance_type=instance_type,
        instance_count=1,
        role=role,
        transformers_version="4.40",
        pytorch_version="2.2",
        py_version="py311",
        hyperparameters=hyperparameters,
        max_run=max_runtime_seconds,
        output_path=output_s3,
        environment={
            "WANDB_PROJECT": settings.wandb_project,
        },
    )

    huggingface_estimator.fit(
        {
            "train": train_data_s3,
            "validation": val_data_s3,
        }
    )
    return huggingface_estimator
