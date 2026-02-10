import re
import unicodedata

from bibclean import config


_punct_re = re.compile(r"[^\w\s]")
_ws_re = re.compile(r"\s+")


def remove_diacritics(text: str) -> str:
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _normalize_journal_abbrev(text: str) -> str:
    if not text:
        return ""
    for abbr, full in config.journal_abbrev_map.items():
        pattern = r"\b" + re.escape(abbr) + r"\b"
        text = re.sub(pattern, full, text)
    return text


def _remove_boilerplate_tokens(text: str) -> str:
    if not text:
        return ""
    if not config.boilerplate_tokens:
        return text
    pattern = r"\b(?:" + "|".join(re.escape(tok) for tok in config.boilerplate_tokens) + r")\b"
    return re.sub(pattern, " ", text)


def _merge_initials_tokens(text: str) -> str:
    if not text:
        return ""
    tokens = text.split()
    merged = []
    buffer = ""
    for tok in tokens:
        if len(tok) == 1 and tok.isalpha():
            buffer += tok
            continue
        if buffer:
            merged.append(buffer)
            buffer = ""
        merged.append(tok)
    if buffer:
        merged.append(buffer)
    return " ".join(merged)


def normalize_text(text: str) -> str:
    if text is None:
        return ""
    text = text.replace("&", " and ")
    text = remove_diacritics(text)
    text = text.lower()
    text = _punct_re.sub(" ", text)
    text = _normalize_journal_abbrev(text)
    text = _remove_boilerplate_tokens(text)
    if config.enable_initials_normalization:
        text = _merge_initials_tokens(text)
    text = _ws_re.sub(" ", text).strip()
    return text


def normalize_doi(doi: str) -> str:
    if doi is None:
        return ""
    doi = doi.strip().lower()
    doi = doi.replace("doi:", "").replace("doi ", "")
    doi = doi.strip().strip(".;,)")
    return doi
