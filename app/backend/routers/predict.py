"""
Routes de prédiction : /predict et /attention

/predict     : reçoit une image, retourne les prédictions ViT et ResNet
/attention   : reçoit une image, retourne la heatmap d'attention du ViT (base64)
"""

import io

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from PIL import Image, UnidentifiedImageError

from utils.attention import generate_attention_overlay

router = APIRouter(tags=["prediction"])

MAX_FILE_SIZE_MB = 10
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def _load_and_validate_image(file: UploadFile, contents: bytes) -> Image.Image:
    """Valide le fichier reçu et renvoie une image PIL RGB.

    Centralise la gestion d'erreurs (format invalide, taille excessive,
    fichier corrompu) pour être réutilisée par les deux endpoints.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Format non supporté ({file.content_type}). Formats acceptés : jpeg, png, webp.",
        )

    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"Fichier trop volumineux ({size_mb:.1f} Mo). Maximum : {MAX_FILE_SIZE_MB} Mo.",
        )

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Image corrompue ou illisible.")

    return image


@router.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    """Reçoit une image, retourne les prédictions ViT et ResNet.

    Réponse :
        {
          "vit": {"predicted_class": int, "confidence": float, "top3": [...]},
          "resnet": {"predicted_class": int, "confidence": float, "top3": [...]}
        }
    """
    contents = await file.read()
    _load_and_validate_image(file, contents)  # valide, lève une erreur claire sinon

    models = request.app.state.models

    return {
        "vit": models["vit"].predict(contents),
        "resnet": models["resnet"].predict(contents),
    }


@router.post("/attention")
async def attention(request: Request, file: UploadFile = File(...)):
    """Reçoit une image, retourne la heatmap d'attention du ViT.

    Réponse :
        {"attention_overlay_base64": "<image PNG encodée en base64>"}
    """
    contents = await file.read()
    image = _load_and_validate_image(file, contents)

    models = request.app.state.models
    overlay_b64 = generate_attention_overlay(image, model=models.get("vit"))

    return {"attention_overlay_base64": overlay_b64}
