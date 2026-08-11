import torch

from src.models.vit_scratch import ViTScratch


def test_vit_patch16():
    """
    Vérifie que le ViT fonctionne avec des patches 16x16.
    """

    model = ViTScratch(
        image_size=224,
        patch_size=16,
        num_classes=200
    )

    x = torch.randn(2, 3, 224, 224)

    output = model(x)

    assert output.shape == (2, 200)


def test_vit_patch32():
    """
    Vérifie que le ViT fonctionne avec des patches 32x32.
    """

    model = ViTScratch(
        image_size=224,
        patch_size=32,
        num_classes=200
    )

    x = torch.randn(2, 3, 224, 224)

    output = model(x)

    assert output.shape == (2, 200)


def test_patch_numbers():
    """
    Vérifie le nombre de patches pour les deux tailles.
    """

    model16 = ViTScratch(
        image_size=224,
        patch_size=16,
        num_classes=200
    )

    model32 = ViTScratch(
        image_size=224,
        patch_size=32,
        num_classes=200
    )

    assert model16.patch_embedding.num_patches == 196
    assert model32.patch_embedding.num_patches == 49
