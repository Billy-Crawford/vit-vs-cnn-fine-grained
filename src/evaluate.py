import os
import time

import torch
import torch.nn as nn

from src.data.dataloader import create_dataloaders
from src.models.vit_scratch import ViTScratch
from src.models.vit_pretrained import ViTPretrained
from src.models.resnet50 import ResNet50


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
# Evaluation
# ==========================================================

@torch.no_grad()
def evaluate(model, test_loader, device):
    """
    Évalue un modèle sur le test set.
    """

    model.eval()

    criterion = nn.CrossEntropyLoss()

    running_loss = 0.0
    correct = 0
    total = 0

    start_time = time.time()

    for batch_idx, (images, labels) in enumerate(
        test_loader,
        start=1
    ):

        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)

        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)

        predictions = outputs.argmax(dim=1)

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

        if batch_idx == 1 or batch_idx % 10 == 0:
            accuracy = correct / total

            print(
                f"  Batch [{batch_idx}/{len(test_loader)}] "
                f"| Acc: {accuracy:.4f}",
                flush=True
            )

    test_loss = running_loss / total
    test_accuracy = correct / total
    test_time = time.time() - start_time

    return test_loss, test_accuracy, test_time


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("ÉVALUATION FINALE")
    print("=" * 60)

    print(f"Device : {DEVICE}")

    # ------------------------------------------------------
    # Data
    # ------------------------------------------------------

    _, _, test_loader = create_dataloaders(
        batch_size=BATCH_SIZE
    )

    print(
        f"Test images : {len(test_loader.dataset)}"
    )

    print("=" * 60)
    print()

    criterion = nn.CrossEntropyLoss()

    results = {}

    # ======================================================
    # 1. ViT Scratch
    # ======================================================

    print("=" * 60)
    print("1. ViT SCRATCH")
    print("=" * 60)

    model = ViTScratch(
        patch_size=16,
        num_classes=NUM_CLASSES
    )

    checkpoint = "results/runs/vit_scratch_best.pth"

    if not os.path.exists(checkpoint):
        print(f"Checkpoint introuvable : {checkpoint}")
    else:

        model.load_state_dict(
            torch.load(
                checkpoint,
                map_location=DEVICE
            )
        )

        model.to(DEVICE)

        loss, accuracy, elapsed = evaluate(
            model,
            test_loader,
            DEVICE
        )

        results["ViT Scratch"] = {
            "loss": loss,
            "accuracy": accuracy,
            "time": elapsed
        }

        print()
        print(f"Test Loss : {loss:.4f}")
        print(f"Test Acc  : {accuracy:.4f}")
        print(f"Temps     : {elapsed:.1f}s")

    # ======================================================
    # 2. ViT Pretrained
    # ======================================================

    print()
    print("=" * 60)
    print("2. ViT PRETRAINED")
    print("=" * 60)

    model = ViTPretrained(
        num_classes=NUM_CLASSES,
        pretrained=False
    )

    checkpoint = "results/runs/vit_pretrained_best.pth"

    if not os.path.exists(checkpoint):
        print(f"Checkpoint introuvable : {checkpoint}")
    else:

        model.load_state_dict(
            torch.load(
                checkpoint,
                map_location=DEVICE
            )
        )

        model.to(DEVICE)

        loss, accuracy, elapsed = evaluate(
            model,
            test_loader,
            DEVICE
        )

        results["ViT Pretrained"] = {
            "loss": loss,
            "accuracy": accuracy,
            "time": elapsed
        }

        print()
        print(f"Test Loss : {loss:.4f}")
        print(f"Test Acc  : {accuracy:.4f}")
        print(f"Temps     : {elapsed:.1f}s")

    # ======================================================
    # 3. ResNet50
    # ======================================================

    print()
    print("=" * 60)
    print("3. RESNET50")
    print("=" * 60)

    model = ResNet50(
        num_classes=NUM_CLASSES,
        pretrained=False
    )

    checkpoint = "results/runs/resnet50_best.pth"

    if not os.path.exists(checkpoint):
        print(f"Checkpoint introuvable : {checkpoint}")
    else:

        model.load_state_dict(
            torch.load(
                checkpoint,
                map_location=DEVICE
            )
        )

        model.to(DEVICE)

        loss, accuracy, elapsed = evaluate(
            model,
            test_loader,
            DEVICE
        )

        results["ResNet50"] = {
            "loss": loss,
            "accuracy": accuracy,
            "time": elapsed
        }

        print()
        print(f"Test Loss : {loss:.4f}")
        print(f"Test Acc  : {accuracy:.4f}")
        print(f"Temps     : {elapsed:.1f}s")

    # ======================================================
    # Résumé
    # ======================================================

    print()
    print("=" * 60)
    print("RÉSULTATS FINAUX")
    print("=" * 60)

    print(
        f"{'Modèle':<20}"
        f"{'Loss':>12}"
        f"{'Accuracy':>12}"
        f"{'Temps (s)':>12}"
    )

    print("-" * 60)

    for name, result in results.items():

        print(
            f"{name:<20}"
            f"{result['loss']:>12.4f}"
            f"{result['accuracy']:>12.4f}"
            f"{result['time']:>12.1f}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()

