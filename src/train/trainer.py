import json
import os
import time

import torch
import torch.nn as nn


class Trainer:
    """
    Moteur d'entraînement commun aux modèles ViT et ResNet.

    Gère :
    - entraînement
    - validation
    - accuracy
    - sauvegarde du meilleur modèle
    - historique des métriques
    - sélection automatique du device
    - affichage de progression
    """

    def __init__(
        self,
        model,
        train_loader,
        val_loader,
        criterion=None,
        optimizer=None,
        device=None,
        save_path="results/runs/best_model.pth"
    ):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader

        # ==========================================================
        # Fonction de perte
        # ==========================================================

        self.criterion = criterion or nn.CrossEntropyLoss()

        # ==========================================================
        # Sélection automatique du device
        # ==========================================================

        if device is None:
            if torch.backends.mps.is_available():
                device = torch.device("mps")
            elif torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")

        self.device = device

        print(f"Device sélectionné : {self.device}")

        self.model.to(self.device)

        # ==========================================================
        # Optimiseur
        # ==========================================================

        self.optimizer = optimizer

        # ==========================================================
        # Chemin de sauvegarde
        # ==========================================================

        self.save_path = save_path

        save_dir = os.path.dirname(self.save_path)

        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

        # ==========================================================
        # Historique
        # ==========================================================

        self.history = {
            "train_loss": [],
            "train_accuracy": [],
            "val_loss": [],
            "val_accuracy": []
        }

        # ==========================================================
        # Meilleure validation
        # ==========================================================

        self.best_val_accuracy = 0.0

    # ==============================================================
    # TRAIN
    # ==============================================================

    def train_one_epoch(self, max_batches=None):
        """
        Entraîne le modèle pendant une epoch.
        """

        self.model.train()

        running_loss = 0.0
        correct = 0
        total = 0

        start_time = time.time()

        total_batches = len(self.train_loader)

        for batch_idx, (images, labels) in enumerate(
            self.train_loader,
            start=1
        ):

            if max_batches is not None and batch_idx > max_batches:
                break

            images = images.to(self.device)
            labels = labels.to(self.device)

            # ------------------------------------------------------
            # Réinitialisation des gradients
            # ------------------------------------------------------

            self.optimizer.zero_grad()

            # ------------------------------------------------------
            # Forward
            # ------------------------------------------------------

            outputs = self.model(images)

            # ------------------------------------------------------
            # Loss
            # ------------------------------------------------------

            loss = self.criterion(outputs, labels)

            # ------------------------------------------------------
            # Backpropagation
            # ------------------------------------------------------

            loss.backward()

            # ------------------------------------------------------
            # Mise à jour des poids
            # ------------------------------------------------------

            self.optimizer.step()

            # ------------------------------------------------------
            # Statistiques
            # ------------------------------------------------------

            running_loss += loss.item() * images.size(0)

            predictions = outputs.argmax(dim=1)

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

            # ------------------------------------------------------
            # Affichage
            # ------------------------------------------------------

            if batch_idx == 1 or batch_idx % 10 == 0:

                current_loss = running_loss / total
                current_accuracy = correct / total

                elapsed = time.time() - start_time

                print(
                    f"  Batch [{batch_idx}/{total_batches}] "
                    f"| Loss: {current_loss:.4f} "
                    f"| Acc: {current_accuracy:.4f} "
                    f"| Temps: {elapsed:.1f}s",
                    flush=True
                )

        # ==========================================================
        # Statistiques finales de l'epoch
        # ==========================================================

        epoch_loss = running_loss / total
        epoch_accuracy = correct / total

        epoch_time = time.time() - start_time

        return epoch_loss, epoch_accuracy, epoch_time

    # ==============================================================
    # VALIDATION
    # ==============================================================

    @torch.no_grad()
    def validate(self):
        """
        Évalue le modèle sur le validation set.

        Important :
        - utilise val_loader
        - aucun backward
        - aucun optimizer.step()
        """

        self.model.eval()

        running_loss = 0.0
        correct = 0
        total = 0

        start_time = time.time()

        total_batches = len(self.val_loader)

        for batch_idx, (images, labels) in enumerate(
            self.val_loader,
            start=1
        ):

            images = images.to(self.device)
            labels = labels.to(self.device)

            # ------------------------------------------------------
            # Forward uniquement
            # ------------------------------------------------------

            outputs = self.model(images)

            # ------------------------------------------------------
            # Loss
            # ------------------------------------------------------

            loss = self.criterion(outputs, labels)

            # ------------------------------------------------------
            # Statistiques
            # ------------------------------------------------------

            running_loss += loss.item() * images.size(0)

            predictions = outputs.argmax(dim=1)

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

            # ------------------------------------------------------
            # Affichage
            # ------------------------------------------------------

            if batch_idx == 1 or batch_idx % 10 == 0:

                current_loss = running_loss / total
                current_accuracy = correct / total

                print(
                    f"  Val [{batch_idx}/{total_batches}] "
                    f"| Loss: {current_loss:.4f} "
                    f"| Acc: {current_accuracy:.4f}",
                    flush=True
                )

        # ==========================================================
        # Statistiques finales
        # ==========================================================

        epoch_loss = running_loss / total
        epoch_accuracy = correct / total

        epoch_time = time.time() - start_time

        return epoch_loss, epoch_accuracy, epoch_time

    # ==============================================================
    # FIT
    # ==============================================================

    def fit(self, epochs, max_train_batches=None):
        """
        Lance l'entraînement complet.
        """

        print("=" * 60)
        print("DÉBUT DE L'ENTRAÎNEMENT")
        print("=" * 60)

        print(f"Device : {self.device}")
        print(f"Epochs : {epochs}")
        print(f"Train batches : {len(self.train_loader)}")
        print(f"Validation batches : {len(self.val_loader)}")
        print("=" * 60)
        print()

        total_start_time = time.time()

        for epoch in range(epochs):

            print(
                f"Epoch [{epoch + 1}/{epochs}]"
            )
            print("-" * 60)

            # ------------------------------------------------------
            # TRAIN
            # ------------------------------------------------------

            train_loss, train_accuracy, train_time = (
                self.train_one_epoch(max_batches=max_train_batches)
            )

            # ------------------------------------------------------
            # VALIDATION
            # ------------------------------------------------------

            val_loss, val_accuracy, val_time = (
                self.validate()
            )

            # ------------------------------------------------------
            # Historique
            # ------------------------------------------------------

            self.history["train_loss"].append(
                train_loss
            )

            self.history["train_accuracy"].append(
                train_accuracy
            )

            self.history["val_loss"].append(
                val_loss
            )

            self.history["val_accuracy"].append(
                val_accuracy
            )

            # ------------------------------------------------------
            # Affichage epoch
            # ------------------------------------------------------

            print()
            print(
                f"Epoch [{epoch + 1}/{epochs}] terminée"
            )

            print(
                f"Train Loss : {train_loss:.4f}"
            )

            print(
                f"Train Acc  : {train_accuracy:.4f}"
            )

            print(
                f"Val Loss   : {val_loss:.4f}"
            )

            print(
                f"Val Acc    : {val_accuracy:.4f}"
            )

            print(
                f"Train Time : {train_time:.1f}s"
            )

            print(
                f"Val Time   : {val_time:.1f}s"
            )

            # ------------------------------------------------------
            # Sauvegarde du meilleur modèle
            # ------------------------------------------------------

            if val_accuracy > self.best_val_accuracy:

                self.best_val_accuracy = val_accuracy

                torch.save(
                    self.model.state_dict(),
                    self.save_path
                )

                print()
                print(
                    f"✓ Meilleur modèle sauvegardé : "
                    f"{self.save_path}"
                )

            print()

        # ==========================================================
        # FIN
        # ==========================================================

        total_time = time.time() - total_start_time

        print("=" * 60)
        print("ENTRAÎNEMENT TERMINÉ")
        print("=" * 60)

        print(
            f"Meilleure Val Accuracy : "
            f"{self.best_val_accuracy:.4f}"
        )

        print(
            f"Temps total : {total_time:.1f}s"
        )

        print("=" * 60)

        # ==========================================================
        # Sauvegarde de l'historique
        # ==========================================================

        metrics_dir = "results/metrics"
        os.makedirs(metrics_dir, exist_ok=True)

        model_name = os.path.splitext(
            os.path.basename(self.save_path)
        )[0]

        history_path = os.path.join(
            metrics_dir,
            f"{model_name}_history.json"
        )

        with open(history_path, "w") as f:
            json.dump(self.history, f, indent=4)

        print(
            f"Historique sauvegardé : {history_path}"
        )

        return self.history