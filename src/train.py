import random
from collections import defaultdict
import json
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset

from dataset import (
    train_loader,
    validation_loader,
    CLASS_NAMES,
)

# ============================================================
# CLASS-BALANCED DATASET FOR CPU TRAINING
# ============================================================

def get_balanced_indices(dataset, samples_per_class, seed=42):

    class_indices = defaultdict(list)

    for index, relative_path in enumerate(dataset.image_paths):
        class_name = Path(relative_path).parent.name
        class_indices[class_name].append(index)

    # Find the smallest class size
    min_available = min(
        len(class_indices[class_name])
        for class_name in CLASS_NAMES
    )

    # Automatically adjust samples per class
    actual_samples = min(samples_per_class, min_available)

    print("\nSmallest class size:", min_available)
    print("Selected images per class:", actual_samples)

    rng = random.Random(seed)
    selected_indices = []

    for class_name in CLASS_NAMES:

        available = class_indices[class_name]

        selected = rng.sample(available, actual_samples)
        selected_indices.extend(selected)

    rng.shuffle(selected_indices)

    return selected_indices

# Select balanced training images
train_indices = get_balanced_indices(
    train_loader.dataset,
    samples_per_class=132
)

# Select balanced validation images
val_indices = get_balanced_indices(
    validation_loader.dataset,
    samples_per_class=26
)

# Create subsets
train_subset = Subset(
    train_loader.dataset,
    train_indices
)

val_subset = Subset(
    validation_loader.dataset,
    val_indices
)

# Create DataLoaders
train_loader = DataLoader(
    train_subset,
    batch_size=32,
    shuffle=True,
    num_workers=0
)

validation_loader = DataLoader(
    val_subset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)

print("\nCLASS-BALANCED CPU DATASET")
print("Training images:", len(train_loader.dataset))
print("Validation images:", len(validation_loader.dataset))
print("Training images per class: 132")
print("Validation images per class: 26")

from model import create_model


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_DIR / "models"
RESULTS_DIR = PROJECT_DIR / "results"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODELS_DIR / "vit_b16_best.pth"
CLASSES_PATH = MODELS_DIR / "classes.json"
HISTORY_PATH = RESULTS_DIR / "training_history.json"

NUM_CLASSES = 38
EPOCHS = 1
LEARNING_RATE = 0.001

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("\n" + "=" * 60)
print("PLANT DISEASE DETECTION - ViT TRAINING")
print("=" * 60)

print("Device:", device)
print("Epochs:", EPOCHS)
print("Learning rate:", LEARNING_RATE)


# ============================================================
# VERIFY DATASET
# ============================================================

class_names = CLASS_NAMES

assert len(class_names) == NUM_CLASSES, (
    f"Expected {NUM_CLASSES} classes, found {len(class_names)}"
)

print("\nTraining images:", len(train_loader.dataset))
print("Validation images:", len(validation_loader.dataset))
print("Number of classes:", len(class_names))


# ============================================================
# SAVE CLASS NAMES
# ============================================================

with open(CLASSES_PATH, "w", encoding="utf-8") as f:
    json.dump(class_names, f, indent=4)

print("Class names saved:", CLASSES_PATH)


# ============================================================
# LOAD MODEL
# ============================================================

model = create_model(
    num_classes=NUM_CLASSES,
    freeze_backbone=True,
)

model = model.to(device)

trainable_parameters = sum(
    p.numel()
    for p in model.parameters()
    if p.requires_grad
)

print("\nModel loaded successfully.")
print("Trainable parameters:", trainable_parameters)


# ============================================================
# LOSS AND OPTIMIZER
# ============================================================

criterion = nn.CrossEntropyLoss()

optimizer = optim.AdamW(
    filter(
        lambda p: p.requires_grad,
        model.parameters(),
    ),
    lr=LEARNING_RATE,
    weight_decay=1e-4,
)


# ============================================================
# TRAIN ONE EPOCH
# ============================================================

def train_one_epoch():

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(train_loader):

        images = images.to(device)
        labels = labels.to(device)

        # Forward pass
        outputs = model(images)

        # Calculate loss
        loss = criterion(outputs, labels)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Calculate statistics
        batch_size = labels.size(0)

        running_loss += loss.item() * batch_size

        predictions = outputs.argmax(dim=1)

        correct += (predictions == labels).sum().item()
        total += batch_size

        if (batch_idx + 1) % 50 == 0:
            print(
                f"Training batch "
                f"{batch_idx + 1}/{len(train_loader)} "
                f"| Loss: {loss.item():.4f}"
            )

    epoch_loss = running_loss / total
    epoch_accuracy = 100.0 * correct / total

    return epoch_loss, epoch_accuracy


# ============================================================
# VALIDATION
# ============================================================

def validate():

    model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():

        for batch_idx, (images, labels) in enumerate(validation_loader):

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(outputs, labels)

            batch_size = labels.size(0)

            running_loss += loss.item() * batch_size

            predictions = outputs.argmax(dim=1)

            correct += (predictions == labels).sum().item()
            total += batch_size

            if (batch_idx + 1) % 50 == 0:
                print(
                    f"Validation batch "
                    f"{batch_idx + 1}/{len(validation_loader)}"
                )

    val_loss = running_loss / total
    val_accuracy = 100.0 * correct / total

    return val_loss, val_accuracy


# ============================================================
# TRAINING LOOP
# ============================================================

best_val_accuracy = -1.0

history = {
    "train_loss": [],
    "train_accuracy": [],
    "val_loss": [],
    "val_accuracy": [],
}

start_time = time.time()

print("\nStarting training...\n")

for epoch in range(EPOCHS):

    print("\n" + "=" * 60)
    print(f"EPOCH {epoch + 1}/{EPOCHS}")
    print("=" * 60)

    epoch_start = time.time()

    # Training
    train_loss, train_accuracy = train_one_epoch()

    # Validation
    val_loss, val_accuracy = validate()

    # Save history
    history["train_loss"].append(train_loss)
    history["train_accuracy"].append(train_accuracy)
    history["val_loss"].append(val_loss)
    history["val_accuracy"].append(val_accuracy)

    epoch_time = time.time() - epoch_start

    print("\nEpoch results:")
    print(f"Training loss       : {train_loss:.4f}")
    print(f"Training accuracy   : {train_accuracy:.2f}%")
    print(f"Validation loss     : {val_loss:.4f}")
    print(f"Validation accuracy : {val_accuracy:.2f}%")
    print(f"Epoch duration      : {epoch_time / 60:.2f} minutes")

    # Save best model
    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            model.state_dict(),
            MODEL_PATH,
        )

        print("\nBest model checkpoint saved:")
        print(MODEL_PATH)

    # Save history after each epoch
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


# ============================================================
# TRAINING COMPLETED
# ============================================================

total_time = time.time() - start_time

print("\n" + "=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)

print(f"Best validation accuracy: {best_val_accuracy:.2f}%")
print(f"Total training time: {total_time / 60:.2f} minutes")

print("\nGenerated files:")
print("Model:", MODEL_PATH)
print("Classes:", CLASSES_PATH)
print("History:", HISTORY_PATH)

print("\nNext step: evaluate the saved model on the test dataset.")