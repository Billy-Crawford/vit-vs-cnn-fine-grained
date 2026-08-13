import os

DATA_ROOT = os.environ.get('CUB_DATA_ROOT', '/content/drive/MyDrive/Projet_annuel/Dataset/CUB_200_2011/CUB_200_2011')
OUT_DIR = os.environ.get('CUB_OUT_DIR', '/content/drive/MyDrive/Projet_annuel/data_processed')
MLFLOW_URI = os.environ.get('CUB_MLFLOW_URI', 'sqlite:////content/drive/MyDrive/Projet_annuel/mlflow.db')

SEED = 42
IMAGE_SIZE = 224
VAL_FRACTION = 0.15
SUBSET_FRACTIONS = [0.10, 0.25, 0.50, 1.00]

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]