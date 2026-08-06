# ViT vs CNN — Classification fine-grained

Projet M1 IA — comparaison Vision Transformer vs CNN sur une tâche de classification fine-grained, avec étude d'ablation (taille de patch, pré-entraînement).

## Équipe
- A — Data / Experiment Engineer : [Nom]
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
(à compléter — instructions backend/frontend)
