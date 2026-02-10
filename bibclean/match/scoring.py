from typing import Tuple

from rapidfuzz import fuzz

from bibclean.models import Reference


def score_pair(ref_a: Reference, ref_b: Reference) -> Tuple[int, str]:
    if ref_a.doi and ref_b.doi and ref_a.doi == ref_b.doi:
        return 100, "doi_exact"

    base_score = fuzz.token_set_ratio(ref_a.norm, ref_b.norm)
    adjustments = 0

    if ref_a.year and ref_b.year and ref_a.year != ref_b.year:
        adjustments -= 10
    if ref_a.first_author and ref_b.first_author and ref_a.first_author != ref_b.first_author:
        adjustments -= 10

    confidence = int(round(base_score + adjustments))
    confidence = max(0, min(100, confidence))
    return confidence, "fuzzy"
