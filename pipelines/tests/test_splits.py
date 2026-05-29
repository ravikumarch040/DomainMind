from domainmind.training.splits import stratified_split


def test_stratified_split_no_empty():
    records = [
        {"text": "a", "source_chunk": "doc1"},
        {"text": "b", "source_chunk": "doc1"},
        {"text": "c", "source_chunk": "doc2"},
        {"text": "d", "source_chunk": "doc2"},
    ]
    train, val, test = stratified_split(records, seed=42)
    assert len(train) + len(val) + len(test) == len(records)
    assert len(train) >= 2
