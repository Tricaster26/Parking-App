import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

image_size = (180, 180)
batch_size = 128

train_ds = tf.keras.utils.image_dataset_from_directory(
    "ParksAreUs/Parking Finder Code/Parking_Dataset/test",
    #only have one class
    labels=None,
    # entire folder is our set, no need to split
    validation_split=None,
    seed=123,
    image_size=image_size,
    batch_size=batch_size,
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    "ParksAreUs/Parking Finder Code/Parking_Dataset/valid",
    labels=None,
    validation_split=None,
    seed=123,
    image_size=image_size,
    batch_size=batch_size,
)

import matplotlib.pyplot as plt

aug_ds = keras.Sequential([
    layers.Rescaling(1./255),
    layers.RandomRotation(0.2),
    layers.RandomRotation(0.7),
    layers.RandomFlip("horizontal_and_vertical"),
])

def model:
    
