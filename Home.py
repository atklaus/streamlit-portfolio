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
import os
import cv2
from tensorflow import keras
import numpy as np
from layout.header import page_header, set_page_container_style

@st.experimental_singleton(suppress_st_warning=True, show_spinner=False)
def init_model():
    return keras.models.load_model('img_model')

page_header('Almost Data Science')
stu.get_sidebar()
st.markdown("<h1 style='text-align: center; color: grey;'>Big headline</h1>", unsafe_allow_html=True)


with st.expander(label='Learn More'):
    if st.checkbox("Training Performance",key='expand_1'):
        pass
        # st.write("Hello world")
    # if st.checkbox("Fake expand2",key='expand_2'):
    #     st.markdown("1. Double click into a cell to edit")
    #     st.markdown("2. Hit enter or click away to store the change")
    #     st.markdown("3. Click submit and changes will be recorded")
    #     st.markdown("4. You can validate this update by reloading the page and seeing the values")


