from domainmind.data.cleaning import DeduplicationPipeline, clean_document


def test_clean_document_rejects_short():
    assert clean_document("too short") is None


def test_clean_document_accepts_valid():
    text = " ".join(f"compliance term {i}" for i in range(60))
    result = clean_document(text)
    assert result is not None
    assert len(result.split()) >= 50


def test_deduplication():
    deduper = DeduplicationPipeline(threshold=0.85)
    text = " ".join(["compliance"] * 100)
    assert deduper.is_duplicate(text, "doc1") is False
    assert deduper.is_duplicate(text, "doc2") is True
