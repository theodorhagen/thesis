import pandas as pd
import os
print(os.getcwd())

df = pd.read_csv('../patchlists/patches_winter.csv')
sample_ids_winter = df['patch_id'].head(100).tolist()

df = pd.read_csv('../patchlists/patches_spring.csv')
sample_ids_spring = df['patch_id'].head(100).tolist()

df = pd.read_csv('../patchlists/patches_summer.csv')
sample_ids_summer = df['patch_id'].head(100).tolist()

df = pd.read_csv('../patchlists/patches_fall.csv')
sample_ids_fall = df['patch_id'].head(100).tolist()

sample_ids = sample_ids_winter + sample_ids_spring + sample_ids_summer + sample_ids_fall

def get_tile_from_patchid(pid):
    return '_'.join(pid.split('_')[:-2])

with open('../patchlists/patch_ids_subset.txt', 'w') as f:
    for pid in sample_ids:
        tile = get_tile_from_patchid(pid)
        f.write(f"BigEarthNet-S2/{tile}/{pid}/\n")