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

@st.cache_resource('Loading model...')
def init_model():
    with open('wnba_success.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    return loaded_model

# Load the model from the file

def get_player_url(player_name_search):
    # Constructing the Google search URL
    player = player_name_search

    user_agent = random.choice(utils.user_agents) 
    headers = {'User-Agent': user_agent} 

    query = f"{player} college stats sports-reference women's basketball"
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
                print(f"For {player} from {college}, stats link: {link_url}")
            else:
                print(f"No desired pattern found in link for {player} from {college}")
        else:
            print(f"No link found for {player} from {college}")
    else:
        print(f"Failed to fetch search results for {player} from {college}")
    time.sleep(5)
    return link_url
    # To avoid making too many rapid requests, sleep for a few seconds between searches



page_header('Predicting WNBA Success')

stu.V_SPACE(1)
model = init_model()

st.subheader('Predicting WNBA Success from College Performance')

model = init_model()

player_name_search = st.text_input(placeholder='Search for a player you would like to predict')

# for player_url in list(wnba_df['url']):
try:
    player_url = get_player_url(player_name_search)
    session = requests.session()
    headers, proxy_rand = utils.requst_params(utils.user_agents, utils.available_proxies)
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
    base_df['player_name'] =row['player_name']
    base_df['position'] =position
    base_df['height'] =height
    base_df['awards'] =awards
    base_df.to_csv('ncaa_ref/' + player_name + '.csv')
    time.sleep(10)

except Exception as error:
# handle the exception
    print(row['player_name']+ "ERROR:", error)

