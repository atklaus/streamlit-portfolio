import streamlit as st
import pandas as pd
from app.config import BASE_DIR, CREDS
from app.layout.header import page_header
import os
from app.shared_ui import st_utils as stu
import os
import numpy as np
import pickle
import time
import random
from bs4 import BeautifulSoup, Comment
from shared import utils
import requests
import re
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import joblib
import datetime

MODEL_PATH = os.path.join(BASE_DIR, "projects", "wnba_success", "model", "wnba_success.pkl")
IMPUTER_PATH = os.path.join(BASE_DIR, "projects", "wnba_success", "model", "imputer.pkl")
PDF_PATH = os.path.join(BASE_DIR, "projects", "wnba_success", "assets", "Predicting_WNBA_Success.pdf")

BASE_URL = 'https://www.sports-reference.com'
SEASON_URL_TEMPLATE = 'https://www.sports-reference.com/cbb/seasons/women/{}-school-stats.html'


@st.cache_resource(show_spinner='Loading model...',ttl=43200)
def init_model():
    loaded_model = joblib.load(MODEL_PATH)

    # with open(MODEL_PATH, 'rb') as model_file:
    #     loaded_model = pickle.load(model_file)
    return loaded_model

@st.cache_resource(show_spinner=False, ttl=43200)
def init_imputer():
    return joblib.load(IMPUTER_PATH)

def get_pg_sos_fallback():
    try:
        imputer = init_imputer()
    except Exception:
        return None
    if not hasattr(imputer, "feature_names_in_") or not hasattr(imputer, "statistics_"):
        return None
    try:
        idx = list(imputer.feature_names_in_).index("pg_sos")
    except ValueError:
        return None
    return imputer.statistics_[idx]

# Load the model from the file

def get_player_url(search_dict):
    # Constructing the Google search URL
    user_agent = random.choice(utils.user_agents) 
    headers = {'User-Agent': user_agent} 

    query = f"{search_dict['player']} college stats sports-reference women's basketball"
    # query = f"{player} college stats sports-reference women's basketball {row['college_team']}"

    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    link_url = None

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the first link with "sports-reference.com" in its href attribute
        link = soup.find('a', href=lambda x: x and "www.sports-reference.com/cbb/players/" in x)

        if link:
            # Extract the desired URL using regular expression
            match = re.search(r'(https://www.sports-reference.com/.*?\.html)', link['href'])
            if match:
                link_url = match.group(1)
                print(f"For {search_dict['player']} from {search_dict['college']}, stats link: {link_url}")
            else:
                print(f"No desired pattern found in link for {search_dict['player']} from {search_dict['college']}")
        else:
            print(f"No link found for {search_dict['player']} from {search_dict['college']}")
            print(f"No link found for {search_dict['player']} from {search_dict['college']}")

    else:
        print(f"Failed to fetch search results for {search_dict['player']} from {search_dict['college']}")
    time.sleep(5)
    return link_url
    # To avoid making too many rapid requests, sleep for a few seconds between searches

def _find_table_in_comments(soup, table_ids, header_text):
    header_text = (header_text or "").lower()
    table_ids = table_ids or []
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment_text = str(comment).lower()
        if header_text and header_text not in comment_text and not any(tid in comment_text for tid in table_ids):
            continue
        comment_soup = BeautifulSoup(comment, "lxml")
        for table_id in table_ids:
            table = comment_soup.find("table", id=table_id)
            if table is not None:
                return table
        table = comment_soup.find("table")
        if table is not None:
            return table
    return None

def _find_stats_table(soup, header_text, table_ids=None):
    header_text = (header_text or "").strip()
    header_text_lower = header_text.lower()

    h2_tag = soup.find(
        lambda tag: tag.name in ("h2", "h3")
        and tag.get_text(strip=True).lower() == header_text_lower
    )
    if h2_tag is None:
        h2_tag = soup.find(
            lambda tag: tag.name in ("h2", "h3")
            and header_text_lower in tag.get_text(strip=True).lower()
        )

    table = h2_tag.find_next("table") if h2_tag is not None else None

    if table is None and table_ids:
        for table_id in table_ids:
            table = soup.find("table", id=table_id)
            if table is not None:
                break

    if table is None:
        table = _find_table_in_comments(soup, table_ids, header_text_lower)

    return table

def _table_to_df(table):
    if table is None:
        return None
    try:
        return pd.read_html(str(table))[0]
    except ValueError:
        return None

