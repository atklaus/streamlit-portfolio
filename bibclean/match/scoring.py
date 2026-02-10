from typing import Tuple

import re

from rapidfuzz import fuzz

from bibclean import config
from bibclean.models import Reference


def _journal_key(norm_text: str) -> str:
    for full_name in config.journal_abbrev_map.values():
        pattern = r"\b" + re.escape(full_name) + r"\b"
        if re.search(pattern, norm_text):
            return full_name
    return ""


def score_pair(ref_a: Reference, ref_b: Reference) -> Tuple[int, str]:
    if ref_a.doi and ref_b.doi and ref_a.doi == ref_b.doi:
        return 100, "doi_exact"

    base_score = fuzz.token_set_ratio(ref_a.norm, ref_b.norm)
    adjustments = 0

    if ref_a.year and ref_b.year and ref_a.year != ref_b.year:
        adjustments -= 10
    if ref_a.first_author and ref_b.first_author and ref_a.first_author != ref_b.first_author:
        adjustments -= 10
    journal_a = _journal_key(ref_a.norm)
    journal_b = _journal_key(ref_b.norm)
    if journal_a and journal_a == journal_b:
        adjustments += config.journal_match_bonus

    confidence = int(round(base_score + adjustments))
    confidence = max(0, min(100, confidence))
    if config.enable_structured_override:
        if (
            ref_a.year
            and ref_b.year
            and ref_a.year == ref_b.year
            and ref_a.volume
            and ref_b.volume
            and ref_a.volume == ref_b.volume
            and ref_a.page
            and ref_b.page
            and ref_a.page == ref_b.page
        ):
            confidence = max(confidence, 98)
    return confidence, "fuzzy"
