import pandas as pd
import sqlite3

from collections import Counter

from constants import *


# load the datasets
df_occurrences = pd.read_csv(DATASET_OCCURRENCES, sep='\t', low_memory=False)
df_multimedia = pd.read_csv(DATASET_MULTIMEDIA, sep='\t', low_memory=False)
print(f'{CHAR_ARROW} Loaded the datasets')

# create the list of species
pd.DataFrame({'species': df_occurrences['species'].unique()}).to_csv(
    CSV_SPECIES, index=False)
print(f'{CHAR_ARROW} Created the list of species')

# handle occurrences and multimedia
columns_occurrences = {
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

columns_multimedia = {
    'gbifID': 'gbif_id',
    'references': 'image_link'
}

df_occurrences = df_occurrences.rename(columns={'county': 'county_temp'})
df_occurrences = df_occurrences.rename(columns=columns_occurrences)
df_occurrences = df_occurrences.dropna(
    subset=['latitude', 'longitude'], how='all')
df_occurrences = df_occurrences.reset_index(drop=True)

df_occurrences['district'].fillna(
    df_occurrences['stateProvince'], inplace=True)
df_occurrences['county'].fillna(df_occurrences['municipality'], inplace=True)
df_occurrences['county'].fillna(df_occurrences['county_temp'], inplace=True)
df_occurrences['author'].fillna(df_occurrences['identifiedBy'], inplace=True)
df_occurrences['author'].fillna(df_occurrences['rightsHolder'], inplace=True)
df_occurrences = df_occurrences.dropna(subset=['year'])
df_occurrences['month'].fillna(6, inplace=True)
df_occurrences['day'].fillna(15, inplace=True)

print(f'{CHAR_ARROW} Renamed occurrences columns and dropped NULLS')

df_observations = df_occurrences.loc[:, list(columns_occurrences.values())]

df_observations['date'] = pd.to_datetime(df_observations[['year', 'month', 'day']].astype(int).astype(str).agg('-'.join, axis=1), format='%Y-%m-%d')
df_observations = df_observations.drop(['year', 'month', 'day'], axis=1)


df_multimedia = df_multimedia.rename(columns=columns_multimedia)
print(f'{CHAR_ARROW} Renamed multimedia columns')

# handle species
species_list = list(df_occurrences['species'].unique())

columns_species = [
    'species',
    'infraspecificEpithet',
    'class',
    'iucnRedListCategory',
    'kingdom',
    'sex',
    'phylum',
    'specificEpithet',
    'vernacularName',
    'genericName',
    'family',
    'datasetName',
    'higherClassification',
    'subgenus',
    'organismName'
]

df_species = pd.DataFrame(columns=columns_species)


def get_most_common(lst):
    counts = Counter(lst)
    return counts.most_common()[0][0]


for species in species_list:
    species_related = df_occurrences[df_occurrences['species'] == species]
    to_add = [species]
    for column in columns_species[1:]:
        results = list(species_related[column].dropna())
        if len(results) > 1:
            to_add.append(get_most_common(results))
        elif len(results) == 1:
            to_add.append(results[0])
        else:
            to_add.append("")
    df_species.loc[len(df_species.index)] = to_add

print(f'{CHAR_ARROW} Finished building the species dataframe')

# load databases
connection = sqlite3.connect(DATABASE_FUNGI)

df_observations.to_sql('observations', con=connection, if_exists='replace')
df_multimedia.to_sql('images', con=connection, if_exists='replace')
df_species.to_sql('species', con=connection, if_exists='replace')

print(f'{CHAR_ARROW} Loaded each dataframe into the database')

connection.close()
