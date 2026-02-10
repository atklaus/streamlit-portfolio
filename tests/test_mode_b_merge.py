import os

from bibclean.io.scopus_csv import build_documents_from_scopus, load_scopus_csv
from bibclean.io.wos_plaintext import build_documents_from_wos, parse_wos_plaintext
from bibclean.merge import merge_documents


def test_mode_b_merge_placeholder():
    scopus_path = os.path.join("fixtures", "scopus_sample.csv")
    wos_path = os.path.join("fixtures", "wos_sample.txt")

    df, ref_col = load_scopus_csv(scopus_path)
    scopus_docs = build_documents_from_scopus(df, ref_col)

    wos_file = parse_wos_plaintext(wos_path)
    wos_docs = build_documents_from_wos(wos_file.records)

    canonical_docs, mappings = merge_documents(scopus_docs + wos_docs)

    assert len(canonical_docs) >= 1
    assert len(mappings) == len(scopus_docs) + len(wos_docs)
