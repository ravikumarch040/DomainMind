"""Verify merge parity — LLD §5.2."""

from transformers import pipeline
import torch


def verify_merge(
    adapter_path: str,
    merged_path: str,
    test_prompts: list[str],
) -> bool:
    gen_kwargs = {"max_new_tokens": 50, "do_sample": False}

    pipe_adapter = pipeline(
        "text-generation",
        model=adapter_path,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    pipe_merged = pipeline(
        "text-generation",
        model=merged_path,
        device_map="auto",
        torch_dtype=torch.float16,
    )

    all_match = True
    for prompt in test_prompts:
        out_adapter = pipe_adapter(prompt, **gen_kwargs)[0]["generated_text"]
        out_merged = pipe_merged(prompt, **gen_kwargs)[0]["generated_text"]
        if out_adapter != out_merged:
            print(f"MISMATCH on prompt: {prompt[:60]}...")
            all_match = False

    if all_match:
        print("Merge verification passed — all outputs match.")
    return all_match
