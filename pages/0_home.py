import base64
import os

import streamlit as st

from app import config as c
from app.shared_ui import st_utils as stu
from app.layout import header
from app.ui.cards import ProjectCard, render_project_cards

header.page_header('DataEngBuilds',page_name=os.path.basename(__file__))
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
<p>I'm a data engineer, and below is a collection of things I've built, interactive tools, data pipelines, and applied ML experiments. Hope you enjoy!</p>
"""

st.markdown(header_html, unsafe_allow_html=True)

st.markdown(
    """<hr style="height:2px;border:none;color:#316b62;background-color:#316b62;margin: 0.75rem 0;" /> """,
    unsafe_allow_html=True,
)

stu.V_SPACE(1)
def _split_label(label: str) -> tuple[str, str]:
    icon = "◆"
    title = label
    parts = label.split(" ", 1)
    if len(parts) == 2 and not any(ch.isalnum() for ch in parts[0]):
        icon = parts[0]
        title = parts[1].strip()
    return icon, title


show_mod_dict = c.MOD_ACCESS.copy()
show_mod_dict.pop("home")
ICON_OVERRIDES = {
    "ellipses": "🫧",
}

cards = []
for mod in show_mod_dict.keys():
    mod_entry = show_mod_dict[mod]
    icon, title = _split_label(mod_entry["button"])
    icon = ICON_OVERRIDES.get(mod_entry["name"], icon)
    cards.append(
        ProjectCard(
            title=title,
            description=mod_entry["description"],
            icon=icon,
            destination=header.get_page_path(mod_entry["name"]),
        )
    )

render_project_cards(cards)
stu.V_SPACE(1)

st.markdown(
    """<hr style="height:2px;border:none;color:#316b62;background-color:#316b62;margin: 0.75rem 0;" /> """,
    unsafe_allow_html=True,
)

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

footer_html = f"""
<style>
.ads-footer-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: space-between;
}}
.ads-footer h4 {{
    margin: 0 0 0.5rem 0;
    color: #316b62;
}}
.ads-footer a {{
    text-decoration: none;
}}
.ads-footer-meta {{
    font-size: 0.85rem;
    opacity: 0.75;
    margin-top: 0.5rem;
}}
</style>
<div class="ads-footer">
  <div class="ads-footer-grid">
    <div>
      <h4>Contact</h4>
      <div><a href="mailto:atk14219@gmail.com" target="_blank">Email</a></div>
    </div>
    <div>
      <h4>About</h4>
      <div>Website coded in Python using Streamlit and hosted through DigitalOcean</div>
    </div>
      <h4></h4>
    <div class="ads-footer-meta">
      © 2026 Copyright, All Rights Reserved. dataengbuilds.com
    </div>
  </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
