import pandas as pd

#Creates a txt file with a subset of patches for extraction
winter_df = pd.read_parquet('patchlists/patches_winter.parquet')
sample_ids_winter = winter_df['patch_id'].head(100).tolist()

spring_df = pd.read_parquet('patchlists/patches_spring.parquet')
sample_ids_spring = spring_df['patch_id'].head(100).tolist()

summer_df = pd.read_parquet('patchlists/patches_summer.parquet')
sample_ids_summer = summer_df['patch_id'].head(100).tolist()

fall_df = pd.read_parquet('patchlists/patches_fall.parquet')
sample_ids_fall = fall_df['patch_id'].head(100).tolist()

sample_ids = sample_ids_winter + sample_ids_spring + sample_ids_summer + sample_ids_fall

def get_tile_from_patchid(pid):
    return '_'.join(pid.split('_')[:-2])

with open('patchlists/patch_ids_subset.txt', 'w') as f:
    for pid in sample_ids:
        tile = get_tile_from_patchid(pid)
        f.write(f"BigEarthNet-S2/{tile}/{pid}/\n")

#create metadata-csv for each new df
for season, df in zip(['winter', 'spring', 'summer', 'fall'], [winter_df.head(100), spring_df.head(100), summer_df.head(100), fall_df.head(100)]):
    df.to_parquet(f'patchlists/patches_{season}_subset.parquet', index=False)