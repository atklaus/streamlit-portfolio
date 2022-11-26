import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from config import BASE_DIR, CREDS
from layout.header import page_header
from git import Repo
import os
import lib.st_utils as stu



# The code below is for the title and logo.
st.set_page_config(
    page_title="Test"
    , page_icon="⚙️"
    ,layout='wide'
    ,initial_sidebar_state="collapsed",
    )

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""

# Remove defaults from sidebar
st.markdown(no_sidebar_style, unsafe_allow_html=True)


with st.sidebar:
    st.subheader('Team Pages')

    Home = st.button("Home")
    update_team_info = st.button("Update Team Info")
    if Home:
        stu.switch_page("Home")
    if update_team_info:
        stu.switch_page("Update Team Info")
