import sys
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import socket
import streamlit as st

dotenv_path = Path('/Users/adamklaus/.env')
load_dotenv(dotenv_path=dotenv_path)

CREDS = os.environ
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
LOCAL_DEV = 'C02G254GML7H'

MOD_ACCESS = {
    'home': {
    'button' : ''
    ,'name' : ''
    ,'description':''
    }

    ,'wnba_success': {
    'button' : '🏀 Predicting WNBA Success'
    ,'name' : 'wnba_success'
    ,'description':"Using college stats to predict which players would have successful WNBA careers"
    }

    ,'landscape_img': {
    'button' : '🏔️  Landscape Image Prediction'
    ,'name' : 'landscape_img'
    ,'description':'Predict the landscape of a given image using a convolutional neural network'
    }

    ,'random_ellipses': {
    'button' : '♾️ Random Ellipses'
    ,'name' : 'ellipses'
    ,'description':'Given two ellipses, determine their overlapping area with a pseudo random number generator'
    }

    ,'game_of_life': {
    'button' : '👾 Game of Life'
    ,'name' : 'game_of_life'
    ,'description':"Visualize preset and random simulations of Conway's game of life"
    }


    ,'happy_prime': {
    'button' : '🙂 Happy Prime'
    ,'name' : 'happy_prime'
    ,'description':'Calculator to determine whether an integer is happy or sad'
    }

    ,'bibliometrix_reference_cleaner': {
    'button' : '📚 Bibliometrix Reference Cleaner'
    ,'name' : 'bibliometrix_reference_cleaner'
    ,'description':'Canonicalize cited references for bibliometrix/Biblioshiny'
    }

    }
