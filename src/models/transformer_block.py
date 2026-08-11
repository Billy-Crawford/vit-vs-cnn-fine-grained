import torch
import torch.nn as nn


class TransformerBlock(nn.Module):
    """
    Bloc Transformer utilisé dans notre Vision Transformer.

    Architecture :

        LayerNorm
            ↓
        Multi-Head Self-Attention
            ↓
        Connexion résiduelle
            ↓
        LayerNorm
            ↓
        MLP
            ↓
        Connexion résiduelle

    Entrée :
        [B, N, embed_dim]

    Sortie :
        [B, N, embed_dim]
    """

    def __init__(
        self,
        embed_dim=384,
        num_heads=6,
        mlp_ratio=4.0,
        dropout=0.0
    ):
        super().__init__()

        # Première normalisation avant l'attention.
        self.norm1 = nn.LayerNorm(embed_dim)

        # Multi-Head Self-Attention.
        self.attention = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )

        # Deuxième normalisation avant le MLP.
        self.norm2 = nn.LayerNorm(embed_dim)

        # Dimension cachée du MLP.
        mlp_hidden_dim = int(embed_dim * mlp_ratio)

        # MLP du Transformer.
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, mlp_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mlp_hidden_dim, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        """
        x :
            [B, N, embed_dim]

        retourne :
            [B, N, embed_dim]
        """

        # ==========================================
        # 1. Multi-Head Self-Attention
        # ==========================================

        # Pre-LayerNorm.
        residual = x
        x_norm = self.norm1(x)

        # Self-Attention.
        attention_output, _ = self.attention(
            x_norm,
            x_norm,
            x_norm,
            need_weights=False
        )

        # Connexion résiduelle.
        x = residual + attention_output

        # ==========================================
        # 2. MLP
        # ==========================================

        # Pre-LayerNorm.
        residual = x
        x_norm = self.norm2(x)

        # MLP.
        mlp_output = self.mlp(x_norm)

        # Connexion résiduelle.
        x = residual + mlp_output

        return x
