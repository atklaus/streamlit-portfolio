import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
import config as c
import base64


BACKGROUND_COLOR = 'white'
COLOR = 'black'

def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = .1,
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
                    padding-top: {padding_top}rem;    
                    padding-bottom: {padding_bottom}rem;                        
                    }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

def switch_page(page_name: str):

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
        st.write('## ' + 'Almost Data Science')
        for module_key, module_values in c.MOD_ACCESS.items():
            if module_key == "home":  # Special case for the home button
                if st.button("Home"):
                    switch_page("Home")
            else:
                if st.button(module_values['button']):
                    switch_page(module_values['name'])

        # # Navigation bar with radio buttons
        # nav_selection = st.sidebar.radio(
        #     "Navigation",
        #     ("Home", "Interests", "Conway's Game of Life", "About")
        # )

        # # Content for the Home section
        # if nav_selection == "Home":
        #     st.title("Welcome to My Website!")
        #     st.write("Here you'll find a collection of my interactive projects and interests.")

        # # Content for the Interests section
        # elif nav_selection == "Interests":
        #     st.title("My Interests")
        #     st.write("Here's a collection of my favorite topics, hobbies, and pastimes.")

        # # Content for Conway's Game of Life section
        # elif nav_selection == "Conway's Game of Life":
        #     st.title("Conway's Game of Life")
        #     st.write("Explore the fascinating world of cellular automata with Conway's Game of Life.")

        # # Content for the About section
        # elif nav_selection == "About":
        #     st.title("About Me")
        #     st.write("Learn more about my background, experience, and interests.")

        # You can add additional code and logic for each section, including Streamlit widgets, images, and more.


def navigate_to_link(link):
    # Your condition to decide when to navigate
        link_url = "https://www.linkedin.com/in/adam-klaus/"  # Replace with your desired URL
        st.write(f'<meta http-equiv="refresh" content="0; URL={link_url}" />', unsafe_allow_html=True)



def page_header(title, container_style=True):
    # st.set_page_config(layout="wide", page_title=title, page_icon="static/images/ads_logo.png")
    st.set_page_config(
        page_title=title
        , page_icon="static/images/favicon.ico"
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

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    if container_style:
        set_page_container_style(padding_top=1)
    get_sidebar()

    def get_image_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    logo_path = "static/images/ads_logo.png"
    logo_base64 = get_image_base64(logo_path)

    st.markdown("""
    <style>
        * {
        overflow-anchor: none !important;
        }
    </style>""", unsafe_allow_html=True)

    # URLs for GitHub and LinkedIn logos
    github_logo_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    linkedin_logo_url = "https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg"

    # Replace the following URLs with your actual GitHub and LinkedIn URLs
    github_profile_url = "https://github.com/atklaus"
    linkedin_profile_url = "https://linkedin.com/in/adam-klaus"
    navbar_html = f"""
    <div style="background-color: #316b62; padding: 10px; border-radius: 10px; display: flex; justify-content: space-around; flex-wrap: wrap;">
        <a href="https://www.almostdatascience.com/"><i class="fas fa-home" style="font-size:24px; color: white;"></i></a>
        <a href="https://www.almostdatascience.com/"><i class="fas fa-star" style="font-size:24px; color: white;"></i></a>
        <a href="https://www.almostdatascience.com/"><i class="fas fa-info-circle" style="font-size:24px; color: white;"></i></a>
        <a href="{github_profile_url}" target="_blank"><img src="{github_logo_url}" alt="GitHub" style="height: 24px; filter: invert(1);"></a>
        <a href="{linkedin_profile_url}" target="_blank"><img src="{linkedin_logo_url}" alt="LinkedIn" style="height: 24px; filter: invert(1) hue-rotate(180deg);"></a>
    </div>
    """

    # Import Font Awesome
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

    # Display the navbar
    st.markdown(navbar_html, unsafe_allow_html=True)



    # navbar_html = f"""
    #     <head>
    #         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    #     </head>
    #     <div style="display: flex; justify-content: space-between; align-items: center; background-color: #316b62; padding: 10px; border-radius: 15px;">
    #         <div style="display: flex; align-items: center;">
    #             <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height: 80px; margin-right: 10px;">
    #             <div style="line-height: 10x; font-size: 25px; color: #ffffff;">Almost<br>Data<br>Science</div>
    #         </div>
    #         <div>
    #             <a href="#" style="margin-left: 30px; font-size: 30px; text-decoration: none; color: #ffffff;"><i class="fas fa-home"></i></a>
    #             <a href="#" style="margin-left: 30px; font-size: 30px; text-decoration: none; color: #ffffff;"><i class="fas fa-info-circle"></i></a>
    #             <a href="https://www.linkedin.com/in/adam-klaus/" target="_blank" style="margin-left: 30px; font-size: 30px; text-decoration: none; color: #ffffff;"><i class="fab fa-linkedin"></i></a>
    #             <a href="https://github.com/atklaus" target="_blank" style="margin-left: 30px; font-size: 30px; text-decoration: none; color: #ffffff;"><i class="fab fa-github"></i></a>
    #         </div>
    #     </div>
    # """

    # # Embed the navbar_html into Streamlit
    # st.markdown(navbar_html, unsafe_allow_html=True)

    # st.markdown(navbar_html, unsafe_allow_html=True)

# Using st.experimental_memo to execute the navigation function once

    
    # c1,c2, c3, c4, c5, c6, c7= st.columns([1.2,1,23,1,1,1,1])
    # with c1:
    #     # st.write("")
    #     # st.image("static/images/ads_logo.png", width=120)
    #     st.image("static/images/ads_logo.png", width=75)

    # with c2:
    #     st.markdown('##### ' + title)

    
    # with c3:
    #     pass
    #     # Add Link to your repo

    #     # Add Link to your repo
    #     # st.markdown("[![Foo](https://drive.google.com/uc?export=view&id=1BWAJbKLhh9e2EsR_s8NW8LPmmMwqRRTu)](http://google.com.au/)")        
    #     # st.markdown(git,unsafe_allow_html=True)

    # with c4:
    #     st.write("")
    #     css_example = '''                    
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    #     <a href=/"> <i class="fa-sharp fa-solid fa-house fa-2x" style="color:white"></i></a>
    #     '''
    #     st.write(css_example, unsafe_allow_html=True)

    # with c5:
    #     st.write("")
    #     css_example = '''                    
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    #     <a href="https://github.com/atklaus"> <i class="fa-brands fa-github fa-2x" style="color:white"></i></a>
    #     '''
    #     st.write(css_example, unsafe_allow_html=True)

    # with c6:
    #     st.write("")
    #     css_example = '''                    
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    #     <a href="https://www.linkedin.com/in/adam-klaus/"> <i class="fa-brands fa-linkedin fa-2x" style="color:white"></i></a>
    #     '''
    #     st.write(css_example, unsafe_allow_html=True)

    # with c7:
    #     st.write("")
    #     css_example = '''                    
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    #     <a href="/"> <i class="fa-solid fa-info fa-2x" style="color:white"></i></a>
    #     '''
    #     st.write(css_example, unsafe_allow_html=True)    



    # with c7:
    #     st.write("")
    #     css_example = '''                    
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    #     <a href="https://twitter.com/SantaKlaus_1"> <i class="fa-brands fa-twitter fa-2x" style="color:white"></i></a>
    #     '''
    #     st.write(css_example, unsafe_allow_html=True)