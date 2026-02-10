from typing import List, Tuple


def apply_mapping_to_wos_records(
    records: List[List[Tuple[str, str]]], mapping: dict[str, str]
) -> List[List[Tuple[str, str]]]:
    updated_records: List[List[Tuple[str, str]]] = []
    for record in records:
        updated = []
        for tag, value in record:
            if tag == "CR":
                raw = value.strip()
                canonical = mapping.get(raw, raw)
                updated.append((tag, canonical))
            else:
                updated.append((tag, value))
        updated_records.append(updated)
    return updated_records
