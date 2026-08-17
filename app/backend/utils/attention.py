"""
Génération de la carte d'attention (heatmap) du ViT.

État actuel : MOCK. Le vrai hook sur la dernière couche d'attention du
ViT est développé par le rôle B (voir plan de projet, section B ->
"Cartes d'attention"). En attendant, ce module génère une heatmap
factice mais visuellement plausible, pour développer et tester
l'endpoint et l'affichage frontend.

À remplacer une fois que B fournit sa fonction de génération d'overlay
(réutilisable telle qu'annoncée dans le plan).
"""

import base64
import io
import random

import numpy as np
from PIL import Image


def generate_mock_attention_overlay(image: Image.Image) -> str:
    """Génère une heatmap factice superposée à l'image, encodée en base64.

    Args:
        image: image PIL originale (déjà chargée par l'endpoint).

    Returns:
        Chaîne base64 (PNG) de l'image avec overlay, prête à être
        renvoyée telle quelle au frontend.
    """
    w, h = image.size

    # Grille d'attention factice (ex: 14x14, comme un ViT patch16 sur 224px)
    grid_size = 14
    fake_attention = np.random.rand(grid_size, grid_size)
    fake_attention = (fake_attention - fake_attention.min()) / (
        fake_attention.max() - fake_attention.min() + 1e-8
    )

    heatmap = Image.fromarray((fake_attention * 255).astype(np.uint8)).resize(
        (w, h), resample=Image.BILINEAR
    )
    heatmap = heatmap.convert("L")

    # Colorisation simple (rouge = forte attention) et overlay semi-transparent
    heatmap_rgba = Image.new("RGBA", (w, h))
    heatmap_pixels = heatmap.load()
    overlay_pixels = heatmap_rgba.load()
    for x in range(w):
        for y in range(h):
            intensity = heatmap_pixels[x, y]
            overlay_pixels[x, y] = (255, 0, 0, int(intensity * 0.5))

    base = image.convert("RGBA")
    combined = Image.alpha_composite(base, heatmap_rgba)

    buffer = io.BytesIO()
    combined.convert("RGB").save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def generate_attention_overlay(image: Image.Image, model=None) -> str:
    """Point d'entrée utilisé par l'API. Bascule vers le mock tant que
    le vrai modèle/hook n'est pas branché.
    """
    # TODO (une fois B a livré) : appeler la vraie fonction de B ici,
    # ex. model.get_attention_overlay(image), puis encoder en base64.
    return generate_mock_attention_overlay(image)
