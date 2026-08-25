"""
Chargement des modèles ViT et ResNet-50 - checkpoints réels de B.

Les checkpoints (.pth) sont directement dans le repo Git
(results/runs/*.pth), donc pas besoin d'attendre un export MLflow
partagé pour les charger : on utilise torch.load() + les vraies classes
de B (src/models/vit_pretrained.py, src/models/resnet50.py).

QUAND CHANGER DE CHECKPOINT (ex. B livre une meilleure version) :
mettre à jour VIT_CHECKPOINT / RESNET_CHECKPOINT ci-dessous, et
VIT_PATCH_SIZE si on change de variante ViT (16 ou 32).
"""

import os
import random
import sys

# Racine du repo : app/backend/models/loader.py -> remonte à la racine
_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
sys.path.insert(0, _REPO_ROOT)

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() != "false"

N_CLASSES = 200
IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Checkpoint ViT retenu pour la démo : patch32 pré-entraîné (meilleur run
# enregistré par B - top1 53.85%, top5 83.50%, voir src/register_mlflow.py)
VIT_PATCH_SIZE = 32
VIT_CHECKPOINT = os.path.join(_REPO_ROOT, "results", "runs", "vit_pretrained_patch32_best.pth")
RESNET_CHECKPOINT = os.path.join(_REPO_ROOT, "results", "runs", "resnet50_best.pth")


class MockModel:
    """Modèle factice : prédictions aléatoires mais réalistes."""

    def __init__(self, name: str):
        self.name = name
        self.raw_model = None

    def predict(self, image_bytes: bytes):
        classes = random.sample(range(N_CLASSES), 3)
        confidences = sorted([random.uniform(0.4, 0.95) for _ in range(3)], reverse=True)
        return {
            "predicted_class": classes[0],
            "confidence": round(confidences[0], 4),
            "top3": [
                {"class_id": c, "confidence": round(conf, 4)}
                for c, conf in zip(classes, confidences)
            ],
        }


class TorchModelWrapper:
    """Adapte un modèle PyTorch (ViTPretrained ou ResNet50 de B) à
    l'interface .predict() attendue par routers/predict.py.

    Expose .raw_model, utilisé par utils/attention.py pour un futur
    hook d'attention sur le ViT.
    """

    def __init__(self, torch_model):
        import torch
        self.raw_model = torch_model
        self.raw_model.eval()
        self._torch = torch

    def _build_transform(self):
        import torchvision.transforms as T
        return T.Compose([
            T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            T.ToTensor(),
            T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])

    def predict(self, image_bytes: bytes):
        import io
        from PIL import Image

        transform = self._build_transform()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = transform(img).unsqueeze(0)

        with self._torch.no_grad():
            logits = self.raw_model(tensor)
            probs = self._torch.softmax(logits, dim=1)[0]
            top3_conf, top3_idx = probs.topk(3)

        return {
            "predicted_class": int(top3_idx[0]),
            "confidence": round(float(top3_conf[0]), 4),
            "top3": [
                {"class_id": int(i), "confidence": round(float(c), 4)}
                for i, c in zip(top3_idx.tolist(), top3_conf.tolist())
            ],
        }


def _load_vit():
    import torch
    from src.models.vit_pretrained import ViTPretrained

    model = ViTPretrained(num_classes=N_CLASSES, pretrained=False, patch_size=VIT_PATCH_SIZE)
    state_dict = torch.load(VIT_CHECKPOINT, map_location="cpu")
    model.load_state_dict(state_dict)
    return TorchModelWrapper(model)


def _load_resnet():
    import torch
    from src.models.resnet50 import ResNet50

    model = ResNet50(num_classes=N_CLASSES, pretrained=False)
    state_dict = torch.load(RESNET_CHECKPOINT, map_location="cpu")
    model.load_state_dict(state_dict)
    return TorchModelWrapper(model)


def load_models():
    if USE_MOCK:
        return {"vit": MockModel("vit"), "resnet": MockModel("resnet")}

    return {"vit": _load_vit(), "resnet": _load_resnet()}