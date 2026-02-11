from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from rapidfuzz import fuzz

from . import config
from .models import Document
from .normalize.text import normalize_text
from .utils import stable_hash


@dataclass
class DocumentMapping:
    raw_doc_id: str
    canonical_index: int
    match_reason: str
    confidence: int


def compute_canonical_doc_id(doc: Document) -> str:
    if doc.doi:
        return f"doi:{doc.doi}"
    base = f"{doc.title}|{doc.year or ''}|{doc.first_author or ''}"
    return f"hash:{stable_hash(base)}"


def _merge_into(canonical: Document, incoming: Document) -> None:
    if not canonical.doi and incoming.doi:
        canonical.doi = incoming.doi
    if not canonical.title and incoming.title:
        canonical.title = incoming.title
    if not canonical.year and incoming.year:
        canonical.year = incoming.year
    if not canonical.authors and incoming.authors:
        canonical.authors = incoming.authors
    if not canonical.first_author and incoming.first_author:
        canonical.first_author = incoming.first_author
    canonical.references.extend(incoming.references)


def merge_documents(documents: List[Document]) -> Tuple[List[Document], List[DocumentMapping]]:
    canonical_docs: List[Document] = []
    mappings: List[DocumentMapping] = []

    index_by_doi: Dict[str, int] = {}
    block_index: Dict[str, List[int]] = {}

    for doc in documents:
        block_key = (
            f"{doc.year}:{doc.first_author}"
            if doc.year and doc.first_author
            else None
        )
        if doc.doi:
            existing_idx = index_by_doi.get(doc.doi)
            if existing_idx is not None:
                _merge_into(canonical_docs[existing_idx], doc)
                mappings.append(
                    DocumentMapping(
                        raw_doc_id=doc.raw_doc_id,
                        canonical_index=existing_idx,
                        match_reason="doi_exact",
                        confidence=100,
                    )
                )
                continue
            canonical_docs.append(doc)
            canonical_idx = len(canonical_docs) - 1
            index_by_doi[doc.doi] = canonical_idx
            if block_key:
                block_index.setdefault(block_key, []).append(canonical_idx)
            mappings.append(
                DocumentMapping(
                    raw_doc_id=doc.raw_doc_id,
                    canonical_index=canonical_idx,
                    match_reason="new",
                    confidence=100,
                )
            )
            continue
        candidates = block_index.get(block_key, []) if block_key else []

        best_idx = None
        best_score = 0
        doc_title_norm = normalize_text(doc.title)

        for idx in candidates:
            cand = canonical_docs[idx]
            score = fuzz.token_set_ratio(doc_title_norm, normalize_text(cand.title))
            if score > best_score:
                best_score = score
                best_idx = idx

        if best_idx is not None and best_score >= config.doc_merge_threshold:
            _merge_into(canonical_docs[best_idx], doc)
            mappings.append(
                DocumentMapping(
                    raw_doc_id=doc.raw_doc_id,
                    canonical_index=best_idx,
                    match_reason="title_year_author_fuzzy",
                    confidence=int(round(best_score)),
                )
            )
        else:
            canonical_docs.append(doc)
            canonical_idx = len(canonical_docs) - 1
            mappings.append(
                DocumentMapping(
                    raw_doc_id=doc.raw_doc_id,
                    canonical_index=canonical_idx,
                    match_reason="new",
                    confidence=100,
                )
            )
            if block_key:
                block_index.setdefault(block_key, []).append(canonical_idx)

    return canonical_docs, mappings
