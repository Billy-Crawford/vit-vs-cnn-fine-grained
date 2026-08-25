# ============================================================
# Dockerfile — Backend FastAPI (ViT vs CNN Inference)
# ============================================================
# Multi-plateforme (Linux/macOS/Windows), optimisé CPU et sécurisé.
# ============================================================

FROM python:3.11-slim AS base

# Empêche Python d'écrire des fichiers .pyc et active le flushing immédiat des logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    USE_MOCK=false \
    CUB_DATA_ROOT=/app/data/CUB_200_2011/CUB_200_2011 \
    CUB_OUT_DIR=/app/data/data_processed \
    CUB_METADATA_CSV=/app/data/data_processed/metadata.csv

WORKDIR /app

# Installation de curl pour le healthcheck et les outils minimaux
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Création d'un utilisateur non-root
RUN useradd -m -u 1000 appuser

# Installation des dépendances avec index CPU PyTorch pour un build léger et déterministe
COPY app/backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copie directe avec assignation des droits non-root (évite la duplication de couches lourdes)
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser app/backend/ app/backend/
COPY --chown=appuser:appuser data/data_processed/ data/data_processed/
COPY --chown=appuser:appuser results/runs/ results/runs/

USER appuser

WORKDIR /app/app/backend

EXPOSE 8000

# Vérification de santé intégrée
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]