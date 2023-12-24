# AnimalGates: Cat Breed Classification System

## Code Documentation

For detailed code documentation, refer to [Code Documentation](<https://drive.google.com/file/d/1i3etmYkegEtu6930kCCHAxDefadX393r/view?usp=sharing>).

## Setup Guide

To set up and run the project, follow the instructions in the [Setup Guide](<https://drive.google.com/file/d/1N5duG3M1jJXAS-8-FWE1XvjGWI0CA3hk/view?usp=sharing>).

## Problem Statement

In residential settings where pet cats have access to outdoor environments, there is a need for a smart, automated system that allows cats to enter and exit the home without human intervention, while ensuring home security and pet safety. Traditional pet doors provide a solution but lack the ability to discriminate between authorized pets and other animals or intruders, posing security risks. Additionally, manual doors require pet owners to constantly monitor and assist their pets' outdoor access, which is not always feasible.

## Project Overview

The AnimalGates project aims to address these issues by developing an intelligent, automated gate opening mechanism specifically designed for cats. This system will utilize a Passive Infrared (PIR) sensor connected to an Arduino board to detect the presence of a cat near the gate. Upon detection, the system will activate a Raspberry Pi, which will then execute a machine learning algorithm to confirm the identity of the cat. If the approaching animal is identified as the resident cat, the system will automatically open the gate to allow entry or exit, then securely close it afterwards. The system utilizes the Cats and Dogs Breeds Classification Oxford Dataset from Kaggle, which contains both cat and dog breeds. Our goal is to accurately identify and classify cat breeds while eliminating the dog data from the dataset.

## Data Preparation

To facilitate the training process, we implemented a Python script called `prepareData` in `trainModel.py`. This script automatically eliminates dog images and organizes the cat data into separate folders. The prepared data is crucial for training a robust model.

## Model Training

For the classification task, we employed a ResNet model. The `trainModel.py` script trains the model on the preprocessed cat data and provides insights into the training accuracy. The choice of ResNet ensures the model's ability to capture intricate features, leading to better performance in breed classification.

## Model Evaluation

To assess the model's performance, we created the `AnimalGateTesting.ipynb` notebook. This notebook compares the accuracy of our trained ResNet model with pre-existing pretrained models using the same dataset. This step helps validate the effectiveness of our custom model.

## Breed Detection

The `DetectCatModel` component of our system takes an image sample as input and prints the model's classification results to the console. This real-time detection capability is essential for the Animal Gate to make informed decisions based on the identified cat breed.

##Code Structure Overview :
-------------------------
* Import Statements: The code imports various libraries and modules required for image processing, image classification, and web application development.
* Flask Application Setup: The code initializes a Flask application.
* Image Capture: The code defines a function capture_image() that captures an image using the Raspberry Pi Camera and saves it to a specified filepath.
* Image Preprocessing: The code defines a function prepare_image() that preprocesses the input image for prediction. It resizes the image, converts it to a NumPy array, and expands the dimensions to match the input shape of the MobileNet model.
* Image Classification: The code defines a function classify_image() that performs image classification using the MobileNet model. It preprocesses the input image, feeds it to the MobileNet model, and returns the predicted results.
* Flask Route: The code defines a Flask route /classify that captures an image, performs image classification, and returns the top predicted category with its confidence as a JSON response.

## How to Use

To replicate our results, follow these steps:

1. Run `prepareData` in `trainModel.py` to organize and preprocess the cat data.
2. Execute `trainModel.py` to train the ResNet model and obtain training accuracy insights.
3. Use the `AnimalGateTesting.ipynb` notebook to compare the performance of our model with pretrained models.
4. Employ the `DetectCat` model component to perform real-time breed detection on image samples.

## Steps to execute 'DetectCat' :

(a)To run our application , the 1st and most important is to create python virtual environment and can be done using command { python3 -m venv /path_to_store_file/ }.

(b)Once the python virtual environment is created then we should activate the environment to run our application which can be done using command { source /path_to_store_file/bin/activate }.

(c)Then after, change the directory to the folder where "DetectCat.py" is located. 

(d) Now , compile the python file using command { python3 DetectCat.py }. Upon sucessful compilation open browser redirect to { ip_address:port_number/method_name }.
Here in our code 172.20.10.2 is ip_address, 5000 is port_number and classify is method_name. Change ip_address accordingly to which network is connected.
