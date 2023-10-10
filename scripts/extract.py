import pandas as pd
import sqlite3

DATASET_OCCURRENCES = '../data/datasets/sample_occurrence.txt'
DATASET_VERBATIM = '../data/datasets/sample_verbatim.txt'

CSV_SPECIES = '../data/processed/species.csv'

DB_OCURRENCES = '../data/databases/occurrences.db'

CHAR_ARROW = '\u2192'

CHUNK_SIZE = 5000


# load the datasets
print(f'Executing extract.py')

occurrences_df = pd.read_csv(DATASET_OCCURRENCES, sep='\t')
print(f'\t{CHAR_ARROW} Loaded occurrences.txt successfully')

verbatim_df = pd.read_csv(DATASET_VERBATIM, sep='\t')
print(f'\t{CHAR_ARROW} Loaded verbatim.txt successfully')

# fetch the columns
occurrences_columns = set(occurrences_df.columns)
print(f'\t{CHAR_ARROW} Fetched occurrences columns successfully')

verbatim_columns = set(verbatim_df.columns)
print(f'\t{CHAR_ARROW} Fetched verbatim columns successfully')

occurrences_only_columns = occurrences_columns - verbatim_columns
verbatim_only_columns = verbatim_columns - occurrences_columns
all_columns = occurrences_columns | verbatim_columns

num_lines_occurrences = occurrences_df.shape[0]
num_lines_verbatim = verbatim_df.shape[0]

# join occurence and verbatim dataframes
for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]
print(f'\t{CHAR_ARROW} Joined the occurrence and verbatim dataframes successfully')

# remove empty columns from resulting dataframe
initial_num_columns = occurrences_df.shape[1]
occurrences_df = occurrences_df.dropna(axis=1, how='all')
final_num_columns = occurrences_df.shape[1]
print(f'\t{CHAR_ARROW} Removed empty columns from the resulting dataframe')

# save the species list
species = pd.DataFrame({'species': occurrences_df['species'].unique()})
species.to_csv(CSV_SPECIES, index=False)
print(f'\t{CHAR_ARROW} Saved the species list to a file successfully')

# generate the database
conn = sqlite3.connect(DB_OCURRENCES)
occurrences_df.to_sql(DB_OCURRENCES, conn, 'occurrences', if_exists='replace')
conn.close()
print(f'\t{CHAR_ARROW} Generated the database successfully')
