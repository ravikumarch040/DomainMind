"""End-to-end data pipeline orchestrator."""

import json
from pathlib import Path

from domainmind.data.chunking import analyze_token_distribution, build_character_chunker
from domainmind.data.cleaning import DeduplicationPipeline, clean_document
from domainmind.data.formatting import format_training_example, to_jsonl_record
from domainmind.data.loaders import load_document
from domainmind.data.phi_scrubber import scrub_phi
from domainmind.data.synthetic import build_dataset
from domainmind.settings import settings


def run_pipeline(
    input_dir: Path,
    output_path: Path,
    *,
    skip_synthetic: bool = False,
    max_chunks: int | None = None,
) -> dict:
    """Run full pipeline: load → clean → scrub → dedup → chunk → label → format."""
    deduper = DeduplicationPipeline(threshold=0.85)
    chunks: list[str] = []
    stats = {"loaded": 0, "rejected_clean": 0, "duplicates": 0, "phi_scrubbed": 0}

    for path in sorted(input_dir.rglob("*")):
        if path.suffix.lower() not in {".pdf", ".docx", ".html", ".htm", ".txt", ".md"}:
            continue
        try:
            doc = load_document(path)
        except Exception:
            continue
        stats["loaded"] += 1

        cleaned = clean_document(doc.text)
        if cleaned is None:
            stats["rejected_clean"] += 1
            continue

        scrubbed = scrub_phi(cleaned)
        stats["phi_scrubbed"] += scrubbed.entities_found + scrubbed.regex_replacements

        if deduper.is_duplicate(scrubbed.text, doc.doc_id):
            stats["duplicates"] += 1
            continue

        try:
            from domainmind.data.chunking import token_aware_chunk
            from transformers import AutoTokenizer

            tokenizer = AutoTokenizer.from_pretrained(settings.base_model_name)
            doc_chunks = token_aware_chunk(scrubbed.text, tokenizer)
        except Exception:
            splitter = build_character_chunker()
            doc_chunks = splitter.split_text(scrubbed.text)
        chunks.extend(doc_chunks)

    if max_chunks:
        chunks = chunks[:max_chunks]

    try:
        token_stats = analyze_token_distribution(chunks, settings.base_model_name)
    except Exception:
        token_stats = {"p50": 0, "p95": 512, "p99": 1024, "max": 2048, "count": len(chunks)}

    records: list[dict] = []
    if skip_synthetic or not settings.openai_api_key:
        for chunk in chunks:
            records.append(
                {
                    "system": settings.system_prompt,
                    "instruction": f"Summarize this compliance passage:\n{chunk[:500]}",
                    "response": chunk[:1000],
                    "source_chunk": chunk,
                }
            )
    else:
        import asyncio

        dataset = asyncio.run(build_dataset(chunks))
        try:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(settings.base_model_name)
        except Exception:
            tokenizer = None
        for item in dataset:
            if tokenizer:
                text = format_training_example(
                    tokenizer,
                    item["system"],
                    item["instruction"],
                    item["response"],
                )
            else:
                text = f"[INST] {item['system']}\n\n{item['instruction']} [/INST] {item['response']}"
            records.append({**item, **to_jsonl_record(text)})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for r in records:
            if "text" not in r:
                r["text"] = (
                    f"[INST] {r['system']}\n\n{r['instruction']} [/INST] {r['response']}"
                )
            f.write(json.dumps({"text": r["text"]}) + "\n")

    return {**stats, "chunks": len(chunks), "records": len(records), **token_stats}
