import torch
import torch.nn as nn


class PatchEmbedding(nn.Module):
    """
    Transforme une image en une séquence de patches.

    Entrée :
        [B, 3, 224, 224]

    Sortie :
        [B, num_patches, embed_dim]
    """

    def __init__(
        self,
        image_size=224,
        patch_size=16,
        in_channels=3,
        embed_dim=384
    ):
        super().__init__()

        # Vérifie que l'image peut être divisée exactement
        # en patches de taille patch_size.
        if image_size % patch_size != 0:
            raise ValueError(
                "image_size doit être divisible par patch_size"
            )

        self.image_size = image_size
        self.patch_size = patch_size
        self.num_patches = (image_size // patch_size) ** 2

        # Projection des patches vers l'espace des embeddings.
        self.projection = nn.Conv2d(
            in_channels=in_channels,
            out_channels=embed_dim,
            kernel_size=patch_size,
            stride=patch_size
        )

    def forward(self, x):
        """
        x : [B, 3, 224, 224]

        retourne :
            [B, num_patches, embed_dim]
        """

        # [B, 3, 224, 224]
        x = self.projection(x)

        # [B, embed_dim, H', W']
        x = x.flatten(2)

        # [B, embed_dim, num_patches]
        x = x.transpose(1, 2)

        # [B, num_patches, embed_dim]
        return x