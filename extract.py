import pandas as pd


occurrences_df = pd.read_csv('data/occurrence.txt', sep='\t')
verbatim_df = pd.read_csv('data/verbatim.txt', sep='\t')
#multimedia_df = pd.read_csv('data/multimedia.txt', sep='\t')


occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)


occurrences_only_columns = occurrences_columns - verbatim_columns
verbatim_only_columns = verbatim_columns - occurrences_columns


num_lines_occurrences = occurrences_df.shape[0]
num_lines_verbatim = verbatim_df.shape[0]
#num_lines_multimedia = multimedia_df.shape[0]

print(f"Number of lines in 'occurences.txt': {num_lines_occurrences}")
print(f"Number of lines in 'verbatim.txt': {num_lines_verbatim}")
#print(f"Number of lines in 'multimedia.txt': {num_lines_multimedia}")

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
#print(f"Remaining columns: {set(occurrences_df.columns)}")


# extract Species (no occurrence dependent information) to a new csv

species_df = occurrences_df[['species']].copy() # add more columns if fit (not all occurrences have the species taxon btw)
# a lot of species will appear multiple times, need to define how to filter
species_df.to_csv('data/processed/species.csv', index=False)


# extract Occurrences to a new csv