import pandas as pd

from bibclean.io.scopus_csv import split_scopus_references


def apply_mapping_to_scopus(
    df: pd.DataFrame, ref_col: str, mapping: dict[str, str]
) -> pd.DataFrame:
    df_out = df.copy()

    def _map(value: str) -> str:
        refs = split_scopus_references(value)
        mapped = [mapping.get(ref, ref) for ref in refs]
        return "; ".join(mapped)

    df_out[ref_col] = df_out[ref_col].fillna("").apply(_map)
    return df_out
