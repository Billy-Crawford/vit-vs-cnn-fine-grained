import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights


class ResNet50(nn.Module):
    """
    ResNet-50 utilisé comme baseline CNN.

    Entrée :
        [B, 3, 224, 224]

    Sortie :
        [B, num_classes]
    """

    def __init__(
        self,
        num_classes=200,
        pretrained=False
    ):
        super().__init__()

        weights = ResNet50_Weights.DEFAULT if pretrained else None

        self.model = resnet50(weights=weights)

        # Remplace la tête de classification ImageNet (1000 classes)
        # par une tête adaptée au CUB-200-2011 (200 classes).
        in_features = self.model.fc.in_features

        self.model.fc = nn.Linear(
            in_features,
            num_classes
        )

    def forward(self, x):
        return self.model(x)

