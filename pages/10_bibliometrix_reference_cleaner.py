import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
import streamlit as st

from layout.header import page_header
import lib.st_utils as stu

from bibclean import config as bc_config
from bibclean.apply.scopus_apply import apply_mapping_to_scopus
from bibclean.apply.wos_apply import apply_mapping_to_wos_records
from bibclean.canonicalize import canonicalize_references
from bibclean.io.detect import detect_input_format
from bibclean.io.scopus_csv import (
    build_documents_from_scopus,
    extract_scopus_references,
    load_scopus_csv,
)
from bibclean.io.wos_plaintext import (
    WosFile,
    build_documents_from_wos,
    extract_wos_references,
    parse_wos_plaintext,
    write_wos_plaintext,
)
from bibclean.match.cluster import UnionFind
from bibclean.merge import compute_canonical_doc_id, merge_documents
from bibclean.normalize.parse import extract_doi


page_header("Bibliometrix Reference Cleaner", page_name=os.path.basename(__file__))

stu.V_SPACE(1)

st.subheader("Bibliometrix Reference Cleaner")


@contextmanager
def _temp_config(overrides: dict):
    originals = {key: getattr(bc_config, key) for key in overrides}
    for key, value in overrides.items():
        setattr(bc_config, key, value)
    try:
        yield
    finally:
        for key, value in originals.items():
            setattr(bc_config, key, value)


def _init_state():
    if "bibclean" not in st.session_state:
        st.session_state["bibclean"] = {
            "stage": "idle",
            "mode": "Mode A",
            "outputs": {},
            "review_df": None,
            "artifacts": {},
        }
    return st.session_state["bibclean"]


def _reset_state():
    st.session_state.pop("bibclean", None)
    st.rerun()


