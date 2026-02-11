import re

from ..models import Reference


def _title_block(norm_text: str) -> str:
    if not norm_text:
        return ""
    text = re.sub(r"\d", " ", norm_text)
    tokens = [tok for tok in text.split() if len(tok) > 1]
    return " ".join(tokens).strip()


def build_block_key(ref: Reference) -> str:
    if ref.doi:
        return f"doi:{ref.doi}"
    if ref.year and ref.first_author:
        return f"ya:{ref.year}:{ref.first_author}"
    title_block = _title_block(ref.norm)
    if title_block:
        return f"tb:{title_block[:24]}"
    prefix = ref.norm[:12] if ref.norm else ""
    return f"pref:{prefix}"
