import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset

from src.data.dataloader import create_dataloaders
from src.models.vit_scratch import ViTScratch


# ==========================================================
# Configuration
# ==========================================================

BATCH_SIZE = 8
STEPS = 100
LEARNING_RATE = 1e-3

DEVICE = (
    torch.device("mps")
    if torch.backends.mps.is_available()
    else torch.device("cpu")
)


# ==========================================================
# Dataset
# ==========================================================

train_loader, _, _ = create_dataloaders(
    batch_size=BATCH_SIZE
)

# On garde seulement 32 images
dataset = Subset(
    train_loader.dataset,
    range(32)
)

loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)


# ==========================================================
# Model
# ==========================================================

model = ViTScratch(
    patch_size=16,
    num_classes=200
).to(DEVICE)


# ==========================================================
# Loss + optimizer
# ==========================================================

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=0
)


# ==========================================================
# Training
# ==========================================================

print("=" * 60)
print("ViT OVERFIT TEST")
print("=" * 60)

model.train()

for step in range(STEPS):

    total_loss = 0
    correct = 0
    total = 0

    for images, labels in loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        total_loss += loss.item() * images.size(0)

        predictions = outputs.argmax(dim=1)

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    accuracy = correct / total

    if (step + 1) % 10 == 0:

        print(
            f"Step [{step + 1}/{STEPS}] "
            f"| Loss: {total_loss / total:.4f} "
            f"| Acc: {accuracy:.4f}",
            flush=True
        )


print("=" * 60)
print("OVERFIT TEST TERMINÉ")
print("=" * 60)

