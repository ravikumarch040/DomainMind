# DomainMind — QLoRA Fine-Tuning Pipeline Design Guide

> **Project:** DomainMind — Domain-Specific LLM Fine-Tuning Platform  
> **Scope:** Data preparation · Training configuration · LoRA rank selection · Model merging  
> **Stack:** Python · HuggingFace Transformers · PEFT · TRL · bitsandbytes · Mistral 7B / Llama 3 8B  
> **Author:** Ravindra Kumar · Principal Engineer

---

## Table of Contents

1. [Overview](#1-overview)
2. [Data Preparation](#2-data-preparation)
   - 2.1 [Corpus Cleaning Pipeline](#21-corpus-cleaning-pipeline)
   - 2.2 [Chunking Strategy](#22-chunking-strategy)
   - 2.3 [Instruction-Tuning Dataset Format](#23-instruction-tuning-dataset-format)
   - 2.4 [Synthetic Data Generation with GPT-4o](#24-synthetic-data-generation-with-gpt-4o)
3. [QLoRA Training Configuration](#3-qlora-training-configuration)
   - 3.1 [Configuration Dataclass](#31-configuration-dataclass)
   - 3.2 [Building the Model and Tokenizer](#32-building-the-model-and-tokenizer)
   - 3.3 [Attaching LoRA Adapters](#33-attaching-lora-adapters)
4. [LoRA Rank Selection](#4-lora-rank-selection)
   - 4.1 [Decision Framework](#41-decision-framework)
   - 4.2 [Hyperparameter Sweep](#42-hyperparameter-sweep)
   - 4.3 [Diagnosing Rank Choice from Training Signals](#43-diagnosing-rank-choice-from-training-signals)
5. [Merging LoRA Adapters with the Base Model](#5-merging-lora-adapters-with-the-base-model)
   - 5.1 [Merge and Save](#51-merge-and-save)
   - 5.2 [Verifying the Merge](#52-verifying-the-merge)
   - 5.3 [GGUF Quantization for Lightweight Deployment](#53-gguf-quantization-for-lightweight-deployment)
6. [Critical Mistakes to Avoid](#6-critical-mistakes-to-avoid)
7. [Architecture Summary](#7-architecture-summary)
8. [Resume Talking Points](#8-resume-talking-points)

---

## 1. Overview

The quality of a fine-tuned model is determined primarily by **data quality**, not training configuration. A perfectly tuned model trained on bad data will underperform a mediocre config trained on excellent data. This guide covers the complete pipeline in the correct order of importance.

```
Raw domain corpus
       │
       ▼
  Cleaning & deduplication
       │
       ▼
  Chunking & tokenization
       │
       ▼
  Instruction dataset formatting
       │
       ▼
  QLoRA training (4-bit base + float16 adapters)
       │
       ▼
  Evaluation (validation loss + RAGAS metrics)
       │
       ▼
  Merge adapters → full float16 model
       │
       ▼
  vLLM serving (OpenAI-compatible endpoint)
```

**Key principle:** LoRA adapters train on top of a frozen, 4-bit quantized base model. Only the adapter weights (~1–2% of total parameters) are updated during training. At inference time, the adapter is either merged into the base model or applied dynamically.

---

## 2. Data Preparation

### 2.1 Corpus Cleaning Pipeline

Before formatting a single training example, raw documents must pass through four cleaning stages: boilerplate removal, unicode normalization, quality gating, and deduplication.

```python
# pipeline/cleaning.py
import re, hashlib, unicodedata
from datasketch import MinHash, MinHashLSH


def clean_document(text: str) -> str | None:
    """
    Cleans a raw document string.
    Returns None if the document fails quality gates.
    """
    # Stage 1: Remove boilerplate
    text = re.sub(r'\n{3,}', '\n\n', text)               # collapse excess newlines
    text = re.sub(r'Page \d+ of \d+', '', text)           # page number markers
    text = re.sub(r'(?i)confidential|internal only', '', text)

    # Stage 2: Unicode normalization — critical for medical/legal corpora
    text = unicodedata.normalize('NFKC', text)

    # Stage 3: Quality gates — discard garbage chunks
    words = text.split()
    if len(words) < 50:
        return None                                        # too short
    if len(set(words)) / len(words) < 0.3:
        return None                                        # repetitive garbage

    return text.strip()


class DeduplicationPipeline:
    """
    MinHash LSH deduplication — finds near-duplicate documents
    efficiently at scale without pairwise comparison.
    """
    def __init__(self, threshold: float = 0.85):
        self.lsh = MinHashLSH(threshold=threshold, num_perm=128)
        self.seen: dict = {}

    def is_duplicate(self, text: str, doc_id: str) -> bool:
        m = MinHash(num_perm=128)
        for word in text.lower().split():
            m.update(word.encode())
        try:
            result = self.lsh.query(m)
            if result:
                return True
            self.lsh.insert(doc_id, m)
            return False
        except ValueError:
            return False
```

> **Why MinHash LSH?** Exact deduplication via hashing misses near-duplicates (same content, slightly different formatting). MinHash with 85% similarity threshold catches reworded duplicates that would otherwise cause the model to memorize specific phrasing patterns.

---

### 2.2 Chunking Strategy

Naive fixed-size chunking destroys semantic coherence. The model ends up learning from truncated sentences and broken context windows. Use recursive chunking that respects document structure, and prefer token-aware chunking using the model's own tokenizer.

```python
# pipeline/chunking.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer


def build_character_chunker(chunk_size: int = 512, overlap: int = 64):
    """
    Separator priority: paragraph > sentence > word > character.
    This preserves meaning at the highest available natural boundary.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
        length_function=len,
    )


def token_aware_chunk(
    text: str,
    tokenizer: AutoTokenizer,
    max_tokens: int = 400,
    overlap_tokens: int = 64,
) -> list[str]:
    """
    Token-aware chunking using the model's own tokenizer.
    Preferred over character chunking — avoids mid-token splits
    and gives accurate length estimates for the training context window.
    """
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i : i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
        i += max_tokens - overlap_tokens                   # slide with overlap
    return chunks
```

**Choosing `max_tokens`:** Run a token length distribution analysis across your corpus. Set `max_tokens` to cover the 95th percentile. Going higher wastes GPU memory; going lower forces excessive splitting of naturally coherent passages.

```python
# Analyze your corpus before committing to a chunk size
import numpy as np
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

lengths = [len(tokenizer.encode(chunk)) for chunk in all_chunks]
print(f"p50:  {int(np.percentile(lengths, 50))} tokens")
print(f"p95:  {int(np.percentile(lengths, 95))} tokens")
print(f"p99:  {int(np.percentile(lengths, 99))} tokens")
print(f"max:  {max(lengths)} tokens")
```

---

### 2.3 Instruction-Tuning Dataset Format

Both Mistral Instruct and Llama 3 Instruct have specific chat templates. Using the wrong format causes the model to learn incorrect turn boundaries, leading to poor instruction-following behavior.

**Always use `apply_chat_template` — never hand-roll the format string.**

```python
# pipeline/formatting.py
from transformers import AutoTokenizer


def format_training_example(
    tokenizer: AutoTokenizer,
    system: str,
    instruction: str,
    response: str,
) -> str:
    """
    Formats a single training example using the model's native chat template.
    Works correctly for both Mistral and Llama 3 — no manual template strings needed.
    """
    messages = [
        {"role": "system",    "content": system},
        {"role": "user",      "content": instruction},
        {"role": "assistant", "content": response},
    ]
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False,   # False during training — response is included
    )


# Example output for Mistral Instruct v0.3:
# <s>[INST] {system}\n\n{instruction} [/INST] {response}</s>

# Example output for Llama 3 Instruct:
# <|begin_of_text|><|start_header_id|>system<|end_header_id|>
# {system}<|eot_id|><|start_header_id|>user<|end_header_id|>
# {instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
# {response}<|eot_id|>
```

**Final JSONL dataset structure:**

```jsonl
{"text": "<s>[INST] You are a compliance expert...\n\nWhat are the key requirements for SOC 2 Type II? [/INST] SOC 2 Type II requires...</s>"}
{"text": "<s>[INST] You are a compliance expert...\n\nExplain the difference between HIPAA and HITECH. [/INST] HIPAA establishes...</s>"}
```

---

### 2.4 Synthetic Data Generation with GPT-4o

You will rarely have thousands of hand-labeled Q&A pairs. GPT-4o as a data labeler is a well-established and accepted technique for bootstrapping fine-tuning datasets from raw documents.

```python
# pipeline/synthetic_data.py
import openai, json, asyncio
from typing import AsyncIterator


LABELER_PROMPT = """\
You are a domain expert creating high-quality training data for an AI system.

Given the following passage from a {domain} document, generate {n_pairs} question-answer
pairs. Requirements:
- Questions must require genuine understanding of the content, not keyword matching
- Answers must be comprehensive, cite specific details from the passage
- Questions should vary in type: factual, inferential, procedural, comparative
- Do NOT generate questions answerable from general knowledge alone

Return valid JSON only, no markdown:
{{"pairs": [{{"question": "...", "answer": "..."}}]}}

Passage:
{passage}"""


async def generate_qa_pairs(
    passage: str,
    domain: str,
    n_pairs: int = 3,
    client: openai.AsyncOpenAI = None,
) -> list[dict]:
    """Generates synthetic Q&A pairs from a document chunk using GPT-4o."""
    client = client or openai.AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": LABELER_PROMPT.format(
            domain=domain,
            passage=passage,
            n_pairs=n_pairs,
        )}],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("pairs", [])


async def build_dataset(
    chunks: list[str],
    domain: str,
    system_prompt: str,
) -> list[dict]:
    """Processes all chunks concurrently and builds the training dataset."""
    client = openai.AsyncOpenAI()
    tasks = [generate_qa_pairs(chunk, domain, client=client) for chunk in chunks]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    dataset = []
    for chunk, pairs in zip(chunks, results):
        if isinstance(pairs, Exception):
            continue
        for pair in pairs:
            dataset.append({
                "system":      system_prompt,
                "instruction": pair["question"],
                "response":    pair["answer"],
                "source_chunk": chunk,          # keep for traceability
            })
    return dataset
```

> **Data labeling cost estimate:** At ~$0.005 per GPT-4o call and 3 pairs per chunk, 10,000 chunks costs approximately $50 and produces 30,000 training examples — a solid fine-tuning dataset for most domain adaptation tasks.

---

## 3. QLoRA Training Configuration

### 3.1 Configuration Dataclass

Every training run must be fully reproducible. Centralizing all hyperparameters in a typed dataclass ensures you can log the complete config to Weights & Biases and re-run any experiment exactly.

```python
# training/config.py
from dataclasses import dataclass, field


@dataclass
class QLoRAConfig:
    # ── Base model ──────────────────────────────────────────────────────────
    model_name: str = "mistralai/Mistral-7B-Instruct-v0.3"
    # Alternative: "meta-llama/Meta-Llama-3-8B-Instruct"

    # ── 4-bit quantization (QLoRA = quantized base + float16 adapters) ──────
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"           # NF4 outperforms FP4 for LLMs
    bnb_4bit_compute_dtype: str = "bfloat16"   # bfloat16 > float16 on A100/H100
    bnb_4bit_use_double_quant: bool = True      # saves ~0.4 bits/param extra

    # ── LoRA adapter ────────────────────────────────────────────────────────
    lora_r: int = 16                            # rank — see Section 4
    lora_alpha: int = 32                        # effective scale = alpha/r = 2.0
    lora_dropout: float = 0.05
    lora_target_modules: list = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",    # attention projections
        "gate_proj", "up_proj", "down_proj",         # MLP feed-forward layers
    ])
    # Targeting ALL linear layers (attention + MLP) gives ~15-20% better results
    # than attention-only, at the cost of ~2x adapter parameter count.

    # ── Training hyperparameters ────────────────────────────────────────────
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 8       # effective batch = 2 × 8 = 16
    learning_rate: float = 2e-4                # starting point; sweep 5e-5 to 3e-4
    lr_scheduler_type: str = "cosine"          # cosine outperforms linear for fine-tuning
    warmup_ratio: float = 0.03                 # 3% of total steps for LR warmup
    weight_decay: float = 0.001
    max_seq_length: int = 2048                 # set from token length distribution analysis
    max_grad_norm: float = 0.3                 # gradient clipping — essential with 4-bit

    # ── Efficiency settings ─────────────────────────────────────────────────
    gradient_checkpointing: bool = True        # trades compute for memory — always enable
    optim: str = "paged_adamw_8bit"            # paged optimizer reduces GPU memory spikes
    packing: bool = True                       # sequence packing = 30–50% throughput gain
    fp16: bool = False
    bf16: bool = True                          # bfloat16 if GPU supports it (A100+)

    # ── Logging & saving ────────────────────────────────────────────────────
    output_dir: str = "./outputs"
    logging_steps: int = 10
    save_strategy: str = "steps"
    save_steps: int = 100
    eval_steps: int = 100
    load_best_model_at_end: bool = True
    report_to: str = "wandb"
```

---

### 3.2 Building the Model and Tokenizer

```python
# training/model.py
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import prepare_model_for_kbit_training
import torch


def build_model_and_tokenizer(cfg: QLoRAConfig):
    # Configure 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=cfg.load_in_4bit,
        bnb_4bit_quant_type=cfg.bnb_4bit_quant_type,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=cfg.bnb_4bit_use_double_quant,
    )

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name,
        quantization_config=bnb_config,
        device_map="auto",                          # distributes across available GPUs
        trust_remote_code=True,
        attn_implementation="flash_attention_2",    # 2–4x faster, lower memory
    )

    # CRITICAL: prepares the quantized model for gradient computation
    # This casts layer norms and embedding to float32 for numerical stability
    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=cfg.gradient_checkpointing,
    )

    # Must disable KV cache during training — causes incorrect gradients if enabled
    model.config.use_cache = False
    model.config.pretraining_tp = 1                # 1 for single-GPU training

    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    tokenizer.pad_token = tokenizer.eos_token      # Mistral has no dedicated pad token
    tokenizer.padding_side = "right"               # right padding for causal LM training

    return model, tokenizer
```

---

### 3.3 Attaching LoRA Adapters

```python
# training/lora.py
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from transformers import TrainingArguments
from datasets import Dataset


def attach_lora(model, cfg: QLoRAConfig):
    lora_config = LoraConfig(
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        target_modules=cfg.lora_target_modules,
        lora_dropout=cfg.lora_dropout,
        bias="none",                    # standard setting; "all" rarely improves results
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    # Example output:
    # trainable params: 83,886,080 || all params: 7,324,999,680 || trainable%: 1.1448
    return model


def build_trainer(
    model,
    tokenizer,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    cfg: QLoRAConfig,
) -> SFTTrainer:
    training_args = TrainingArguments(
        output_dir=cfg.output_dir,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        learning_rate=cfg.learning_rate,
        lr_scheduler_type=cfg.lr_scheduler_type,
        warmup_ratio=cfg.warmup_ratio,
        weight_decay=cfg.weight_decay,
        max_grad_norm=cfg.max_grad_norm,
        optim=cfg.optim,
        fp16=cfg.fp16,
        bf16=cfg.bf16,
        gradient_checkpointing=cfg.gradient_checkpointing,
        logging_steps=cfg.logging_steps,
        save_strategy=cfg.save_strategy,
        save_steps=cfg.save_steps,
        eval_steps=cfg.eval_steps,
        evaluation_strategy="steps",
        load_best_model_at_end=cfg.load_best_model_at_end,
        report_to=cfg.report_to,
    )

    # DataCollator masks prompt tokens — loss computed on response tokens ONLY
    # This is not optional; training on prompt tokens actively harms performance
    response_template = "[/INST]"                  # Mistral marker; adjust for Llama 3
    collator = DataCollatorForCompletionOnlyLM(
        response_template,
        tokenizer=tokenizer,
    )

    return SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        dataset_text_field="text",
        max_seq_length=cfg.max_seq_length,
        data_collator=collator,
        packing=cfg.packing,                       # sequence packing for efficiency
        args=training_args,
    )
```

---

## 4. LoRA Rank Selection

Rank is the single most impactful LoRA hyperparameter. It controls how many "directions" in weight space the adapter can represent. Rank `r` adds a weight update `ΔW = B·A` where `B` is `d × r` and `A` is `r × d`.

- Higher rank → more expressive → more parameters → higher overfitting risk
- Lower rank → less expressive → fewer parameters → faster training, less overfitting risk

### 4.1 Decision Framework

| Scenario | Recommended rank | Reasoning |
|---|---|---|
| Domain vocabulary / terminology adaptation | r = 8 | Shallow task; base model structure is sufficient |
| Style and response format adaptation | r = 16 | Moderate task; needs reasonable expressiveness |
| Domain-specific reasoning patterns | r = 32 | Deeper behavioral change required |
| Full task adaptation (very different domain) | r = 64 | Significant deviation from pretraining distribution |
| Very small dataset (< 1,000 examples) | r = 8 | Low rank prevents overfitting |
| Large dataset (> 50,000 examples) | r = 32–64 | Dataset can support higher expressiveness |

**Alpha/rank ratio:** Always keep `lora_alpha = 2 × lora_r` as a starting default. This gives a scale factor of 2.0 — the most commonly effective value across published research.

| lora_r | lora_alpha | Scale (alpha/r) |
|--------|------------|-----------------|
| 8 | 16 | 2.0 |
| 16 | 32 | 2.0 |
| 32 | 64 | 2.0 |
| 64 | 128 | 2.0 |

For DomainMind's typical use case — adapting a general LLM to understand company-specific documents and response formats — **r=16 with alpha=32** is the correct starting point.

---

### 4.2 Hyperparameter Sweep

Never commit to a rank without running at least a 3-point comparison. Use Weights & Biases Sweeps to run experiments in parallel:

```python
# training/sweep.py
import wandb


sweep_config = {
    "method": "grid",
    "metric": {"name": "eval/loss", "goal": "minimize"},
    "parameters": {
        "lora_r":        {"values": [8, 16, 32]},
        "lora_alpha":    {"values": [16, 32, 64]},   # keeps scale=2.0 across ranks
        "learning_rate": {"values": [1e-4, 2e-4]},
    },
}

def train_run(config=None):
    with wandb.init(config=config):
        cfg = QLoRAConfig(
            lora_r=wandb.config.lora_r,
            lora_alpha=wandb.config.lora_alpha,
            learning_rate=wandb.config.learning_rate,
        )
        model, tokenizer = build_model_and_tokenizer(cfg)
        model = attach_lora(model, cfg)
        trainer = build_trainer(model, tokenizer, train_ds, eval_ds, cfg)
        trainer.train()

sweep_id = wandb.sweep(sweep_config, project="domainmind-qlora")
wandb.agent(sweep_id, function=train_run, count=6)
```

---

### 4.3 Diagnosing Rank Choice from Training Signals

| Signal observed | Diagnosis | Fix |
|---|---|---|
| Training loss drops fast then plateaus very early | Rank too low — model cannot learn enough | Increase rank to next tier |
| Val loss rises while train loss falls | Rank too high for dataset size — overfitting | Reduce rank or add more training data |
| Both losses drop together, plateau at similar values | Good fit — rank is appropriate | Lock in this rank |
| Training loss oscillates without converging | Learning rate too high for this rank | Reduce LR by 2x |
| Slow loss decrease, training feels stuck | Rank too low or LR too low | Increase both incrementally |

---

## 5. Merging LoRA Adapters with the Base Model

After training, two separate artifacts exist: the 4-bit quantized base model and the float16 LoRA adapter weights. For production serving with vLLM, these must be merged into a single full-precision model.

### 5.1 Merge and Save

```python
# training/merge.py
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


def merge_and_save(
    base_model_id: str,
    adapter_path: str,
    output_path: str,
) -> str:
    """
    Merges trained LoRA adapter weights into the base model.

    CRITICAL: Load the base model WITHOUT quantization for merging.
    Merging from a 4-bit quantized model bakes quantization errors
    permanently into the merged weights.
    """
    print("Loading base model in float16 for merging...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="cpu",              # merge on CPU to avoid GPU OOM
        trust_remote_code=True,
    )

    print("Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, adapter_path)

    print("Merging adapter weights into base model...")
    # merge_and_unload() computes:
    #   W_merged = W_base + (B @ A) × (alpha / r)
    # Result is a standard transformer with no adapter overhead.
    model = model.merge_and_unload()

    print("Saving merged model...")
    model.save_pretrained(
        output_path,
        safe_serialization=True,       # saves as .safetensors (safer than .bin)
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    tokenizer.save_pretrained(output_path)

    print(f"Merged model saved to: {output_path}")
    return output_path
```

> **Memory note:** A 7B model in float16 is approximately 14 GB. The merge operation briefly holds two copies in memory. If GPU VRAM is insufficient, always merge on CPU (`device_map="cpu"`) — it is slower but always safe.

---

### 5.2 Verifying the Merge

Before serving the merged model, verify that its outputs are identical to the adapter-applied model on the same inputs:

```python
# training/verify.py
from transformers import pipeline
import torch


def verify_merge(
    adapter_path: str,
    merged_path: str,
    test_prompts: list[str],
) -> bool:
    """
    Verifies that the merged model produces identical outputs to the
    adapter-applied model. Fails loudly if outputs differ.
    """
    pipe_adapter = pipeline(
        "text-generation", model=adapter_path,
        device_map="auto", torch_dtype=torch.float16,
    )
    pipe_merged = pipeline(
        "text-generation", model=merged_path,
        device_map="auto", torch_dtype=torch.float16,
    )

    all_match = True
    for prompt in test_prompts:
        gen_kwargs = {"max_new_tokens": 50, "do_sample": False}
        out_adapter = pipe_adapter(prompt, **gen_kwargs)[0]["generated_text"]
        out_merged  = pipe_merged(prompt,  **gen_kwargs)[0]["generated_text"]

        if out_adapter != out_merged:
            print(f"MISMATCH on prompt: {prompt[:60]}...")
            print(f"  Adapter: {out_adapter[-100:]}")
            print(f"  Merged:  {out_merged[-100:]}")
            all_match = False

    if all_match:
        print("Merge verification passed — all outputs match.")
    return all_match
```

---

### 5.3 GGUF Quantization for Lightweight Deployment

After merging, optionally quantize to GGUF format for CPU inference or reduced GPU footprint. This is useful for demo environments or resource-constrained deployments:

```bash
# Step 1: Convert HuggingFace model to GGUF format
python convert_hf_to_gguf.py ./merged_model \
    --outfile domainmind-7b-f16.gguf \
    --outtype f16

# Step 2: Quantize to Q4_K_M (recommended sweet spot)
# Q4_K_M = 4-bit quantization with mixed precision for key layers
./llama-quantize domainmind-7b-f16.gguf domainmind-7b-Q4_K_M.gguf Q4_K_M
```

**GGUF quantization format comparison:**

| Format | Size (7B model) | Quality loss | Use case |
|--------|----------------|--------------|----------|
| F16 | ~14 GB | None | Production GPU serving |
| Q8_0 | ~7 GB | Minimal | High-quality CPU inference |
| Q4_K_M | ~4 GB | Low | Recommended default for CPU |
| Q3_K_M | ~3 GB | Moderate | Memory-constrained environments |
| Q2_K | ~2.5 GB | High | Demo only — not for production |

---

## 6. Critical Mistakes to Avoid

These are silent failure modes that tutorials consistently skip. Each one can cost days of debugging.

### Mistake 1 — Training on prompt tokens

Loss must be computed on response tokens only. If the loss includes prompt tokens, the model learns to predict the system prompt and user instruction, which wastes capacity and degrades answer quality.

`DataCollatorForCompletionOnlyLM` handles this correctly by masking all tokens before the response template marker. **This is not optional.**

```python
# WRONG: bare data collator — loss computed over entire sequence
trainer = SFTTrainer(model=model, ...)

# CORRECT: completion-only collator — loss on response tokens only
collator = DataCollatorForCompletionOnlyLM("[/INST]", tokenizer=tokenizer)
trainer = SFTTrainer(model=model, data_collator=collator, ...)
```

### Mistake 2 — Leaving KV cache enabled during training

The KV cache is designed for inference-time autoregressive generation. During training, with teacher forcing, it causes incorrect gradient computation. Always disable before training and re-enable before inference:

```python
# Before training
model.config.use_cache = False

# After training / before inference
model.config.use_cache = True
```

### Mistake 3 — Evaluating only on training-domain data

Always reserve 5–10 test questions that cover edge cases not explicitly present in your training data. If the model performs well on training questions but poorly on these held-out cases, it has overfit to surface patterns rather than learned domain reasoning.

This is the most common fine-tuning failure mode and the one most likely to be probed in a senior AI engineer interview.

```python
# Golden test set — manually written, NEVER used in training or validation
# These should challenge the model on:
# - Implicit reasoning (not just retrieval)
# - Conflicting information resolution
# - Out-of-distribution phrasing
# - Multi-hop questions requiring connecting two pieces of domain knowledge

GOLDEN_TEST_SET = [
    {
        "instruction": "...",
        "expected_answer": "...",
        "evaluation_criteria": "Tests implicit reasoning about X",
    },
    # ... 50 examples minimum
]
```

### Mistake 4 — Merging from a quantized base model

Always load the base model in `float16` for merging. Merging from 4-bit NF4 weights permanently bakes quantization errors into the final model, degrading quality in a way that is impossible to recover from without retraining.

### Mistake 5 — Ignoring sequence length distribution

Setting `max_seq_length` too high wastes GPU memory (attention is quadratic in sequence length). Setting it too low forces excessive chunking. Always analyze your dataset's token length distribution before setting this value.

---

## 7. Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    DomainMind Pipeline                   │
├─────────────────┬───────────────────────────────────────┤
│  Data Layer     │  Raw docs → Clean → Chunk → Format    │
│                 │  GPT-4o labeler → JSONL dataset       │
│                 │  DVC version control                   │
├─────────────────┼───────────────────────────────────────┤
│  Training Layer │  Mistral 7B (4-bit NF4 quantized)     │
│                 │  + LoRA adapters (r=16, α=32)         │
│                 │  SFTTrainer + CompletionOnlyCollator   │
│                 │  W&B experiment tracking               │
├─────────────────┼───────────────────────────────────────┤
│  Merge Layer    │  Base model (float16) + adapter merge  │
│                 │  merge_and_unload() → safetensors      │
│                 │  Optional GGUF quantization            │
├─────────────────┼───────────────────────────────────────┤
│  Serving Layer  │  vLLM (OpenAI-compatible endpoint)     │
│                 │  .NET 8 API gateway + JWT auth         │
│                 │  Request logging → PostgreSQL          │
├─────────────────┼───────────────────────────────────────┤
│  RAG Layer      │  Qdrant vector DB + hybrid search      │
│                 │  Cross-encoder re-ranking              │
│                 │  Context injection + citation          │
├─────────────────┼───────────────────────────────────────┤
│  Eval Layer     │  RAGAS + ROUGE + BERTScore             │
│                 │  4-system comparison dashboard         │
│                 │  CI gate on faithfulness score         │
└─────────────────┴───────────────────────────────────────┘
```

---

## 8. Resume Talking Points

Use these when discussing DomainMind in interviews. They demonstrate genuine engineering depth rather than tutorial-level knowledge.

**On data preparation:**
> "I ran a MinHash LSH deduplication pass before training — at 85% similarity threshold — because exact-hash deduplication misses near-duplicates that cause models to memorize phrasing patterns rather than learn domain reasoning."

**On training configuration:**
> "I use `DataCollatorForCompletionOnlyLM` to mask prompt tokens from the loss computation. Training on the full sequence — including the instruction — wastes model capacity on predicting things the system already controls."

**On rank selection:**
> "I ran a W&B grid sweep across r=8, r=16, and r=32. For our domain adaptation task — adapting response format and terminology, not fundamentally new reasoning — r=16 with alpha=32 gave the best validation loss without overfitting. Higher ranks overfit on our dataset size."

**On the merge step:**
> "I always load the base model in float16, not 4-bit, for the merge step. Merging from quantized weights permanently bakes quantization errors into the merged model — a mistake that costs a full retraining run to fix."

**On evaluation:**
> "I maintained a golden test set of 50 questions that were never used in training or validation. They specifically test implicit reasoning and multi-hop domain knowledge — the failure modes that only show up if the model overfit to surface patterns."

**On the RAG vs fine-tune tradeoff:**
> "Fine-tuning adapts the model's style, terminology, and response format. RAG provides up-to-date factual grounding. They solve different problems. DomainMind uses both — fine-tuning for behavior adaptation, RAG for knowledge retrieval — and the combined system measurably outperforms either alone on our evaluation harness."

---

*Document generated for DomainMind project portfolio — Ravindra Kumar, Principal Engineer*
