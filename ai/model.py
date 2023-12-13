import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
import os
import sys

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the extracted features and file names
features_array = np.load('./ai/chair_features.npy')
file_names_array = np.load('./ai/chair_file_names.npy')


# Function to extract features for a single image
def extract_features(img_path, model):
  img = image.load_img(img_path, target_size=(96, 96))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  img_array = preprocess_input(img_array)
  features = model.predict(img_array)
  return features.flatten()

# Function to recommend similar images and plot them
def recommend_and_plot_similar_images(query_img_path, features_array, file_names_array, top_k=5):

  # Folder containing chair images
  data_folder = 'img'

  model = tf.keras.models.load_model(os.path.join('', './ai/Model_DD'))

  query_features = extract_features(query_img_path, model)

  # Calculate cosine similarity between the query image and all other images
  similarities = cosine_similarity([query_features], features_array)[0]

  # Get indices of top-k similar images
  top_indices = np.argsort(similarities)[-top_k:][::-1]

  # Get file names of the top-k similar images
  top_images = file_names_array[top_indices]

  # Plot the query image
  # plt.figure(figsize=(10, 5))
  # plt.subplot(1, top_k + 1, 1)
  # plt.title('Query Image')
  # img = mpimg.imread(query_img_path)
  # plt.imshow(img)
  # plt.axis('off')

  # Plot the similar images
  for i, image_name in enumerate(top_images, start=1):
    # img_path = os.path.join(data_folder, image_name)
    print(image_name)
    # img = mpimg.imread(img_path)
    # plt.subplot(1, top_k + 1, i + 1)
    # plt.title(f'Similar Image {i}')
    # plt.imshow(img)
    # plt.axis('off')

    # plt.show()

# Example usage: Provide the path to the query image
# query_image_path = 'img/666.jpg'  # Adjust the path
query_image_path = sys.argv[1]
recommend_and_plot_similar_images(query_image_path, features_array, file_names_array)
# # Display the recommended similar images
# print(f"Recommended Similar Images for '{os.path.basename(query_image_path)}':")
# for i, image_name in enumerate(similar_images, start=1):
#     print(f"{i}. {image_name}")