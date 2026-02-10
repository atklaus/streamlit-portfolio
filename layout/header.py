import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path
import re
from streamlit.errors import StreamlitAPIException
import config as c
import base64
import textwrap
from lib.cloud_functions import CloudFunctions as CF
import extra_streamlit_components as stx
import uuid
import random
import string


cf = CF(bucket='analytics')

BACKGROUND_COLOR = 'white'
COLOR = 'black'

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
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 0, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = .1,
        color: str = COLOR, background_color: str = BACKGROUND_COLOR,
        apply: bool = True,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        css = f'''
            <style>
            .appview-container .main .block-container{{
                    padding-top: {padding_top}rem !important;    
                    padding-bottom: {padding_bottom}rem !important;                        
                    padding-left: {padding_left}rem !important;
                    padding-right: {padding_right}rem !important;
                    }}
            </style>
            '''
        if apply:
            st.markdown(css, unsafe_allow_html=True)
        return css

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



def get_sidebar():
    with st.sidebar:
        st.write('## ' + 'Almost Data Science')
        for module_key, module_values in c.MOD_ACCESS.items():
            if module_key == "home":  # Special case for the home button
                if st.button("Home"):
                    switch_page("Home")
            else:
                if st.button(module_values['button']):
                    switch_page(module_values['name'])


def navigate_to_link(link):
    # Your condition to decide when to navigate
        link_url = "https://www.linkedin.com/in/adam-klaus/"  # Replace with your desired URL
        st.write(f'<meta http-equiv="refresh" content="0; URL={link_url}" />', unsafe_allow_html=True)


def page_header(title, page_name, container_style=True):


    st.set_page_config(
        page_title=title,
        page_icon="static/images/favicon.ico",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    logo_path = "static/images/ads_logo.png"
    # logo_base64 = get_image_base64(logo_path)


    tags = f"""<head>
    <!-- Other existing tags -->
    <meta property="og:title" content="Almost Data Science" />
    <meta property="og:description" content="Portfolio Website by Adam Klaus" />
    <meta property="og:image" content="{logo_path}" />
    </head>"""

    no_sidebar_style = ""
    # cf.store_session(prefix='activity/{}.json.gz',page_name=page_name)


    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden; height: 0 !important; padding: 0 !important; margin: 0 !important;}
    div[data-testid="stFooter"] {display: none !important; height: 0 !important; padding: 0 !important; margin: 0 !important;}
    .stApp > footer {display: none !important; height: 0 !important; padding: 0 !important; margin: 0 !important;}
    header {visibility: visible; height: auto; padding: 0; margin: 0;}
    div[data-testid="stHeader"] {height: auto !important; min-height: 2.5rem !important;}
    div[data-testid="stToolbar"] {visibility: visible; height: auto !important; padding: 0.25rem !important;}
    .stAppViewContainer {padding-top: 0 !important;}
    .appview-container .main .block-container {margin-top: 0 !important; padding-top: 0 !important;}
    .block-container > div:first-child {margin-top: 0 !important; padding-top: 0 !important;}
    .stElementContainer:first-child {margin-top: 0 !important;}
    .element-container:first-child {margin-top: 0 !important;}
    .stApp > header {height: 0 !important;}
    .stApp {margin-top: 0 !important; padding-top: 0 !important;}
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    div[data-testid="stSidebarNav"] {display: block !important;}
    button[data-testid="collapsedControl"] {display: flex !important;}
    </style>
    """
    container_style_css = set_page_container_style(padding_top=0, apply=False) if container_style else ""
    get_sidebar()

    overflow_anchor_style = """
    <style>
    * {
        overflow-anchor: none !important;
    }
    </style>
    """

    # Replace the following URLs with your actual GitHub and LinkedIn URLs
    github_profile_url = "https://github.com/atklaus"
    linkedin_profile_url = "https://linkedin.com/in/adam-klaus"
    navbar_html = f"""
    <div style="background-color: #316b62; padding: 10px; border-radius: 10px; display: flex; justify-content: space-around; flex-wrap: wrap;">
        <a href="https://www.almostdatascience.com/"><i class="fas fa-home" style="font-size:24px; color: white;"></i></a>
        <a href="https://www.almostdatascience.com/"><i class="fas fa-star" style="font-size:24px; color: white;"></i></a>
        <a href="https://www.almostdatascience.com/"><i class="fas fa-info-circle" style="font-size:24px; color: white;"></i></a>
        <a href="{github_profile_url}"><i class="fas fa-code" style="font-size:24px; color: white;"></i></a>
        <a href="{linkedin_profile_url}"><i class="fab fa-linkedin" style="font-size:24px; color: white;"></i></a>
    </div>
    """

    font_awesome = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">'

    def _clean_html(text: str) -> str:
        return textwrap.dedent(text).strip()

    combined = "\n".join(
        [
            _clean_html(tags),
            _clean_html(no_sidebar_style),
            _clean_html(hide_streamlit_style),
            _clean_html(container_style_css) if container_style_css else "",
            _clean_html(overflow_anchor_style),
            _clean_html(font_awesome),
            _clean_html(navbar_html),
        ]
    )

    st.markdown(combined, unsafe_allow_html=True)
