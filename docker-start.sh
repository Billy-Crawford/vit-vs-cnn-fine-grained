#!/usr/bin/env bash
# ============================================================
# ViT vs CNN ÔÇö Script de lancement Docker (Linux / macOS)
# ============================================================

set -e

echo "============================================================"
echo "  Lancement de ViT vs CNN via Docker Compose"
echo "============================================================"

if ! command -v docker &> /dev/null; then
    echo "[ERREUR] Docker n'est pas install├® ou inaccessible dans le PATH."
    exit 1
fi

if [ ! -f .env ]; then
    echo "[INFO] Cr├®ation du fichier .env depuis .env.example..."
    cp .env.example .env
fi

echo "[INFO] Construction et d├®marrage des conteneurs..."
docker compose up --build -d

echo ""
echo "============================================================"
echo "  Application lanc├®e avec succ├¿s !"
echo "============================================================"
echo "  - Frontend D├®mo  : http://localhost:3000"
echo "  - Backend API    : http://localhost:8000/docs"
echo "  - MLflow (opt.)  : http://localhost:5000 (docker compose --profile mlflow up)"
echo "============================================================"
echo "Pour voir les logs : docker compose logs -f"
echo "Pour arr├¬ter       : docker compose down"
echo ""
