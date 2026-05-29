"""PHI scrubber — Microsoft Presidio + compliance regex. Runs before chunking."""

import re
from dataclasses import dataclass

# HIPAA / compliance patterns (supplement Presidio)
COMPLIANCE_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]"),  # SSN
    (r"\bMRN[:\s#]*\d+\b", "[MRN_REDACTED]"),
    (r"\b\d{2}/\d{2}/\d{4}\b", "[DATE_REDACTED]"),
    (r"\b\d{3}-\d{3}-\d{4}\b", "[PHONE_REDACTED]"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]"),
]

_analyzer = None
_anonymizer = None


def _get_presidio():
    global _analyzer, _anonymizer
    if _analyzer is None:
        try:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine

            _analyzer = AnalyzerEngine()
            _anonymizer = AnonymizerEngine()
        except Exception:
            _analyzer = False
            _anonymizer = False
    return _analyzer, _anonymizer


@dataclass
class ScrubResult:
    text: str
    entities_found: int
    regex_replacements: int


def scrub_regex(text: str) -> tuple[str, int]:
    count = 0
    for pattern, replacement in COMPLIANCE_PATTERNS:
        new_text, n = re.subn(pattern, replacement, text, flags=re.IGNORECASE)
        if n:
            count += n
            text = new_text
    return text, count


def scrub_phi(text: str, language: str = "en") -> ScrubResult:
    """Remove PHI/PII from text. Presidio when available, always apply regex."""
    regex_count = 0
    entities = 0

    text, regex_count = scrub_regex(text)

    analyzer, anonymizer = _get_presidio()
    if analyzer and anonymizer:
        results = analyzer.analyze(text=text, language=language)
        entities = len(results)
        if results:
            from presidio_anonymizer.entities import OperatorConfig

            text = anonymizer.anonymize(
                text=text,
                analyzer_results=results,
                operators={"DEFAULT": OperatorConfig("replace", {"new_value": "[PHI_REDACTED]"})},
            ).text

    return ScrubResult(text=text, entities_found=entities, regex_replacements=regex_count)


def contains_phi_patterns(text: str) -> bool:
    """Check if text still contains known PHI patterns (for CI tests)."""
    for pattern, _ in COMPLIANCE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
