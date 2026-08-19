from torch.utils.data import DataLoader

from src.data.cub_dataset import CUBDataset
from src.data.transforms import (
    get_train_transforms,
    get_eval_transforms,
)
import torch

METADATA_PATH = "data/metadata.csv"

IMAGE_ROOT = "data/CUB_200_2011/CUB_200_2011/images"

TRAIN_SPLIT = "data/split_train.csv"
VAL_SPLIT = "data/split_val.csv"
TEST_SPLIT = "data/split_test.csv"


def create_dataloaders(
    batch_size=32,
    num_workers=0,
    augment=True,
    train_frac=1.0,
):
    """
    Crée les DataLoaders Train, Validation et Test.
    """

    # Dataset d'entraînement
    train_dataset = CUBDataset(
        metadata_path=METADATA_PATH,
        split_path=TRAIN_SPLIT,
        image_root=IMAGE_ROOT,
        transform=get_train_transforms(
            augment=augment
        ),
    )

    if train_frac < 1.0:
        train_size = int(len(train_dataset) * train_frac)

        train_dataset, _ = torch.utils.data.random_split(
            train_dataset,
            [train_size, len(train_dataset) - train_size],
            generator=torch.Generator().manual_seed(42)
        )

    # Dataset de validation
    val_dataset = CUBDataset(
        metadata_path=METADATA_PATH,
        split_path=VAL_SPLIT,
        image_root=IMAGE_ROOT,
        transform=get_eval_transforms(),
    )

    # Dataset de test
    test_dataset = CUBDataset(
        metadata_path=METADATA_PATH,
        split_path=TEST_SPLIT,
        image_root=IMAGE_ROOT,
        transform=get_eval_transforms(),
    )

    # DataLoader Train
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )

    # DataLoader Validation
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    # DataLoader Test
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    return train_loader, val_loader, test_loader

