import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path
from config import BASE_DIR, CREDS
from layout.header import page_header
import datetime
from datetime import date, datetime
from dateutil import tz
import git
import os
import lib.st_utils as stu
import os
import cv2
from tensorflow import keras
import numpy as np
import pickle

@st.experimental_singleton(suppress_st_warning=True, show_spinner=False)
def init_model():
    with open('wnba_success.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    return loaded_model
    
model = init_model()

# Load the model from the file

