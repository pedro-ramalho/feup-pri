import sqlite3
import csv

SOLR_SPECIES_CSV_PATH = 'solr/data/species.csv'
SOLR_OBSERVATIONS_CSV_PATH = 'solr/data/observations.csv'
SOLR_IMAGES_CSV_PATH = 'solr/data/images.csv'

conn = sqlite3.connect('data/databases/fungi.db')
cursor = conn.cursor()

species_columns = [col[1] for col in cursor.fetchall()]

species_list = [
    'Agrocybe pediades',  # 1 observation
    'Amanita pantherina',  # 2 observations
    'Astraeus hygrometricus',  # 3 observations
    'Schizophyllum commune',  # 4 observations
    'Cyclocybe aegerita',  # 5 observations
    'Macrolepiota procera',  # 6 observations
    'Lobaria pulmonaria',  # 8 observations
    'Amanita muscaria',  # 9 observations
    'Clathrus ruber',  # 9 observations
    'Evernia prunastri',  # 12 observations
    'Xanthoria parietina',  # 18 observations
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
    'PRAGMA table_info(species)').fetchall()][1:]
observations_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(observations)').fetchall()][1:]
images_columns = [col[1] for col in cursor.execute(
    'PRAGMA table_info(images)').fetchall()][1:]


def wr_csv(path: str, data: list) -> None:
    with open(path, 'w', newline='') as file:
        file_writer = csv.writer(file)
        file_writer.writerows(data)


wr_csv(SOLR_SPECIES_CSV_PATH, species)
wr_csv(SOLR_OBSERVATIONS_CSV_PATH, observations)
wr_csv(SOLR_IMAGES_CSV_PATH, images)

conn.close()
