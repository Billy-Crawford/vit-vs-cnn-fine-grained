"""
Backend FastAPI - Démo ViT vs CNN (fine-grained classification)
Rôle C - Reporting / Backend Developer

Lancement (dev) :
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Documentation interactive une fois lancé :
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import predict
from models.loader import load_models

app = FastAPI(
    title="ViT vs CNN - Démo API",
    description="API de démonstration comparant un ViT et un ResNet-50 sur classification fine-grained (CUB-200-2011).",
    version="1.0.0",
)

# CORS ouvert pour le développement local (frontend Next.js sur un autre port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)


@app.on_event("startup")
def startup_event():
    """Charge les modèles une seule fois au démarrage du serveur.

    IMPORTANT (dépendance sur le rôle B) :
    Tant que B n'a pas livré de checkpoints entraînés, load_models() renvoie
    des modèles factices (mock) - voir models/loader.py. Dès qu'un checkpoint
    est disponible, mettre à jour MODEL_PATHS dans loader.py.
    """
    app.state.models = load_models()
    print("Modèles chargés (mock ou réels selon disponibilité).")


@app.get("/health")
def health_check():
    """Vérifie que l'API tourne et que les modèles sont chargés."""
    return {
        "status": "ok",
        "models_loaded": list(app.state.models.keys()) if hasattr(app.state, "models") else [],
    }
