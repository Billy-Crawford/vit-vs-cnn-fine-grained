import os
import torch
import mlflow
import mlflow.pytorch

from src.models.vit_pretrained import ViTPretrained


# ============================================================
# CONFIGURATION
# ============================================================

CHECKPOINT = "results/runs/vit_pretrained_patch32_best.pth"

EXPERIMENT_NAME = "CUB-200-2011_ViT"

MODEL_NAME = "ViT_Pretrained_Patch32"

NUM_CLASSES = 200
PATCH_SIZE = 32
IMAGE_SIZE = 224


# ============================================================
# CHARGEMENT DU MODÈLE
# ============================================================

device = torch.device("cpu")

model = ViTPretrained(
    num_classes=NUM_CLASSES,
    pretrained=False,
    patch_size=PATCH_SIZE,
)

checkpoint = torch.load(
    CHECKPOINT,
    map_location=device,
)

model.load_state_dict(checkpoint)

model.to(device)
model.eval()


# ============================================================
# CONFIGURATION MLflow
# ============================================================

mlflow.set_tracking_uri("sqlite:///mlflow.db")

mlflow.set_experiment(EXPERIMENT_NAME)


# ============================================================
# ENREGISTREMENT
# ============================================================

with mlflow.start_run(
    run_name="ViT_Pretrained_Patch32_Final"
) as run:

    # --------------------------------------------------------
    # Paramètres
    # --------------------------------------------------------

    mlflow.log_param("model", "ViT")
    mlflow.log_param("pretraining", "ImageNet")
    mlflow.log_param("patch_size", PATCH_SIZE)
    mlflow.log_param("image_size", IMAGE_SIZE)
    mlflow.log_param("num_classes", NUM_CLASSES)
    mlflow.log_param("dataset", "CUB-200-2011")

    # --------------------------------------------------------
    # Métriques
    # --------------------------------------------------------

    mlflow.log_metric("test_top1_accuracy", 0.5385)
    mlflow.log_metric("test_top5_accuracy", 0.8350)
    mlflow.log_metric("test_loss", 1.8115)

    # --------------------------------------------------------
    # Artefact original
    # --------------------------------------------------------

    mlflow.log_artifact(
        CHECKPOINT,
        artifact_path="checkpoint"
    )

    # --------------------------------------------------------
    # Modèle PyTorch MLflow
    # --------------------------------------------------------

    mlflow.pytorch.log_model(
        model,
        name="model",
        serialization_format="pickle",
    )

    print()
    print("=" * 60)
    print("MODÈLE ENREGISTRÉ DANS MLFLOW")
    print("=" * 60)
    print(f"Run ID : {run.info.run_id}")
    print(f"Experiment : {EXPERIMENT_NAME}")
    print(f"Model : {MODEL_NAME}")
    print(f"Patch size : {PATCH_SIZE}")
    print(f"Top-1 : 53.85%")
    print(f"Top-5 : 83.50%")
    print("=" * 60)

