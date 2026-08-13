from PIL import Image
from torch.utils.data import Dataset

class CUBDataset(Dataset):
    def __init__(self, dataframe, transform=None, label_map=None):
        self.df = dataframe.reset_index(drop=True)
        self.transform = transform
        self.label_map = label_map or {c: i for i, c in enumerate(sorted(dataframe['class_id'].unique()))}

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img = Image.open(row['image_path']).convert('RGB')
        if self.transform:
            img = self.transform(img)
        label = self.label_map[row['class_id']]
        return img, label