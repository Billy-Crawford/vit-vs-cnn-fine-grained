import torch

from src.data.dataloader import create_dataloaders
from src.models.resnet50 import ResNet50
from src.train.trainer import Trainer


# ==========================================================
# Configuration
# ==========================================================

BATCH_SIZE = 32
EPOCHS = 3
LEARNING_RATE = 1e-4

NUM_CLASSES = 200

TRAIN_FRAC = 1.0

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
    batch_size=BATCH_SIZE,
    train_frac=TRAIN_FRAC
)


# ==========================================================
# Model
# ==========================================================

model = ResNet50(
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
    save_path="results/runs/resnet50_best.pth"
)


# ==========================================================
# Informations
# ==========================================================

print("=" * 60)
print("RESNET50 PRETRAINED")
print("=" * 60)

print(f"Batch size    : {BATCH_SIZE}")
print(f"Epochs        : {EPOCHS}")
print(f"Learning rate : {LEARNING_RATE}")
print(f"Device        : {DEVICE}")
print(f"Train         : {len(train_loader.dataset)}")
print(f"Validation    : {len(val_loader.dataset)}")
print(f"Test          : {len(test_loader.dataset)}")
print(f"Train fraction : {TRAIN_FRAC}")

print("=" * 60)


# ==========================================================
# Training
# ==========================================================

history = trainer.fit(EPOCHS)

