import csv
import os
import time

import torch

from src.data.dataloader import create_dataloaders
from src.models.vit_scratch import ViTScratch
from src.models.resnet50 import ResNet50
from src.train.trainer import Trainer


# ==========================================================
# Configuration
# ==========================================================

BATCH_SIZE = 32
EPOCHS = 3
LEARNING_RATE = 1e-4
NUM_CLASSES = 200

FRACTIONS = [0.10, 0.25, 0.50]


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
# Résultats
# ==========================================================

RESULTS_PATH = "results/data_fraction_results.csv"

os.makedirs("results/runs", exist_ok=True)
os.makedirs("results/metrics", exist_ok=True)


# ==========================================================
# Évaluation
# ==========================================================

@torch.no_grad()
def evaluate(model, loader):

    model.eval()

    correct = 0
    total = 0

    for images, labels in loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        outputs = model(images)
        predictions = outputs.argmax(dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

    return correct / total


# ==========================================================
# Boucle expérimentale
# ==========================================================

results = []


for fraction in FRACTIONS:

    print()
    print("=" * 70)
    print(f"TRAINING FRACTION : {fraction:.0%}")
    print("=" * 70)

    train_loader, val_loader, test_loader = create_dataloaders(
        batch_size=BATCH_SIZE,
        augment=True,
        train_frac=fraction
    )

    print(f"Train images : {len(train_loader.dataset)}")
    print(f"Validation   : {len(val_loader.dataset)}")
    print(f"Test         : {len(test_loader.dataset)}")


    # ======================================================
    # 1. ViT Scratch
    # ======================================================

    print()
    print(">>> ViT Scratch Patch16")

    model = ViTScratch(
        patch_size=16,
        num_classes=NUM_CLASSES
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=0.01
    )

    checkpoint_path = (
        f"results/runs/"
        f"vit_scratch_fraction_{int(fraction * 100)}.pth"
    )

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        device=DEVICE,
        save_path=checkpoint_path
    )

    start = time.time()

    trainer.fit(EPOCHS)

    elapsed = time.time() - start

    model.load_state_dict(
        torch.load(
            checkpoint_path,
            map_location=DEVICE
        )
    )

    model.to(DEVICE)

    test_accuracy = evaluate(
        model,
        test_loader
    )

    print(f"ViT Test Accuracy : {test_accuracy:.4f}")

    results.append({
        "model": "ViT Scratch",
        "fraction": fraction,
        "train_size": len(train_loader.dataset),
        "test_accuracy": test_accuracy,
        "time": elapsed
    })


    # ======================================================
    # 2. ResNet50
    # ======================================================

    print()
    print(">>> ResNet50")

    model = ResNet50(
        num_classes=NUM_CLASSES,
        pretrained=True
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=0.01
    )

    checkpoint_path = (
        f"results/runs/"
        f"resnet50_fraction_{int(fraction * 100)}.pth"
    )

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        device=DEVICE,
        save_path=checkpoint_path
    )

    start = time.time()

    trainer.fit(EPOCHS)

    elapsed = time.time() - start

    model.load_state_dict(
        torch.load(
            checkpoint_path,
            map_location=DEVICE
        )
    )

    model.to(DEVICE)

    test_accuracy = evaluate(
        model,
        test_loader
    )

    print(f"ResNet50 Test Accuracy : {test_accuracy:.4f}")

    results.append({
        "model": "ResNet50",
        "fraction": fraction,
        "train_size": len(train_loader.dataset),
        "test_accuracy": test_accuracy,
        "time": elapsed
    })


# ==========================================================
# Sauvegarde
# ==========================================================

with open(
    RESULTS_PATH,
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "model",
            "fraction",
            "train_size",
            "test_accuracy",
            "time"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


# ==========================================================
# Résultats
# ==========================================================

print()
print("=" * 70)
print("RÉSULTATS DATA FRACTION")
print("=" * 70)

for result in results:

    print(
        f"{result['model']:<15} "
        f"{result['fraction']:>5.0%} "
        f"| Train: {result['train_size']:>5} "
        f"| Test Acc: {result['test_accuracy']:.4f}"
    )

print("=" * 70)
print(f"Résultats sauvegardés : {RESULTS_PATH}")
