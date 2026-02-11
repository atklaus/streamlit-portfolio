# Streamlit Portfolio

This repo is one Streamlit shell plus multiple self-contained projects/tools.

**Run Locally**
1. Install dependencies: `poetry install`
2. Start the app: `poetry run streamlit run app.py`

**Structure**
- `app/` — Streamlit shell config, layout helpers, shared UI utilities.
- `pages/` — Streamlit multipage entry points (kept at repo root for Streamlit's built-in routing).
- `projects/` — Self-contained projects/tools (code, assets, fixtures, tests).
- `shared/` — Non-UI utilities used across projects.
- `static/` — Site-wide assets (logos, resume, icons).
- `scripts/` — One-off/dev scripts.

**Add A New Project**
1. Create a folder under `projects/<your_project>/`.
2. Put code in that folder and expose the public API in `projects/<your_project>/__init__.py`.
3. Add any project assets in subfolders like `assets/`, `model/`, `fixtures/`, `tests/`.
4. Add a new Streamlit page in `pages/` named like `N_<slug>.py`.
5. Register the page in `app/config.py` under `MOD_ACCESS`.

See `projects/README.md` for per-project conventions.
