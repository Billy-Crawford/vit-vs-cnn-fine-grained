"""
Réévalue tous les checkpoints présents dans results/runs/ sur le test set,
et régénère results/final_results.csv à jour.

Pourquoi ce script : final_results.csv et results.csv actuels ne
contiennent que 3 lignes (ViT Scratch, ViT Pretrained, ResNet50) issues
d'un entraînement à 1 epoch très ancien. Depuis, de nouveaux checkpoints
ont été produits (vit_pretrained_patch32_best.pth, les variantes
data-fraction, etc.) mais jamais réévalués dans un CSV consolidé.

Usage (depuis la racine du repo) :
    python src/evaluate_all_checkpoints.py

Sortie : results/final_results.csv, avec une ligne par checkpoint
présent dans results/runs/*.pth (top1, top5, loss, nb paramètres,
temps d'inférence). Les checkpoints qui échouent au chargement (ex.
hyperparamètres non standards) sont listés séparément en fin
d'exécution plutôt que de faire planter tout le script.
"""

import csv
import glob
import os
import sys
import time

import torch
import torch.nn as nn
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

from src.models.vit_scratch import ViTScratch
from src.models.vit_pretrained import ViTPretrained
from src.models.resnet50 import ResNet50
from src.data.transforms import get_val_transform

N_CLASSES = 200
METADATA_CSV = os.path.join(REPO_ROOT, "data", "data_processed", "metadata.csv")
SPLIT_TEST_CSV = os.path.join(REPO_ROOT, "data", "data_processed", "split_test.csv")
RUNS_DIR = os.path.join(REPO_ROOT, "results", "runs")
OUTPUT_CSV = os.path.join(REPO_ROOT, "results", "final_results.csv")


class CUBTestDataset(Dataset):
    def __init__(self, dataframe, transform, label_map):
        self.df = dataframe.reset_index(drop=True)
        self.transform = transform
        self.label_map = label_map

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img = Image.open(row["image_path"]).convert("RGB")
        img = self.transform(img)
        label = self.label_map[row["class_id"]]
        return img, label


# Chemin local vers le dataset CUB-200-2011 (adapter si besoin)
LOCAL_DATASET_ROOT = os.environ.get(
    "CUB_DATA_ROOT",
    r"C:\Abdoul-raouf\Master\S1\Project annuel\CUB_200_2011\CUB_200_2011",
)


def build_test_loader(batch_size=32):
    metadata = pd.read_csv(METADATA_CSV)
    test_ids = pd.read_csv(SPLIT_TEST_CSV)
    test_df = metadata[metadata["image_id"].isin(test_ids["image_id"])].copy()

    # Reconstruit image_path avec le chemin local, au lieu du chemin
    # Colab de A stocké dans metadata.csv
    test_df["image_path"] = test_df["image_name"].apply(
        lambda name: os.path.join(LOCAL_DATASET_ROOT, "images", name)
    )

    label_map = {c: i for i, c in enumerate(sorted(metadata["class_id"].unique()))}

    dataset = CUBTestDataset(test_df, get_val_transform(), label_map)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    return loader

def build_model_for_checkpoint(filename: str) -> nn.Module:
    name = filename.lower()

    if name.startswith("resnet50"):
        return ResNet50(num_classes=N_CLASSES, pretrained=False)

    if name.startswith("vit_pretrained"):
        patch_size = 32 if "patch32" in name else 16
        return ViTPretrained(num_classes=N_CLASSES, pretrained=False, patch_size=patch_size)

    if name.startswith("vit_scratch"):
        patch_size = 32 if "patch32" in name else 16
        return ViTScratch(num_classes=N_CLASSES, patch_size=patch_size)

    raise ValueError(f"Architecture non reconnue pour le fichier : {filename}")


@torch.no_grad()
def evaluate_checkpoint(model, loader, device, criterion):
    model.eval()
    model.to(device)

    total_loss = 0.0
    correct_top1 = 0
    correct_top5 = 0
    total = 0

    start = time.time()
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        total_loss += loss.item() * images.size(0)

        top5_preds = outputs.topk(5, dim=1).indices
        correct_top1 += (top5_preds[:, 0] == labels).sum().item()
        correct_top5 += (top5_preds == labels.unsqueeze(1)).any(dim=1).sum().item()
        total += labels.size(0)
    elapsed = time.time() - start

    return {
        "test_loss": total_loss / total,
        "top1_accuracy": correct_top1 / total,
        "top5_accuracy": correct_top5 / total,
        "n_params": sum(p.numel() for p in model.parameters()),
        "eval_time_sec": round(elapsed, 1),
    }


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device : {device}")

    loader = build_test_loader()
    criterion = nn.CrossEntropyLoss()

    checkpoint_paths = sorted(glob.glob(os.path.join(RUNS_DIR, "*.pth")))
    print(f"{len(checkpoint_paths)} checkpoints trouvés dans {RUNS_DIR}")

    results = []
    failures = []

    for ckpt_path in checkpoint_paths:
        filename = os.path.basename(ckpt_path)
        model_name = os.path.splitext(filename)[0]
        print(f"\n--- {model_name} ---")

        try:
            model = build_model_for_checkpoint(filename)
            state_dict = torch.load(ckpt_path, map_location=device)
            model.load_state_dict(state_dict)
        except Exception as e:
            print(f"ÉCHEC du chargement : {e}")
            failures.append((model_name, str(e)))
            continue

        metrics = evaluate_checkpoint(model, loader, device, criterion)
        metrics["model"] = model_name
        results.append(metrics)

        print(
            f"top1={metrics['top1_accuracy']:.4f} "
            f"top5={metrics['top5_accuracy']:.4f} "
            f"loss={metrics['test_loss']:.4f} "
            f"params={metrics['n_params']:,}"
        )

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    fieldnames = ["model", "top1_accuracy", "top5_accuracy", "test_loss", "n_params", "eval_time_sec"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\n{len(results)} checkpoints évalués avec succès -> {OUTPUT_CSV}")

    if failures:
        print(f"\n{len(failures)} checkpoint(s) n'ont pas pu être chargés :")
        for name, error in failures:
            print(f"  - {name}: {error}")
        print(
            "\nPour ces checkpoints, vérifier les hyperparamètres exacts "
            "utilisés à l'entraînement (embed_dim, depth, num_heads, etc.) "
            "auprès de B si non standards."
        )


if __name__ == "__main__":
    main()