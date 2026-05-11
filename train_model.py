import cv2
import os
from PIL import Image
import numpy as np

# Path to dataset
path = 'dataset'

# Create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load face detector
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Function to get images and labels
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')  # grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])

        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)

    return faceSamples, ids

print("Training faces...")

faces, ids = getImagesAndLabels(path)

recognizer.train(faces, np.array(ids))

# Save trained model
recognizer.write('trainer/trainer.yml')

print("Training completed successfully")