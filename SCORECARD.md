# Portfolio Readiness Scorecard

Scale: 0-5 per criterion. Total out of 40.

## A) First-impression clarity - 5/5
Evidence:
- `README.md` overview + quickstart + repo map
- `pages/0_home.py` headline and flagship/labs grouping
- Flagship visuals and links in `README.md`

## B) Cohesive story - 5/5
Evidence:
- `docs/PORTFOLIO.md` portfolio narrative and flagship highlights
- `app/config.py` tiers and tags used to separate flagship vs labs
- Project-level architecture diagrams in flagship READMEs

## C) UX polish - 4/5
Evidence:
- `app/ui/cards.py` card CSS, responsive grid, focus states
- `.streamlit/config.toml` theme configuration
 - `app/layout/header.py` header strip now includes page title
Gaps:
- Some pages rely on default Streamlit styling without shared typography/layout

## D) Project depth - 3/5
Evidence:
- `projects/bibclean/` pipeline modules + `projects/bibclean/tests/`
- `pages/2_wnba_success.py` live scraping and model inference pipeline
Gaps:
- Several projects are lightweight labs rather than production-grade pipelines

## E) Reproducibility - 5/5
Evidence:
- `README.md` quickstart and Docker workflow
- `Dockerfile` containerized runtime
- `.env.example` for local secrets
- Offline fixtures for WNBA in `projects/wnba_success/fixtures/`

## F) Code quality - 3/5
Evidence:
- Clear project separation in `projects/`
- Shared utilities in `shared/` and `app/`
Gaps:
- Limited type hints and some large Streamlit pages with mixed concerns

## G) Data engineering signal - 4/5
Evidence:
- `projects/bibclean/` normalization, blocking, clustering
- `shared/cloud_functions.py` and `pages/7_analytics.py` for storage-backed analytics
 - WNBA offline fixtures and fallback logic in `pages/2_wnba_success.py`
Gaps:
- Limited examples of incremental refresh, storage formats, or orchestration

## H) Public GitHub polish - 5/5
Evidence:
- Root and per-project READMEs, plus `docs/PORTFOLIO.md`
- Basic CI workflow (see `.github/workflows/ci.yml`)
- Visuals and Mermaid diagrams for flagship projects

## Total: 34/40

## Changelog (2026-02-13)
- Added flagship screenshots in `static/images/*` and embedded them in `README.md` and `docs/PORTFOLIO.md`.
- Added Mermaid architecture diagrams to flagship project READMEs.
- Implemented offline fixture mode for WNBA predictions (`projects/wnba_success/fixtures/` + `pages/2_wnba_success.py`).
- Polished navigation header to show page title and reinforced card click styling.
