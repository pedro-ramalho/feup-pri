import pandas as pd
import sqlite3

occurrences_df = pd.read_csv(
    '../data/occurrence.txt', sep='\t', low_memory=False)
verbatim_df = pd.read_csv('../data/verbatim.txt', sep='\t', low_memory=False)

occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)


occurrences_only_columns = occurrences_columns - verbatim_columns
verbatim_only_columns = verbatim_columns - occurrences_columns
all_columns = occurrences_columns | verbatim_columns


num_lines_occurrences = occurrences_df.shape[0]
num_lines_verbatim = verbatim_df.shape[0]

print(f"Number of lines in 'occurences.txt': {num_lines_occurrences}")
print(f"Number of lines in 'verbatim.txt': {num_lines_verbatim}")

print("Columns present in 'occurences.txt' but not in 'verbatim.txt':")
print(occurrences_only_columns)

print("\nColumns present in 'verbatim.txt' but not in 'occurences.txt':")
print(verbatim_only_columns)


# join occurence and verbatim dataframes
for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]

# remove empty columns from resulting dataframe
initial_num_columns = occurrences_df.shape[1]
occurrences_df = occurrences_df.dropna(axis=1, how='all')
final_num_columns = occurrences_df.shape[1]
print(f"Number of columns removed: {initial_num_columns - final_num_columns}")

occurrences_df['species'].unique().to_csv(
    '../data/processed/species.csv', index=False)

# generate database
conn = sqlite3.connect('occurrences.db')

occurrences_df.to_sql("occurrences.db", conn,
                      "occurrences", if_exists="replace")

conn.close()
