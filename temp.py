import pandas as pd

occurrences_df = pd.read_csv('data/occurrence.txt', sep='\t', low_memory=False)
verbatim_df = pd.read_csv('data/verbatim.txt', sep='\t', low_memory=False)

occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)

occurrences_only_columns = occurrences_columns - verbatim_columns
verbatim_only_columns = verbatim_columns - occurrences_columns

for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]

for col in occurrences_df.columns:
    null_percentage = occurrences_df[col].isnull().sum() / len(occurrences_df[col])
    print(f"{col}: {null_percentage*100}")