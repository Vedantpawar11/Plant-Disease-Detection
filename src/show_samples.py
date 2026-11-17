from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import random

# Project root
PROJECT_DIR = Path(__file__).resolve().parent.parent

# PlantVillage color dataset
DATASET_DIR = PROJECT_DIR / "PlantVillage-Dataset" / "raw" / "color"

print("Dataset location:")
print(DATASET_DIR)

if not DATASET_DIR.exists():
    print("ERROR: Dataset directory not found!")
    exit()

# Get class folders
classes = [
    folder for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
]

print("Number of classes:", len(classes))

# Select 9 random classes
selected_classes = random.sample(
    classes,
    min(9, len(classes))
)

plt.figure(figsize=(12, 10))

for i, class_folder in enumerate(selected_classes):

    images = [
        file for file in class_folder.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

    if not images:
        continue

    image_path = random.choice(images)

    image = Image.open(image_path)

    plt.subplot(3, 3, i + 1)
    plt.imshow(image)
    plt.title(class_folder.name, fontsize=8)
    plt.axis("off")

plt.tight_layout()
plt.show()