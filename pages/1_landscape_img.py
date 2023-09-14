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

# @st.experimental_singleton(suppress_st_warning=True, show_spinner=False)
def init_model():
    return keras.models.load_model('img_model')

page_header('Almost Data Science')

model = init_model()

def center_crop(img, new_width=None, new_height=None):        

    width = img.shape[1]
    height = img.shape[0]

    if new_width is None:
        new_width = min(width, height)

    if new_height is None:
        new_height = min(width, height)

    left = int(np.ceil((width - new_width) / 2))
    right = width - int(np.floor((width - new_width) / 2))

    top = int(np.ceil((height - new_height) / 2))
    bottom = height - int(np.floor((height - new_height) / 2))

    if len(img.shape) == 2:
        center_cropped_img = img[top:bottom, left:right]
    else:
        center_cropped_img = img[top:bottom, left:right, ...]

    return center_cropped_img


st.title('Landscape Image Prediction')

uploaded_file = st.file_uploader("Choose an image")
if uploaded_file is not None:
# To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    img = cv2.imdecode(np.fromstring(bytes_data, np.uint8), cv2.IMREAD_UNCHANGED)
    # img = cv2.imread(bytes_data)
    new_height = 150
    new_width = 150
    crop_img = center_crop(img, new_width, new_height)
    # crop_img = img[0:150, 0:150] # Crop from {x, y, w, h } => {0, 0, 300, 400}
    prediction = model.predict(crop_img.reshape(-1,150,150,3))
    class_names = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']
    pred = class_names[prediction.argmax()]
    st.image(crop_img, channels="BGR")
    st.info('Answer: ' + pred.upper())

with st.expander(label='Learn More'):
    if st.checkbox("Training Performance",key='expand_1'):
        pass
        # st.write("Hello world")
    # if st.checkbox("Fake expand2",key='expand_2'):
    #     st.markdown("1. Double click into a cell to edit")
    #     st.markdown("2. Hit enter or click away to store the change")
    #     st.markdown("3. Click submit and changes will be recorded")
    #     st.markdown("4. You can validate this update by reloading the page and seeing the values")

