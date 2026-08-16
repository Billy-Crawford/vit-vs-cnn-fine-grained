import torch
import torch.nn as nn


class PositionalEncoding(nn.Module):
    """
    Positional encoding apprenable pour le Vision Transformer.

    Ajoute une information de position à chaque token.

    Entrée :
        [B, num_patches + 1, embed_dim]

    Sortie :
        [B, num_patches + 1, embed_dim]
    """

    def __init__(
        self,
        num_patches,
        embed_dim=384
    ):
        super().__init__()

        self.num_patches = num_patches
        self.embed_dim = embed_dim

        # Un embedding de position pour chaque token.
        # +1 correspond au token [CLS].
        self.position_embeddings = nn.Parameter(
            torch.zeros(
                1,
                num_patches + 1,
                embed_dim
            )
        )

        nn.init.trunc_normal_(
            self.position_embeddings,
            std=0.02
        )

    def forward(self, x):
        """
        x :
            [B, num_patches + 1, embed_dim]

        retourne :
            [B, num_patches + 1, embed_dim]
        """

        return x + self.position_embeddings