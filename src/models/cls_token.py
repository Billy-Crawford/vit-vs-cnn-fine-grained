import torch
import torch.nn as nn


class CLSToken(nn.Module):
    """
    Token [CLS] apprenable utilisé par le Vision Transformer.

    Ajoute un token au début de la séquence de patches.

    Entrée :
        [B, num_patches, embed_dim]

    Sortie :
        [B, num_patches + 1, embed_dim]
    """

    def __init__(self, embed_dim=384):
        super().__init__()

        # Token [CLS] apprenable.
        self.cls_token = nn.Parameter(
            torch.randn(1, 1, embed_dim)
        )

    def forward(self, x):
        """
        x :
            [B, num_patches, embed_dim]

        retourne :
            [B, num_patches + 1, embed_dim]
        """

        batch_size = x.size(0)

        # Répète le token [CLS] pour chaque élément du batch.
        cls_tokens = self.cls_token.expand(
            batch_size,
            -1,
            -1
        )

        # Ajoute [CLS] au début de la séquence.
        x = torch.cat(
            (cls_tokens, x),
            dim=1
        )

        return x
