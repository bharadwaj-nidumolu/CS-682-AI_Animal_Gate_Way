import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import imagenet_utils
from PIL import Image
import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

image_path = '/home/pi/Desktop/capture_image'
image_file_name = 'captured_image.jpg'
filepath = os.path.join(image_path,image_file_name)

# Load MobileNet model
mobileNetModel = tf.keras.applications.mobilenet.MobileNet()

# Function to prepare image for prediction
def prepare_image(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

# Function to perform image classification
def classify_image(img):
    preprocessed_image = prepare_image(img)
    results = mobileNetModel.predict(preprocessed_image)
    return results

# Function to capture an image using Raspberry Pi Camera
def capture_image():
    cap_img = ["libcamera-still","-0",filepath]
    try:
        subprocess.run(cap_img,check=True)
	print(f"Saved image to {filepath}")
    except subprocess.CalledProcessError as e:
	print(f"An error occurred:{e}")
    return image_path

# Route to capture image, classify it, and display the result
@app.route('/classify', methods=['GET'])
def classify():
    capture_image()
    img = Image.open(image_path + image_file_name)
    result = classify_image(img)
    decoded_result = imagenet_utils.decode_predictions(result)
    serializable_results = []
    for category in decoded_result[0]:  # Assuming batch size of 1
        category_dict = {
            'name': category[1],
            'confidence': float(category[2])  # Convert numpy float32 to Python float
        }
        serializable_results.append(category_dict)

    return jsonify(serializable_results[0])


if __name__ == '__main__':
    app.run(debug=True, host='172.20.10.2', port=5000) # ip_address & port number