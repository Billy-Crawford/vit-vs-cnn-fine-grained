# App de démo — ViT vs CNN (CUB-200-2011)

État actuel : **backend et frontend fonctionnels avec des modèles factices
(mock)**. Les vraies prédictions/heatmaps seront branchées dès que le rôle B
livre des checkpoints entraînés (voir `backend/models/loader.py` et
`backend/utils/attention.py`).

## Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Documentation interactive : http://localhost:8000/docs

Endpoints :
- `GET /health` — vérifie que l'API tourne
- `POST /predict` — reçoit une image, renvoie les prédictions ViT + ResNet
- `POST /attention` — reçoit une image, renvoie la heatmap d'attention (base64)

## Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:3000

Par défaut le frontend appelle `http://localhost:8000` pour l'API. Pour
changer l'URL (ex. déploiement), définir la variable d'environnement
`NEXT_PUBLIC_API_URL`.

## Brancher les vrais modèles (une fois B a livré)

1. Placer les checkpoints (`.pth`) dans `backend/checkpoints/`
2. Dans `backend/models/loader.py` :
   - Mettre à jour `MODEL_PATHS`
   - Passer `USE_MOCK = False`
   - Décommenter le bloc de chargement réel (imports `torch`, `timm`,
     `torchvision`)
3. Dans `backend/utils/attention.py`, remplacer l'appel au mock par la
   vraie fonction de hook d'attention fournie par B
4. Ajouter `torch`, `torchvision`, `timm` à `requirements.txt`

## Déploiement (optionnel)

Piste : Hugging Face Spaces (Docker ou Gradio/Streamlit wrapper autour de
l'API FastAPI). À documenter ici une fois réalisé.
