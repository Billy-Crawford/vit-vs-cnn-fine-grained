# ViT vs CNN — Classification fine-grained

Projet M1 IA — comparaison Vision Transformer vs CNN sur une tâche de classification fine-grained (CUB-200-2011), avec étude d'ablation (taille de patch, pré-entraînement, quantité de données) et application de démonstration.

## Équipe
- A — Data / Experiment Engineer : SONHOUIN Abdoul-raouf
- B — Model / Research Engineer : NGARTOBAYE OUMAROU BILLY
- C — Reporting / Backend Developer : YEYE Koffi Gagnon

## Structure du repo

/data/data_processed # métadonnées et splits générés (dataset brut non versionné)
/notebooks # notebooks d'exploration et d'entraînement
/src/data # preprocessing, dataset PyTorch, splits, transforms
/src/models # architectures ViT (scratch/pré-entraîné) et ResNet-50
/src/train # boucle d'entraînement (scheduler, AMP, early stopping)
/src/evaluate_all_checkpoints.py # réévaluation de tous les checkpoints
/src/register_all_to_mlflow.py # enregistrement MLflow
/app/backend # API FastAPI (prédictions, attention, classes)
/app/frontend # app Next.js de démo
/report # rapport LaTeX
/results # checkpoints, métriques, figures


## Protocole
- Seed : 42
- Résolution : 224×224
- Métriques : accuracy top-1, top-5

## Pipeline data (rôle A)

Les fichiers déjà générés sont dans `data/data_processed/` :
- `metadata.csv` : toutes les images + classes + split officiel CUB
- `split_train.csv`, `split_val.csv`, `split_test.csv` : indices (image_id) du split train/val/test (seed=42)
- `split_train_{10,25,50,100}pct.csv` : sous-échantillons stratifiés pour la courbe data-hungry
- `figures/` : EDA (distribution des classes, résolutions, exemples de classes proches)

### Réutiliser le pipeline data dans un notebook

```python
import os
os.environ['CUB_DATA_ROOT'] = '<TON_CHEMIN>/CUB_200_2011/CUB_200_2011'
os.environ['CUB_OUT_DIR'] = '<TON_CHEMIN>/data_processed'

from src.data.transforms import get_val_transform, get_train_transform
from src.data.dataset import CUBDataset
import pandas as pd

metadata = pd.read_csv('data/data_processed/metadata.csv')
train_ids = pd.read_csv('data/data_processed/split_train.csv')
train_df = metadata[metadata['image_id'].isin(train_ids['image_id'])]

train_ds = CUBDataset(train_df, transform=get_train_transform('weak'))
```

**Important** : `metadata.csv` contient des chemins d'image locaux à la machine qui l'a généré — reconstruis `image_path` avec ton propre `CUB_DATA_ROOT` si besoin :
```python
metadata['image_path'] = metadata['image_name'].apply(lambda x: f"{os.environ['CUB_DATA_ROOT']}/images/{x}")
```

## Entraînement et évaluation (rôle B)

Les scripts d'entraînement sont dans `src/train/` (un par architecture/variante). Les checkpoints entraînés sont versionnés dans `results/runs/*.pth`.

Pour réévaluer tous les checkpoints sur le test set et régénérer les résultats finaux :
```bash
python src/evaluate_all_checkpoints.py
```
Ça produit `results/final_results.csv` avec top-1, top-5, loss et nombre de paramètres pour chaque configuration.

## Suivi des expériences (MLflow)

La base `mlflow.db` est locale (exclue du dépôt via `.gitignore`) — chacun la régénère chez soi :

```bash
# 1. Réévalue tous les checkpoints présents dans results/runs/ sur le test set
python src/evaluate_all_checkpoints.py

# 2. Enregistre les résultats et les 3 meilleurs modèles dans MLflow
python src/register_all_to_mlflow.py

# 3. Visualiser les runs
mlflow ui
```

Ouvrir ensuite `http://127.0.0.1:5000`. L'expérience `CUB-200-2011_ablation` contient les 12 configurations comparées dans le rapport, avec leurs hyperparamètres, métriques (top-1, top-5, loss) et — pour les 3 meilleurs modèles (ResNet-50, ViT pré-entraîné patch32, ViT from scratch) — le modèle PyTorch complet packagé.

Nécessite `pip install mlflow torch torchvision timm pandas` (déjà couvert par `requirements.txt`).

## App de démo — ViT vs CNN

L'application est fonctionnelle avec les vrais modèles entraînés (checkpoints dans `results/runs/`).

### 🚀 Lancement rapide avec Docker (Recommandé — Multi-plateforme)

Pour garantir que l'application tourne à l'identique sur toutes les machines (Windows, macOS, Linux) sans conflits d'environnement :

```bash
# 1. Copier le fichier de configuration (si ce n'est pas déjà fait)
cp .env.example .env

# 2. Construire et démarrer les conteneurs
docker compose up --build -d
```

Ou sous Windows : double-cliquer simplement sur `docker-start.bat`.

- **Frontend Démo (Next.js)** : [http://localhost:3000](http://localhost:3000)
- **Backend API (FastAPI Docs)** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **MLflow UI (Optionnel)** : `docker compose --profile mlflow up -d` puis ouvrir [http://localhost:5000](http://localhost:5000)

**Commandes utiles Docker :**
```bash
# Voir les logs en direct de tous les conteneurs
docker compose logs -f

# Voir les logs du backend uniquement
docker compose logs -f backend

# Voir les logs du frontend uniquement
docker compose logs -f frontend

# Arrêter l'application
docker compose down

# Redémarrer l'application (sans rebuild)
docker compose up -d

# Lancer avec l'interface MLflow en plus (port 5000)
docker compose --profile mlflow up -d
```

---

### Lancement en local (sans Docker)

#### Backend (FastAPI)

```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Documentation interactive : http://localhost:8000/docs

Endpoints :
- `GET /health` — vérifie que l'API tourne et que les modèles sont chargés
- `GET /classes` — renvoie le mapping `{index: nom_espèce}` (200 espèces CUB)
- `POST /predict` — reçoit une image, renvoie les prédictions ViT + ResNet (classe, confiance, top-3)
- `POST /attention` — reçoit une image, renvoie la carte d'attention réelle du ViT superposée (base64)

#### Frontend (Next.js)

```bash
cd app/frontend
npm install
npm run dev
```

Ouvrir http://localhost:3000

Par défaut le frontend appelle `http://localhost:8000`. Pour changer l'URL (ex. déploiement distant), définir la variable d'environnement `NEXT_PUBLIC_API_URL`.

### Tests

```bash
cd app/backend
pytest tests/ -v
```

### Déploiement

Le projet est entièrement conteneurisé via les Dockerfiles multi-stage (`Dockerfile` pour le backend PyTorch/FastAPI et `app/frontend/Dockerfile` pour le frontend Next.js standalone).
Il peut être déployé directement sur n'importe quel serveur ou service cloud supportant Docker (VPS, Hugging Face Spaces, Render, AWS ECS, GCP Cloud Run, Azure App Service).