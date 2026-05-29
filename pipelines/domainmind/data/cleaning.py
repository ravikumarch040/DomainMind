"""Corpus cleaning and MinHash LSH deduplication — LLD §2.1."""

import re
import unicodedata

from datasketch import MinHash, MinHashLSH


def clean_document(text: str) -> str | None:
    """
    Cleans a raw document string.
    Returns None if the document fails quality gates.
    """
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"Page \d+ of \d+", "", text)
    text = re.sub(r"(?i)confidential|internal only", "", text)
    text = unicodedata.normalize("NFKC", text)

    words = text.split()
    if len(words) < 50:
        return None
    if len(set(words)) / len(words) < 0.3:
        return None

    return text.strip()


class DeduplicationPipeline:
    """MinHash LSH deduplication at configurable similarity threshold."""

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
