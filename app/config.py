import os
from dotenv import load_dotenv

load_dotenv()

CREDS = os.environ
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# Set this in your local environment to filter local analytics:
# export LOCAL_DEV_HOSTNAME="$(hostname)"
LOCAL_DEV = os.environ.get("LOCAL_DEV_HOSTNAME", "")

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
