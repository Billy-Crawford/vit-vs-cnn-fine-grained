"""
Backend FastAPI - Démo ViT vs CNN (fine-grained classification)
Rôle C - Reporting / Backend Developer

Lancement (dev) :
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Documentation interactive une fois lancé :
    http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import predict
from models.loader import load_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.models = load_models()
    print("Modèles chargés (mock ou réels selon disponibilité).")
    yield


app = FastAPI(
    title="ViT vs CNN - Démo API",
    description="API de démonstration comparant un ViT et un ResNet-50 sur classification fine-grained (CUB-200-2011).",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "models_loaded": list(app.state.models.keys()) if hasattr(app.state, "models") else [],
    }