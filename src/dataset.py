import os
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import rasterio
from skimage.transform import resize

class BigEarthNetDataset(Dataset):
    ALL_LABELS = [
        'Permanent crops', 'Complex cultivation patterns', 'Marine waters', 
        'Natural grassland and sparsely vegetated areas', 'Moors, heathland and sclerophyllous vegetation', 
        'Mixed forest', 'Coastal wetlands', 'Industrial or commercial units', 'Urban fabric', 'Arable land', 
        'Land principally occupied by agriculture, with significant areas of natural vegetation', 
        'Agro-forestry areas', 'Broad-leaved forest', 'Inland waters', 'Coniferous forest', 
        'Transitional woodland, shrub', 'Beaches, dunes, sands', 'Pastures', 'Inland wetlands'
    ]
    ALL_LABELS.sort()

    LABEL2IDX = {label: i for i, label in enumerate(ALL_LABELS)}

    ALL_BANDS = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B11', 'B12']


    def __init__(self, parquet_path, root_dir, bands=ALL_BANDS, label2idx=LABEL2IDX, transform=None):
        
        self.df = pd.read_parquet(parquet_path)
        self.root_dir = root_dir
        self.bands = bands
        self.label2idx = label2idx
        self.transform = transform


    def __len__(self):
        return len(self.df)
    
    
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        patch_id = row['patch_id']
        tile = '_'.join(patch_id.split('_')[:-2])
        patch_dir = os.path.join(self.root_dir, "BigEarthNet-S2-Subset", tile, patch_id)

        #stack all channels into a Numpy 3D-array with shape (12, 120, 120) for pytorch
        channels = []
        for band in self.bands:
            band_path = os.path.join(patch_dir, f'{patch_id}_{band}.tif')
            with rasterio.open(band_path) as src:
                arr = src.read(1)
            if arr.shape != (120, 120):
                #resizing with bilinear interpolation
                arr = resize(arr, (120, 120), order=1, preserve_range=True, anti_aliasing=True).astype(arr.dtype)
            channels.append(arr)
        image = np.stack(channels, axis=0)

        #create multi-hot-vector for labels
        label_names = row['labels']
        label_vec = np.array([1.0 if label in label_names else 0.0 for label in self.label2idx], dtype=np.float32)


        #transform image
        if self.transform:
            image = self.transform(image)
        
        return image, label_vec

