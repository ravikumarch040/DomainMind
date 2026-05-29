"""W&B hyperparameter sweep — LLD §4.2."""

import wandb

from domainmind.training.config import QLoRAConfig
from domainmind.training.train import run_training


sweep_config = {
    "method": "grid",
    "metric": {"name": "eval/loss", "goal": "minimize"},
    "parameters": {
        "lora_r": {"values": [8, 16, 32]},
        "lora_alpha": {"values": [16, 32, 64]},
        "learning_rate": {"values": [1e-4, 2e-4]},
    },
}


def train_run(config=None, train_ds=None, eval_ds=None):
    with wandb.init(config=config):
        cfg = QLoRAConfig(
            lora_r=wandb.config.lora_r,
            lora_alpha=wandb.config.lora_alpha,
            learning_rate=wandb.config.learning_rate,
        )
        return run_training(cfg, train_ds, eval_ds)


def launch_sweep(train_ds, eval_ds, project: str = "domainmind-qlora", count: int = 6):
    sweep_id = wandb.sweep(sweep_config, project=project)

    def _fn(config=None):
        train_run(config, train_ds, eval_ds)

    wandb.agent(sweep_id, function=_fn, count=count)
    return sweep_id
