import torch
import torch.nn as nn

from torchvision.models import vit_b_16, ViT_B_16_Weights


# ============================================================
# CONFIGURATION
# ============================================================

NUM_CLASSES = 38


# ============================================================
# LOAD PRETRAINED VIT
# ============================================================

def create_model(num_classes=NUM_CLASSES, freeze_backbone=True):

    print("Loading pretrained ViT-B/16...")

    weights = ViT_B_16_Weights.DEFAULT

    model = vit_b_16(weights=weights)

    # --------------------------------------------------------
    # Freeze the pretrained backbone
    # --------------------------------------------------------

    if freeze_backbone:
        for parameter in model.parameters():
            parameter.requires_grad = False

    # --------------------------------------------------------
    # Replace ImageNet classifier
    #
    # Original:
    # 768 features -> 1000 classes
    #
    # New:
    # 768 features -> 38 classes
    # --------------------------------------------------------

    in_features = model.heads.head.in_features

    model.heads.head = nn.Linear(
        in_features,
        num_classes
    )

    return model


# ============================================================
# TEST MODEL
# ============================================================

if __name__ == "__main__":

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Device:", device)

    model = create_model(
        num_classes=38,
        freeze_backbone=True
    )

    model = model.to(device)

    print("\nModel created successfully.")

    # Count parameters
    total_params = sum(
        p.numel()
        for p in model.parameters()
    )

    trainable_params = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print("Total parameters:", total_params)
    print("Trainable parameters:", trainable_params)

    # --------------------------------------------------------
    # Test with one batch
    # --------------------------------------------------------

    dummy_input = torch.randn(
        2, 3, 224, 224
    ).to(device)

    with torch.no_grad():
        output = model(dummy_input)

    print("\nInput shape :", dummy_input.shape)
    print("Output shape:", output.shape)

    print("\nExpected output shape:")
    print("(2, 38)")