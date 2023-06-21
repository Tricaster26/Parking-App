import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

image_size = (320, 320)
batch_size = 128

train_ds = tf.keras.utils.image_dataset_from_directory(
    "ParksAreUs/Parking Finder Code/train",
    #only have one class
    labels='inferred',
    # entire folder is our set, no need to split
    validation_split=None,
    seed=123,
    image_size=image_size,
    batch_size=batch_size,
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    "ParksAreUs/Parking Finder Code/valid",
    labels=None,
    validation_split=None,
    seed=123,
    image_size=image_size,
    batch_size=batch_size,
)

import matplotlib.pyplot as plt

#crop and rotate images to account for randomness in google maps
aug_ds = keras.Sequential([
    layers.RandomCrop(180,180),
    layers.RandomRotation(0.5)
])

plt.figure(figsize=(10, 10))
for images, _ in train_ds.take(1):
    for i in range(9):
        aug_images = aug_ds(images)
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(aug_images[i].numpy().astype("uint8"))
        plt.axis("off")

train_ds = train_ds.map(lambda img , labels: (aug_ds(img), labels),num_parallel_calls=tf.data.AUTOTUNE)

def prepare(ds , shuffle = False, augment = False):
    if shuffle:
        ds = ds.shuffle(1000)
    #large dataset so lare batch size
    #ds= ds.batch(32)

    if augment:
      #augment the data
      ds = ds.map(lambda img, label: (aug_ds(img), label),num_parallel_calls=tf.data.AUTOTUNE)
     #prefetch to improve performance
    return ds.prefetch(buffer_size=tf.data.AUTOTUNE)

train_ds = prepare(train_ds, shuffle = True, augment = True)
val_ds = prepare(val_ds)

model = tf.keras.Sequential([
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(2)
])
