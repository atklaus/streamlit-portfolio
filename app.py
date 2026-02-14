import streamlit as st

st.set_page_config(
    page_title="DataEngBuilds",
    page_icon="static/images/favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with st.sidebar:
    st.empty()

PAGES = [
    st.Page("pages/0_home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/2_wnba_success.py", title="WNBA Success", icon="🏀"),
    st.Page("pages/8_bibliometrix_reference_cleaner.py", title="Bibliometrix Cleaner", icon="📚"),
    st.Page("pages/1_landscape_img.py", title="Landscape Prediction", icon="🏔️"),
    st.Page("pages/4_game_of_life.py", title="Game of Life", icon="👾"),
    st.Page("pages/5_ellipses.py", title="Random Ellipses", icon="♾️"),
    st.Page("pages/6_happy_prime.py", title="Happy Prime", icon="🙂"),
    st.Page("pages/7_analytics.py", title="Analytics", icon="📈"),
]

nav = st.navigation(PAGES, position="hidden")
nav.run()
