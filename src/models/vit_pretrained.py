import torch.nn as nn
import timm


class ViTPretrained(nn.Module):
    """
    Vision Transformer pré-entraîné sur ImageNet.

    Le backbone ViT est chargé depuis timm avec ses
    poids ImageNet, puis sa tête de classification est
    remplacée pour CUB-200-2011 (200 classes).

    Parameters
    ----------
    num_classes : int
        Nombre de classes de la tâche cible.
    pretrained : bool
        Si True, charge les poids ImageNet.
    """

    def __init__(
        self,
        num_classes=200,
        pretrained=True
    ):
        super().__init__()

        self.model = timm.create_model(
            "vit_small_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes
        )

    def forward(self, x):
        """
        Parameters
        ----------
        x : torch.Tensor
            Images de forme [B, 3, 224, 224].

        Returns
        -------
        torch.Tensor
            Logits de forme [B, num_classes].
        """

        return self.model(x)
