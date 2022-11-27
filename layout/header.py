import streamlit as st

BACKGROUND_COLOR = 'white'
COLOR = 'black'

def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10,
        color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
            .appview-container .main .block-container{{
                    padding-top: {padding_top}rem;    }}
            </style>
            ''',
            unsafe_allow_html=True,
        )



def page_header(title):
    # st.set_page_config(layout="wide", page_title=title, page_icon="static/images/ads_logo.png")
    st.set_page_config(
        page_title=title
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
    set_page_container_style(padding_top=.25)


    c1,c2, c3= st.columns([1,1,12])
    with c1:
        st.image("static/images/ads_logo.png", width=120)

    with c2:
        st.write('')
        st.header(title)
    