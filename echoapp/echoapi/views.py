from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
import requests

### ML related libraries
import os
import io
import torch
from transformers import ViTForImageClassification, ViTFeatureExtractor
from safetensors.torch import load_file
from PIL import Image
import torchvision.transforms as transforms

import joblib
import numpy as np
import cv2
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create your views here.

# Set device for macOS M-series GPU or CPU
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

# Load the model architecture and checkpoint
# Please give path to model folder.
checkpoint_path = "../../my-gcs-bucket/checkpoint-10000/"
num_classes = 30  # Adjust this to match your dataset's number of classes
model = ViTForImageClassification.from_pretrained(
    "google/vit-base-patch16-224-in21k",
    num_labels=num_classes
)

# Load weights from `model.safetensors`
state_dict = load_file(os.path.join(checkpoint_path, "model.safetensors"))
model.load_state_dict(state_dict, strict=False)
model.to(device)
model.eval()  # Set model to evaluation mode

# Load the feature extractor
feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")

# Load class names
with open(os.path.join(checkpoint_path, "class_names.json"), "r") as f:
    class_names = json.load(f)

# Transformation to resize, convert to tensor, and normalize the image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=feature_extractor.image_mean,
        std=feature_extractor.image_std
    )
])

API_KEY = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"

@csrf_exempt
def get_emad(request):
    """API view to handle the request for fetching map images."""
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            center_lat = data.get('latitude')
            center_lon = data.get('longitude')

            if not center_lat or not center_lon:
                return JsonResponse({'error': 'Missing latitude, longitude, or API key'}, status=400)
            
            images = fetch_images(center_lat, center_lon, API_KEY)


            # Forest-related labels
            forest_labels_aid_guide = [
                "Forest",
                "Park",      # Conditionally includes forested areas
                "Farmland",  # May include some tree cover, but primarily agricultural
                "Meadow"     # Open grassland, sometimes bordering forest
            ]

            # Non-forest labels
            non_forest_labels_aid_guide = [
                "Center", "Airport", "Beach", "BareLand", "BaseballField",
                "Bridge", "Church", "Commercial", "DenseResidential", "Desert",
                "Industrial", "MediumResidential", "Parking", "Playground",
                "RailwayStation", "Resort", "School", "Square", "Stadium",
                "StorageTanks", "Viaduct"
            ]

            aid_labels = []
            for img in images:
                aid_labels.append(predict_pil_image(img))

            aid_forest = []
            aid_non_forest = []

            for index, aid in enumerate(aid_labels):
                if aid in forest_labels_aid_guide:
                    aid_forest.append((index, aid))
                elif aid in non_forest_labels_aid_guide:
                    aid_non_forest.append((index, aid))

            # image_path = '../../../../sherry/input/test-jpg/test_20.jpg'  # Replace with the path to your image
            
            forest_labels = []
            for index, label in aid_forest:
                forest_labels.extend(classify_image(images[index]))
                #print(f"Predicted labels for the image: {forest_labels}")

            
            # forest_labels = []
            # for img in images:
            #     forest_labels.extend(classify_image(img))
            #     #print(f"Predicted labels for the image: {forest_labels}")

            metadata_str = get_google_maps_response_as_string(center_lat, center_lon, API_KEY)

            report_openai = generate_satellite_report(aid_forest, aid_non_forest, forest_labels, metadata_str, provider="openai")
            
            data = {
                'status': 'success',
                'message': 'Data fetched successfully!',
                'data': {'count_images': len(images), 'aid_labels_forest': aid_forest, 'aid_labels_non_forest':aid_non_forest, 'forest_labels': forest_labels, 'info': metadata_str, 'report': report_openai}
            }
    
            return JsonResponse(data)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

def generate_satellite_report(aid_labels, aid_non_forest, forest_conditions, location, provider="ollama", api_url=None):
    # Prepare the prompt dynamically
    prompt = f"""
    You are an assistant specialized in generating insightful, fact-based reports on forest health. Your task is to produce a clear, structured, and engaging report on the forest conditions in the specified area based on satellite image data. Avoid using exact technical labels; instead, describe findings in a way that is accessible and informative. Any important facts, percentages, or numerical data should be highlighted in **bold** for emphasis. The data provided includes:
    
    1. **Forest Classification Labels**: {aid_labels} (descriptions of forested areas derived from 16 satellite images).
    2. **Non-Forest Classification Labels**: {aid_non_forest} (descriptions of non-forested areas).
    3. **Forest Condition Details**: {forest_conditions} (indicators of forest health, where certain labels like "primary" suggest strong forest vitality, and others provide context such as cloud cover, haze, water presence, roads, etc.).
    4. **Location Details**: {location} (geographic and environmental characteristics relevant to this region).
    
    Considering the specific environmental and geographical characteristics of this area, the report should include:
    - A factual overview of the forest conditions, summarizing the overall health, density, and key observations about the forested areas.
    - A detailed analysis of forest health, using descriptive language (e.g., "dense green cover" or "fragmented patches") to communicate forest status without raw model labels.
    - Commentary on geographic and environmental influences (e.g., climate, nearby urban areas, water bodies) that may affect the forest health and ecosystem balance.
    - Identification of any noticeable trends, patterns, or anomalies in the data, especially regarding environmental concerns like deforestation or signs of robust forest growth.
    - Practical recommendations tailored to this location, with specific steps that can support forest health and carbon storage, if possible. Ensure that recommendations are based strictly on provided data and avoid any speculation or hallucination.

    **Note**: This report is based on satellite image data. Use only the information provided, avoid assumptions, and ensure a professional, factual, and structured presentation. Remember to highlight significant percentages, numbers, and key findings in **bold** to enhance readability and emphasis.
    """


    
    # Set up the request payload based on the provider
    if provider == "ollama":
        if api_url is None:
            api_url = "http://localhost:11434/v1/chat/completions"
        
        data = {
            "model": "gpt-4-turbo",  # Adjust model name as needed for Ollama
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3000,
            "temperature": 0.5
        }
        
        # Send request to Ollama API
        response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        
    elif provider == "openai":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please add it to the .env file.")
        
        api_url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": "gpt-3.5-turbo",  # Adjust model name as needed
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.5
        }
        
        # Send request to OpenAI API
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
    
    else:
        raise ValueError("Invalid provider. Choose either 'ollama' or 'openai'.")
    
    # Check if the response was successful
    if response.status_code == 200:
        result = response.json()
        # Extract and return the generated report
        report = result["choices"][0]["message"]["content"]
        return report
    else:
        # Return error message if the request failed
        return f"Error {response.status_code}: {response.text}"

