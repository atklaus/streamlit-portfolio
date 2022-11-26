import streamlit as st

def page_header(title):
    st.set_page_config(layout="wide", page_title=title, page_icon="static/images/grainger_logo.jpeg")

    c1,c2 = st.columns([1,2])
    with c1:
        st.image("static/images/grainger_logo.jpeg", width=120)

    with c2:
        st.write('')
        st.header(title)
    