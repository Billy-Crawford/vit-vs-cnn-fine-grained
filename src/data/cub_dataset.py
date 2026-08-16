from pathlib import Path

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset


class CUBDataset(Dataset):
    """
    Dataset PyTorch pour CUB-200-2011.

    Les fichiers split_train.csv, split_val.csv et split_test.csv
    contiennent uniquement les image_id.
    Les informations complémentaires sont récupérées depuis metadata.csv.
    """

    def __init__(
        self,
        metadata_path,
        split_path,
        image_root,
        transform=None,
    ):
        self.metadata_path = Path(metadata_path)
        self.split_path = Path(split_path)
        self.image_root = Path(image_root)
        self.transform = transform

        # Chargement des métadonnées
        metadata = pd.read_csv(self.metadata_path)

        # Chargement du split
        split = pd.read_csv(self.split_path)

        # Jointure entre image_id et metadata
        self.data = split.merge(
            metadata,
            on="image_id",
            how="left",
        )

        # Vérification des IDs
        if self.data["image_name"].isna().any():
            raise ValueError(
                "Certains image_id du split ne sont pas présents "
                "dans metadata.csv"
            )

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]

        # Construction du chemin local
        image_path = self.image_root / row["image_name"]

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image introuvable : {image_path}"
            )

        # Chargement de l'image
        image = Image.open(image_path).convert("RGB")

        # Transformation
        if self.transform is not None:
            image = self.transform(image)

        # CUB utilise des labels de 1 à 200.
        # PyTorch attend des labels de 0 à 199.
        label = int(row["class_id"]) - 1

        return image, label

