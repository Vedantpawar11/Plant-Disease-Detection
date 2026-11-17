from pathlib import Path
import json
from collections import Counter

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = (
    PROJECT_DIR
    / "PlantVillage-Dataset"
    / "raw"
    / "color"
)

LEAF_MAP_FILE = (
    PROJECT_DIR
    / "PlantVillage-Dataset"
    / "leaf-map.json"
)

# --------------------------------------------------
# LOAD LEAF MAP
# --------------------------------------------------

print("Loading leaf-map.json...")

with open(LEAF_MAP_FILE, "r", encoding="utf-8") as f:
    leaf_map = json.load(f)

print("Leaf-map entries:", len(leaf_map))

# --------------------------------------------------
# FUNCTION USED TO CREATE LOOKUP KEY
# --------------------------------------------------

def get_image_identifier(filename):
    """
    Convert an image filename into the identifier
    used by leaf-map.json.
    """

    identifier = filename

    # Remove special suffix
    identifier = identifier.replace("_final_masked", "")

    # If filename contains ___, keep the last part
    if "___" in identifier:
        identifier = identifier.split("___")[-1]

    # Remove 'copy'
    identifier = identifier.split("copy")[0]

    # Remove extensions
    for ext in [".jpg", ".JPG", ".jpeg", ".JPEG",
                ".png", ".PNG"]:
        identifier = identifier.replace(ext, "")

    return identifier.strip().lower()


# --------------------------------------------------
# FIND ALL IMAGES
# --------------------------------------------------

print("\nScanning color dataset...")

all_images = []

for class_folder in DATASET_DIR.iterdir():

    if not class_folder.is_dir():
        continue

    for image_file in class_folder.iterdir():

        if image_file.suffix.lower() in [
            ".jpg",
            ".jpeg",
            ".png"
        ]:
            all_images.append(
                (class_folder.name, image_file)
            )

print("Total images found:", len(all_images))

# --------------------------------------------------
# MATCH IMAGES WITH LEAF MAP
# --------------------------------------------------

mapped = 0
unmapped = 0
ambiguous = 0

leaf_ids = []

unmapped_examples = []
ambiguous_examples = []

for class_name, image_file in all_images:

    identifier = get_image_identifier(
        image_file.name
    )

    if identifier not in leaf_map:

        unmapped += 1

        if len(unmapped_examples) < 20:
            unmapped_examples.append(
                str(image_file)
            )

        continue

    suggestions = leaf_map[identifier]

    # One mapping
    if len(suggestions) == 1:

        leaf_id = suggestions[0]

        mapped += 1
        leaf_ids.append(leaf_id)

    # Multiple mappings
    else:

        ambiguous += 1

        # Try to select mapping belonging
        # to the current class
        selected = None

        for suggestion in suggestions:

            if class_name in suggestion:
                selected = suggestion
                break

        if selected is not None:

            mapped += 1
            leaf_ids.append(selected)

        else:

            if len(ambiguous_examples) < 20:
                ambiguous_examples.append(
                    f"{class_name} -> {image_file.name}"
                )

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n==============================")
print("LEAF MAPPING RESULTS")
print("==============================")

print("Total images:", len(all_images))
print("Mapped images:", mapped)
print("Unmapped images:", unmapped)
print("Ambiguous mappings:", ambiguous)

# --------------------------------------------------
# UNIQUE LEAF IDS
# --------------------------------------------------

print("\nUnique leaf IDs:", len(set(leaf_ids)))

# --------------------------------------------------
# UNMAPPED EXAMPLES
# --------------------------------------------------

if unmapped_examples:

    print("\nFirst unmapped examples:")

    for item in unmapped_examples:
        print(item)

# --------------------------------------------------
# AMBIGUOUS EXAMPLES
# --------------------------------------------------

if ambiguous_examples:

    print("\nFirst ambiguous examples:")

    for item in ambiguous_examples:
        print(item)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n==============================")
print("SUMMARY")
print("==============================")

if unmapped == 0:

    print("SUCCESS: Every image was mapped.")

else:

    print(
        "WARNING:",
        unmapped,
        "images could not be mapped."
    )

print("\nNext step will be the leakage-safe split.")