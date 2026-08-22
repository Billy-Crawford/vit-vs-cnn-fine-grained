import matplotlib.pyplot as plt

fractions = [10, 25, 50, 100]
resnet_top1 = [5.11, 23.47, 48.74, 71.87]
vit_scratch_top1 = [1.09, 0.97, 2.16, 1.07]

plt.figure(figsize=(6, 4.2))
plt.plot(fractions, resnet_top1, marker='o', linewidth=2, label='ResNet-50 (pré-entraîné)', color='#2c5f3d')
plt.plot(fractions, vit_scratch_top1, marker='s', linewidth=2, label='ViT (from scratch)', color='#a63d2f')

plt.xlabel("Fraction du jeu d'entraînement utilisée (%)")
plt.ylabel("Accuracy top-1 sur le test set (%)")
plt.title("Sensibilité à la quantité de données (courbe data-hungry)")
plt.xticks(fractions)
plt.ylim(0, 80)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('report/figures/data_hungry_curve.png', dpi=200)