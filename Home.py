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
from lib.st_utils import switch_page, V_SPACE
import os
import numpy as np
from layout.header import page_header
import config as c
import math

page_header('Almost Data Science')

# Add the HTML code to the Streamlit app
# st.markdown(navbar_html, unsafe_allow_html=True)

# stu.V_SPACE(1)
st.markdown("## Hi, I'm Adam!")
st.caption("### I'm a data professional and below is a collection of my interactive modules. These contain programming challenges, data visualizations, and deployed Machine Learning models. Hope you enjoy!")

st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)

def make_module(mod_dict):
    clickable = st.button(mod_dict['button'],key='home_' + mod)
    st.caption(mod_dict['description'])
    if clickable:
        switch_page(mod_dict['name'])

show_mod_dict = c.MOD_ACCESS.copy()
show_mod_dict.pop('home')

rows_count = math.ceil(len(show_mod_dict)/5)
mod_keys = list(show_mod_dict.keys())

# Divide modules into rows and columns for display
mod_keys = list(show_mod_dict.keys())
rows_count = math.ceil(len(show_mod_dict) / 5)
for row in range(rows_count):
    cols = st.columns(5)
    for col_idx in range(5):
        if row * 5 + col_idx < len(mod_keys):
            mod = mod_keys[row * 5 + col_idx]
            with cols[col_idx]:
                make_module(show_mod_dict[mod])
        else:
            with cols[col_idx]:
                V_SPACE(1)
    V_SPACE(2)

# Example icons (replace with your specific icons)
icons = [
    "https://image.flaticon.com/icons/png/512/147/147144.png",
    "https://image.flaticon.com/icons/png/512/147/147146.png",
    "https://image.flaticon.com/icons/png/512/147/147148.png",
    "https://image.flaticon.com/icons/png/512/147/147141.png",
    "https://image.flaticon.com/icons/png/512/147/147140.png",
]

# Example cards data
cards_data = [
    {"title": "Project 1", "description": "Description of Project 1", "link": "#"},
    {"title": "Project 2", "description": "Description of Project 2", "link": "#"},
    {"title": "Project 3", "description": "Description of Project 3", "link": "#"},
    {"title": "Project 4", "description": "Description of Project 4", "link": "#"},
    {"title": "Project 5", "description": "Description of Project 5", "link": "#"},
]

# Custom CSS for the cards
card_style = """
<style>
.card {
    border-radius: 20px;
    background-color: #316b62;
    padding: 15px;
    text-align: center;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    width: 100%;
    margin-bottom: 20px;
    color: white;
}
.card a {
    color: inherit;
    text-decoration: none;
    display: block;
}
.card img {
    margin: 0 auto;
    display: block;
}
.card h2 {
    margin: 10px 0;
}
</style>
"""

st.markdown(card_style, unsafe_allow_html=True)

# Create a row of cards
cols = st.columns(5)
for i, card in enumerate(cards_data):
    with cols[i]:
        icon_image = icons[i]
        card_content = (
            f'<div class="card">'
            f'<a href="{card["link"]}" target="_blank">'
            f'<img src="{icon_image}" width="100">'
            f'<h2>{card["title"]}</h2>'
            f"<p>{card['description']}</p>"
            f"</a></div>"
        )
        st.markdown(card_content, unsafe_allow_html=True)

# Define columns with appropriate widths
col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 8, 4])

# Pages Section
with col1:
    st.markdown("**Pages**")
    st.markdown('[Experience](%s)' % '/', unsafe_allow_html=True)
    st.markdown('[Interests](%s)' % '/', unsafe_allow_html=True)

# Contact Section
with col2:
    st.markdown("**Contact**")
    st.markdown('[atklaus@wisc.edu](%s)' % '/', unsafe_allow_html=True)
    # st.markdown('[Resume](%s)' % '/', unsafe_allow_html=True)

# About Section
with col3:
    st.markdown("**About this Page**")
    st.caption('Website coded in Python using Streamlit')

# Empty Space
with col4:
    pass

# Copyright Section
with col5:
    V_SPACE(1)

    st.markdown('© 2023 Copyright, All Right Reserved. almostdatascience.com', unsafe_allow_html=True)
