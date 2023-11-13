import sqlite3
import csv

SOLR_SPECIES_CSV_PATH = 'solr/data/species.csv'
SOLR_OBSERVATIONS_CSV_PATH = 'solr/data/observations.csv'
SOLR_IMAGES_CSV_PATH = 'solr/data/images.csv'

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
    f'SELECT * FROM observations WHERE species="{sp}"').fetchall() for sp in species_list]

images = []
for observation_list in observations:
    for observation in observation_list:
        query = f'SELECT * FROM images WHERE gbif_id="{observation[2]}"'
        images.append(cursor.execute(query).fetchall())

species_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(species)').fetchall()]
observations_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(observations)').fetchall()]
images_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(images)').fetchall()]


def wr_csv(path: str, columns: list, data: list) -> None:
    with open(path, 'w', newline='') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(columns)
        file_writer.writerows(data)


def flatten_list(lst: list) -> list:
    flattened_list = []
    for lst_elem in lst:
        if len(lst_elem) > 0:
            for tup_elem in lst_elem:
                flattened_list.append(tup_elem)

    return flattened_list


observations = flatten_list(observations)
images = flatten_list(images)

wr_csv(SOLR_SPECIES_CSV_PATH, species_columns, species)
wr_csv(SOLR_OBSERVATIONS_CSV_PATH, observations_columns, observations)
wr_csv(SOLR_IMAGES_CSV_PATH, images_columns, images)

print(f'species: {species}')
print()
print(f'observations: {observations}')
print()
print(f'images: {images}')

conn.close()
