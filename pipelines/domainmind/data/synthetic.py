"""Synthetic data generation with GPT-4o — LLD §2.4."""

import asyncio
import json
from typing import AsyncIterator

import openai

from domainmind.settings import settings

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
    domain: str | None = None,
    n_pairs: int = 3,
    client: openai.AsyncOpenAI | None = None,
) -> list[dict]:
    domain = domain or settings.domain
    client = client or openai.AsyncOpenAI(api_key=settings.openai_api_key or None)
    response = await client.chat.completions.create(
        model=settings.openai_model_labeler,
        messages=[
            {
                "role": "user",
                "content": LABELER_PROMPT.format(
                    domain=domain, passage=passage, n_pairs=n_pairs
                ),
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    data = json.loads(response.choices[0].message.content or "{}")
    return data.get("pairs", [])


async def build_dataset(
    chunks: list[str],
    domain: str | None = None,
    system_prompt: str | None = None,
) -> list[dict]:
    system_prompt = system_prompt or settings.system_prompt
    domain = domain or settings.domain
    client = openai.AsyncOpenAI(api_key=settings.openai_api_key or None)
    tasks = [generate_qa_pairs(chunk, domain, client=client) for chunk in chunks]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    dataset = []
    for chunk, pairs in zip(chunks, results):
        if isinstance(pairs, Exception):
            continue
        for pair in pairs:
            dataset.append(
                {
                    "system": system_prompt,
                    "instruction": pair["question"],
                    "response": pair["answer"],
                    "source_chunk": chunk,
                }
            )
    return dataset
