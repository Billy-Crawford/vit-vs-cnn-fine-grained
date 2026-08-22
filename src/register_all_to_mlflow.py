"""
Enregistre dans MLflow tous les checkpoints listés dans
results/final_results.csv, avec leurs vraies métriques (issues de
src/evaluate_all_checkpoints.py) et leurs hyperparamètres.

Contrairement à src/register_mlflow.py (qui enregistre un seul modèle
avec des métriques codées en dur), ce script couvre l'ensemble des 12
configurations entraînées, pour satisfaire l'exigence de packaging
MLflow de façon plus complète.

Le modèle PyTorch complet (mlflow.pytorch.log_model) n'est packagé que
pour les 3 meilleurs modèles de chaque famille d'architecture
(resnet50_best, vit_pretrained_patch32_best, vit_scratch_best), pour
éviter un temps d'exécution et un espace disque excessifs sur les 12
checkpoints.

Usage (depuis la racine du repo) :
    python src/register_all_to_mlflow.py

Le tracking MLflow est local au repo (fichier mlflow.db à la racine) -
peut être versionné dans Git si l'équipe souhaite le partager tel quel,
ou migré vers un Drive partagé plus tard.
"""

import os
import sys

import mlflow
import mlflow.pytorch
import pandas as pd
import torch

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

from src.models.vit_scratch import ViTScratch
from src.models.vit_pretrained import ViTPretrained
from src.models.resnet50 import ResNet50

FINAL_RESULTS_CSV = os.path.join(REPO_ROOT, "results", "final_results.csv")
RUNS_DIR = os.path.join(REPO_ROOT, "results", "runs")
EXPERIMENT_NAME = "CUB-200-2011_ablation"
N_CLASSES = 200

FULL_MODEL_LOGGING = {
    "resnet50_best",
    "vit_pretrained_patch32_best",
    "vit_scratch_best",
}


def parse_config(model_name: str) -> dict:
    name = model_name.lower()

    if name.startswith("resnet50"):
        architecture = "ResNet50"
    elif name.startswith("vit_pretrained"):
        architecture = "ViT_Pretrained"
    elif name.startswith("vit_scratch"):
        architecture = "ViT_Scratch"
    else:
        architecture = "unknown"

    patch_size = 32 if "patch32" in name else 16

    fraction = 100
    for frac in (10, 25, 50):
        if f"fraction_{frac}" in name:
            fraction = frac
            break

    augmentation = "sans_aug" if "noaug" in name else "standard"

    return {
        "architecture": architecture,
        "patch_size": patch_size,
        "train_fraction_pct": fraction,
        "augmentation": augmentation,
    }


def build_model(model_name: str, config: dict):
    if config["architecture"] == "ResNet50":
        return ResNet50(num_classes=N_CLASSES, pretrained=False)
    if config["architecture"] == "ViT_Pretrained":
        return ViTPretrained(num_classes=N_CLASSES, pretrained=False, patch_size=config["patch_size"])
    if config["architecture"] == "ViT_Scratch":
        return ViTScratch(num_classes=N_CLASSES, patch_size=config["patch_size"])
    raise ValueError(f"Architecture inconnue pour {model_name}")


def main():
    if not os.path.exists(FINAL_RESULTS_CSV):
        print(f"Fichier introuvable : {FINAL_RESULTS_CSV}")
        print("Lancer d'abord : python src/evaluate_all_checkpoints.py")
        return

    results = pd.read_csv(FINAL_RESULTS_CSV)

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(EXPERIMENT_NAME)

    for _, row in results.iterrows():
        model_name = row["model"]
        config = parse_config(model_name)

        print(f"\n--- {model_name} ---")

        with mlflow.start_run(run_name=model_name):
            mlflow.log_param("architecture", config["architecture"])
            mlflow.log_param("patch_size", config["patch_size"])
            mlflow.log_param("train_fraction_pct", config["train_fraction_pct"])
            mlflow.log_param("augmentation", config["augmentation"])
            mlflow.log_param("dataset", "CUB-200-2011")
            mlflow.log_param("num_classes", N_CLASSES)
            mlflow.log_param("optimizer", "AdamW")
            mlflow.log_param("learning_rate", 1e-4)
            mlflow.log_param("weight_decay", 0.01)
            mlflow.log_param("epochs", 3)

            mlflow.log_metric("test_top1_accuracy", row["top1_accuracy"])
            mlflow.log_metric("test_top5_accuracy", row["top5_accuracy"])
            mlflow.log_metric("test_loss", row["test_loss"])
            mlflow.log_metric("n_params", row["n_params"])

            ckpt_path = os.path.join(RUNS_DIR, f"{model_name}.pth")
            if os.path.exists(ckpt_path):
                mlflow.log_artifact(ckpt_path, artifact_path="checkpoint")

            if model_name in FULL_MODEL_LOGGING and os.path.exists(ckpt_path):
                try:
                    model = build_model(model_name, config)
                    state_dict = torch.load(ckpt_path, map_location="cpu")
                    model.load_state_dict(state_dict)
                    model.eval()
                    mlflow.pytorch.log_model(model, name="model", serialization_format="pickle")
                    print("Modèle PyTorch complet packagé.")
                except Exception as e:
                    print(f"Packaging du modèle échoué (métriques déjà loggées) : {e}")

            print(
                f"top1={row['top1_accuracy']:.4f} "
                f"top5={row['top5_accuracy']:.4f} "
                f"loggé dans MLflow."
            )

    print(f"\nTerminé. {len(results)} runs enregistrés dans l'expérience '{EXPERIMENT_NAME}'.")
    print("Pour visualiser : mlflow ui  (depuis la racine du repo)")


if __name__ == "__main__":
    main()