import pandas as pd
import sqlite3
from collections import Counter

DATASET_OCCURRENCES = '../data/datasets/occurrence.txt'
DATASET_VERBATIM = '../data/datasets/verbatim.txt'

CSV_SPECIES = '../data/processed/species.csv'
CSV_SPECIES_DATA = '../data/processed/species_data.csv'

DB_FUNGI = '../data/databases/fungi.db'


def get_most_common(lst):
    counts = Counter(lst)
    return counts.most_common()[0][0]


species_file = open(CSV_SPECIES, "r")

species_list = map(lambda x: x[:-1], species_file.readlines())

occurrences_df = pd.read_csv(DATASET_OCCURRENCES, sep='\t', low_memory=False)
verbatim_df = pd.read_csv(DATASET_VERBATIM, sep='\t', low_memory=False)

occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)

interesting_columns = [
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

verbatim_only_columns = verbatim_columns - occurrences_columns

for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]

species_df = pd.DataFrame(columns=interesting_columns)

for species in species_list:
    species_related = occurrences_df[occurrences_df['species'] == species]
    to_add = [species]
    for column in interesting_columns[1:]:
        results = list(species_related[column].dropna())
        if len(results) > 1:
            print(
                f"{species} has more than one value in {column}. Example: {results[0]}, {results[1]}")
            to_add.append(get_most_common(results))
        elif len(results) == 1:
            to_add.append(results[0])
        else:
            to_add.append("")
    species_df.loc[len(species_df.index)] = to_add

species_df.to_csv(CSV_SPECIES_DATA)

conn = sqlite3.connect(DB_FUNGI)

species_df.to_sql('species', con=conn, if_exists='replace')

conn.close()
