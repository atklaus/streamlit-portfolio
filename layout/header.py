import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
import config as c
import base64
from lib.cloud_functions import CloudFunctions as CF
import extra_streamlit_components as stx
import uuid
import random
import string
import bcrypt


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
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = .1,
        color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
            .appview-container .main .block-container{{
                    padding-top: {padding_top}rem;    
                    padding-bottom: {padding_bottom}rem;                        
                    }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

def switch_page(page_name: str):

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("Home.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

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
        page_title=title
        , page_icon="static/images/favicon.ico"
        ,layout='wide'
        ,initial_sidebar_state="collapsed",
        )
    no_sidebar_style = """
        <style>
            div[data-testid="stSidebarNav"] {display: none;}
        </style>
    """
    cf.store_session(prefix='activity/{}.json.gz',page_name=page_name)

    # Remove defaults from sidebar
    st.markdown(no_sidebar_style, unsafe_allow_html=True)


    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    if container_style:
        set_page_container_style(padding_top=.01)
    get_sidebar()

    def get_image_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    logo_path = "static/images/ads_logo.png"
    logo_base64 = get_image_base64(logo_path)

    st.markdown("""
    <style>
        * {
        overflow-anchor: none !important;
        }
    </style>""", unsafe_allow_html=True)

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

    # Import Font Awesome
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

    # Display the navbar
    st.markdown(navbar_html, unsafe_allow_html=True)

