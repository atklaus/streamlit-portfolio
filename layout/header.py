import re
from pathlib import Path

import streamlit as st

import config as c

BACKGROUND_COLOR = "white"
COLOR = "black"

# hide_streamlit_style = """
#                 <style>
#                 div[data-testid="stToolbar"] {
#                 visibility: hidden;
#                 height: 0%;
#                 position: fixed;
#                 }
#                 div[data-testid="stDecoration"] {
#                 visibility: hidden;
#                 height: 0%;
#                 position: fixed;
#                 }
#                 div[data-testid="stStatusWidget"] {
#                 visibility: hidden;
#                 height: 0%;
#                 position: fixed;
#                 }
#                 #MainMenu {
#                 visibility: hidden;
#                 height: 0%;
#                 }
#                 header {
#                 visibility: hidden;
#                 height: 0%;
#                 }
#                 footer {
#                 visibility: hidden;
#                 height: 0%;
#                 }
#                 </style>
#                 """


def set_page_container_style(
    max_width: int = 1100,
    max_width_100_percent: bool = False,
    padding_top: int = 0,
    padding_right: int = 10,
    padding_left: int = 1,
    padding_bottom: int = 0.1,
    color: str = COLOR,
    background_color: str = BACKGROUND_COLOR,
    apply: bool = True,
):
    if max_width_100_percent:
        max_width_str = "max-width: 100%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    css = f"""
        <style>
        .appview-container .main .block-container{{
                padding-top: {padding_top}rem !important;
                padding-bottom: {padding_bottom}rem !important;
                padding-left: {padding_left}rem !important;
                padding-right: {padding_right}rem !important;
                {max_width_str}
                }}
        </style>
        """
    if apply:
        st.markdown(css, unsafe_allow_html=True)
    return css


def _standardize_name(name: str) -> str:
    return name.strip().lower().replace("_", " ")


def _page_index():
    pages_dir = Path(__file__).resolve().parent.parent / "pages"
    index = {}
    if pages_dir.exists():
        for path in pages_dir.glob("*.py"):
            slug = re.sub(r"^\d+_", "", path.stem)
            index[_standardize_name(slug)] = f"pages/{path.name}"
    index["home"] = "pages/0_home.py"
    return index


def get_page_path(name: str) -> str:
    index = _page_index()
    return index.get(_standardize_name(name), index["home"])


def render_sidebar_nav():
    page_index = _page_index()
    with st.sidebar:
        st.write("## Almost Data Science")
        for module_key, module_values in c.MOD_ACCESS.items():
            raw_name = module_values.get("name", module_key)
            slug = _standardize_name(raw_name)
            if slug in {"", "home"}:
                target = page_index["home"]
            else:
                target = page_index.get(slug)
            if not target:
                continue
            st.page_link(target, label=module_values["button"] or "Home")


def page_header(title, page_name, container_style=True):
    st.set_page_config(
        page_title=title,
        page_icon="static/images/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    render_sidebar_nav()
    if container_style:
        set_page_container_style(padding_top=0, apply=True)
