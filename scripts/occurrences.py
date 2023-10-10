import pandas as pd

DATASET_OCCURRENCES = '../data/datasets/occurrence.txt'
DATASET_VERBATIM = '../data/datasets/verbatim.txt'

CSV_OCCURRENCES = '../data/processed/occurrences_data.csv'

occurrences_df = pd.read_csv(DATASET_OCCURRENCES, sep='\t', low_memory=False)
verbatim_df = pd.read_csv(DATASET_VERBATIM, sep='\t', low_memory=False)

occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)


verbatim_only_columns = verbatim_columns - occurrences_columns

for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]


interestingColumns = [
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

occurrences_df = occurrences_df[interestingColumns]

occurrences_df.to_csv(CSV_OCCURRENCES)
