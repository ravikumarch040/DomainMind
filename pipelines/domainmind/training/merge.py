"""Merge LoRA adapters — LLD §5.1."""

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def merge_and_save(
    base_model_id: str,
    adapter_path: str,
    output_path: str,
) -> str:
    print("Loading base model in float16 for merging...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="cpu",
        trust_remote_code=True,
    )

    if hasattr(base_model, "is_loaded_in_4bit") and base_model.is_loaded_in_4bit:
        raise RuntimeError(
            "Cannot merge from 4-bit quantized base — load fp16 base only (LLD Mistake #4)"
        )

    print("Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, adapter_path)

    print("Merging adapter weights into base model...")
    model = model.merge_and_unload()

    print("Saving merged model...")
    model.save_pretrained(output_path, safe_serialization=True)

    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    tokenizer.save_pretrained(output_path)

    print(f"Merged model saved to: {output_path}")
    return output_path
