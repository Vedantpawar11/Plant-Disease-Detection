from pathlib import Path

# Project root
PROJECT_DIR = Path(__file__).resolve().parent.parent

# PlantVillage color dataset
DATASET_DIR = PROJECT_DIR / "PlantVillage-Dataset" / "raw" / "color"

print("Dataset location:")
print(DATASET_DIR)

# Check whether directory exists
if not DATASET_DIR.exists():
    print("\nERROR: Dataset directory not found!")
    exit()

# Get class folders
classes = sorted([
    folder for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
])

print("\nNumber of classes:", len(classes))

print("\nDisease classes:")

for i, folder in enumerate(classes):
    print(f"{i}: {folder.name}")

# Count images
print("\nImage count per class:")

total_images = 0

for folder in classes:

    images = [
        file for file in folder.iterdir()
        if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

    count = len(images)
    total_images += count

    print(f"{folder.name}: {count}")

print("\nTotal images:", total_images)