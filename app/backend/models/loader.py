"""
Chargement des modèles ViT et ResNet-50.

État actuel : MOCK. Tant que le rôle B n'a pas livré de checkpoints
entraînés, ce module renvoie des objets factices qui produisent des
prédictions aléatoires mais cohérentes en forme (mêmes shapes, mêmes
types) que les vrais modèles. Ça permet à tout le backend/frontend
d'être développé et testé sans dépendre de l'avancement de B.

Pour brancher les vrais modèles une fois prêts :
1. Renseigner MODEL_PATHS ci-dessous avec les chemins des checkpoints (.pth)
2. Mettre USE_MOCK = False
3. Vérifier que les classes réelles (timm ViT / torchvision ResNet) sont
   importées correctement - décommenter les imports en bas du fichier.
"""

import random

# --- Config à mettre à jour par C une fois les checkpoints de B disponibles ---
USE_MOCK = True

MODEL_PATHS = {
    "vit": "checkpoints/vit_best.pth",
    "resnet": "checkpoints/resnet50_best.pth",
}

N_CLASSES = 200  # CUB-200-2011


class MockModel:
    """Modèle factice : renvoie des prédictions aléatoires mais réalistes.

    Utile pour développer et tester tout le pipeline API + frontend
    sans dépendre des checkpoints réels de B.
    """

    def __init__(self, name: str):
        self.name = name

    def predict(self, image_bytes: bytes):
        """Simule une prédiction : classe + confiance + top-3."""
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


def load_models():
    """Charge (ou mocke) les modèles ViT et ResNet-50."""
    if USE_MOCK:
        return {
            "vit": MockModel("vit"),
            "resnet": MockModel("resnet"),
        }

    # --- Chargement réel, à activer une fois les checkpoints de B disponibles ---
    # import torch
    # import timm
    # import torchvision.models as tv_models
    #
    # vit = timm.create_model("vit_small_patch16_224", pretrained=False, num_classes=N_CLASSES)
    # vit.load_state_dict(torch.load(MODEL_PATHS["vit"], map_location="cpu"))
    # vit.eval()
    #
    # resnet = tv_models.resnet50(weights=None)
    # resnet.fc = torch.nn.Linear(resnet.fc.in_features, N_CLASSES)
    # resnet.load_state_dict(torch.load(MODEL_PATHS["resnet"], map_location="cpu"))
    # resnet.eval()
    #
    # return {"vit": vit, "resnet": resnet}

    raise NotImplementedError(
        "USE_MOCK=False mais le chargement réel n'est pas encore implémenté. "
        "Décommenter le bloc ci-dessus une fois les checkpoints de B disponibles."
    )
