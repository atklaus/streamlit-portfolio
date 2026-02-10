import csv
import os
from typing import Literal


def detect_input_format(path: str) -> Literal["scopus_csv", "wos_plaintext"]:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".csv":
        try:
            with open(path, "r", newline="", errors="ignore") as f:
                reader = csv.reader(f)
                header = next(reader, [])
            if len(header) == 1 and "," in header[0]:
                header = next(csv.reader([header[0]]))
            if any(col.strip().lower() == "references" for col in header):
                return "scopus_csv"
        except Exception:
            pass

    first_non_empty = ""
    has_er_tag = False
    try:
        with open(path, "r", errors="ignore") as f:
            for line in f:
                if not first_non_empty and line.strip():
                    first_non_empty = line.strip()
                if line.strip() == "ER":
                    has_er_tag = True
                if first_non_empty and has_er_tag:
                    break
    except Exception:
        pass

    if first_non_empty.startswith("FN ") and "Web of Science" in first_non_empty:
        return "wos_plaintext"
    if has_er_tag:
        return "wos_plaintext"

    raise ValueError(f"Unable to detect input format for {path}")
