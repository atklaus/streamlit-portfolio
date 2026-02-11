import base64
import math
import os

import streamlit as st

import config as c
import lib.st_utils as stu
import layout.header as header

header.page_header('Almost Data Science',page_name=os.path.basename(__file__))
# cf = CF(bucket='analytics')
# cf.store_session(prefix='activity/{}.json.gz')

# Add the HTML code to the Streamlit app
# st.markdown(navbar_html, unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)
logo_path = "static/images/ads_logo.png"
logo_base64 = stu.get_image_base64(logo_path)

# stu.V_SPACE(1)

header_html = f"""
<div style="display: flex; align-items: center;">
    <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height: 120px; width: auto; max-width: 120px; margin-right: 10px;">
    <h2 style="margin: 0;">Hi, I'm Adam!</h2>
</div>
<br>
<p>I’m a data engineer, and this is a collection of interactive builds I’ve worked on, from data pipelines and applied ML tools to exploratory visualizations and engineering experiments. Hope you enjoy!</p>
"""

st.markdown(header_html, unsafe_allow_html=True)

st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)

show_mod_dict = c.MOD_ACCESS.copy()
show_mod_dict.pop("home")

n_per_row = 4
mod_keys = list(show_mod_dict.keys())
rows_count = math.ceil(len(mod_keys) / n_per_row)
for row in range(rows_count):
    cols = st.columns(n_per_row)
    for col_idx in range(n_per_row):
        idx = row * n_per_row + col_idx
        if idx < len(mod_keys):
            mod = mod_keys[idx]
            mod_entry = show_mod_dict[mod]
            target = header.get_page_path(mod_entry["name"])
            with cols[col_idx]:
                st.page_link(target, label=mod_entry["button"])
                st.caption(mod_entry["description"])
        else:
            with cols[col_idx]:
                stu.V_SPACE(1)
    st.write("")



# # Display data (optional)
# data = load_data()
# st.write(f"Total Visits: {data['visit_count']}")
# st.write(f"Unique Sessions: {len(data['session_ids'])}")

# stu.V_SPACE(4)
st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)
# Adjust columns for flexibility
col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 3])


file_path = os.getcwd()+ '/static/files/Adam_Klaus_Resume.pdf'
pdf_path = "Adam_Klaus_Resume.pdf"

with open(file_path, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

def get_pdf_base64(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf

# Your existing Streamlit code here...

pdf_path = "static/files/Adam_Klaus_Resume.pdf"
pdf_base64 = get_pdf_base64(pdf_path)

# Pages Section
with col1:
    st.markdown("<h4 style='text-align: center; color: #316b62;'>Pages</h4>", unsafe_allow_html=True)
    st.page_link("pages/3_interests.py", label="Interests")

# Contact Section
with col2:
    st.markdown("<h4 style='text-align: center; color: #316b62;'>Contact</h4>", unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;"><a href="mailto:atk14219@gmail.com" target="_blank">Email</a></p>', unsafe_allow_html=True)

    st.markdown(
        f'<p style="text-align: center;"><a href="data:application/pdf;base64,{pdf_base64}" download="Adam_Klaus_Resume.pdf" target="_blank">Resume</a></p>',
        unsafe_allow_html=True
    )

# About Section
with col3:
    st.markdown("<h4 style='text-align: center; color: #316b62;'>About</h4>", unsafe_allow_html=True)
    st.caption('Website coded in Python using Streamlit and hosted through DigitalOcean')

# Empty Space
with col4:
    pass

# Copyright Section
with col5:
    stu.V_SPACE(1)
    st.markdown('<p style="text-align: center; font-size: small;">© 2023 Copyright, All Rights Reserved. almostdatascience.com</p>', unsafe_allow_html=True)

stu.V_SPACE(1)




# font_awesome_link = """
# <head>
# <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
# </head>
# """
# st.markdown(font_awesome_link, unsafe_allow_html=True)

# # Example icons (replace with your specific FontAwesome icon classes)
# icons = [
#     "fas fa-home",
#     "fas fa-user",
#     "fas fa-cogs",
#     "fas fa-chart-line",
#     "fas fa-database",
# ]

# # The rest is the same
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
#     font-size: 18px;  /* Smaller project name */
#     margin: 10px 0;
# }
# </style>
# """

# st.markdown(card_style, unsafe_allow_html=True)

# chunk_size = 4
# for i in range(0, len(cards_data), chunk_size):
#     chunked_cards = cards_data[i:i + chunk_size]
#     chunked_icons = icons[i:i + chunk_size]

#     cols = st.columns(len(chunked_cards))
#     for j, card in enumerate(chunked_cards):
#         with cols[j]:
#             icon_class = chunked_icons[j]
#             card_content = (
#                 f'<div class="card">'
#                 f'<a href="{card["link"]}" target="_blank">'
#                 f'<i class="{icon_class}" style="font-size:48px; color: white;"></i>'
#                 f'<h2>{card["title"]}</h2>'
#                 f"<p>{card['description']}</p>"
#                 f"</a></div>"
#             )
#             st.markdown(card_content, unsafe_allow_html=True)
        
