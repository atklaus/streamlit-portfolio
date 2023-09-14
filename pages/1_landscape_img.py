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
import os
import lib.st_utils as stu
import os
import cv2
from tensorflow import keras
import numpy as np

@st.cache_resource(ttl=43200,show_spinner='Loading Model')
def init_model():
    return keras.models.load_model('img_model')


def image_to_tiles(img, tile_size=(150, 150), overlap=50):
    tiles = []
    stride = tile_size[0] - overlap
    for x in range(0, img.shape[1] - tile_size[1] + stride, stride):
        for y in range(0, img.shape[0] - tile_size[0] + stride, stride):
            tile = img[y:y+tile_size[0], x:x+tile_size[1]]
            if tile.shape[0] == tile_size[0] and tile.shape[1] == tile_size[1]:
                tiles.append(tile)
    return tiles

def predict_tiles(tiles, model):
    predictions = []
    for tile in tiles:
        prediction = model.predict(tile.reshape(-1,150,150,3))
        predictions.append(prediction)
    return np.array(predictions)

def combine_predictions(predictions):
    return predictions.mean(axis=0)


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

# Usage in your Streamlit code

page_header('Landscape Image Prediction')

stu.V_SPACE(1)
model = init_model()

st.subheader('Landscape Image Prediction')

uploaded_file = st.file_uploader("Choose an image")
if uploaded_file is not None:
# To read file as bytes:
    class_names = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']

    with st.spinner('Making prediction...'):
        bytes_data = uploaded_file.getvalue()
        img = cv2.imdecode(np.fromstring(bytes_data, np.uint8), cv2.IMREAD_UNCHANGED)
        # img = cv2.imread(bytes_data)
        # new_height = 150
        # new_width = 150
        # crop_img = center_crop(img, new_width, new_height)
        # # crop_img = img[0:150, 0:150] # Crop from {x, y, w, h } => {0, 0, 300, 400}
        # prediction = model.predict(crop_img.reshape(-1,150,150,3))
        # pred = class_names[prediction.argmax()]
        tiles = image_to_tiles(img,overlap=1)
        tile_predictions = predict_tiles(tiles, model)
        combined_prediction = combine_predictions(tile_predictions)
        pred = class_names[combined_prediction.argmax()]
    st.image(img, channels="BGR")
    st.info('Answer: **' + pred.upper() + '**')

with st.expander(label='Learn More'):
    if st.checkbox("Training Performance",key='expand_1'):
        pass
        # st.write("Hello world")
    # if st.checkbox("Fake expand2",key='expand_2'):
    #     st.markdown("1. Double click into a cell to edit")
    #     st.markdown("2. Hit enter or click away to store the change")
    #     st.markdown("3. Click submit and changes will be recorded")
    #     st.markdown("4. You can validate this update by reloading the page and seeing the values")

