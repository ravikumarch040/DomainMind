from domainmind.data.phi_scrubber import contains_phi_patterns, scrub_phi, scrub_regex


SYNTHETIC_PHI_FIXTURE = """
Patient John Doe, SSN 123-45-6789, MRN# 445566, DOB 01/15/1980.
Contact: jane.doe@hospital.org, phone 555-123-4567.
"""


def test_scrub_regex_removes_ssn():
    text, count = scrub_regex(SYNTHETIC_PHI_FIXTURE)
    assert count > 0
    assert "123-45-6789" not in text


def test_scrub_phi_ci_fixture():
    result = scrub_phi(SYNTHETIC_PHI_FIXTURE)
    assert not contains_phi_patterns(result.text), "PHI patterns must be removed post-scrub"


def test_contains_phi_patterns_detects_ssn():
    assert contains_phi_patterns("SSN 123-45-6789")
