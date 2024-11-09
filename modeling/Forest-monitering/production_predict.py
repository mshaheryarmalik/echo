import joblib
import numpy as np
import cv2
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

# Function to preprocess the image
def preprocess_image(image_bytes):
    # Convert byte array to numpy array
    np_array = np.frombuffer(image_bytes, np.uint8)
    # Decode the image as grayscale
    image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    # Resize to match training dimensions (40x40 pixels)
    image_resized = cv2.resize(image, (rescaled_dim, rescaled_dim), interpolation=cv2.INTER_LINEAR)
    # Flatten the image to a single vector
    image_flattened = image_resized.reshape(1, -1)
    # Scale using the pre-fitted scaler
    image_scaled = scaler.transform(image_flattened)
    return image_scaled

# Function to classify an image
def classify_image(image_bytes):
    # Preprocess the image
    X = preprocess_image(image_bytes)
    # Predict the labels
    predictions = clf.predict(X)
    # Map the prediction to class labels
    predicted_labels = lb.inverse_transform(predictions)
    return predicted_labels

"""
Example usage with image byte array
"""
# Load an image and convert it to byte array for testing
with open('../../../../sherry/input/test-jpg/test_20.jpg', 'rb') as f:
    image_bytes = f.read()

# Classify the image
predicted_labels = classify_image(image_bytes)
print(f"Predicted labels for the image: {predicted_labels}")
