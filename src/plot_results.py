import json
import os

import pandas as pd
import matplotlib.pyplot as plt


RESULTS_DIR = "results"
METRICS_DIR = os.path.join(RESULTS_DIR, "metrics")
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")

os.makedirs(FIGURES_DIR, exist_ok=True)


# ============================================================
# 1. COURBES D'APPRENTISSAGE
# ============================================================

def plot_learning_curves():
    models = {
        "ViT Scratch Patch16": "vit_scratch_patch16_noaug_best_history.json",
        "ViT Pretrained Patch32": "vit_pretrained_patch32_best_history.json",
    }

    for name, filename in models.items():

        path = os.path.join(METRICS_DIR, filename)

        with open(path, "r") as f:
            history = json.load(f)

        epochs = range(1, len(history["train_accuracy"]) + 1)

        plt.figure(figsize=(8, 5))

        plt.plot(
            epochs,
            history["train_accuracy"],
            marker="o",
            label="Train Accuracy",
        )

        plt.plot(
            epochs,
            history["val_accuracy"],
            marker="o",
            label="Validation Accuracy",
        )

        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.title(f"Learning Curve — {name}")
        plt.legend()
        plt.grid(True, alpha=0.3)

        safe_name = name.lower().replace(" ", "_")

        plt.savefig(
            os.path.join(
                FIGURES_DIR,
                f"{safe_name}_learning_curve.png",
            ),
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()


# ============================================================
# 2. ABLATION PATCH SIZE × PRÉ-ENTRAÎNEMENT
# ============================================================

def plot_ablation():

    models = [
        "ViT Scratch Patch16",
        "ViT Scratch Patch32",
        "ViT Pretrained Patch16",
        "ViT Pretrained Patch32",
    ]

    top1 = [
        0.0107,
        0.0200,
        0.0994,
        0.5385,
    ]

    top5 = [
        0.0475,
        0.0846,
        0.2537,
        0.8350,
    ]

    x = range(len(models))

    width = 0.35

    plt.figure(figsize=(10, 6))

    plt.bar(
        [i - width / 2 for i in x],
        top1,
        width,
        label="Top-1",
    )

    plt.bar(
        [i + width / 2 for i in x],
        top5,
        width,
        label="Top-5",
    )

    plt.xticks(
        list(x),
        models,
        rotation=20,
        ha="right",
    )

    plt.ylabel("Accuracy")
    plt.title("Ablation — Patch Size × Pré-entraînement")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    plt.savefig(
        os.path.join(
            FIGURES_DIR,
            "ablation_patch_pretraining.png",
        ),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ============================================================
# 3. VI T SCRATCH vs RESNET50 — FRACTIONS DE DONNÉES
# ============================================================

def plot_data_fraction():

    path = os.path.join(
        RESULTS_DIR,
        "data_fraction_results.csv",
    )

    df = pd.read_csv(path)

    plt.figure(figsize=(8, 5))

    for model in df["model"].unique():

        subset = df[df["model"] == model]

        plt.plot(
            subset["fraction"] * 100,
            subset["test_accuracy"] * 100,
            marker="o",
            linewidth=2,
            label=model,
        )

    plt.xlabel("Fraction du dataset d'entraînement (%)")
    plt.ylabel("Test Accuracy (%)")

    plt.title(
        "Influence de la quantité de données"
    )

    plt.xticks([10, 25, 50])

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig(
        os.path.join(
            FIGURES_DIR,
            "data_fraction_comparison.png",
        ),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ============================================================
# 4. COMPARAISON FINALE
# ============================================================

def plot_final_comparison():

    models = [
        "ViT Scratch\nPatch16",
        "ViT Scratch\nPatch32",
        "ViT Pretrained\nPatch16",
        "ViT Pretrained\nPatch32",
        "ResNet50",
    ]

    accuracy = [
        0.0107,
        0.0200,
        0.0994,
        0.5385,
        0.4874,
    ]

    plt.figure(figsize=(10, 6))

    plt.bar(
        models,
        [x * 100 for x in accuracy],
    )

    plt.ylabel("Test Accuracy (%)")
    plt.title("Comparaison des modèles")

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.savefig(
        os.path.join(
            FIGURES_DIR,
            "final_model_comparison.png",
        ),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("GÉNÉRATION DES FIGURES")
    print("=" * 70)

    plot_learning_curves()
    print("✓ Courbes d'apprentissage")

    plot_ablation()
    print("✓ Ablation Patch × Pré-entraînement")

    plot_data_fraction()
    print("✓ Influence de la quantité de données")

    plot_final_comparison()
    print("✓ Comparaison finale")

    print("=" * 70)
    print("Figures sauvegardées dans :", FIGURES_DIR)
    print("=" * 70)

