import pandas as pd
import sqlite3


observation_columns = {
    'species' : 'species',
    'gbifID' : 'gbif_id',
    'year' : 'year',
    'month': 'month',
    'day': 'day',
    'countryCode': 'country_code', # ES or PT
    'level1Name': 'district', # level1Name & stateProvince - Distrito 
    'level2Name': 'county', # level2Name & municipality & county - Concelho
    'level3Name' : 'parish', # level3Name - Freguesia 
    'decimalLongitude': 'longitude', # decimalLongitude
    'decimalLatitude' : 'latitude', # decimalLatitude
    'recordedBy' : 'author'
}

occurrences_df = pd.read_csv('data/occurrence.txt', sep='\t', low_memory=False)
multimedia_df = pd.read_csv('data/multimedia.txt', sep="\t", low_memory=False)

occurrences_df = occurrences_df.rename(columns={"county": "county_temp"})
occurrences_df = occurrences_df.rename(columns=observation_columns)

media_columns = {
    'gbifID': 'gbif_id',
    'references': 'image_link'
}

occurrences_df = occurrences_df.dropna(subset=['latitude', 'longitude'], how='all')
occurrences_df = occurrences_df.reset_index(drop=True)

occurrences_df['district'].fillna(occurrences_df['stateProvince'], inplace=True)
occurrences_df['county'].fillna(occurrences_df['municipality'], inplace=True)
occurrences_df['county'].fillna(occurrences_df['county_temp'], inplace=True)
occurrences_df['author'].fillna(occurrences_df['identifiedBy'], inplace=True)
occurrences_df['author'].fillna(occurrences_df['rightsHolder'], inplace=True)

observations_df = occurrences_df.loc[:, list(observation_columns.values())]


multimedia_df = multimedia_df.rename(columns=media_columns)
print(f"multimedia_df length {len(multimedia_df['image_link'])}")

multimedia_df = multimedia_df[multimedia_df['type'] == 'StillImage']
print(f"multimedia_df length {len(multimedia_df['image_link'])}")
multimedia_df = multimedia_df.loc[:, list(media_columns.values())]
print(f"multimedia_df length {len(multimedia_df['image_link'])}")

conn = sqlite3.connect('fungi.db')

observations_df.to_sql('observations', con=conn, if_exists='replace')
multimedia_df.to_sql('images', con=conn, if_exists='replace')

conn.close()