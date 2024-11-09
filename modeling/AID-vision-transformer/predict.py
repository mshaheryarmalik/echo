import os
import torch
from transformers import ViTForImageClassification, ViTFeatureExtractor
from safetensors.torch import load_file
from PIL import Image
import torchvision.transforms as transforms
import json
from sklearn.metrics import accuracy_score

# Set device for macOS M-series GPU or CPU
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

# Load the model architecture
checkpoint_path = "./checkpoint-10000"
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

# Function to predict the label of an image
def predict_image(image_path):
    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")  # Ensure image is in RGB mode
    image = transform(image)  # Apply transformations
    image = image.unsqueeze(0)  # Add batch dimension (1, 3, 224, 224)
    image = image.to(device)
    
    # Run the image through the model
    with torch.no_grad():  # No need for gradients in inference
        outputs = model(pixel_values=image)
        logits = outputs.logits
        predicted_label = logits.argmax(-1).item()  # Get the predicted class index
    
    return predicted_label

# Function to test accuracy
def test_accuracy(data_dir, n):
    all_preds = []
    all_labels = []
    
    # Loop through each class folder
    for class_idx, class_name in enumerate(class_names):
        class_dir = os.path.join(data_dir, class_name)
        images = os.listdir(class_dir)[:n]  # Get the first `n` images in the class directory
        
        for image_name in images:
            image_path = os.path.join(class_dir, image_name)
            predicted_label = predict_image(image_path)
            
            # Append predicted and true labels
            all_preds.append(predicted_label)
            all_labels.append(class_idx)  # Use class index as the true label

    # Calculate accuracy
    accuracy = accuracy_score(all_labels, all_preds)
    print(f"Accuracy on {n} samples per class: {accuracy * 100:.2f}%")
    return accuracy

# Example usage
data_dir = "./AID"  # Replace with the path to your dataset directory containing class subfolders
n = 30  # Number of images to test per class
test_accuracy(data_dir, n)
