import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights


class ResNet50(nn.Module):
    """
    ResNet50 pré-entraîné sur ImageNet.

    La dernière couche est remplacée pour classifier
    les 200 classes de CUB-200-2011.
    """

    def __init__(
        self,
        num_classes=200,
        pretrained=True
    ):
        super().__init__()

        if pretrained:
            weights = ResNet50_Weights.DEFAULT
        else:
            weights = None

        self.model = resnet50(weights=weights)

        # Nombre d'entrées de la couche finale
        in_features = self.model.fc.in_features

        # Nouvelle tête pour CUB-200-2011
        self.model.fc = nn.Linear(
            in_features,
            num_classes
        )

    def forward(self, x):
        return self.model(x)

