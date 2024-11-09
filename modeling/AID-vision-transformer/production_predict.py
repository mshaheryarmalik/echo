import os
import torch
from transformers import ViTForImageClassification, ViTFeatureExtractor
from safetensors.torch import load_file
from PIL import Image
import torchvision.transforms as transforms
import json

# Set device for macOS M-series GPU or CPU
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

# Load the model architecture and checkpoint
# Please give path to model folder.
checkpoint_path = "../../../../checkpoint-10000"
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

# Function to predict the label of a PIL image
def predict_pil_image(pil_image):
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

# Example usage with a PIL image
# Load an example image (you can replace this with any PIL image object)

"""
USAGE
"""

# image_path = "../../../../AID/Bridge/bridge_3.jpg"
# pil_image = Image.open(image_path)
# predicted_label = predict_pil_image(pil_image)
# print(f"Predicted label: {predicted_label}")
