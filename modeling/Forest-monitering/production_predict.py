import joblib
import numpy as np
import cv2
from PIL import Image
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

# Load the saved model and pre-trained scaler/binarizer if available
model_filename = "multilabel_logistic_regression.pkl"
scaler_filename = "scaler.pkl"
binarizer_filename = "binarizer.pkl"

# Load the classifier model
clf = joblib.load(model_filename)

# Hard-code the labels if a pre-trained binarizer is unavailable
labels = [
    "agriculture", "clear", "habitation", "primary", "road", "partly_cloudy", 
    "slash_burn", "haze", "cultivation", "water", "cloudy", "blooming", 
    "selective_logging", "conventional_mine", "bare_ground", "blow_down", 
    "artisinal_mine"
]

# Load the binarizer or initialize it with hard-coded labels
try:
    lb = joblib.load(binarizer_filename)
except FileNotFoundError:
    lb = MultiLabelBinarizer(classes=labels)
    lb.fit([labels])  # Fit the binarizer with the full list of labels

# Load the pre-trained scaler or initialize a new one
try:
    scaler = joblib.load(scaler_filename)
except FileNotFoundError:
    scaler = MinMaxScaler()  # Fallback if a pre-trained scaler is unavailable

# Set rescaled_dim to 40 to match the feature size expected by the model
rescaled_dim = 40  # The dimension used during training

# Function to preprocess a PIL image
def preprocess_image(pil_image):
    # Convert PIL image to grayscale
    image = pil_image.convert("L")
    # Resize to match training dimensions (40x40 pixels)
    image_resized = image.resize((rescaled_dim, rescaled_dim), Image.LANCZOS)
    # Convert to numpy array and flatten to a single vector
    image_flattened = np.array(image_resized).reshape(1, -1)
    # Scale using the pre-fitted scaler
    image_scaled = scaler.transform(image_flattened)
    return image_scaled

# Function to classify an image
def classify_image(pil_image):
    # Preprocess the image
    X = preprocess_image(pil_image)
    # Predict the labels
    predictions = clf.predict(X)
    # Map the prediction to class labels
    predicted_labels = lb.inverse_transform(predictions)
    return predicted_labels

"""
Example usage with PIL image
"""
# Load an image as a PIL image
image_path = '../../../../sherry/input/test-jpg/test_20.jpg'
pil_image = Image.open(image_path)

# Classify the image
predicted_labels = classify_image(pil_image)
print(f"Predicted labels for the image: {predicted_labels}")
