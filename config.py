import sys
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import git
from git import Repo
sys.path.insert(1, os.path.join(sys.path[0], '..'))

dotenv_path = Path('/Users/adamklaus/.env')
load_dotenv(dotenv_path=dotenv_path)

CREDS = os.environ
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  


MOD_ACCESS = {
    'home': {
    'button' : ''
    ,'name' : ''
    ,'description':''
    }

    ,'wnba_success': {
    'button' : '🏀 Predicting WNBA Success'
    ,'name' : 'wnba_success'
    ,'description':"Visualize preset and random simulations of Conway's game of life"
    }

    ,'landscape_img': {
    'button' : '🏔️  Landscape Image Prediction'
    ,'name' : 'landscape_img'
    ,'description':'Predict the landscape of a given image using a convolutional neural network'
    }

    ,'happy_prime': {
    'button' : '🙂 Happy Prime'
    ,'name' : 'happy_prime'
    ,'description':'Calculator to determine whethern an integer is happy or sad'
    }

    ,'random_ellipses': {
    'button' : '♾️ Random Ellipses'
    ,'name' : 'random_ellipses'
    ,'description':'Given two ellipses, determine their overlapping area with a pseudo random number generator'
    }

    ,'game_of_life': {
    'button' : '👾 Game of Life'
    ,'name' : 'game_of_life'
    ,'description':"Visualize preset and random simulations of Conway's game of life"
    }
    }

