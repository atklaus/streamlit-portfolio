import csv
from typing import List, Tuple

import pandas as pd

from bibclean.models import Document
from bibclean.normalize.parse import extract_doi, extract_first_author, extract_year
from bibclean.normalize.text import normalize_doi
from bibclean.utils import find_column_case_insensitive, safe_str, stable_hash


def _parse_csv_line(line: str) -> List[str]:
    return next(csv.reader([line]))


def _split_scopus_line(line: str, header_len: int) -> List[str]:
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]
    fields = _parse_csv_line(line)
    if len(fields) == header_len:
        return [field.strip() for field in fields]
    if len(fields) > header_len:
        quote_idx = line.find(',"')
        if quote_idx != -1:
            authors = line[:quote_idx]
            rest = line[quote_idx + 1 :]
            rest_fields = _parse_csv_line(rest)
            if len(rest_fields) == header_len - 1:
                return [authors.strip()] + [field.strip() for field in rest_fields]
        excess = len(fields) - header_len
        authors = ",".join(fields[: excess + 1])
        return [authors.strip()] + [field.strip() for field in fields[excess + 1 :]]
    if len(fields) < header_len:
        fields = fields + [""] * (header_len - len(fields))
    return [field.strip() for field in fields]


def _normalize_scopus_rows(rows: List[List[str]]) -> Tuple[List[str], List[List[str]]]:
    if not rows:
        raise ValueError("Scopus CSV appears empty")

    header = rows[0]
    if len(header) == 1 and "," in header[0]:
        header = [col.strip() for col in _parse_csv_line(header[0])]

    data_rows = rows[1:]
    normalized_rows: List[List[str]] = []
    for row in data_rows:
        if len(row) == 1 and "," in row[0]:
            row = _split_scopus_line(row[0], len(header))

        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        elif len(row) > len(header):
            head = row[: len(header) - 1]
            tail = row[len(header) - 1 :]
            row = head + [",".join(tail)]

        normalized_rows.append(row)

    return header, normalized_rows


def load_scopus_csv(path: str) -> Tuple[pd.DataFrame, str]:
    with open(path, "r", newline="", errors="ignore") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header, normalized_rows = _normalize_scopus_rows(rows)
    df = pd.DataFrame(normalized_rows, columns=header)

    ref_col = find_column_case_insensitive(df.columns, "References")
    if not ref_col:
        raise ValueError("Scopus CSV must include a References column")
    return df, ref_col


def split_scopus_references(value: str) -> List[str]:
    if value is None:
        return []
    raw = str(value).strip().strip('"')
    parts = [part.strip() for part in raw.split(";")]
    refs: List[str] = []
    current: List[str] = []
    for part in parts:
        if not part:
            continue
        current.append(part)
        if extract_doi(part) or extract_year(part):
            refs.append("; ".join(current).strip())
            current = []
    if current:
        refs.append("; ".join(current).strip())
    return refs


def extract_scopus_references(df: pd.DataFrame, ref_col: str) -> List[str]:
    references: List[str] = []
    for value in df[ref_col].fillna(""):
        references.extend(split_scopus_references(value))
    return references


def build_documents_from_scopus(df: pd.DataFrame, ref_col: str) -> List[Document]:
    title_col = find_column_case_insensitive(df.columns, "Title")
    year_col = find_column_case_insensitive(df.columns, "Year")
    doi_col = find_column_case_insensitive(df.columns, "DOI")
    authors_col = find_column_case_insensitive(df.columns, "Authors")

    documents: List[Document] = []
    for _, row in df.iterrows():
        title = safe_str(row[title_col]) if title_col else ""
        year_raw = safe_str(row[year_col]) if year_col else ""
        year = extract_year(year_raw) if year_raw else None
        doi_raw = safe_str(row[doi_col]) if doi_col else ""
        doi = normalize_doi(doi_raw) if doi_raw else None
        authors = safe_str(row[authors_col]) if authors_col else ""
        first_author = extract_first_author(authors) if authors else None
        refs = split_scopus_references(row[ref_col])
        raw_doc_id = stable_hash(f"{title}|{year or ''}|{doi or ''}")

        documents.append(
            Document(
                raw_doc_id=raw_doc_id,
                title=title,
                year=year,
                doi=doi,
                first_author=first_author,
                authors=authors,
                references=refs,
                source="scopus",
            )
        )

    return documents
