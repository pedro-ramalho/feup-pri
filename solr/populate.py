import sqlite3
import json
import csv
import os

COLLECTION_SPECIES = 'species'
COLLECTION_OBSERVATIONS = 'observations'
COLLECTION_IMAGES = 'images'

SOLR_SPECIES_CSV_PATH = 'solr/data/species.csv'
SOLR_OBSERVATIONS_CSV_PATH = 'solr/data/observations.csv'
SOLR_IMAGES_CSV_PATH = 'solr/data/images.csv'

SOLR_SPECIES_COLLECTION_PATH = 'solr/data/species.json'
SOLR_OBSERVATIONS_COLLECTION_PATH = 'solr/data/observations.json'
SOLR_IMAGES_COLLECTION_PATH = 'solr/data/images.json'

conn = sqlite3.connect('data/databases/fungi.db')
cursor = conn.cursor()

species_list = [
    'Agrocybe pediades',  # 1 observation, 6 MV, Missing!
    'Amanita pantherina',  # 2 observations, 6 MV, Summary + 10 Abstracts
    'Astraeus hygrometricus',  # 3 observations, 6 MV, Summary + 10 Abstracts
    'Schizophyllum commune',  # 4 observations, 6 MV, Summary + 10 Abstracts
    'Cyclocybe aegerita',  # 5 observations, 6 MV, Summary + 10 Abstracts
    'Macrolepiota procera',  # 6 observations, 6 MV, Missing!
    'Lobaria pulmonaria',  # 8 observations, 6 MV, Summary + 10 Abstracts
    'Amanita muscaria',  # 9 observations, 6 MV, Summary + 10 Abstracts
    'Clathrus ruber',  # 9 observations, 6 MV, Summary + 2 Abstracts
    'Evernia prunastri',  # 12 observations, 6 MV, Summary + 10 Abstracts
    'Xanthoria parietina',  # 18 observations, 6 MV, Summary + 10 Abstracts
]

species = [cursor.execute(
    f'SELECT * FROM species WHERE species = "{sp}"').fetchall()[0] for sp in species_list]

observations = [cursor.execute(
    f'SELECT * FROM observations WHERE species="{sp}" LIMIT 10').fetchall() for sp in species_list]

images = []
for observation_list in observations:
    for observation in observation_list:
        query = f'SELECT * FROM images WHERE gbif_id="{observation[2]}" LIMIT 10'
        images.append(cursor.execute(query).fetchall())

species_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(species)').fetchall()]
observations_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(observations)').fetchall()]
images_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(images)').fetchall()]


def flatten_list(lst: list) -> list:
    flattened_list = []
    for lst_elem in lst:
        if len(lst_elem) > 0:
            for tup_elem in lst_elem:
                flattened_list.append(tup_elem)

    return flattened_list


observations = flatten_list(observations)
images = flatten_list(images)


def mk_dict(keys: list, data: list) -> list[dict[str, str]]:
    return [dict(zip(keys, data[i])) for i in range(len(data))]


species_dicts = mk_dict(species_columns, species)
observations_dicts = mk_dict(observations_columns, observations)
images_dicts = mk_dict(images_columns, images)


def populate_collection(data: list[dict[str, str]], collection_name: str) -> None:
    with open(f'solr/data/{collection_name}.json', 'w') as file:
        json.dump(data, file, indent=4)


populate_collection(species_dicts, COLLECTION_SPECIES)
populate_collection(observations_dicts, COLLECTION_OBSERVATIONS)
populate_collection(images_dicts, COLLECTION_IMAGES)


def concatenate_summary_abstracts(species_list: list, data_directory: str) -> list:
    concatenated_data = []

    for species in species_list:
        file_path = os.path.join(
            data_directory, f'unprocessed/{species[0]}/{species}.json')

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                species_data = json.load(file)

                species_data['species'] = species

                concatenated_data.append(species_data)

    return concatenated_data


concatenated_data = concatenate_summary_abstracts(species_list, 'data/')

with open('solr/data/summary-abstracts.json', 'w') as file:
    json.dump(concatenated_data, file, indent=4)

conn.close()
