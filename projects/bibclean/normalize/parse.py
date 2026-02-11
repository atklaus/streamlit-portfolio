import re
from typing import Optional

from .text import normalize_doi


_year_re = re.compile(r"\b(\d{4})\b")
_doi_re = re.compile(r"10\.\d{4,9}/[^\s;,)]+", re.IGNORECASE)
_author_re = re.compile(r"[A-Za-z]+")


def extract_year(text: str) -> Optional[str]:
    if not text:
        return None
    match = _year_re.search(text)
    if not match:
        return None
    return match.group(1)


def extract_doi(text: str) -> Optional[str]:
    if not text:
        return None
    match = _doi_re.search(text)
    if not match:
        return None
    return normalize_doi(match.group(0))


def extract_first_author(text: str) -> Optional[str]:
    if not text:
        return None
    segment = text
    if "," in text:
        segment = text.split(",", 1)[0]
    match = _author_re.search(segment)
    if not match:
        return None
    return match.group(0).lower()


def extract_volume(norm_text: str) -> Optional[str]:
    if not norm_text:
        return None
    text = norm_text.lower()
    match = re.search(r"\b(?:v|vol|volume)\s*(\d+)\b", text)
    if match:
        return match.group(1)
    return None


def extract_page_or_article(norm_text: str, year: Optional[str], volume: Optional[str]) -> Optional[str]:
    if not norm_text:
        return None
    text = norm_text.lower()
    match = re.search(r"\b(?:p|pp)\s*(\d{3,})\b", text)
    if match:
        return match.group(1)

    tokens = [tok for tok in re.split(r"\s+", text) if tok.isdigit() and len(tok) >= 5]
    for tok in tokens:
        if year and tok == year:
            continue
        if volume and tok == volume:
            continue
        return tok
    return None
