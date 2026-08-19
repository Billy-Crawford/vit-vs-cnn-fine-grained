import time

import torch
import torch.nn as nn

from src.data.dataloader import create_dataloaders
from src.models.vit_scratch import ViTScratch
from src.models.vit_pretrained import ViTPretrained


# ==========================================================
# Configuration
# ==========================================================

BATCH_SIZE = 32
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

_, _, test_loader = create_dataloaders(
    batch_size=BATCH_SIZE
)


# ==========================================================
# Évaluation
# ==========================================================

@torch.no_grad()
def evaluate(model, loader):

    model.eval()

    criterion = nn.CrossEntropyLoss()

    total_loss = 0.0
    correct_top1 = 0
    correct_top5 = 0
    total = 0

    start = time.time()

    for images, labels in loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        outputs = model(images)

        # Loss
        loss = criterion(outputs, labels)

        total_loss += loss.item() * labels.size(0)

        # Top-1
        predictions = outputs.argmax(dim=1)

        correct_top1 += (
            predictions == labels
        ).sum().item()

        # Top-5
        _, top5 = outputs.topk(
            5,
            dim=1
        )

        correct_top5 += (
            top5 == labels.unsqueeze(1)
        ).any(dim=1).sum().item()

        total += labels.size(0)

    elapsed = time.time() - start

    return (
        total_loss / total,
        correct_top1 / total,
        correct_top5 / total,
        elapsed
    )


# ==========================================================
# Chargement checkpoint
# ==========================================================

def load_checkpoint(model, path):

    checkpoint = torch.load(
        path,
        map_location="cpu"
    )

    model.load_state_dict(checkpoint)

    model.to(DEVICE)

    return model


# ==========================================================
# Modèles
# ==========================================================

models = {

    # ------------------------------------------------------
    # Scratch — Patch16
    # ------------------------------------------------------

    "ViT Scratch Patch16": load_checkpoint(
        ViTScratch(
            patch_size=16,
            num_classes=NUM_CLASSES
        ),
        "results/runs/vit_scratch_best.pth"
    ),

    # ------------------------------------------------------
    # Scratch — Patch32
    # ------------------------------------------------------

    "ViT Scratch Patch32": load_checkpoint(
        ViTScratch(
            patch_size=32,
            num_classes=NUM_CLASSES
        ),
        "results/runs/vit_scratch_patch32_best.pth"
    ),

    # ------------------------------------------------------
    # Pretrained — Patch16
    # ------------------------------------------------------

    "ViT Pretrained Patch16": load_checkpoint(
        ViTPretrained(
            num_classes=NUM_CLASSES,
            pretrained=False,
            patch_size=16
        ),
        "results/runs/vit_pretrained_best.pth"
    ),

    # ------------------------------------------------------
    # Pretrained — Patch32
    # ------------------------------------------------------

    "ViT Pretrained Patch32": load_checkpoint(
        ViTPretrained(
            num_classes=NUM_CLASSES,
            pretrained=False,
            patch_size=32
        ),
        "results/runs/vit_pretrained_patch32_best.pth"
    ),
}


# ==========================================================
# Évaluation
# ==========================================================

print("=" * 75)
print("ABLATION ViT — PATCH SIZE × PRÉ-ENTRAÎNEMENT")
print("=" * 75)

print(f"Device      : {DEVICE}")
print(f"Test images : {len(test_loader.dataset)}")

print("=" * 75)


results = []


for name, model in models.items():

    print()
    print("=" * 75)
    print(name)
    print("=" * 75)

    loss, top1, top5, elapsed = evaluate(
        model,
        test_loader
    )

    print(f"Test Loss : {loss:.4f}")
    print(f"Top-1     : {top1:.4f}")
    print(f"Top-5     : {top5:.4f}")
    print(f"Temps     : {elapsed:.1f}s")

    results.append(
        {
            "model": name,
            "loss": loss,
            "top1": top1,
            "top5": top5,
            "time": elapsed
        }
    )


# ==========================================================
# Tableau final
# ==========================================================

print()
print("=" * 75)
print("TABLEAU D'ABLATION FINAL")
print("=" * 75)

print(
    f"{'Modèle':<30}"
    f"{'Loss':>10}"
    f"{'Top-1':>10}"
    f"{'Top-5':>10}"
    f"{'Temps':>12}"
)

print("-" * 75)

for result in results:

    print(
        f"{result['model']:<30}"
        f"{result['loss']:>10.4f}"
        f"{result['top1']:>10.4f}"
        f"{result['top5']:>10.4f}"
        f"{result['time']:>12.1f}"
    )

print("=" * 75)
