import streamlit as st
import pandas as pd
from config import BASE_DIR, CREDS
from layout.header import page_header
import os
import lib.st_utils as stu
import os
import numpy as np
import pickle
import time
import random
from bs4 import BeautifulSoup
import lib.utils as utils
import requests
import re
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
import joblib
import datetime

BASE_URL = 'https://www.sports-reference.com'
SEASON_URL_TEMPLATE = 'https://www.sports-reference.com/cbb/seasons/women/{}-school-stats.html'


@st.cache_resource(show_spinner='Loading model...')
def init_model():
    with open('wnba_model/wnba_success.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    return loaded_model

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
    
    h2_tag = soup.find('h2', string='Advanced')
    table = h2_tag.find_next('table')            
    player_adv_df = pd.read_html(str(table))[0]
    dataframes['adv_'] = player_adv_df.add_prefix('adv_')

    h2_tag = soup.find('h2', string='Per Game')
    table = h2_tag.find_next('table')            
    player_pg_df = pd.read_html(str(table))[0]
    dataframes['pg_'] = player_pg_df.add_prefix('pg_')

    h2_tag = soup.find('h2', string='Totals')
    table = h2_tag.find_next('table')            
    player_tot_df = pd.read_html(str(table))[0]
    dataframes['tot_'] = player_tot_df.add_prefix('tot_')

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


page_header('Predicting WNBA Success')

stu.V_SPACE(1)

st.subheader('Predicting WNBA Success from College Performance')
model = init_model()

col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 6, 4])


st.cache_data(ttl=42300)
def get_team_urls(year=2023):
    user_agent = random.choice(utils.user_agents) 
    headers = {'User-Agent': user_agent} 
    season_url = SEASON_URL_TEMPLATE.format(year)
    response = requests.get(season_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html5lib')
    url_dict = utils.get_url_dict(soup)
    
    return {key: BASE_URL + val for key, val in url_dict.items() if f'/women/{year}' in val and '/cbb/schools/' in val}

st.cache_data(ttl=42300)
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

# Pages Section
search_dict = {}
with col1:
    current_year = datetime.datetime.now().year
    past_20_years = list(range(current_year - 19, current_year + 1))
    past_20_years.sort(reverse=True)

    search_dict['season'] = st.selectbox(label='Select Season',options=past_20_years)

with col2:
    search_dict['college'] = st.selectbox(label='Select College',options=college_list)

with col3:
    test= get_team_urls(search_dict['season'])
    player_dict = get_player_urls(test[search_dict['college']])
    player_list = list(player_dict)
    player_list.sort()
    search_dict['player'] = st.selectbox(label='Select Player',options=player_list)
    search_dict['player_url'] = player_dict[search_dict['player']]


search = st.button('Predict Success', key='submit_wnba')

if search:
    with st.spinner("Running model..."):
        base_df = get_player_df(search_dict)

        top_features = ['pg_2p%', 'adv_stl%', 'pg_fg%', 'pg_pts', 'pg_sos', 'adv_trb%', 'adv_ast%', 'pg_tov']
        df= base_df[top_features] 
        st.write(df)




        loaded_scaler = joblib.load('wnba_model/scaler.pkl')
        loaded_imputer = joblib.load('wnba_model/imputer.pkl')

        # new_data = loaded_imputer.transform(df)
        new_data = loaded_scaler.transform(df)  # Note the [ ] to make it 2D

        predicted_values = model.predict(new_data)
        prob_values = model.predict_proba(new_data)
        pred_df = base_df[["player_name"]].copy()
        pred_df["Predicted_Value"] = predicted_values
        pred_df["Probability_Pos"]  = prob_values[:,1]
        pred_df["Probability_Neg"]  = prob_values[:,0]
        pred_df.sort_values(by=['Probability_Pos'],ascending=False,inplace=True)
        player_name = base_df["player_name"].iloc[0]
        pred_prob = '{:.1%}'.format(pred_df["Probability_Pos"].iloc[0])
        result = """
        {player_name} has the following predicted probability of being successful in the WNBA (Win Shares > 1):
        **{pred_prob}**
        """.format(player_name=player_name, pred_prob=pred_prob)

        st.info(result)

