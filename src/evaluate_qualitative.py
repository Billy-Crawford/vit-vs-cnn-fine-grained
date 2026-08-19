import torch

from src.models.vit_pretrained import ViTPretrained


CHECKPOINT = "results/runs/vit_pretrained_patch32_best.pth"


def main():

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    print("=" * 60)
    print("TEST DU MEILLEUR MODÈLE")
    print("=" * 60)

    print(f"Device     : {device}")
    print(f"Checkpoint : {CHECKPOINT}")

    model = ViTPretrained(
        num_classes=200,
        pretrained=False,
        patch_size=32,
    )

    checkpoint = torch.load(
        CHECKPOINT,
        map_location=device,
        weights_only=False,
    )

    print("Checkpoint type :", type(checkpoint))

    if isinstance(checkpoint, dict):
        print("Checkpoint keys :", checkpoint.keys())

        if "model_state_dict" in checkpoint:
            model.load_state_dict(checkpoint["model_state_dict"])
        elif "state_dict" in checkpoint:
            model.load_state_dict(checkpoint["state_dict"])
        else:
            model.load_state_dict(checkpoint)
    else:
        model.load_state_dict(checkpoint)

    model.to(device)
    model.eval()

    # Test avec une image artificielle
    x = torch.randn(
        1,
        3,
        224,
        224,
        device=device,
    )

    with torch.no_grad():
        output = model(x)

    print("Input shape  :", x.shape)
    print("Output shape :", output.shape)

    assert output.shape == (1, 200)

    print()
    print("✓ Modèle chargé correctement")
    print("✓ Sortie compatible avec 200 classes")
    print("=" * 60)


if __name__ == "__main__":
    main()

