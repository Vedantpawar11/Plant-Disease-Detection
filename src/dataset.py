from pathlib import Path
from PIL import Image

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_DIR / "PlantVillage-Dataset" / "raw" / "color"
SPLITS_DIR = PROJECT_DIR / "splits"


# ============================================================
# CLASS NAMES
# ============================================================

CLASS_NAMES = sorted([
    p.name for p in DATASET_DIR.iterdir()
    if p.is_dir()
])

CLASS_TO_IDX = {
    class_name: idx
    for idx, class_name in enumerate(CLASS_NAMES)
}


# ============================================================
# TRANSFORMS
# ============================================================

# Training augmentation
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# Validation/Test transform
eval_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# DATASET CLASS
# ============================================================

class PlantVillageDataset(Dataset):

    def __init__(self, split_file, transform=None):

        self.split_file = Path(split_file)
        self.transform = transform

        # Read image paths
        self.image_paths = (
            self.split_file
            .read_text(encoding="utf-8")
            .splitlines()
        )

        # Remove empty lines
        self.image_paths = [
            path.strip()
            for path in self.image_paths
            if path.strip()
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):

        relative_path = self.image_paths[index]

        image_path = PROJECT_DIR / "PlantVillage-Dataset" / relative_path

        # Load image
        image = Image.open(image_path).convert("RGB")

        # Extract class name
        class_name = Path(relative_path).parent.name

        # Convert class name to integer
        label = CLASS_TO_IDX[class_name]

        # Apply transformation
        if self.transform:
            image = self.transform(image)

        return image, label


# ============================================================
# CREATE DATASETS
# ============================================================

train_dataset = PlantVillageDataset(
    SPLITS_DIR / "train.txt",
    transform=train_transform
)

validation_dataset = PlantVillageDataset(
    SPLITS_DIR / "validation.txt",
    transform=eval_transform
)

test_dataset = PlantVillageDataset(
    SPLITS_DIR / "color_test.txt",
    transform=eval_transform
)


# ============================================================
# CREATE DATALOADERS
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,
    num_workers=0
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)


# ============================================================
# INFORMATION
# ============================================================

print("Number of classes:", len(CLASS_NAMES))

print("\nClasses:")

for idx, class_name in enumerate(CLASS_NAMES):
    print(f"{idx}: {class_name}")

print("\nDataset sizes:")
print("Training   :", len(train_dataset))
print("Validation :", len(validation_dataset))
print("Test       :", len(test_dataset))