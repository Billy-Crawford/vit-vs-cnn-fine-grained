import os
import pandas as pd
from .config import DATA_ROOT, OUT_DIR

def build_metadata():
    images = pd.read_csv(f'{DATA_ROOT}/images.txt', sep=' ', names=['image_id', 'image_name'])
    labels = pd.read_csv(f'{DATA_ROOT}/image_class_labels.txt', sep=' ', names=['image_id', 'class_id'])
    classes = pd.read_csv(f'{DATA_ROOT}/classes.txt', sep=' ', names=['class_id', 'class_name'])
    split = pd.read_csv(f'{DATA_ROOT}/train_test_split.txt', sep=' ', names=['image_id', 'is_training'])

    df = images.merge(labels, on='image_id').merge(classes, on='class_id').merge(split, on='image_id')
    df['image_path'] = df['image_name'].apply(lambda x: f'{DATA_ROOT}/images/{x}')

    missing = df[~df['image_path'].apply(os.path.exists)]
    if len(missing) > 0:
        print(f"ATTENTION : {len(missing)} images manquantes")

    os.makedirs(OUT_DIR, exist_ok=True)
    df.to_csv(f'{OUT_DIR}/metadata.csv', index=False)
    print(f"metadata.csv sauvegardé : {df.shape}")
    return df

if __name__ == '__main__':
    build_metadata()