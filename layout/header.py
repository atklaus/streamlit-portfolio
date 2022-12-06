import streamlit as st
from streamlit_option_menu import option_menu
import lib.st_utils as stu

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


def switch_page(page_name: str):
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("Home.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def get_sidebar():
    with st.sidebar:
        st.subheader('Team Pages')

        Home = st.button("Home")
        scenery_pred = st.button("Landscape Image Prediction")
        if Home:
            switch_page("Home")
        if scenery_pred:
            switch_page("Landscape")


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
    
    set_page_container_style(padding_top=1)
    get_sidebar()

    
    c1,c2, c3, c4, c5, c6, c7= st.columns([1.2,1,23,1,1,1,1])
    with c1:
        # st.write("")
        # st.image("static/images/ads_logo.png", width=120)
        st.image("static/images/ads_logo.png", width=75)

    with c2:
        st.markdown('##### ' + title)

    
    with c3:
        pass
        # Add Link to your repo

        # Add Link to your repo
        # st.markdown("[![Foo](https://drive.google.com/uc?export=view&id=1BWAJbKLhh9e2EsR_s8NW8LPmmMwqRRTu)](http://google.com.au/)")        
        # st.markdown(git,unsafe_allow_html=True)

    with c4:
        st.write("")
        css_example = '''                    
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <a href=/"> <i class="fa-sharp fa-solid fa-house fa-2x" style="color:white"></i></a>
        '''
        st.write(css_example, unsafe_allow_html=True)

    with c5:
        st.write("")
        css_example = '''                    
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <a href="https://github.com/atklaus"> <i class="fa-brands fa-github fa-2x" style="color:white"></i></a>
        '''
        st.write(css_example, unsafe_allow_html=True)

    with c6:
        st.write("")
        css_example = '''                    
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <a href="https://www.linkedin.com/in/adam-klaus/"> <i class="fa-brands fa-linkedin fa-2x" style="color:white"></i></a>
        '''
        st.write(css_example, unsafe_allow_html=True)

    with c7:
        st.write("")
        css_example = '''                    
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <a href="/"> <i class="fa-solid fa-info fa-2x" style="color:white"></i></a>
        '''
        st.write(css_example, unsafe_allow_html=True)    

    st.markdown("""<hr style="height:3px;border:none;color:#316b62;background-color:#316b62;" /> """, unsafe_allow_html=True)

    # with c7:
    #     st.write("")
    #     css_example = '''                    
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    #     <a href="https://twitter.com/SantaKlaus_1"> <i class="fa-brands fa-twitter fa-2x" style="color:white"></i></a>
    #     '''
    #     st.write(css_example, unsafe_allow_html=True)