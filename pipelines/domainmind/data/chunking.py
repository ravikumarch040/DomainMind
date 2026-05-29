"""Chunking strategy — LLD §2.2."""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer


def build_character_chunker(chunk_size: int = 512, overlap: int = 64):
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
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    i = 0
    while i < len(tokens):
        chunk_tokens = tokens[i : i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
        i += max_tokens - overlap_tokens
    return chunks


def analyze_token_distribution(chunks: list[str], model_name: str) -> dict[str, int]:
    import numpy as np

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    lengths = [len(tokenizer.encode(c)) for c in chunks]
    return {
        "p50": int(np.percentile(lengths, 50)),
        "p95": int(np.percentile(lengths, 95)),
        "p99": int(np.percentile(lengths, 99)),
        "max": max(lengths),
        "count": len(lengths),
    }
