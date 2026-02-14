# DataEngBuilds - Data Engineering Portfolio

DataEngBuilds is my Streamlit portfolio for end-to-end data engineering work. Start at the app homepage to explore featured projects and their production-style pipelines.

## Featured

### Predicting WNBA Success
Predict WNBA success from NCAA stats with live scraping and a cached model.
- Data: live scrape from sports-reference.com
- ML: classification with feature scaling and imputation
- Engineering: offline fixture mode and cached artifacts
Links: `pages/2_wnba_success.py` (open in app) | `projects/wnba_success/README.md` (project details)

### Landscape Image Prediction
Classify landscapes from user uploads using a tiled CNN inference pipeline.
- Data: user-uploaded images
- ML: CNN inference with tile aggregation
- Engineering: model artifacts packaged in repo
Links: `pages/1_landscape_img.py` (open in app) | `projects/landscape_img/README.md` (project details)

### Bibliometrix Reference Cleaner
Clean and canonicalize Scopus or WoS references for bibliometrix/Biblioshiny.
- Data: Scopus CSV and WoS plaintext exports
- ML: fuzzy matching and clustering
- Engineering: deterministic normalization with tests
Links: `pages/8_bibliometrix_reference_cleaner.py` (open in app) | `projects/bibclean/README.md` (project details)

## Other fun projects
- Random Ellipses: Monte Carlo overlap estimator. `projects/ellipses/README.md`
- Game of Life: Conway simulation visualizer. `projects/game_of_life/README.md`
- Happy Prime: happy number and prime check. `projects/happy_prime/README.md`

## Quickstart
**Poetry**: `poetry install` then `poetry run streamlit run app.py`
**Docker**: `docker build -t dataengbuilds .` then `docker run -p 8501:8501 --env-file .env dataengbuilds`

## Architecture (High Level)
User -> Streamlit UI (`app.py`, `pages/*`) -> project modules (`projects/*`) -> data sources and model artifacts.
Optional storage and analytics use DigitalOcean Spaces. More detail in `docs/PORTFOLIO.md`.

## Repo Map
- `app.py` - Streamlit entrypoint
- `app/` - shell config and shared UI
- `pages/` - multipage Streamlit routes
- `projects/` - project code and artifacts
- `shared/` - utilities and services
- `static/` - assets
- `docs/` - portfolio narrative

## Telemetry Logging
Logs are JSONL events and Parquet session snapshots for DuckDB analysis.
Default paths: `data/logs/` (local) or `/app/data/logs` (Docker).
Admin page: `pages/9_telemetry_admin.py`.

## Tests
Run: `poetry run pytest projects/bibclean/tests` and `python -m compileall app pages projects shared`.
