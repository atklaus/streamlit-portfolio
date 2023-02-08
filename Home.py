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
from layout.header import page_header

page_header('Almost Data Science')


# col1, col2= st.columns([.0, .95])
# with col1:
#     st.markdown("#")
#     st.write('')
#     # st.image("static/images/ads_logo.png", width=120)
#     st.image("static/images/ads_logo.png", width=100)

# with col2:
st.markdown("#")
st.markdown("## Hi, I'm Adam!")
st.caption("### I'm a data professional and below is a collection of my interactive modules. These contain programming challenges, data visualizations and deployed Machine Learning models. Hope you enjoy!")
st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns([1, .1, 1, .1, 1, .1, 1])

with col1:
    landscape = st.button("🏔️  Landscape Image Prediction")
    st.caption('### Predict the landscape of a given image using a convolutional neural network')
    if landscape:
        stu.switch_page("Landscape")
with col3:
    happy_prime = st.button("🙂 Happy Prime",key='hp')
    st.caption('### Calculator to determine whethern an integer is happy or sad')
with col5:
    happy_prime = st.button("♾️ Random Ellipses",key='re')
    st.caption('### Given two ellipses, determine their overlapping area with a pseudo random number generator')
with col7:
    happy_prime = st.button("👾 Game of Life",key='gof')
    st.caption("### Visualize preset and random simulations of Conway's game of life")


st.markdown('#')
st.markdown('#')
st.markdown('#')
st.markdown('#')
st.markdown('#')
st.markdown('#')
st.markdown('#')
st.markdown('#')

# with st.expander(label='Learn More'):
#     if st.checkbox("Training Performance",key='expand_1'):
#         pass
#         # st.write("Hello world")
#     # if st.checkbox("Fake expand2",key='expand_2'):
#     #     st.markdown("1. Double click into a cell to edit")
#     #     st.markdown("2. Hit enter or click away to store the change")
#     #     st.markdown("3. Click submit and changes will be recorded")
#     #     st.markdown("4. You can validate this update by reloading the page and seeing the values")


col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.6, 8, 4])
with col1:
    st.caption('Pages')
    st.caption('[Experience](%s)' % '/')
    st.caption('[Interests](%s)' % '/')
    
with col2:
    st.caption('Contact')
    st.caption('[atklaus@wisc.edu](%s)' % '/')
    st.caption('[Resume](%s)' % '/')

with col3:
    st.caption('About this Page')
    st.caption('Website coded in Python using Streamlit')
    

with col4:
    pass

with col5:
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')
    st.caption('© 2021 Copyright, All Right Reserved. almostdatascience.com')
