# ViT vs CNN — Classification fine-grained

Projet M1 IA — comparaison Vision Transformer vs CNN sur une tâche de classification fine-grained, avec étude d'ablation (taille de patch, pré-entraînement).

## Équipe
- A — Data / Experiment Engineer : [SONHOUIN Abdoul-raouf]
- B — Model / Research Engineer : [Nom]
- C — Reporting / Backend Developer : [Nom]

## Structure du repo

/data # dataset (non versionné)

/notebooks # notebooks d'exploration

/src/data # preprocessing, dataset PyTorch, splits

/src/models # architectures ViT/ResNet 

/src/train # boucle d'entraînement

/src/eval # analyse des résultats, attention maps

/app/backend # API FastAPI

/app/frontend # app Next.js de démo

/report # rapport LaTeX

/results # tableaux, figures, logs de runs


## Protocole
- Seed : 42
- Résolution : 224×224
- Métriques : accuracy top-1, F1 macro

## Installation

### App de démo — ViT vs CNN (CUB-200-2011)

État actuel : **backend et frontend fonctionnels avec des modèles factices
(mock)**. Les vraies prédictions/heatmaps seront branchées dès que le rôle B
livre des checkpoints entraînés (voir `backend/models/loader.py` et
`backend/utils/attention.py`).

#### Backend (FastAPI)

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

#### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:3000

Par défaut le frontend appelle `http://localhost:8000` pour l'API. Pour
changer l'URL (ex. déploiement), définir la variable d'environnement
`NEXT_PUBLIC_API_URL`.

#### Brancher les vrais modèles (une fois B a livré)

1. Placer les checkpoints (`.pth`) dans `backend/checkpoints/`
2. Dans `backend/models/loader.py` :
   - Mettre à jour `MODEL_PATHS`
   - Passer `USE_MOCK = False`
   - Décommenter le bloc de chargement réel (imports `torch`, `timm`,
     `torchvision`)
3. Dans `backend/utils/attention.py`, remplacer l'appel au mock par la
   vraie fonction de hook d'attention fournie par B
4. Ajouter `torch`, `torchvision`, `timm` à `requirements.txt`

#### Déploiement (optionnel)

Piste : Hugging Face Spaces (Docker ou Gradio/Streamlit wrapper autour de
l'API FastAPI). À documenter ici une fois réalisé.
=======
(à compléter — instructions backend/frontend)


## Pipeline data (rôle A)

Les fichiers déjà générés sont dans `data/processed/` :
- `metadata.csv` : toutes les images + classes + split officiel CUB
- `split_train.csv`, `split_val.csv`, `split_test.csv` : indices (image_id) du split train/val/test (seed=42)
- `split_train_{10,25,50,100}pct.csv` : sous-échantillons stratifiés pour la courbe data-hungry

### Pour réutiliser dans ton notebook (rôle B)

```python
import os
os.environ['CUB_DATA_ROOT'] = '<TON_CHEMIN_DRIVE>/CUB_200_2011'  # adapte à ton Drive
os.environ['CUB_OUT_DIR'] = '<TON_CHEMIN_DRIVE>/data_processed'

from src.data.transforms import get_val_transform, get_train_transform
from src.data.dataset import CUBDataset
import pandas as pd

metadata = pd.read_csv('data/processed/metadata.csv')
train_ids = pd.read_csv('data/processed/split_train.csv')
train_df = metadata[metadata['image_id'].isin(train_ids['image_id'])]

train_ds = CUBDataset(train_df, transform=get_train_transform('weak'))
```

**Important** : `metadata.csv` contient des chemins d'image pointant vers le Drive de A — remplace `image_path` en le reconstruisant depuis ta propre copie du dataset si besoin :
```python
metadata['image_path'] = metadata['image_name'].apply(lambda x: f"{os.environ['CUB_DATA_ROOT']}/images/{x}")
```