def get_player_df(search_dict):
    # player_url = get_player_url(search_dict)
    player_url = BASE_URL + search_dict['player_url']
    session = requests.session()
    user_agent = random.choice(utils.user_agents) 
    headers = {'User-Agent': user_agent} 

    response = session.get(player_url, headers = headers)
    # response = session.get(player_url)
    if response.status_code != 200:
        print(response.status_code)
    else:
        pass


    page_html = BeautifulSoup(response.text, 'html5lib')
    awards,name,position,height = utils.extract_details_from_page(page_html)

    div_class = page_html.findAll('h1')
    player_name = div_class[0].find('span').text

    prefixes = {'adv_': 'Advanced', 'pg_': 'Per Game', 'tot_': 'Totals'}
    # Initialize an empty dictionary to hold dataframes
    dataframes = {}

    soup = BeautifulSoup(response.content, 'lxml')
    
    missing_sections = []
    adv_table = _find_stats_table(soup, "Advanced", table_ids=["players_advanced", "advanced"])
    player_adv_df = _table_to_df(adv_table)
    if player_adv_df is None:
        missing_sections.append("Advanced")
    else:
        dataframes["adv_"] = player_adv_df.add_prefix("adv_")

    pg_table = _find_stats_table(soup, "Per Game", table_ids=["players_per_game", "per_game"])
    player_pg_df = _table_to_df(pg_table)
    if player_pg_df is None:
        missing_sections.append("Per Game")
    else:
        dataframes["pg_"] = player_pg_df.add_prefix("pg_")

    tot_table = _find_stats_table(soup, "Totals", table_ids=["players_totals", "totals"])
    player_tot_df = _table_to_df(tot_table)
    if player_tot_df is None:
        missing_sections.append("Totals")
    else:
        dataframes["tot_"] = player_tot_df.add_prefix("tot_")

    if missing_sections:
        st.error(
            "Stats tables missing on Sports-Reference for "
            f"{search_dict.get('player', 'this player')}: "
            + ", ".join(missing_sections)
            + ". Try a different player or season."
        )
        return None

    # Perform merging
    base_df = dataframes['pg_'].merge(dataframes['adv_'], how='left', left_on='pg_Season', right_on='adv_Season')
    base_df = base_df.merge(dataframes['tot_'], how='left', left_on='pg_Season', right_on='tot_Season')
    base_df['player_name'] =player_name
    base_df['position'] =position
    base_df['height'] =height
    base_df['awards'] =awards
    # base_df.to_csv('ncaa_ref/' + player_name + '.csv')
    base_df = prep_df(base_df)

    return base_df

def prep_df(df):
    # Convert column names to lowercase
    df.rename(columns={'adv_per_x': 'adv_per_college','adv_per_y':'per_pro','adv_ws/48':'ws_48_pro','player_name_x':'player_name'}, inplace=True)
    df.columns = df.columns.str.lower()

    # Remove columns with 'unnamed' in their names
    df = df.loc[:, ~df.columns.str.contains('unnamed', case=False)]
    df = df[df['pg_season'] == 'Career']
    return df


import base64

# Your existing imports and code here...

# Function to display PDF within Streamlit app
@st.cache_data(show_spinner='Loading pdf...')
def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width=100% height="500" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# Add this function to display the detailed context of your paper
def display_paper_context():
    with st.expander("Learn more about the predictive model and it's background"):

        # pdf_path = "static/files/Predicting_WNBA_Success.pdf"
        # pdf_base64 = utils.get_pdf_base64(pdf_path)

        # st.markdown(
        #     f'<p style="text-align: center;"><a href="data:application/pdf;base64,{pdf_base64}" download="Predicting_WNBA_Success.pdf" target="_blank">Download Paper</a></p>',
        #     unsafe_allow_html=True
        # )


        pdf_path = PDF_PATH

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="Download Paper",
            data=pdf_bytes,
            file_name="Predicting_WNBA_Success.pdf",
            mime="application/pdf",
            key='submit_wnba_download'
        )


        # Display the PDF using the function
        file_path = PDF_PATH

        displayPDF(file_path)


# Your existing code for page_header and other parts...
page_header('Predicting WNBA Player Success',page_name=os.path.basename(__file__))


stu.V_SPACE(1)

st.subheader('Predicting WNBA Success from College Performance')
st.write("This page provides insights into WNBA players' success, leveraging predictive modeling based on college performance.")


