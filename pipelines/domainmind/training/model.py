"""Build model and tokenizer — LLD §3.2."""

import torch
from peft import prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from domainmind.training.config import QLoRAConfig


def build_model_and_tokenizer(cfg: QLoRAConfig):
    compute_dtype = torch.bfloat16 if cfg.bnb_4bit_compute_dtype == "bfloat16" else torch.float16

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=cfg.load_in_4bit,
        bnb_4bit_quant_type=cfg.bnb_4bit_quant_type,
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=cfg.bnb_4bit_use_double_quant,
    )

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="sdpa",  # flash_attention_2 when available
    )

    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=cfg.gradient_checkpointing,
    )

    model.config.use_cache = False
    model.config.pretraining_tp = 1

    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    return model, tokenizer


def assert_training_ready(model, collator) -> None:
    """Pre-train assertions for Critical Mistakes to Avoid."""
    assert model.config.use_cache is False, "KV cache must be disabled during training"
    from trl import DataCollatorForCompletionOnlyLM

    assert isinstance(
        collator, DataCollatorForCompletionOnlyLM
    ), "Must use DataCollatorForCompletionOnlyLM"
