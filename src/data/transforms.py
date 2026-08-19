import torchvision.transforms as T
from .config import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD


def get_val_transform():
    """
    Transformations utilisées pour validation et test.
    """
    return T.Compose([
        T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        T.ToTensor(),
        T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])


def get_train_transform(strength='weak'):
    """
    Transformations utilisées pour l'entraînement.
    strength='weak'   -> augmentation légère
    strength='strong' -> augmentation plus agressive (data-hungry curve)
    """
    if strength == 'weak':
        return T.Compose([
            T.RandomResizedCrop(IMAGE_SIZE, scale=(0.8, 1.0)),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    elif strength == 'strong':
        return T.Compose([
            T.RandomResizedCrop(IMAGE_SIZE, scale=(0.7, 1.0)),
            T.RandomHorizontalFlip(),
            T.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05),
            T.RandomRotation(15, fill=127),
            T.ToTensor(),
            T.Normalize(IMAGENET_MEAN, IMAGENET_STD),
            T.RandomErasing(p=0.3),
        ])
    else:
        raise ValueError(f"strength inconnu: {strength}")


# --- Alias de compatibilité (utilisés par src/train/*.py de B) ---
def get_eval_transforms():
    return get_val_transform()


def get_train_transforms(augment=True):
    """Alias compatible avec l'appel get_train_transforms(augment=True)
    utilisé dans les scripts d'entraînement de B."""
    if augment:
        return get_train_transform(strength='weak')
    return get_val_transform()