def _write_upload_to_temp(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix
    handle, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(handle, "wb") as f:
        f.write(uploaded_file.getvalue())
    return path


def _df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def _json_to_bytes(payload: dict) -> bytes:
    return json.dumps(payload, indent=2).encode("utf-8")


def _wos_to_bytes(wos_file) -> bytes:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.close()
    write_wos_plaintext(tmp.name, wos_file)
    with open(tmp.name, "rb") as f:
        return f.read()


def _build_outputs_list(entries):
    outputs = []
    for entry in entries:
        if entry["data"] is None:
            continue
        outputs.append(entry)
    return outputs


def _apply_review_merges(mapping_df: pd.DataFrame, review_df: pd.DataFrame) -> pd.DataFrame:
    ref_list = mapping_df["raw_reference"].tolist()
    ref_index = {ref: idx for idx, ref in enumerate(ref_list)}

    uf = UnionFind(len(ref_list))
    for cluster_id, group in mapping_df.groupby("cluster_id"):
        indices = [ref_index[ref] for ref in group["raw_reference"].tolist()]
        if len(indices) > 1:
            base = indices[0]
            for idx in indices[1:]:
                uf.union(base, idx)

    merge_pairs = review_df[review_df["decision"] == "Merge"]
    for _, row in merge_pairs.iterrows():
        a = ref_index.get(row["raw_reference_a"])
        b = ref_index.get(row["raw_reference_b"])
        if a is None or b is None:
            continue
        uf.union(a, b)

    clusters = {}
    for idx in range(len(ref_list)):
        root = uf.find(idx)
        clusters.setdefault(root, []).append(idx)

    canonical_by_root = {}
    for root, indices in clusters.items():
        refs = [ref_list[i] for i in indices]
        doi_refs = [ref for ref in refs if extract_doi(ref)]
        if doi_refs:
            canonical = doi_refs[0]
        else:
            canonical = max(refs, key=len)
        canonical_by_root[root] = canonical

    cluster_order = sorted(canonical_by_root.items(), key=lambda item: item[1])
    cluster_id_by_root = {root: i + 1 for i, (root, _) in enumerate(cluster_order)}

    rows = []
    for idx, ref in enumerate(ref_list):
        root = uf.find(idx)
        canonical = canonical_by_root[root]
        cluster_id = cluster_id_by_root[root]
        row = mapping_df.loc[mapping_df["raw_reference"] == ref].iloc[0].to_dict()
        row["canonical_reference"] = canonical
        row["cluster_id"] = cluster_id
        if row["reason"] == "identity" and canonical != ref:
            row["reason"] = "manual_needed"
        rows.append(row)

    updated = pd.DataFrame(rows)
    return updated.sort_values("raw_reference").reset_index(drop=True)


def _render_outputs(outputs):
    st.markdown("### Downloads")
    for entry in outputs:
        st.download_button(
            entry["label"],
            data=entry["data"],
            file_name=entry["filename"],
            mime=entry.get("mime", "application/octet-stream"),
            key=entry["key"],
        )


state = _init_state()

with st.expander("Settings"):
    mode = st.selectbox("Mode", options=["Mode A", "Mode B"], index=0, key="bibclean_mode")
    auto_merge_threshold = st.slider(
        "Auto merge threshold",
        min_value=50,
        max_value=100,
        value=95,
        step=1,
    )
    review_threshold = st.slider(
        "Review threshold",
        min_value=50,
        max_value=100,
        value=88,
        step=1,
    )
    max_candidates = st.number_input(
        "Max candidates per ref",
        min_value=5,
        max_value=200,
        value=50,
        step=5,
    )
    structured_override = st.toggle("Structured override", value=True)
    initials_normalization = st.toggle("Initials normalization", value=True)
    verbose = st.toggle("Verbose diagnostics", value=False)
    doc_merge_threshold = st.number_input(
        "Document merge threshold (Mode B)",
        min_value=50,
        max_value=100,
        value=int(bc_config.doc_merge_threshold),
        step=1,
        key="bibclean_doc_merge_threshold",
    )
    journal_match_bonus = st.number_input(
        "Journal match bonus",
        min_value=0,
        max_value=10,
        value=int(bc_config.journal_match_bonus),
        step=1,
        key="bibclean_journal_match_bonus",
    )
    boilerplate_tokens_raw = st.text_input(
        "Boilerplate tokens (comma-separated)",
        value=", ".join(bc_config.boilerplate_tokens),
        key="bibclean_boilerplate_tokens",
    )
    st.button("Start over", on_click=_reset_state, key="bibclean_start_over")

with st.expander("How It Works"):
    st.markdown(
        """
**Overview**
- Upload Scopus CSV or WoS plaintext exports and get clean references that import into bibliometrix/Biblioshiny.
- Mode A cleans references within one dataset.
- Mode B merges documents across datasets (conservatively) then cleans references.

**Controls (what they do)**
- **Mode**: Choose single-file cleaning (Mode A) or multi-file merge + clean (Mode B).
- **Auto merge threshold**: Confidence required to auto-merge references (higher = stricter).
- **Review threshold**: Confidence range for manual review candidates.
- **Max candidates per ref**: Caps comparisons per block for speed.
- **Structured override**: If year + volume + page match, boost confidence (helps physics-style citations).
- **Initials normalization**: Joins initials like `M E J` → `MEJ` to improve matching.
- **Document merge threshold (Mode B)**: Fuzzy match threshold for merging documents.
- **Journal match bonus**: Adds a small confidence bonus when normalized journals match.
- **Boilerplate tokens**: Tokens removed during normalization (e.g., `vol`, `pp`).
- **Verbose diagnostics**: Shows reference mapping table in an expander.

**Outputs**
- **Mode A**: cleaned file + `reference_mapping.csv` + `summary.json` + `review_pairs.csv`.
- **Mode B**: `merged_cleaned.csv` + `document_mapping.csv` + `reference_mapping.csv` + `summary.json` + `review_pairs.csv`.

**Review workflow**
- If `review_pairs.csv` has candidates, use the Review table to mark **Merge** or **Keep separate**.
- Click **Apply review decisions** to update outputs without re-running.
"""
    )


if mode == "Mode A":
    uploaded_file = st.file_uploader(
        "Upload a Scopus CSV or WoS plaintext file",
        type=["csv", "txt"],
        key="bibclean_single_upload",
    )
    uploaded_files = [uploaded_file] if uploaded_file else []
else:
    uploaded_files = st.file_uploader(
        "Upload one or more Scopus/WoS files",
        type=["csv", "txt"],
        accept_multiple_files=True,
        key="bibclean_multi_upload",
    )

run_clicked = st.button("Run cleaning", key="bibclean_run")

if run_clicked:
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    else:
        with st.spinner("Processing..."):
            tmp_paths = []
            for upload in uploaded_files:
                if upload is None:
                    continue
                tmp_paths.append(_write_upload_to_temp(upload))

            overrides = {
                "max_candidates_per_ref": int(max_candidates),
                "doc_merge_threshold": int(doc_merge_threshold),
                "journal_match_bonus": int(journal_match_bonus),
                "boilerplate_tokens": [
                    tok.strip() for tok in boilerplate_tokens_raw.split(",") if tok.strip()
                ],
                "enable_structured_override": structured_override,
                "enable_initials_normalization": initials_normalization,
            }

            with _temp_config(overrides):
                if mode == "Mode A":
                    input_path = tmp_paths[0]
                    fmt = detect_input_format(input_path)

                    if fmt == "scopus_csv":
                        df, ref_col = load_scopus_csv(input_path)
                        raw_refs = extract_scopus_references(df, ref_col)
                        mapping_df, summary, mapping_dict, review_pairs_df = canonicalize_references(
                            raw_refs,
                            auto_merge_threshold=auto_merge_threshold,
                            review_threshold=review_threshold,
                            return_review_pairs=True,
                        )
                        summary["input_format"] = "scopus_csv"
                        summary["document_count"] = len(df)
                        cleaned_df = apply_mapping_to_scopus(df, ref_col, mapping_dict)

                        cleaned_bytes = _df_to_csv_bytes(cleaned_df)
                        cleaned_name = f"{Path(uploaded_files[0].name).stem}_cleaned.csv"
                        outputs = _build_outputs_list(
                            [
                                {
                                    "label": "Download cleaned CSV",
                                    "data": cleaned_bytes,
                                    "filename": cleaned_name,
                                    "mime": "text/csv",
                                    "key": "bibclean_download_cleaned",
                                },
                                {
                                    "label": "Download reference_mapping.csv",
                                    "data": _df_to_csv_bytes(mapping_df),
                                    "filename": "reference_mapping.csv",
                                    "mime": "text/csv",
                                    "key": "bibclean_download_mapping",
                                },
                                {
                                    "label": "Download summary.json",
                                    "data": _json_to_bytes(summary),
                                    "filename": "summary.json",
                                    "mime": "application/json",
                                    "key": "bibclean_download_summary",
                                },
                                {
                                    "label": "Download review_pairs.csv",
                                    "data": _df_to_csv_bytes(review_pairs_df),
                                    "filename": "review_pairs.csv",
                                    "mime": "text/csv",
                                    "key": "bibclean_download_review",
                                },
                            ]
                        )

                        state["artifacts"] = {
                            "mode": "A",
                            "format": "scopus_csv",
                            "df": df,
                            "ref_col": ref_col,
                        }

                    else:
                        wos_file = parse_wos_plaintext(input_path)
                        raw_records = [list(record) for record in wos_file.records]
                        header_lines = list(wos_file.header_lines)
                        raw_refs = extract_wos_references(raw_records)
                        mapping_df, summary, mapping_dict, review_pairs_df = canonicalize_references(
                            raw_refs,
                            auto_merge_threshold=auto_merge_threshold,
                            review_threshold=review_threshold,
                            return_review_pairs=True,
                        )
                        summary["input_format"] = "wos_plaintext"
                        summary["document_count"] = len(raw_records)
                        wos_file_clean = WosFile(
                            header_lines=header_lines,
                            records=apply_mapping_to_wos_records(raw_records, mapping_dict),
                        )

                        cleaned_bytes = _wos_to_bytes(wos_file_clean)
                        cleaned_name = f"{Path(uploaded_files[0].name).stem}_cleaned.txt"
                        outputs = _build_outputs_list(
                            [
                                {
                                    "label": "Download cleaned plaintext",
                                    "data": cleaned_bytes,
                                    "filename": cleaned_name,
                                    "mime": "text/plain",
                                    "key": "bibclean_download_cleaned",
                                },
                                {
                                    "label": "Download reference_mapping.csv",
                                    "data": _df_to_csv_bytes(mapping_df),
                                    "filename": "reference_mapping.csv",
                                    "mime": "text/csv",
                                    "key": "bibclean_download_mapping",
                                },
                                {
                                    "label": "Download summary.json",
                                    "data": _json_to_bytes(summary),
                                    "filename": "summary.json",
                                    "mime": "application/json",
                                    "key": "bibclean_download_summary",
                                },
                                {
                                    "label": "Download review_pairs.csv",
                                    "data": _df_to_csv_bytes(review_pairs_df),
                                    "filename": "review_pairs.csv",
                                    "mime": "text/csv",
                                    "key": "bibclean_download_review",
                                },
                            ]
                        )

                        state["artifacts"] = {
                            "mode": "A",
                            "format": "wos_plaintext",
                            "wos_records": raw_records,
                            "wos_header_lines": header_lines,
                        }

                else:
                    documents = []
                    for path in tmp_paths:
                        fmt = detect_input_format(path)
                        if fmt == "scopus_csv":
                            df, ref_col = load_scopus_csv(path)
                            documents.extend(build_documents_from_scopus(df, ref_col))
                        else:
                            wos_file = parse_wos_plaintext(path)
                            documents.extend(build_documents_from_wos(wos_file.records))

                    canonical_docs, doc_mappings = merge_documents(documents)
                    canonical_ids = {
                        idx: compute_canonical_doc_id(doc)
                        for idx, doc in enumerate(canonical_docs)
                    }

                    doc_rows = []
                    for mapping in doc_mappings:
                        doc_rows.append(
                            {
                                "raw_doc_id": mapping.raw_doc_id,
                                "canonical_doc_id": canonical_ids[mapping.canonical_index],
                                "match_reason": mapping.match_reason,
                                "confidence": mapping.confidence,
                            }
                        )

                    doc_mapping_df = pd.DataFrame(doc_rows)

                    raw_refs = []
                    for doc in canonical_docs:
                        raw_refs.extend(doc.references)

                    mapping_df, summary, mapping_dict, review_pairs_df = canonicalize_references(
                        raw_refs,
                        auto_merge_threshold=auto_merge_threshold,
                        review_threshold=review_threshold,
                        return_review_pairs=True,
                    )
                    summary["document_merge"] = {
                        "doc_merge_threshold": bc_config.doc_merge_threshold,
                        "total_documents": len(documents),
                        "canonical_documents": len(canonical_docs),
                    }

                    merged_rows = []
                    for doc in canonical_docs:
                        mapped_refs = [mapping_dict.get(ref, ref) for ref in doc.references]
                        merged_rows.append(
                            {
                                "Title": doc.title,
                                "Year": doc.year or "",
                                "DOI": doc.doi or "",
                                "Authors": doc.authors,
                                "References": "; ".join(mapped_refs),
                            }
                        )

                    merged_df = pd.DataFrame(merged_rows)
                    outputs = _build_outputs_list(
                        [
                            {
                                "label": "Download merged_cleaned.csv",
                                "data": _df_to_csv_bytes(merged_df),
                                "filename": "merged_cleaned.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_merged",
                            },
                            {
                                "label": "Download document_mapping.csv",
                                "data": _df_to_csv_bytes(doc_mapping_df),
                                "filename": "document_mapping.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_docmap",
                            },
                            {
                                "label": "Download reference_mapping.csv",
                                "data": _df_to_csv_bytes(mapping_df),
                                "filename": "reference_mapping.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_mapping",
                            },
                            {
                                "label": "Download summary.json",
                                "data": _json_to_bytes(summary),
                                "filename": "summary.json",
                                "mime": "application/json",
                                "key": "bibclean_download_summary",
                            },
                            {
                                "label": "Download review_pairs.csv",
                                "data": _df_to_csv_bytes(review_pairs_df),
                                "filename": "review_pairs.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_review",
                            },
                        ]
                    )

                    state["artifacts"] = {
                        "mode": "B",
                        "canonical_docs": canonical_docs,
                        "doc_mapping_df": doc_mapping_df,
                    }

            state["mode"] = mode
            state["outputs"] = {
                "mapping_df": mapping_df,
                "mapping_dict": mapping_dict,
                "summary": summary,
                "review_pairs_df": review_pairs_df,
                "download_entries": outputs,
            }
            state["review_df"] = None
            state["stage"] = "processed"


if state["stage"] in {"processed", "reviewed"}:
    summary = state["outputs"]["summary"]
    st.markdown("### Summary")
    metrics = [
        ("Total refs", summary.get("total_reference_instances", 0)),
        ("Unique refs", summary.get("unique_reference_count", 0)),
        ("Clusters", summary.get("clusters", 0)),
        ("Auto-merged", summary.get("auto_merged_clusters", 0)),
        ("Manual review", summary.get("manual_review_count", 0)),
        ("Review pairs", summary.get("review_pair_count", 0)),
    ]
    cols = st.columns(3)
    for idx, (label, value) in enumerate(metrics):
        cols[idx % 3].metric(label, value)

    with st.expander("Summary JSON"):
        st.json(summary)

    if verbose:
        with st.expander("Reference mapping"):
            st.dataframe(state["outputs"]["mapping_df"], use_container_width=True)

    review_pairs_df = state["outputs"]["review_pairs_df"]
    if review_pairs_df is not None and not review_pairs_df.empty:
        st.markdown("### Review candidates")
        if state["review_df"] is None:
            review_df = review_pairs_df.copy()
            review_df["decision"] = "Not sure"
            state["review_df"] = review_df
        else:
            review_df = state["review_df"]

        edited = st.data_editor(
            review_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "decision": st.column_config.SelectboxColumn(
                    "Decision",
                    options=["Merge", "Keep separate", "Not sure"],
                    required=True,
                )
            },
            key="bibclean_review_editor",
        )
        state["review_df"] = edited

        if st.button("Apply review decisions", key="bibclean_apply_review"):
            updated_mapping = _apply_review_merges(state["outputs"]["mapping_df"], edited)
            mapping_dict = dict(
                zip(
                    updated_mapping["raw_reference"],
                    updated_mapping["canonical_reference"],
                )
            )

            artifacts = state["artifacts"]
            outputs = []
            if artifacts.get("mode") == "A":
                if artifacts.get("format") == "scopus_csv":
                    df = artifacts["df"]
                    ref_col = artifacts["ref_col"]
                    cleaned_df = apply_mapping_to_scopus(df, ref_col, mapping_dict)
                    outputs = _build_outputs_list(
                        [
                            {
                                "label": "Download cleaned CSV",
                                "data": _df_to_csv_bytes(cleaned_df),
                                "filename": "cleaned.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_cleaned_review",
                            },
                            {
                                "label": "Download reference_mapping.csv",
                                "data": _df_to_csv_bytes(updated_mapping),
                                "filename": "reference_mapping.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_mapping_review",
                            },
                            {
                                "label": "Download summary.json",
                                "data": _json_to_bytes(summary),
                                "filename": "summary.json",
                                "mime": "application/json",
                                "key": "bibclean_download_summary_review",
                            },
                        ]
                    )
                else:
                    raw_records = artifacts["wos_records"]
                    header_lines = artifacts.get("wos_header_lines", [])
                    wos_file_clean = WosFile(
                        header_lines=header_lines,
                        records=apply_mapping_to_wos_records(raw_records, mapping_dict),
                    )
                    outputs = _build_outputs_list(
                        [
                            {
                                "label": "Download cleaned plaintext",
                                "data": _wos_to_bytes(wos_file_clean),
                                "filename": "cleaned.txt",
                                "mime": "text/plain",
                                "key": "bibclean_download_cleaned_review",
                            },
                            {
                                "label": "Download reference_mapping.csv",
                                "data": _df_to_csv_bytes(updated_mapping),
                                "filename": "reference_mapping.csv",
                                "mime": "text/csv",
                                "key": "bibclean_download_mapping_review",
                            },
                            {
                                "label": "Download summary.json",
                                "data": _json_to_bytes(summary),
                                "filename": "summary.json",
                                "mime": "application/json",
                                "key": "bibclean_download_summary_review",
                            },
                        ]
                    )
            else:
                canonical_docs = artifacts["canonical_docs"]
                doc_mapping_df = artifacts["doc_mapping_df"]
                merged_rows = []
                for doc in canonical_docs:
                    mapped_refs = [mapping_dict.get(ref, ref) for ref in doc.references]
                    merged_rows.append(
                        {
                            "Title": doc.title,
                            "Year": doc.year or "",
                            "DOI": doc.doi or "",
                            "Authors": doc.authors,
                            "References": "; ".join(mapped_refs),
                        }
                    )
                merged_df = pd.DataFrame(merged_rows)
                outputs = _build_outputs_list(
                    [
                        {
                            "label": "Download merged_cleaned.csv",
                            "data": _df_to_csv_bytes(merged_df),
                            "filename": "merged_cleaned.csv",
                            "mime": "text/csv",
                            "key": "bibclean_download_merged_review",
                        },
                        {
                            "label": "Download document_mapping.csv",
                            "data": _df_to_csv_bytes(doc_mapping_df),
                            "filename": "document_mapping.csv",
                            "mime": "text/csv",
                            "key": "bibclean_download_docmap_review",
                        },
                        {
                            "label": "Download reference_mapping.csv",
                            "data": _df_to_csv_bytes(updated_mapping),
                            "filename": "reference_mapping.csv",
                            "mime": "text/csv",
                            "key": "bibclean_download_mapping_review",
                        },
                        {
                            "label": "Download summary.json",
                            "data": _json_to_bytes(summary),
                            "filename": "summary.json",
                            "mime": "application/json",
                            "key": "bibclean_download_summary_review",
                        },
                    ]
                )

            state["outputs"]["mapping_df"] = updated_mapping
            state["outputs"]["mapping_dict"] = mapping_dict
            state["outputs"]["download_entries"] = outputs
            state["review_df"] = edited
            state["stage"] = "reviewed"
            st.success("Review decisions applied.")

    _render_outputs(state["outputs"]["download_entries"])
