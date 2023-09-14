import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
from config import BASE_DIR, CREDS
from layout.header import page_header
from datetime import date, datetime
from dateutil import tz
import os
import lib.st_utils as stu
import os
from tensorflow import keras
import numpy as np
from layout.header import page_header
import config as c
import math
import requests
from io import BytesIO
import base64

page_header('Almost Data Science')

# Add the HTML code to the Streamlit app
# st.markdown(navbar_html, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)


logo_path = "static/images/ads_logo.png"
logo_base64 = stu.get_image_base64(logo_path)

# stu.V_SPACE(1)

col1, col2 = st.columns([.5, 7])

test = f"""            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height: 120px; margin-right: 10px;">
            </div>
"""

with col1:
    st.markdown(test, unsafe_allow_html=True)

with col2:
    st.markdown("## Hi, I'm Adam!")
    st.caption("### I'm a data professional and below is a collection of my interactive modules. These contain programming challenges, data visualizations, and deployed Machine Learning models. Hope you enjoy!")

st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)

def make_module(mod_dict):
    clickable = st.button(mod_dict['button'],key='home_' + mod)
    st.caption(mod_dict['description'])
    if clickable:
        stu.switch_page(mod_dict['name'])

show_mod_dict = c.MOD_ACCESS.copy()
show_mod_dict.pop('home')

n_per_row = 4
rows_count = math.ceil(len(show_mod_dict)/n_per_row)
mod_keys = list(show_mod_dict.keys())

# Divide modules into rows and columns for display
mod_keys = list(show_mod_dict.keys())
rows_count = math.ceil(len(show_mod_dict) / n_per_row)
for row in range(rows_count):
    cols = st.columns(n_per_row)
    for col_idx in range(n_per_row):
        if row * n_per_row + col_idx < len(mod_keys):
            mod = mod_keys[row * n_per_row + col_idx]
            with cols[col_idx]:
                make_module(show_mod_dict[mod])
        else:
            with cols[col_idx]:
                stu.V_SPACE(1)
    stu.V_SPACE(1)


# # Example icons (replace with your specific icons)
# icons = [
#     "https://image.flaticon.com/icons/png/512/147/147146.png",
#     "https://image.flaticon.com/icons/png/512/147/147146.png",
#     "https://image.flaticon.com/icons/png/512/147/147148.png",
#     "https://image.flaticon.com/icons/png/512/147/147141.png",
#     "https://image.flaticon.com/icons/png/512/147/147140.png",
# ]

# # Example cards data
# cards_data = [
#     {"title": "Project 1", "description": "Description of Project 1", "link": "#"},
#     {"title": "Project 2", "description": "Description of Project 2", "link": "#"},
#     {"title": "Project 3", "description": "Description of Project 3", "link": "#"},
#     {"title": "Project 4", "description": "Description of Project 4", "link": "#"},
#     {"title": "Project 5", "description": "Description of Project 5", "link": "#"},
# ]

# # Custom CSS for the cards
# card_style = """
# <style>
# .card {
#     border-radius: 20px;
#     background-color: #316b62;
#     padding: 15px;
#     text-align: center;
#     box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#     cursor: pointer;
#     width: 100%;
#     margin-bottom: 20px;
#     color: white;
# }
# .card a {
#     color: inherit;
#     text-decoration: none;
#     display: block;
# }
# .card img {
#     margin: 0 auto;
#     display: block;
# }
# .card h2 {
#     margin: 10px 0;
# }
# </style>
# """

# st.markdown(card_style, unsafe_allow_html=True)

# # Create a row of cards
# cols = st.columns(5)
# for i, card in enumerate(cards_data):
#     with cols[i]:
#         icon_image = icons[i]
#         card_content = (
#             f'<div class="card">'
#             f'<a href="{card["link"]}" target="_blank">'
#             f'<img src="{icon_image}" width="100">'
#             f'<h2>{card["title"]}</h2>'
#             f"<p>{card['description']}</p>"
#             f"</a></div>"
#         )
#         st.markdown(card_content, unsafe_allow_html=True)

stu.V_SPACE(4)
st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)

# # Define columns with appropriate widths
col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 8, 4])

# Pages Section
with col1:
    st.markdown("**Pages**")
    st.markdown('[Experience](%s)' % '/', unsafe_allow_html=True)
    st.markdown('[Interests](%s)' % '/', unsafe_allow_html=True)

# Contact Section
with col2:
    st.markdown("**Contact**")
    st.markdown('[atk14219@gmail.com](%s)' % '/', unsafe_allow_html=True)
    st.markdown('[Resume](%s)' % 'static/resume.pdf', unsafe_allow_html=True)

# About Section
with col3:
    st.markdown("**About this Page**")
    st.caption('Website coded in Python using Streamlit and deployed through DigitalOcean')

# Empty Space
with col4:
    pass

# Copyright Section
with col5:
    stu.V_SPACE(1)

    st.markdown('© 2023 Copyright, All Right Reserved. almostdatascience.com', unsafe_allow_html=True)
