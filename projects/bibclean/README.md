# bibclean

Tools for canonicalizing cited references from Scopus or Web of Science so they import cleanly into bibliometrix/Biblioshiny.

**Structure**
- `apply/` — apply canonical mappings to raw exports
- `io/` — parsers + writers for Scopus/WoS
- `match/` — blocking, scoring, clustering logic
- `normalize/` — parsing + normalization helpers
- `fixtures/` — small sample files and demo outputs
- `tests/` — pytest coverage for core flows

**Usage**
- Streamlit page: `pages/8_bibliometrix_reference_cleaner.py`
- CLI (optional): `python -m projects.bibclean.cli --help`
- Tests: `pytest projects/bibclean/tests`
