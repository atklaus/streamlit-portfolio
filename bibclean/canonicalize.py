from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import pandas as pd

from bibclean import config
from bibclean.match.blocking import build_block_key
from bibclean.match.cluster import build_clusters
from bibclean.match.scoring import score_pair
from bibclean.models import Reference
from bibclean.normalize.parse import extract_doi, extract_first_author, extract_year
from bibclean.normalize.text import normalize_text


def _build_reference(raw: str) -> Reference:
    norm = normalize_text(raw)
    doi = extract_doi(raw)
    year = extract_year(raw)
    first_author = extract_first_author(raw)
    temp = Reference(raw=raw, norm=norm, doi=doi, year=year, first_author=first_author, block_key="")
    block_key = build_block_key(temp)
    return Reference(
        raw=raw,
        norm=norm,
        doi=doi,
        year=year,
        first_author=first_author,
        block_key=block_key,
    )


def canonicalize_references(
    raw_references: Iterable[str],
) -> Tuple[pd.DataFrame, Dict, Dict[str, str]]:
    raw_list = [r.strip() for r in raw_references if r and str(r).strip()]
    if not raw_list:
        mapping_df = pd.DataFrame(
            columns=[
                "raw_reference",
                "canonical_reference",
                "cluster_id",
                "confidence",
                "reason",
            ]
        )
        summary = {
            "total_reference_instances": 0,
            "unique_reference_count": 0,
            "clusters": 0,
            "auto_merged_clusters": 0,
            "manual_review_count": 0,
            "thresholds": {
                "auto_merge_threshold": config.auto_merge_threshold,
                "review_threshold": config.review_threshold,
                "max_candidates_per_ref": config.max_candidates_per_ref,
            },
        }
        return mapping_df, summary, {}
    unique_raws = sorted(set(raw_list))

    refs: List[Reference] = [_build_reference(raw) for raw in unique_raws]
    index_by_raw = {ref.raw: idx for idx, ref in enumerate(refs)}

    blocks: Dict[str, List[int]] = {}
    for idx, ref in enumerate(refs):
        blocks.setdefault(ref.block_key, []).append(idx)

    edges: List[Tuple[int, int, int]] = []
    best_score: Dict[int, int] = {idx: 0 for idx in range(len(refs))}
    doi_match: Dict[int, bool] = {idx: False for idx in range(len(refs))}
    edge_confidence: Dict[int, int] = {idx: 0 for idx in range(len(refs))}

    for indices in blocks.values():
        indices.sort(key=lambda i: refs[i].raw)
        for offset, i in enumerate(indices):
            compare_to = indices[offset + 1 : offset + 1 + config.max_candidates_per_ref]
            for j in compare_to:
                confidence, reason = score_pair(refs[i], refs[j])
                if confidence > best_score[i]:
                    best_score[i] = confidence
                if confidence > best_score[j]:
                    best_score[j] = confidence
                if reason == "doi_exact":
                    doi_match[i] = True
                    doi_match[j] = True
                if confidence >= config.auto_merge_threshold:
                    edges.append((i, j, confidence))
                    if confidence > edge_confidence[i]:
                        edge_confidence[i] = confidence
                    if confidence > edge_confidence[j]:
                        edge_confidence[j] = confidence

    clusters, canonical_by_root = build_clusters(refs, edges)

    root_by_index: Dict[int, int] = {}
    for root, indices in clusters.items():
        for idx in indices:
            root_by_index[idx] = root

    cluster_order = []
    for root, canonical_idx in canonical_by_root.items():
        cluster_order.append((refs[canonical_idx].raw, root))
    cluster_order.sort(key=lambda item: item[0])

    cluster_id_by_root = {root: i + 1 for i, (_, root) in enumerate(cluster_order)}

    rows = []
    manual_needed_count = 0
    auto_merged_clusters = 0

    for root, indices in clusters.items():
        if len(indices) > 1:
            auto_merged_clusters += 1

    for idx, ref in enumerate(refs):
        root = root_by_index[idx]
        cluster_id = cluster_id_by_root[root]
        cluster_size = len(clusters[root])
        canonical_ref = refs[canonical_by_root[root]].raw

        if cluster_size > 1:
            reason = "doi_exact" if doi_match[idx] else "fuzzy_high"
            confidence = 100 if doi_match[idx] else edge_confidence[idx]
            canonical_reference = canonical_ref
        else:
            confidence = best_score[idx]
            if confidence >= config.review_threshold:
                reason = "manual_needed"
                manual_needed_count += 1
            else:
                reason = "identity"
            canonical_reference = ref.raw

        rows.append(
            {
                "raw_reference": ref.raw,
                "canonical_reference": canonical_reference,
                "cluster_id": cluster_id,
                "confidence": confidence,
                "reason": reason,
            }
        )

    mapping_df = pd.DataFrame(rows)
    mapping_df = mapping_df.sort_values("raw_reference").reset_index(drop=True)

    mapping_dict = {
        row["raw_reference"]: row["canonical_reference"]
        for row in mapping_df.to_dict(orient="records")
    }

    summary = {
        "total_reference_instances": len(raw_list),
        "unique_reference_count": len(refs),
        "clusters": len(clusters),
        "auto_merged_clusters": auto_merged_clusters,
        "manual_review_count": manual_needed_count,
        "thresholds": {
            "auto_merge_threshold": config.auto_merge_threshold,
            "review_threshold": config.review_threshold,
            "max_candidates_per_ref": config.max_candidates_per_ref,
        },
    }

    return mapping_df, summary, mapping_dict
