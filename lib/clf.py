# Load the test_pred data (which has no target labels)
import os
import cv2
from tensorflow import keras
import numpy as np
model = keras.models.load_model('img_model')


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

filename = '/Users/adamklaus/Downloads/IMG_5828.jpeg'
result_dict = {} # dictionary to store predictions (keyed by file number)
img = cv2.imread(filename)
new_height = 150
new_width = 150
crop_img = center_crop(img, new_width, new_height)
# crop_img = img[0:150, 0:150] # Crop from {x, y, w, h } => {0, 0, 300, 400}
prediction = model.predict(crop_img.reshape(-1,150,150,3))
class_names = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']
class_names[prediction.argmax()]

