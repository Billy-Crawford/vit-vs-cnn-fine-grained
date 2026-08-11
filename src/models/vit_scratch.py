import torch
import torch.nn as nn

from src.models.patch_embedding import PatchEmbedding
from src.models.cls_token import CLSToken
from src.models.positional_encoding import PositionalEncoding
from src.models.transformer_block import TransformerBlock


class ViTScratch(nn.Module):
    """
    Vision Transformer entraîné from scratch.

    Architecture :

        Image
          ↓
        Patch Embedding
          ↓
        CLS Token
          ↓
        Positional Encoding
          ↓
        Transformer Blocks
          ↓
        CLS final
          ↓
        Classification Head

    Entrée :
        [B, 3, 224, 224]

    Sortie :
        [B, num_classes]
    """

    def __init__(
        self,
        image_size=224,
        patch_size=16,
        in_channels=3,
        num_classes=200,
        embed_dim=384,
        depth=6,
        num_heads=6,
        mlp_ratio=4.0,
        dropout=0.0
    ):
        super().__init__()

        # ==========================================
        # 1. Patch Embedding
        # ==========================================

        self.patch_embedding = PatchEmbedding(
            image_size=image_size,
            patch_size=patch_size,
            in_channels=in_channels,
            embed_dim=embed_dim
        )

        # Nombre de patches produits par PatchEmbedding.
        num_patches = self.patch_embedding.num_patches

        # ==========================================
        # 2. CLS Token
        # ==========================================

        self.cls_token = CLSToken(
            embed_dim=embed_dim
        )

        # ==========================================
        # 3. Positional Encoding
        # ==========================================

        self.positional_encoding = PositionalEncoding(
            num_patches=num_patches,
            embed_dim=embed_dim
        )

        # ==========================================
        # 4. Transformer Blocks
        # ==========================================

        self.transformer_blocks = nn.ModuleList(
            [
                TransformerBlock(
                    embed_dim=embed_dim,
                    num_heads=num_heads,
                    mlp_ratio=mlp_ratio,
                    dropout=dropout
                )
                for _ in range(depth)
            ]
        )

        # ==========================================
        # 5. Classification Head
        # ==========================================

        self.norm = nn.LayerNorm(embed_dim)

        self.head = nn.Linear(
            embed_dim,
            num_classes
        )

    def forward(self, x):
        """
        x :
            [B, 3, 224, 224]

        retourne :
            [B, num_classes]
        """

        # ==========================================
        # 1. Transformer l'image en patches
        # ==========================================

        x = self.patch_embedding(x)

        # x :
        # [B, num_patches, embed_dim]

        # ==========================================
        # 2. Ajouter le CLS token
        # ==========================================

        x = self.cls_token(x)

        # x :
        # [B, num_patches + 1, embed_dim]

        # ==========================================
        # 3. Ajouter les informations de position
        # ==========================================

        x = self.positional_encoding(x)

        # x :
        # [B, num_patches + 1, embed_dim]

        # ==========================================
        # 4. Passer dans les Transformer Blocks
        # ==========================================

        for block in self.transformer_blocks:
            x = block(x)

        # ==========================================
        # 5. Récupérer uniquement le CLS token
        # ==========================================

        x = x[:, 0]

        # x :
        # [B, embed_dim]

        # ==========================================
        # 6. Normalisation finale
        # ==========================================

        x = self.norm(x)

        # ==========================================
        # 7. Classification
        # ==========================================

        x = self.head(x)

        # x :
        # [B, num_classes]

        return x
