import pandas as pd
from PIL import Image
import numpy as np
import os

from src.data.dataset import CUBDataset
from src.data.transforms import get_val_transform

# Créer une image factice temporaire
os.makedirs('tests/tmp', exist_ok=True)
fake_img_path = 'tests/tmp/fake.jpg'
Image.fromarray((np.random.rand(300, 300, 3) * 255).astype('uint8')).save(fake_img_path)

# DataFrame minimal, juste pour tester la classe
df_fake = pd.DataFrame({
    'image_path': [fake_img_path] * 3,
    'class_id': [1, 2, 1],
})

ds = CUBDataset(df_fake, transform=get_val_transform())
img, label = ds[0]
print(f"Shape: {img.shape}, Label: {label}, dtype: {img.dtype}")
assert img.shape == (3, 224, 224), "Shape incorrecte"
print("Test OK.")