import os

from bibclean.canonicalize import canonicalize_references
from bibclean.io.wos_plaintext import extract_wos_references, parse_wos_plaintext


def test_wos_abramo_doi_merges():
    path = os.path.join("fixtures", "wos_sample.txt")
    wos_file = parse_wos_plaintext(path)
    raw_refs = extract_wos_references(wos_file.records)

    mapping_df, _summary, mapping_dict = canonicalize_references(raw_refs)

    abramo_refs = [
        ref
        for ref in mapping_df["raw_reference"].tolist()
        if "10.1007/s11192-014-1269-8" in ref
    ]

    assert len(abramo_refs) >= 2
    canonicals = {mapping_dict[ref] for ref in abramo_refs}
    assert len(canonicals) == 1
