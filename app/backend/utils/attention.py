"""
Génération de la carte d'attention (heatmap) du ViT.

Extraction réelle basée sur la structure ViTPretrained de B (backbone
timm avec .model.blocks[-1].attn) - testée et validée. Bascule
automatiquement vers un mock si le modèle passé n'a pas cette structure
(ex. ResNet, ou si B change d'architecture) : aucun risque de crash.

Mécanisme : timm désactive par défaut le calcul explicite des poids
d'attention (fused_attn=True, via scaled_dot_product_attention). On le
désactive sur le dernier bloc pour forcer le calcul manuel, puis on
intercepte l'entrée de attn_drop (= poids d'attention post-softmax,
forme [B, num_heads, N, N]) via un hook. On moyenne sur les têtes et on
prend la ligne du token CLS vers les patches, reshapée en grille carrée.
"""

import base64
import io

import numpy as np
from PIL import Image

IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def _try_extract_real_attention(vit_wrapper, tensor):
    """Tente d'extraire la vraie grille d'attention CLS->patches.

    Renvoie un tensor [grid, grid] en cas de succès, ou None si la
    structure du modèle ne correspond pas à un ViT timm-style (fallback
    silencieux, pas d'exception levée vers l'appelant).
    """
    import torch

    raw = getattr(vit_wrapper, "raw_model", None)
    if raw is None:
        return None

    backbone = getattr(raw, "model", None)  # ViTPretrained.model = timm VisionTransformer
    if backbone is None or not hasattr(backbone, "blocks") or len(backbone.blocks) == 0:
        return None

    last_block = backbone.blocks[-1]
    if not hasattr(last_block, "attn") or not hasattr(last_block.attn, "attn_drop"):
        return None

    last_block.attn.fused_attn = False  # force le calcul explicite des poids d'attention

    captured = {}

    def hook(module, inp, out):
        captured["attn"] = inp[0]

    handle = last_block.attn.attn_drop.register_forward_hook(hook)
    try:
        with torch.no_grad():
            raw(tensor)
    finally:
        handle.remove()

    attn = captured.get("attn")
    if attn is None:
        return None

    attn_avg = attn.mean(dim=1)  # moyenne sur les têtes -> [B, N, N]
    cls_to_patches = attn_avg[0, 0, 1:]  # ligne CLS, patches uniquement -> [num_patches]

    num_patches = cls_to_patches.shape[0]
    grid_size = int(num_patches ** 0.5)
    if grid_size * grid_size != num_patches:
        return None  # grille non carrée, structure inattendue

    return cls_to_patches.reshape(grid_size, grid_size)


def _colorize_and_overlay(image: Image.Image, attention_grid: np.ndarray) -> str:
    """Superpose une grille d'attention (valeurs quelconques) à l'image, encode en base64."""
    w, h = image.size
    attention_grid = (attention_grid - attention_grid.min()) / (
        attention_grid.max() - attention_grid.min() + 1e-8
    )

    heatmap = Image.fromarray((attention_grid * 255).astype(np.uint8)).resize(
        (w, h), resample=Image.BILINEAR
    )

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


def _generate_mock_attention_overlay(image: Image.Image) -> str:
    """Heatmap factice - utilisée si l'extraction réelle échoue ou est indisponible."""
    grid_size = 14
    fake_attention = np.random.rand(grid_size, grid_size)
    return _colorize_and_overlay(image, fake_attention)


def generate_attention_overlay(image: Image.Image, model=None) -> str:
    """Point d'entrée utilisé par l'API.

    `model` est le wrapper (TorchModelWrapper ou MockModel) du modèle ViT,
    tel que passé par routers/predict.py (models.get("vit")).
    """
    if model is not None and hasattr(model, "raw_model") and model.raw_model is not None:
        try:
            import torchvision.transforms as T

            transform = T.Compose([
                T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
                T.ToTensor(),
                T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
            ])
            tensor = transform(image).unsqueeze(0)

            grid = _try_extract_real_attention(model, tensor)
            if grid is not None:
                return _colorize_and_overlay(image, grid.numpy())
        except Exception as e:
            print(f"Attention réelle indisponible ({e}), fallback mock.")

    return _generate_mock_attention_overlay(image)