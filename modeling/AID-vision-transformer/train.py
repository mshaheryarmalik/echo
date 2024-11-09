import os
import torch
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, Subset
from transformers import ViTForImageClassification, ViTFeatureExtractor, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from PIL import Image
from collections import defaultdict
import numpy as np

# Set device for macOS M-series GPU
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

# Path to the pre-downloaded dataset
dataset_path = "./AID"

# Number of samples per class to use for training
samples_per_class = 1  # Adjust this to your desired number of samples per class

# Load feature extractor for normalization values
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224-in21k')

# Prepare dataset with ImageFolder
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=feature_extractor.image_mean,
        std=feature_extractor.image_std
    )
])

# Load dataset
dataset = ImageFolder(root=dataset_path, transform=transform)

# Function to sample a fixed number of items per class
def get_balanced_subset_indices(dataset, samples_per_class):
    class_indices = defaultdict(list)
    for idx, (_, label) in enumerate(dataset):
        class_indices[label].append(idx)
    
    selected_indices = []
    for label, indices in class_indices.items():
        if len(indices) < samples_per_class:
            print(f"Warning: Not enough samples in class {label}. Using {len(indices)} samples.")
        selected_indices.extend(np.random.choice(indices, min(samples_per_class, len(indices)), replace=False))
    return selected_indices

# Get balanced subset indices
balanced_indices = get_balanced_subset_indices(dataset, samples_per_class)

# Create subsets for training and validation
train_idx, val_idx = train_test_split(balanced_indices, test_size=0.2, random_state=42)
train_dataset = Subset(dataset, train_idx)
val_dataset = Subset(dataset, val_idx)

# Load Vision Transformer model
model = ViTForImageClassification.from_pretrained(
    'google/vit-base-patch16-224-in21k',
    num_labels=len(dataset.classes)
)
model.to(device)

# Modified collate function for Trainer API
def collate_fn(batch):
    images, labels = zip(*batch)
    images = torch.stack(images)
    encodings = {
        'pixel_values': images.to(device),
        'labels': torch.tensor(labels).to(device)
    }
    return encodings

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',
    learning_rate=2e-4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=20,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model='eval_loss',
    save_strategy='epoch',
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=collate_fn,
)

# Train the model
trainer.train()

# Evaluate the model
evaluation_results = trainer.evaluate()
print(f"Evaluation Results: {evaluation_results}")

# Save the model and feature extractor for later use
save_directory = "./saved_model"
model.save_pretrained(save_directory)
feature_extractor.save_pretrained(save_directory)
print(f"Model saved to {save_directory}")

import json

# Save the class names
class_names = dataset.classes
with open("saved_model/class_names.json", "w") as f:
    json.dump(class_names, f)
print("Class names saved to 'saved_model/class_names.json'")
