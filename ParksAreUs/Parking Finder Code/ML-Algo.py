import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

image_size = (320, 320)
batch_size = 128

train_ds = tf.keras.utils.image_dataset_from_directory(
    "ParksAreUs/Parking Finder Code/Parking_Dataset/train",
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
    layers.RandomCrop(180,180)
])

plt.figure(figsize=(10, 10))
for images in train_ds.take(1):
    for i in range(9):
        aug_images = aug_ds(images)
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(aug_images[i].numpy().astype("uint8"))
        plt.axis("off")

train_ds = train_ds.map(lambda img: (aug_ds(img)),num_parallel_calls=tf.data.AUTOTUNE)
train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
def model:
