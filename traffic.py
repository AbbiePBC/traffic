import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir) -> tuple[list[np.ndarray], list[int]]:
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images = []
    labels = []
    for label in range(NUM_CATEGORIES):
        category_images = read_and_resize_images(os.path.join(data_dir, str(label)))
        images.extend(category_images)
        labels.extend([label] * len(category_images))

    return images, labels

def read_and_resize_images(data_dir) -> list[np.ndarray]:

    images = []
    for filename in os.listdir(data_dir):
        img = cv2.imread(os.path.join(data_dir, filename))
        img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
        images.append(img)

    return images

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Keras is an api that different machine learning algorithms access.
    # A sequential model is one where layers follow each other.
    model = tf.keras.models.Sequential()

    # Add a convolutional layer with 32 filters, each filter has a 3x3 kernel
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    model.add(tf.keras.layers.Flatten())


    # The number of layers and the types of layers you include in between are up to you.
    # You may wish to experiment with:
    #     different numbers of convolutional and pooling layers
    #     different numbers and sizes of filters for convolutional layers
    #     different pool sizes for pooling layers
    #     different numbers and sizes of hidden layers
    #     dropout layers to reduce overfitting

    # Add output layer with NUM_CATEGORIES units,
    # one for each of the traffic sign categories units
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid"))


    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
