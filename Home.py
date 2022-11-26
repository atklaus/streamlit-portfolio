import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from config import BASE_DIR, CREDS
from layout.header import page_header
import datetime
from datetime import date, datetime
from dateutil import tz
import git
import os
import lib.st_utils as stu

st.set_page_config(
    page_title="almostdatascience"
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

st.title('Picture Categories')

uploaded_file = st.file_uploader("Choose an image")


with st.expander(label='FAQs'):
    if st.checkbox("Why am I not seeing changes I just submitted",key='expand_1'):
        pass
        # st.write("Hello world")
    # if st.checkbox("Fake expand2",key='expand_2'):
    #     st.markdown("1. Double click into a cell to edit")
    #     st.markdown("2. Hit enter or click away to store the change")
    #     st.markdown("3. Click submit and changes will be recorded")
    #     st.markdown("4. You can validate this update by reloading the page and seeing the values")


