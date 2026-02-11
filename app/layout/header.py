import re
from pathlib import Path

import streamlit as st

from .. import config as c

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
    padding_top: float = 0.25,
    padding_right: int = 10,
    padding_left: int = 1,
    padding_bottom: float = 0.25,
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
    repo_root = Path(__file__).resolve().parents[2]
    pages_dir = repo_root / "pages"
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
    with st.sidebar:
        if st.button("Home", use_container_width=True, type="secondary"):
            st.switch_page("pages/0_home.py")

def _hide_streamlit_sidebar_nav():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, page_name, container_style=True):
    st.set_page_config(
        page_title=title,
        page_icon="static/images/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _hide_streamlit_sidebar_nav()
    render_sidebar_nav()
    if container_style:
        set_page_container_style(padding_top=0.25, padding_bottom=0.25, apply=True)

    github_profile_url = "https://github.com/atklaus"
    linkedin_profile_url = "https://linkedin.com/in/adam-klaus"
    navbar_html = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <div style="background-color: #316b62; padding: 10px; border-radius: 10px; display: flex; justify-content: space-around; flex-wrap: wrap; margin: 0.25rem 0 0.75rem 0;">
        <a href="/"><i class="fas fa-home" style="font-size:24px; color: white;"></i></a>
        <a href="{github_profile_url}"><i class="fas fa-code" style="font-size:24px; color: white;"></i></a>
        <a href="{linkedin_profile_url}"><i class="fab fa-linkedin" style="font-size:24px; color: white;"></i></a>
    </div>
    """

    st.markdown(navbar_html, unsafe_allow_html=True)
