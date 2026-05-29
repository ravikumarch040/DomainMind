"""Prompt assembly with source tags and token budget management."""

SOURCE_TAG = "[SOURCE: {doc_name}, {chunk_id}]"


def format_chunk_with_source(chunk: dict) -> str:
    return (
        f"{SOURCE_TAG.format(doc_name=chunk.get('doc_name', 'unknown'), chunk_id=chunk.get('chunk_id', '0'))}\n"
        f"{chunk.get('text', '')}"
    )


def assemble_prompt(
    system_prompt: str,
    user_query: str,
    chunks: list[dict],
    max_chars: int = 12000,
) -> str:
    """Rank-trim chunks to fit token budget — never silent mid-chunk truncation."""
    sorted_chunks = sorted(chunks, key=lambda c: c.get("score", 0), reverse=True)
    context_parts = []
    total = 0
    for chunk in sorted_chunks:
        part = format_chunk_with_source(chunk)
        if total + len(part) > max_chars:
            break
        context_parts.append(part)
        total += len(part)

    context_block = "\n\n".join(context_parts)
    return (
        f"{system_prompt}\n\n"
        f"Use the following retrieved context to answer. Cite sources using [SOURCE: doc, chunk_id] tags.\n\n"
        f"{context_block}\n\n"
        f"User question: {user_query}"
    )
