"""
Chargement des noms d'espèces (CUB-200-2011) à partir de
data/data_processed/metadata.csv (livré par le rôle A).

Indépendant de tout modèle entraîné - basé uniquement sur les
métadonnées du dataset, déjà présentes dans le repo.
"""

import csv
import os
import re

# Chemin par défaut : app/backend/data/classes.py -> remonte à la racine
# du repo -> data/data_processed/metadata.csv
_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
METADATA_CSV_PATH = os.environ.get(
    "CUB_METADATA_CSV",
    os.path.join(_REPO_ROOT, "data", "data_processed", "metadata.csv"),
)


def _clean_class_name(raw_name: str) -> str:
    """Transforme '001.Black_footed_Albatross' en 'Black footed Albatross'."""
    name = re.sub(r"^\d+\.", "", raw_name)
    return name.replace("_", " ").strip()


def load_class_names() -> dict:
    """Renvoie un mapping {label_index: nom_espece}, index 0..199.

    Même logique de tri que le LABEL_MAP de A (src/data/dataset.py) :
    class_id trié par ordre croissant -> index 0..199. Tant que
    metadata.csv est introuvable, renvoie un mapping générique de repli.
    """
    if not os.path.exists(METADATA_CSV_PATH):
        return {i: f"Espèce n°{i:03d}" for i in range(200)}

    seen = {}
    with open(METADATA_CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            class_id = int(row["class_id"])
            if class_id not in seen:
                seen[class_id] = _clean_class_name(row["class_name"])

    sorted_ids = sorted(seen.keys())
    return {i: seen[class_id] for i, class_id in enumerate(sorted_ids)}