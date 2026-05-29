"""Reusable inference wrapper for baseline and eval."""

from dataclasses import dataclass

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from domainmind.training.config import QLoRAConfig


@dataclass
class GenerationResult:
    prompt: str
    text: str


class InferenceWrapper:
    """Consistent inference across baseline, eval, and verification."""

    def __init__(
        self,
        model_name_or_path: str,
        *,
        adapter_path: str | None = None,
        torch_dtype=torch.float16,
        device_map: str = "auto",
    ):
        self.model_name = model_name_or_path
        self.adapter_path = adapter_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        if adapter_path:
            from peft import PeftModel

            base = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                torch_dtype=torch_dtype,
                device_map=device_map,
                trust_remote_code=True,
            )
            model = PeftModel.from_pretrained(base, adapter_path)
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                torch_dtype=torch_dtype,
                device_map=device_map,
                trust_remote_code=True,
            )

        model.config.use_cache = True
        self._pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=self.tokenizer,
            device_map=device_map,
            torch_dtype=torch_dtype,
        )

    def generate(
        self,
        prompt: str,
        *,
        max_new_tokens: int = 256,
        do_sample: bool = False,
        temperature: float = 0.7,
    ) -> GenerationResult:
        kwargs = {"max_new_tokens": max_new_tokens, "do_sample": do_sample}
        if do_sample:
            kwargs["temperature"] = temperature
        out = self._pipe(prompt, **kwargs)[0]["generated_text"]
        return GenerationResult(prompt=prompt, text=out)

    def format_chat(self, system: str, user: str) -> str:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        return self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
