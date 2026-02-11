from __future__ import annotations

import argparse
import json
import logging
import os
from typing import List

import pandas as pd

from . import config
from .apply.scopus_apply import apply_mapping_to_scopus
from .apply.wos_apply import apply_mapping_to_wos_records
from .canonicalize import canonicalize_references
from .io.detect import detect_input_format
from .io.scopus_csv import (
    build_documents_from_scopus,
    extract_scopus_references,
    load_scopus_csv,
)
from .io.wos_plaintext import (
    build_documents_from_wos,
    extract_wos_references,
    parse_wos_plaintext,
    write_wos_plaintext,
)
from .merge import compute_canonical_doc_id, merge_documents
from .utils import ensure_dir


logger = logging.getLogger("bibclean")


def _setup_logging(verbose: bool) -> None:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")


def _write_summary(output_dir: str, summary: dict) -> None:
    path = os.path.join(output_dir, config.summary_filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def _write_reference_mapping(output_dir: str, mapping_df: pd.DataFrame) -> None:
    path = os.path.join(output_dir, config.reference_mapping_filename)
    mapping_df.to_csv(path, index=False)


def _write_review_pairs(output_dir: str, review_pairs_df: pd.DataFrame) -> None:
    if review_pairs_df.empty:
        return
    path = os.path.join(output_dir, config.review_pairs_filename)
    review_pairs_df.to_csv(path, index=False)


def _mode_a(input_path: str, output_dir: str) -> None:
    fmt = detect_input_format(input_path)
    logger.info("Detected format: %s", fmt)

    if fmt == "scopus_csv":
        df, ref_col = load_scopus_csv(input_path)
        raw_refs = extract_scopus_references(df, ref_col)
        mapping_df, summary, mapping_dict, review_pairs_df = canonicalize_references(
            raw_refs,
            return_review_pairs=True,
        )
        summary["input_format"] = "scopus_csv"
        summary["document_count"] = len(df)
        cleaned_df = apply_mapping_to_scopus(df, ref_col, mapping_dict)

        output_name = os.path.splitext(os.path.basename(input_path))[0]
        cleaned_path = os.path.join(output_dir, output_name + config.scopus_clean_suffix)
        cleaned_df.to_csv(cleaned_path, index=False)

        _write_reference_mapping(output_dir, mapping_df)
        _write_review_pairs(output_dir, review_pairs_df)
        _write_summary(output_dir, summary)
        logger.info("Wrote cleaned Scopus CSV to %s", cleaned_path)
        return

    if fmt == "wos_plaintext":
        wos_file = parse_wos_plaintext(input_path)
        raw_refs = extract_wos_references(wos_file.records)
        mapping_df, summary, mapping_dict, review_pairs_df = canonicalize_references(
            raw_refs,
            return_review_pairs=True,
        )
        summary["input_format"] = "wos_plaintext"
        summary["document_count"] = len(wos_file.records)
        updated_records = apply_mapping_to_wos_records(wos_file.records, mapping_dict)
        wos_file.records = updated_records

        output_name = os.path.splitext(os.path.basename(input_path))[0]
        cleaned_path = os.path.join(output_dir, output_name + config.wos_clean_suffix)
        write_wos_plaintext(cleaned_path, wos_file)

        _write_reference_mapping(output_dir, mapping_df)
        _write_review_pairs(output_dir, review_pairs_df)
        _write_summary(output_dir, summary)
        logger.info("Wrote cleaned WoS plaintext to %s", cleaned_path)
        return

    raise ValueError(f"Unsupported input format: {fmt}")


def _mode_b(input_paths: List[str], output_dir: str) -> None:
    documents = []
    for path in input_paths:
        fmt = detect_input_format(path)
        logger.info("Detected format %s for %s", fmt, path)
        if fmt == "scopus_csv":
            df, ref_col = load_scopus_csv(path)
            documents.extend(build_documents_from_scopus(df, ref_col))
        elif fmt == "wos_plaintext":
            wos_file = parse_wos_plaintext(path)
            documents.extend(build_documents_from_wos(wos_file.records))
        else:
            raise ValueError(f"Unsupported input format: {fmt}")

    canonical_docs, doc_mappings = merge_documents(documents)
    canonical_ids = {idx: compute_canonical_doc_id(doc) for idx, doc in enumerate(canonical_docs)}

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
    doc_mapping_path = os.path.join(output_dir, config.document_mapping_filename)
    doc_mapping_df.to_csv(doc_mapping_path, index=False)

    raw_refs = []
    for doc in canonical_docs:
        raw_refs.extend(doc.references)

    mapping_df, summary, mapping_dict, review_pairs_df = canonicalize_references(
        raw_refs,
        auto_merge_threshold=config.merged_auto_merge_threshold,
        return_review_pairs=True,
    )
    summary["document_merge"] = {
        "doc_merge_threshold": config.doc_merge_threshold,
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
    merged_path = os.path.join(output_dir, config.merged_scopus_filename)
    merged_df.to_csv(merged_path, index=False)

    _write_reference_mapping(output_dir, mapping_df)
    _write_review_pairs(output_dir, review_pairs_df)
    _write_summary(output_dir, summary)

    logger.info("Wrote merged CSV to %s", merged_path)
    logger.info("Wrote document mapping to %s", doc_mapping_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Canonicalize cited references for bibliometrix.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    subparsers = parser.add_subparsers(dest="mode", required=True)

    mode_a = subparsers.add_parser("mode-a", help="Clean references within one dataset")
    mode_a.add_argument("--input", required=True, help="Input file path")
    mode_a.add_argument("--output-dir", required=True, help="Output directory")

    mode_b = subparsers.add_parser("mode-b", help="Merge datasets then clean references")
    mode_b.add_argument("--inputs", nargs="+", required=True, help="Input file paths")
    mode_b.add_argument("--output-dir", required=True, help="Output directory")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    _setup_logging(args.verbose)
    ensure_dir(args.output_dir)

    if args.mode == "mode-a":
        _mode_a(args.input, args.output_dir)
    elif args.mode == "mode-b":
        _mode_b(args.inputs, args.output_dir)
    else:
        parser.error(f"Unknown mode {args.mode}")


if __name__ == "__main__":
    main()
