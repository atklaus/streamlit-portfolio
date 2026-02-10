import os

from bibclean.canonicalize import canonicalize_references
from bibclean.io.scopus_csv import extract_scopus_references, load_scopus_csv


def test_scopus_abramo_doi_merges():
    path = os.path.join("fixtures", "scopus_sample.csv")
    df, ref_col = load_scopus_csv(path)
    raw_refs = extract_scopus_references(df, ref_col)

    mapping_df, _summary, mapping_dict = canonicalize_references(raw_refs)

    abramo_refs = [
        ref
        for ref in mapping_df["raw_reference"].tolist()
        if "10.1007/s11192-014-1269-8" in ref
    ]

    assert len(abramo_refs) >= 2
    canonicals = {mapping_dict[ref] for ref in abramo_refs}
    assert len(canonicals) == 1
