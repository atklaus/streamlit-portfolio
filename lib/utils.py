import random
import re
from bs4 import BeautifulSoup
import json
import base64
import json
import boto3
import streamlit as st


user_agents = [
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; AOL 9.7; AOLBuild 4343.1028; Windows NT 6.1; WOW64; Trident/7.0)",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12B466",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; Active Content Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0; WebView/1.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36",
    "Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/50.0.125 Chrome/44.0.2403.125 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MAARJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900T Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4"
]



def requst_params(user_agents, available_proxies):    
    user_agent = random.choice(user_agents) 
    headers = {'User-Agent': user_agent} 
    proxy = random.choice(available_proxies) 
    proxies = {'http': 'http://{}'.format(proxy)} 
    return headers, proxies


def extract_awards(page_html):
    """Extract awards from the provided HTML."""
    html_list = []
    try:
        html_list = page_html.find('ul', id='bling')
        return ','.join([li.text for li in html_list.find_all('li')])
    except:
        return html_list

def extract_name_and_position(page_html):
    """Extract name and position from the provided HTML."""
    name = None
    position = None
    div_class = page_html.find('div', class_='nothumb')
    try:
        name = div_class.find('span').text
    except:
        pass 
    try:
        position = div_class.find_all('p')[0].text.split(':')[1].strip()    
    except:
        pass

    return name, position

def extract_height(page_html):
    """Extract and format height from the provided HTML."""
    try:
        div_class = page_html.find('div', class_='nothumb')
        height = div_class.find_all('p')[1].text.strip()
        match = re.search(r'\((.*?)\)', height)
        
        if match:
            height = match.group(1)  # group(1) corresponds to the first group enclosed in parentheses
            return height.replace('cm','').strip()
    except:
        return None

def extract_details_from_page(page_html):
    """Extract required details from the provided HTML."""
    try:
        awards = extract_awards(page_html)
        name, position = extract_name_and_position(page_html)
        height = extract_height(page_html)
        return awards, name,position,height
    except Exception as e:
        # Logging the exception might be helpful for debugging purposes.
        print(f"Error occurred: {e}")
        return {}

def get_url_dict(page_html):
    '''
    Create a dictionary of all links and their text reference
    '''
    href = page_html.find_all('a')
    href_dict = {}
    for item in href:
        try:
            href_dict[item.text.strip()] = item['href']
        except:
            pass
    
    return href_dict

def get_html(session,url):
    response = session.get(url, headers = dict(referer = url))
    page_html = BeautifulSoup(response.text, 'html5lib')
    return page_html

#Write dictionary to json
def write_dict_to_json(write_dict,filepath):
    js = json.dumps(write_dict)
    # Open new json file if not exist it will create
    fp = open(filepath, 'a')
    # write to json file
    fp.write(js)
    # close the connection
    fp.close()


def read_json(filepath):
    with open(filepath) as f:
        read_dict = json.load(f)
    return read_dict

def get_pdf_base64(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf

def add_dict_to_session(dict_add, vals='all'):

    if vals == 'all':
        keys_list = dict_add.keys()
    else:
        keys_list = vals

    for key in keys_list:
        try:
            st.session_state[key] = dict_add[key]
        except:
            print('Error: Key not in cookies')

