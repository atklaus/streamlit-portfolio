import hashlib
import os
from typing import Iterable, Optional


def stable_hash(value: str) -> str:
    """Deterministic short hash for IDs."""
    if value is None:
        value = ""
    h = hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()
    return h[:12]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def find_column_case_insensitive(columns: Iterable[str], target: str) -> Optional[str]:
    target_lower = target.lower()
    for col in columns:
        if col.lower() == target_lower:
            return col
    return None


def safe_str(value) -> str:
    if value is None:
        return ""
    return str(value)
