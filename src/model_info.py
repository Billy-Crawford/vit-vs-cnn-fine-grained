import torch

from src.models.vit_scratch import ViTScratch
from src.models.vit_pretrained import ViTPretrained
from src.models.resnet50 import ResNet50


def count_parameters(model):
    return sum(
        p.numel()
        for p in model.parameters()
    )


models = {
    "ViT Scratch": ViTScratch(),
    "ViT Pretrained": ViTPretrained(
        pretrained=True
    ),
    "ResNet50": ResNet50(
        pretrained=True
    )
}


print("=" * 70)
print("NOMBRE DE PARAMÈTRES")
print("=" * 70)

for name, model in models.items():

    total = count_parameters(model)

    trainable = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print(
        f"{name:<20} | "
        f"Total : {total:,} | "
        f"Trainable : {trainable:,}"
    )

