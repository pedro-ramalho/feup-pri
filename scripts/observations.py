import pandas as pd
import sqlite3

DATASET_OCCURRENCES = '../data/datasets/occurrence.txt'
DATASET_MULTIMEDIA = '../data/datasets/multimedia.txt'

DB_FUNGI = '../data/databases/fungi.db'

observation_columns = {
    'species': 'species',
    'gbifID': 'gbif_id',
    'year': 'year',
    'month': 'month',
    'day': 'day',
    'countryCode': 'country_code',  
    'level1Name': 'district',  
    'level2Name': 'county',  
    'level3Name': 'parish',  
    'decimalLongitude': 'longitude',  
    'decimalLatitude': 'latitude',  
    'recordedBy': 'author'
}

occurrences_df = pd.read_csv(DATASET_OCCURRENCES, sep='\t', low_memory=False)
multimedia_df = pd.read_csv(DATASET_MULTIMEDIA, sep="\t", low_memory=False)

occurrences_df = occurrences_df.rename(columns={'county': 'county_temp'})
occurrences_df = occurrences_df.rename(columns=observation_columns)

media_columns = {
    'gbifID': 'gbif_id',
    'references': 'image_link'
}

occurrences_df = occurrences_df.dropna(
    subset=['latitude', 'longitude'], how='all')
occurrences_df = occurrences_df.reset_index(drop=True)

occurrences_df['district'].fillna(
    occurrences_df['stateProvince'], inplace=True)
occurrences_df['county'].fillna(occurrences_df['municipality'], inplace=True)
occurrences_df['county'].fillna(occurrences_df['county_temp'], inplace=True)
occurrences_df['author'].fillna(occurrences_df['identifiedBy'], inplace=True)
occurrences_df['author'].fillna(occurrences_df['rightsHolder'], inplace=True)

observations_df = occurrences_df.loc[:, list(observation_columns.values())]

multimedia_df = multimedia_df.rename(columns=media_columns)

conn = sqlite3.connect(DB_FUNGI)

observations_df.to_sql('observations', con=conn, if_exists='replace')
multimedia_df.to_sql('images', con=conn, if_exists='replace')

conn.close()
