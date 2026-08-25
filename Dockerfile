# ============================================================
# Dockerfile ÔÇö Backend FastAPI (ViT vs CNN Inference)
# ============================================================
# Multi-plateforme (Linux/macOS/Windows), optimis├® CPU et s├®curis├®.
# ============================================================

FROM python:3.11-slim AS base

# Emp├¬che Python d'├®crire des fichiers .pyc et active le flushing imm├®diat des logs
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

# Cr├®ation d'un utilisateur non-root
RUN useradd -m -u 1000 appuser

# Installation des d├®pendances avec index CPU PyTorch pour un build l├®ger et d├®terministe
COPY app/backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copie directe avec assignation des droits non-root (├®vite la duplication de couches lourdes)
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser app/backend/ app/backend/
COPY --chown=appuser:appuser data/data_processed/ data/data_processed/
COPY --chown=appuser:appuser results/runs/ results/runs/

USER appuser

WORKDIR /app/app/backend

EXPOSE 8000

# V├®rification de sant├® int├®gr├®e
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]