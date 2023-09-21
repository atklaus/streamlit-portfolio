import streamlit as st

from streamlit_timeline import timeline

# use full page width
st.set_page_config(page_title="Timeline Example", layout="wide")

# load data
with open('example.json', "r") as f:
    data = f.read()

# render timeline
timeline(data, height=800)

def timeline_entry(title, company, image_url, date_range):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.image(image_url, width=50)
    with col2:
        st.subheader(title)
        st.write(company)
    with col3:
        st.write(date_range)

