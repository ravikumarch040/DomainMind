"""QLoRA configuration dataclass — LLD §3.1."""

from dataclasses import dataclass, field, asdict
import json


@dataclass
class QLoRAConfig:
    model_name: str = "mistralai/Mistral-7B-Instruct-v0.3"

    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_compute_dtype: str = "bfloat16"
    bnb_4bit_use_double_quant: bool = True

    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: list = field(
        default_factory=lambda: [
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ]
    )

    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    lr_scheduler_type: str = "cosine"
    warmup_ratio: float = 0.03
    weight_decay: float = 0.001
    max_seq_length: int = 2048
    max_grad_norm: float = 0.3

    gradient_checkpointing: bool = True
    optim: str = "paged_adamw_8bit"
    packing: bool = True
    fp16: bool = False
    bf16: bool = True

    output_dir: str = "./outputs"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 100
    eval_steps: int = 100
    load_best_model_at_end: bool = True
    report_to: str = "wandb"

    response_template: str = "[/INST]"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_dict(cls, d: dict) -> "QLoRAConfig":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
