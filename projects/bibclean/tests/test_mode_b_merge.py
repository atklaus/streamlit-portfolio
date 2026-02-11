from pathlib import Path

from projects.bibclean.io.scopus_csv import build_documents_from_scopus, load_scopus_csv
from projects.bibclean.io.wos_plaintext import build_documents_from_wos, parse_wos_plaintext
from projects.bibclean.merge import merge_documents


def test_mode_b_merge_placeholder():
    fixtures_dir = Path(__file__).resolve().parents[1] / "fixtures"
    scopus_path = fixtures_dir / "scopus_sample.csv"
    wos_path = fixtures_dir / "wos_sample.txt"

    df, ref_col = load_scopus_csv(str(scopus_path))
    scopus_docs = build_documents_from_scopus(df, ref_col)

    wos_file = parse_wos_plaintext(str(wos_path))
    wos_docs = build_documents_from_wos(wos_file.records)

    canonical_docs, mappings = merge_documents(scopus_docs + wos_docs)

    assert len(canonical_docs) >= 1
    assert len(mappings) == len(scopus_docs) + len(wos_docs)
