from dataclasses import dataclass
from typing import Dict, List, Tuple

from ..models import Document
from ..normalize.parse import extract_doi, extract_first_author, extract_year
from ..normalize.text import normalize_doi
from ..utils import stable_hash


@dataclass
class WosFile:
    header_lines: List[str]
    records: List[List[Tuple[str, str]]]


def _parse_line(line: str) -> Tuple[str, str]:
    tag = line[:2]
    value = line[3:] if len(line) > 3 else ""
    return tag, value.strip()


def parse_wos_plaintext(path: str) -> WosFile:
    header_lines: List[str] = []
    records: List[List[Tuple[str, str]]] = []
    current: List[Tuple[str, str]] = []
    in_records = False

    with open(path, "r", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue

            if not in_records:
                if line.startswith("PT "):
                    in_records = True
                else:
                    header_lines.append(line)
                    continue

            if line.strip() == "ER":
                if current:
                    records.append(current)
                    current = []
                continue

            if line.startswith("  ") and current:
                tag, value = current[-1]
                current[-1] = (tag, f"{value} {line.strip()}".strip())
                continue

            current.append(_parse_line(line))

    if current:
        records.append(current)

    return WosFile(header_lines=header_lines, records=records)


def write_wos_plaintext(path: str, wos_file: WosFile) -> None:
    lines: List[str] = []
    lines.extend(wos_file.header_lines)

    for record in wos_file.records:
        for tag, value in record:
            if value:
                lines.append(f"{tag} {value}")
            else:
                lines.append(f"{tag}")
        lines.append("ER")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def get_tag_values(record: List[Tuple[str, str]], tag: str) -> List[str]:
    return [value for t, value in record if t == tag]


def extract_wos_references(records: List[List[Tuple[str, str]]]) -> List[str]:
    refs: List[str] = []
    for record in records:
        refs.extend(get_tag_values(record, "CR"))
    return refs


def build_documents_from_wos(records: List[List[Tuple[str, str]]]) -> List[Document]:
    documents: List[Document] = []

    for record in records:
        ut_values = get_tag_values(record, "UT")
        title_values = get_tag_values(record, "TI")
        year_values = get_tag_values(record, "PY")
        doi_values = get_tag_values(record, "DI")
        author_values = get_tag_values(record, "AU")
        refs = get_tag_values(record, "CR")

        title = title_values[0] if title_values else ""
        year = extract_year(year_values[0]) if year_values else None
        doi = normalize_doi(doi_values[0]) if doi_values else None
        authors = "; ".join(author_values)
        first_author = extract_first_author(author_values[0]) if author_values else None

        if ut_values:
            raw_doc_id = ut_values[0]
        else:
            raw_doc_id = stable_hash(f"{title}|{year or ''}|{first_author or ''}")

        documents.append(
            Document(
                raw_doc_id=raw_doc_id,
                title=title,
                year=year,
                doi=doi,
                first_author=first_author,
                authors=authors,
                references=refs,
                source="wos",
            )
        )

    return documents
