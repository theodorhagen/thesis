import pandas as pd

meta = pd.read_parquet('../data/metadata.parquet')

def patch_to_season(patch_id):
    """
    Defines the season for a given Sentinel-Patch using the corresponding Patch-ID.

    Args:
        patch_id (str): The Patch-ID with format '..._YYYYMMDD_...'.

    Returns:
        str: The season that corresponds to the month on the Patch-ID string.
    """
    date_str = patch_id.split('_')[2]
    month = int(date_str[4:6])
    
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'

#map each patch to one season
meta['season'] = meta['patch_id'].apply(patch_to_season)

#create one df for each season
winter = meta[meta['season'] == 'winter']
spring = meta[meta['season'] == 'spring']
summer = meta[meta['season'] == 'summer']
fall = meta[meta['season'] == 'fall']

#create metadata-csv for each new df
for season, df in zip(['winter', 'spring', 'summer', 'fall'], [winter, spring, summer, fall]):
    df.to_parquet(f'patchlists/patches_{season}.parquet', index=False)