# Load the saved model and pre-trained scaler/binarizer if available
model_filename = "../modeling/Forest-monitoring/multilabel_logistic_regression.pkl"
scaler_filename = "../modeling/Forest-monitoring/scaler.pkl"
binarizer_filename = "../modeling/Forest-monitoring/binarizer.pkl"

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
def classify_image(image_bytes):
    # Convert bytes to PIL image
    pil_image = bytes_to_pil_image(image_bytes)
    # Preprocess the image
    X = preprocess_image(pil_image)
    # Predict the labels
    predictions = clf.predict(X)
    # Map the prediction to class labels
    predicted_labels = lb.inverse_transform(predictions)
    return predicted_labels

# Function to convert bytes to PIL image
def bytes_to_pil_image(image_bytes):
    return Image.open(io.BytesIO(image_bytes))


# Function to predict the label of a PIL image
def predict_pil_image(image_bytes):
    # Convert bytes to PIL image
    pil_image = bytes_to_pil_image(image_bytes)
    
    # Ensure image is in RGB mode
    image = pil_image.convert("RGB")
    
    # Apply transformations
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension (1, 3, 224, 224)
    image = image.to(device)
    
    # Run the image through the model
    with torch.no_grad():  # No need for gradients in inference
        outputs = model(pixel_values=image)
        logits = outputs.logits
        predicted_label = logits.argmax(-1).item()  # Get the predicted class index
    
    # Map class index to class label
    label = class_names[predicted_label]
    
    return label

    
def get_image_url(lat, lon, zoom, size, api_key):
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}x{size}&maptype=satellite&key={api_key}"

def fetch_images(center_lat, center_lon, api_key):
    urls = []
    latitude_offset = 0.09  # Approximate offset in degrees for 10 km (latitude)
    longitude_offset = 0.09  # Approximate offset in degrees for 10 km (longitude)
    zoom = 13               # Adjusted for larger area coverage
    size = 200              # Size of each image tile in pixels

    for i in range(-1, 3):  # For 4x4 grid around center point
        for j in range(-1, 3):
            lat = center_lat + (i * latitude_offset)
            lon = center_lon + (j * longitude_offset)
            url = get_image_url(lat, lon, zoom, size, api_key)
            urls.append(url)

    images = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            images.append(response.content)  # Add image data to the list
        else:
            print(f"Failed to fetch image at {url}")

    return images

def get_google_maps_response_as_string(latitude, longitude, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"
    response = requests.get(url)
    
    # Convert the response JSON into a string
    response_str = json.dumps(response.json(), indent=2)
    
    return response_str

# Example usage
#api_key = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"
#center_lat = 37.7749  # Replace with actual latitude from frontend
#center_lon = -122.4194  # Replace with actual longitude from frontend

#images = fetch_images(center_lat, center_lon, api_key)
#print(images[0])

# 'images' now contains the raw image data for each tile, which you can assemble into a 4x4 grid.

"""
from PIL import Image
import requests
from io import BytesIO

def get_image_url(lat, lon, zoom, size, api_key):
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}x{size}&maptype=satellite&key={api_key}"

def fetch_images(center_lat, center_lon, api_key):
    urls = []
    latitude_offset = 0.09
    longitude_offset = 0.09
    zoom = 13
    size = 200
    
    for i in range(-1, 3):
        for j in range(-1, 3):
            lat = center_lat + (i * latitude_offset)
            lon = center_lon + (j * longitude_offset)
            url = get_image_url(lat, lon, zoom, size, api_key)
            urls.append(url)
    
    images = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            images.append(img)
        else:
            print(f"Failed to fetch image at {url}")
    
    return images

def create_grid(images, grid_size=4, tile_size=(200, 200)):
    grid_image = Image.new('RGB', (tile_size[0] * grid_size, tile_size[1] * grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            img = images[i * grid_size + j]
            img = img.resize(tile_size)  # Ensure each tile is the same size
            print(img)
            grid_image.paste(img, (j * tile_size[0], i * tile_size[1]))
    
    return grid_image

# Example usage
api_key = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"
center_lat = 66.5078
center_lon = 25.7235

# Fetch and display images
images = fetch_images(center_lat, center_lon, api_key)
grid_image = create_grid(images)
grid_image.show()  # Opens the image in the default viewer

# Optionally, save the grid image
grid_image.save("map_grid.png")
"""

#api_key = "AIzaSyAT4zq4L_N2NpYXEqz4GCIm_7ojscrB5rA"
