"""Configuration constants for bibclean.

Keep values here hardcoded for now; Streamlit can later surface them.
"""

auto_merge_threshold = 95
review_threshold = 88
max_candidates_per_ref = 50

doc_merge_threshold = 95

# Journal abbreviations to normalize (lowercase keys)
journal_abbrev_map = {
    "j informetr": "journal of informetrics",
    "nat commun": "nature communications",
}

# Boilerplate tokens to drop during normalization
boilerplate_tokens = [
    "vol",
    "no",
    "pp",
    "p",
    "v",
    "issue",
    "iss",
]

# Output file name suffixes
scopus_clean_suffix = "_cleaned.csv"
wos_clean_suffix = "_cleaned.txt"
merged_scopus_filename = "merged_scopus.csv"
reference_mapping_filename = "reference_mapping.csv"
summary_filename = "summary.json"
document_mapping_filename = "document_mapping.csv"
