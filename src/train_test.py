import torch
import torch.nn as nn
import torch.optim as optim

from src.dataset import train_loader
from src.model import create_model


# ============================================================
# DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)


# ============================================================
# MODEL
# ============================================================

model = create_model(
    num_classes=38,
    freeze_backbone=True
)

model = model.to(device)


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# OPTIMIZER
# ============================================================

optimizer = optim.AdamW(
    filter(
        lambda p: p.requires_grad,
        model.parameters()
    ),
    lr=1e-3,
    weight_decay=1e-4
)


# ============================================================
# TEST TRAINING
# ============================================================

model.train()

num_batches = 5

print("\nStarting training test...")
print("Testing", num_batches, "batches.\n")


for batch_idx, (images, labels) in enumerate(train_loader):

    if batch_idx >= num_batches:
        break

    images = images.to(device)
    labels = labels.to(device)

    # --------------------------------------------------------
    # Forward pass
    # --------------------------------------------------------

    outputs = model(images)

    # --------------------------------------------------------
    # Calculate loss
    # --------------------------------------------------------

    loss = criterion(outputs, labels)

    # --------------------------------------------------------
    # Backpropagation
    # --------------------------------------------------------

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    predictions = outputs.argmax(dim=1)

    correct = (predictions == labels).sum().item()

    accuracy = correct / labels.size(0)

    print(
        f"Batch {batch_idx + 1}/{num_batches} | "
        f"Loss: {loss.item():.4f} | "
        f"Accuracy: {accuracy * 100:.2f}%"
    )


print("\nTraining test completed successfully.")