@st.cache_data(ttl=42300,show_spinner=False)
def get_team_urls(year=2023):

    user_agent = random.choice(utils.user_agents) 
    headers = {'User-Agent': user_agent} 
    season_url = SEASON_URL_TEMPLATE.format(year)
    response = requests.get(season_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html5lib')
    url_dict = utils.get_url_dict(soup)
    
    return {key: BASE_URL + val for key, val in url_dict.items() if f'/women/{year}' in val and '/cbb/schools/' in val}

@st.cache_data(ttl=42300,show_spinner=False)
def get_player_urls(team_url):
    user_agent = random.choice(utils.user_agents) 
    headers = {'User-Agent': user_agent} 

    response = requests.get(team_url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'lxml')
    h2_tag = soup.find('h2', string='Roster')
    table = h2_tag.find_next('table')
    return utils.get_url_dict(table)


test= get_team_urls()
college_list = list(test.keys())
college_list.sort()

search_dict = {}
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    current_year = datetime.datetime.now().year
    past_20_years = list(range(current_year - 19, current_year + 1))
    past_20_years.sort(reverse=True)
    search_dict["season"] = st.selectbox(
        label="Select Season", options=past_20_years, key="wnba_season"
    )

with col2:
    search_dict["college"] = st.selectbox(
        label="Select College", options=college_list, key="wnba_college"
    )

with col3:
    test = get_team_urls(search_dict["season"])
    player_dict = get_player_urls(test[search_dict["college"]])
    player_list = list(player_dict)
    player_list.sort()
    search_dict["player"] = st.selectbox(
        label="Select Player", options=player_list, key="wnba_player"
    )
    search_dict["player_url"] = player_dict[search_dict["player"]]

search = st.button("Predict Success", type="primary")

if search:
    with st.spinner("Running model..."):
        base_df = get_player_df(search_dict)
        if base_df is None or base_df.empty:
            st.stop()

        top_features = ['pg_2p%', 'adv_stl%', 'pg_fg%', 'pg_pts', 'pg_sos', 'adv_trb%', 'adv_ast%', 'pg_tov']
        if "pg_sos" not in base_df.columns or base_df["pg_sos"].isna().all():
            fallback = get_pg_sos_fallback()
            if fallback is not None:
                base_df["pg_sos"] = fallback
                # st.warning(
                #     "Strength of Schedule (pg_sos) not found. "
                #     "Using training mean as fallback."
                # )

        missing_features = [col for col in top_features if col not in base_df.columns]
        if missing_features:
            st.error(
                "Missing required stats for prediction: "
                + ", ".join(missing_features)
                + ". The Sports-Reference page may not include these columns."
            )
            st.write("Available columns:", sorted(base_df.columns))
            st.stop()
        
        df= base_df[top_features] 
        st.markdown("Features used in Prediction")
        st.dataframe(df,
        column_config={
            'pg_2p%':st.column_config.NumberColumn(label='2-Point Field Goal Percentage',format='%.2f %%')
            , 'adv_stl%':st.column_config.NumberColumn(label='Steal Percentage',format='%.2f %%')
            , 'pg_fg%':st.column_config.NumberColumn(label='Field Goal Percentage',format='%.2f %%')
            , 'pg_pts':st.column_config.NumberColumn(label='Points Per Game')
            , 'pg_sos':st.column_config.NumberColumn(label='Strength of Schedule')
            , 'adv_trb%':st.column_config.NumberColumn(label=' Total Rebound Percentage',format='%.2f %%')
            , 'adv_ast%':st.column_config.NumberColumn(label='Assist Percentage',format='%.2f %%')
            , 'pg_tov':st.column_config.NumberColumn(label='Turnovers Per Game')
        },
        hide_index=True
        )

        # loaded_scaler = joblib.load('wnba_model/scaler.pkl')
        # # loaded_imputer = joblib.load('wnba_model/imputer.pkl')

        # # new_data = loaded_imputer.transform(df)
        # new_data = loaded_scaler.transform(df)  # Note the [ ] to make it 2D

        # st.write(model.feature_importances_)

        model = init_model()
        predicted_values = model.predict(df)
        prob_values = model.predict_proba(df)
        pred_df = base_df[["player_name"]].copy()
        pred_df["Predicted_Value"] = predicted_values
        pred_df["Probability_Pos"]  = prob_values[:,1]
        pred_df["Probability_Neg"]  = prob_values[:,0]
        pred_df.sort_values(by=['Probability_Pos'],ascending=False,inplace=True)
        player_name = base_df["player_name"].iloc[0]
        pred_prob = '{:.1%}'.format(pred_df["Probability_Pos"].iloc[0])
        result = """
        **{player_name}** predicted probability of being successful in the WNBA (Win Shares > 0):

        **{pred_prob}**
        """.format(player_name=player_name, pred_prob=pred_prob)

        st.info(result)


stu.V_SPACE(1)



# Call the function to display the paper context
display_paper_context()
