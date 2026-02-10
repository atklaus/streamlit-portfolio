from streamlit.components.v1 import html
import streamlit as st
import base64
from pathlib import Path
import re
from streamlit.errors import StreamlitAPIException

def switch_page(page_name: str):
    def standardize_name(name: str) -> str:
        return name.strip().lower().replace("_", " ")

    page_name = standardize_name(page_name)

    root_dir = Path(__file__).resolve().parent.parent

    if page_name in {"", "home"}:
        home_page = root_dir / "pages" / "0_home.py"
        if not home_page.exists():
            raise FileNotFoundError(f"Home page not found: {home_page}")
        st.switch_page("pages/0_home.py")
        return

    pages_dir = root_dir / "pages"
    if not pages_dir.exists():
        raise FileNotFoundError(f"Pages directory not found: {pages_dir}")

    page_names = []
    for path in pages_dir.glob("*.py"):
        slug = re.sub(r"^\d+_", "", path.stem)
        page_names.append(standardize_name(slug))
        if standardize_name(slug) == page_name:
            st.switch_page(f"pages/{path.name}")
            return

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def V_SPACE(lines):
    for _ in range(lines):
        st.write('&nbsp;')
