import torch.nn as nn
import timm


class ViTPretrained(nn.Module):
    """
    Vision Transformer pré-entraîné sur ImageNet.

    Backbone ViT fourni par timm avec poids ImageNet,
    puis tête de classification adaptée à CUB-200-2011.

    Parameters
    ----------
    num_classes : int
        Nombre de classes de la tâche cible.
    pretrained : bool
        Si True, charge les poids ImageNet.
    patch_size : int
        Taille des patches : 16 ou 32.
    """

    def __init__(
        self,
        num_classes=200,
        pretrained=True,
        patch_size=16
    ):
        super().__init__()

        # ------------------------------------------------------
        # Sélection du backbone selon la taille des patches
        # ------------------------------------------------------

        if patch_size == 16:
            model_name = "vit_small_patch16_224"

        elif patch_size == 32:
            model_name = "vit_small_patch32_224"

        else:
            raise ValueError(
                "patch_size doit être 16 ou 32."
            )

        # ------------------------------------------------------
        # Création du ViT
        # ------------------------------------------------------

        self.model = timm.create_model(
            model_name,
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

