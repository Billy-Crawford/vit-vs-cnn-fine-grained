import torch

from src.data.dataloader import create_dataloaders
from src.models.vit_pretrained import ViTPretrained
from src.train.trainer import Trainer


# ==========================================================
# Configuration
# ==========================================================

BATCH_SIZE = 32
EPOCHS = 3
LEARNING_RATE = 1e-4

NUM_CLASSES = 200


# ==========================================================
# Device
# ==========================================================

if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


# ==========================================================
# Data
# ==========================================================

train_loader, val_loader, test_loader = create_dataloaders(
    batch_size=BATCH_SIZE
)


# ==========================================================
# Model
# ==========================================================

model = ViTPretrained(
    num_classes=NUM_CLASSES,
    pretrained=True
)


# ==========================================================
# Optimizer
# ==========================================================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=0.01
)


# ==========================================================
# Trainer
# ==========================================================

trainer = Trainer(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    optimizer=optimizer,
    device=DEVICE,
    save_path="results/runs/vit_pretrained_best.pth"
)


# ==========================================================
# Informations
# ==========================================================

print("=" * 60)
print("ViT PRETRAINED")
print("=" * 60)

print(f"Batch size    : {BATCH_SIZE}")
print(f"Epochs        : {EPOCHS}")
print(f"Learning rate : {LEARNING_RATE}")
print(f"Device        : {DEVICE}")
print(f"Train         : {len(train_loader.dataset)}")
print(f"Validation    : {len(val_loader.dataset)}")
print(f"Test          : {len(test_loader.dataset)}")

print("=" * 60)


# ==========================================================
# Training
# ==========================================================

history = trainer.fit(
    EPOCHS,
    max_train_batches=10
)

