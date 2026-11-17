from pathlib import Path
import json
import random
from collections import defaultdict, Counter

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

TRAIN_FILE = PROJECT_DIR / "splits" / "color_train.txt"
TEST_FILE = PROJECT_DIR / "splits" / "color_test.txt"
LEAF_MAP_FILE = PROJECT_DIR / "PlantVillage-Dataset" / "leaf-map.json"

OUTPUT_TRAIN = PROJECT_DIR / "splits" / "train.txt"
OUTPUT_VAL = PROJECT_DIR / "splits" / "validation.txt"

VAL_RATIO = 0.20
RANDOM_SEED = 42

# ============================================================
# LOAD FILES
# ============================================================

print("=" * 60)
print("PlantVillage Split Preparation")
print("=" * 60)

train_paths = TRAIN_FILE.read_text(encoding="utf-8").splitlines()
test_paths = TEST_FILE.read_text(encoding="utf-8").splitlines()

with open(LEAF_MAP_FILE, "r", encoding="utf-8") as f:
    leaf_map = json.load(f)

print(f"Official training images : {len(train_paths)}")
print(f"Official test images     : {len(test_paths)}")
print(f"Leaf-map entries         : {len(leaf_map)}")

# ============================================================
# BASIC VALIDATION
# ============================================================

train_set = set(train_paths)
test_set = set(test_paths)

print("\nChecking overlap...")

overlap = train_set & test_set

print(f"Train/Test overlap       : {len(overlap)}")

if overlap:
    raise RuntimeError(
        "ERROR: Some images occur in both train and test!"
    )

# ============================================================
# GROUP TRAINING IMAGES BY CLASS
# ============================================================

class_to_images = defaultdict(list)

for path in train_paths:
    parts = Path(path).parts

    # Expected:
    # raw / color / CLASS_NAME / IMAGE.JPG
    if len(parts) < 4:
        print("Skipping malformed path:", path)
        continue

    class_name = parts[-2]

    class_to_images[class_name].append(path)

print(f"\nNumber of classes: {len(class_to_images)}")

# ============================================================
# DISPLAY CLASS COUNTS
# ============================================================

print("\nImages per class:")
print("-" * 60)

for class_name in sorted(class_to_images):
    print(f"{class_name:<60} {len(class_to_images[class_name])}")

# ============================================================
# CREATE STRATIFIED TRAIN/VALIDATION SPLIT
# ============================================================

random.seed(RANDOM_SEED)

final_train = []
validation = []

print("\nCreating validation split...")

for class_name, images in sorted(class_to_images.items()):

    images = images.copy()

    random.shuffle(images)

    val_count = round(len(images) * VAL_RATIO)

    # Make sure every class has at least one training image
    if val_count >= len(images):
        val_count = len(images) - 1

    val_images = images[:val_count]
    train_images = images[val_count:]

    validation.extend(val_images)
    final_train.extend(train_images)

# ============================================================
# SHUFFLE FINAL LISTS
# ============================================================

random.shuffle(final_train)
random.shuffle(validation)

# ============================================================
# CHECK OVERLAP
# ============================================================

final_train_set = set(final_train)
validation_set = set(validation)

print("\nChecking generated splits...")

print("Training images   :", len(final_train))
print("Validation images :", len(validation))
print("Test images       :", len(test_paths))

print("Train/Validation overlap:",
      len(final_train_set & validation_set))

print("Train/Test overlap:",
      len(final_train_set & test_set))

print("Validation/Test overlap:",
      len(validation_set & test_set))

# ============================================================
# SAVE
# ============================================================

OUTPUT_TRAIN.write_text(
    "\n".join(final_train) + "\n",
    encoding="utf-8"
)

OUTPUT_VAL.write_text(
    "\n".join(validation) + "\n",
    encoding="utf-8"
)

print("\nFiles created:")
print(" ", OUTPUT_TRAIN)
print(" ", OUTPUT_VAL)

# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL SPLIT SUMMARY")
print("=" * 60)

total = len(final_train) + len(validation) + len(test_paths)

print(f"Training   : {len(final_train)}")
print(f"Validation : {len(validation)}")
print(f"Test       : {len(test_paths)}")
print(f"Total      : {total}")

print("=" * 60)
print("Done!")
print("=" * 60)