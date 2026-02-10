from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Reference:
    raw: str
    norm: str
    doi: Optional[str]
    year: Optional[str]
    first_author: Optional[str]
    block_key: str


@dataclass
class Document:
    raw_doc_id: str
    title: str
    year: Optional[str]
    doi: Optional[str]
    first_author: Optional[str]
    authors: str
    references: List[str]
    source: str
