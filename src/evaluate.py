
import torch
from pathlib import Path
from model import create_model
from dataset import test_loader, CLASS_NAMES

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "models" / "vit_b16_best.pth"

# Device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 50)
print("PLANT DISEASE DETECTION - MODEL EVALUATION")
print("=" * 50)

print("Device:", device)
print("Test images:", len(test_loader.dataset))

# Load model
model = create_model(
    num_classes=len(CLASS_NAMES),
    freeze_backbone=True
)

model.load_state_dict(
    torch.load(MODEL_PATH, map_location=device)
)

model = model.to(device)
model.eval()

# Evaluation
correct = 0
total = 0

with torch.no_grad():

    for batch_idx, (images, labels) in enumerate(test_loader):

        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)

        predictions = outputs.argmax(dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

        if (batch_idx + 1) % 50 == 0:
            print(
                f"Evaluated batch "
                f"{batch_idx + 1}/{len(test_loader)}"
            )

# Results
accuracy = 100 * correct / total

print("\n" + "=" * 50)
print("TEST RESULTS")
print("=" * 50)

print("Correct predictions:", correct)
print("Total images:", total)
print(f"Test Accuracy: {accuracy:.2f}%")

print("=" * 50)
