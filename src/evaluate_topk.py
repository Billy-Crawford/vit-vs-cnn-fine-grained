import time

import torch

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
# Données
# ==========================================================

_, _, test_loader = create_dataloaders(
    batch_size=BATCH_SIZE
)


# ==========================================================
# Évaluation Top-K
# ==========================================================

@torch.no_grad()
def evaluate_topk(model, loader, device, k=5):

    model.eval()

    correct_top1 = 0
    correct_top5 = 0
    total = 0

    start_time = time.time()

    for batch_idx, (images, labels) in enumerate(
        loader,
        start=1
    ):

        images = images.to(device)
        labels = labels.to(device)

        # ------------------------------------------------------
        # Forward
        # ------------------------------------------------------

        outputs = model(images)

        # ------------------------------------------------------
        # Top-1
        # ------------------------------------------------------

        predictions = outputs.argmax(dim=1)

        correct_top1 += (
            predictions == labels
        ).sum().item()

        # ------------------------------------------------------
        # Top-5
        # ------------------------------------------------------

        _, top5_predictions = outputs.topk(
            k,
            dim=1
        )

        correct_top5 += (
            top5_predictions == labels.unsqueeze(1)
        ).any(dim=1).sum().item()

        total += labels.size(0)

        # ------------------------------------------------------
        # Progression
        # ------------------------------------------------------

        if batch_idx == 1 or batch_idx % 20 == 0:

            current_top1 = correct_top1 / total
            current_top5 = correct_top5 / total

            print(
                f"  Batch [{batch_idx}/{len(loader)}] "
                f"| Top-1: {current_top1:.4f} "
                f"| Top-5: {current_top5:.4f}",
                flush=True
            )

    top1_accuracy = correct_top1 / total
    top5_accuracy = correct_top5 / total

    elapsed = time.time() - start_time

    return (
        top1_accuracy,
        top5_accuracy,
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
    # 1. ViT Scratch
    # ------------------------------------------------------

    "ViT Scratch": load_checkpoint(
        ViTScratch(
            patch_size=16,
            num_classes=NUM_CLASSES
        ),
        "results/runs/vit_scratch_best.pth"
    ),

    # ------------------------------------------------------
    # 2. ViT Pretrained
    # ------------------------------------------------------

    "ViT Pretrained": load_checkpoint(
        ViTPretrained(
            num_classes=NUM_CLASSES,
            pretrained=True
        ),
        "results/runs/vit_pretrained_best.pth"
    ),

    # ------------------------------------------------------
    # 3. ResNet50
    # ------------------------------------------------------

    "ResNet50": load_checkpoint(
        ResNet50(
            num_classes=NUM_CLASSES,
            pretrained=False
        ),
        "results/runs/resnet50_best.pth"
    )
}


# ==========================================================
# Évaluation
# ==========================================================

print("=" * 70)
print("ÉVALUATION TOP-1 / TOP-5")
print("=" * 70)

print(f"Device      : {DEVICE}")
print(f"Test images : {len(test_loader.dataset)}")

print("=" * 70)


results = []


for name, model in models.items():

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    top1, top5, elapsed = evaluate_topk(
        model=model,
        loader=test_loader,
        device=DEVICE,
        k=5
    )

    print()
    print(f"Top-1 Accuracy : {top1:.4f}")
    print(f"Top-5 Accuracy : {top5:.4f}")
    print(f"Temps          : {elapsed:.1f}s")

    results.append(
        {
            "model": name,
            "top1": top1,
            "top5": top5,
            "time": elapsed
        }
    )


# ==========================================================
# Résultats finaux
# ==========================================================

print()
print("=" * 70)
print("RÉSULTATS TOP-K")
print("=" * 70)

print(
    f"{'Modèle':<25}"
    f"{'Top-1':>12}"
    f"{'Top-5':>12}"
    f"{'Temps (s)':>15}"
)

print("-" * 70)

for result in results:

    print(
        f"{result['model']:<25}"
        f"{result['top1']:>12.4f}"
        f"{result['top5']:>12.4f}"
        f"{result['time']:>15.1f}"
    )

print("=" * 70)

