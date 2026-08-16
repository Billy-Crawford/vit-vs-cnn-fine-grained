import os
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# Chargement des résultats
# ==========================================================

df = pd.read_csv("results/results.csv")

os.makedirs("results/figures", exist_ok=True)


# ==========================================================
# Accuracy
# ==========================================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["model"],
    df["test_accuracy"] * 100
)

plt.ylabel("Accuracy (%)")
plt.xlabel("Modèle")
plt.title("Comparaison des performances sur CUB-200-2011")

plt.ylim(0, 100)

plt.tight_layout()

plt.savefig(
    "results/figures/model_accuracy.png",
    dpi=300
)

plt.close()


# ==========================================================
# Loss
# ==========================================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["model"],
    df["test_loss"]
)

plt.ylabel("Test Loss")
plt.xlabel("Modèle")
plt.title("Comparaison de la loss sur CUB-200-2011")

plt.tight_layout()

plt.savefig(
    "results/figures/model_loss.png",
    dpi=300
)

plt.close()


print("Graphiques générés.")

