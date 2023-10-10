import pandas as pd

from constants import *

DATASET_OCCURRENCES = '../data/datasets/sample_occurrence.txt'
DATASET_VERBATIM = '../data/datasets/sample_verbatim.txt'

CSV_OCCURRENCES = '../data/processed/sample_occurrences_data.csv'

print('Executing occurrences.py')
occurrences_df = pd.read_csv(DATASET_OCCURRENCES, sep='\t', low_memory=False)
print(f'\t{CHAR_ARROW} Loaded occurrences.txt successfully')

verbatim_df = pd.read_csv(DATASET_VERBATIM, sep='\t', low_memory=False)
print(f'\t{CHAR_ARROW} Loaded verbatim.txt successfully')

occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)

verbatim_only_columns = verbatim_columns - occurrences_columns

for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]


interesting_columns = [
    'species',
    'individualCount',
    'organismQuantity',
    'lifeStage',
    'habitat',
    'higherGeography',
    'continent',
    'country',
    'countryCode',
    'waterBody',
    'islandGroup',
    'island',
    'stateProvince',
    'county',
    'municipality',
    'locality',
    'eventDate',
    'decimalLatitude',
    'decimalLongitude',
    'depth',
    'elevation'
]

occurrences_df = occurrences_df[interesting_columns]

occurrences_df.to_csv(CSV_OCCURRENCES)
print(f'\t{CHAR_ARROW} Written a CSV with occurrences data successfully')
