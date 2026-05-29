"""Instruction-tuning dataset format — LLD §2.3."""

from transformers import AutoTokenizer


def format_training_example(
    tokenizer: AutoTokenizer,
    system: str,
    instruction: str,
    response: str,
) -> str:
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": instruction},
        {"role": "assistant", "content": response},
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False,
    )


def to_jsonl_record(text: str) -> dict:
    return {"text": text}
