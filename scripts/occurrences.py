import pandas as pd

occurrences_df = pd.read_csv('../data/occurrence.txt', sep='\t', low_memory=False)
verbatim_df = pd.read_csv('../data/verbatim.txt', sep='\t', low_memory=False)

occurrences_columns = set(occurrences_df.columns)
verbatim_columns = set(verbatim_df.columns)


verbatim_only_columns = verbatim_columns - occurrences_columns

for column in verbatim_only_columns:
    occurrences_df[column] = verbatim_df[column]


interestingColumns = [
    "species",
    "individualCount",
    "organismQuantity",
    "lifeStage",
    "habitat",
    "higherGeography",
    "continent",
    "country",
    "countryCode",
    "waterBody",
    "islandGroup",
    "island",
    "stateProvince",
    "county",
    "municipality",
    "locality",
    "eventDate",
    "decimalLatitude",
    "decimalLongitude",
    "depth",
    "elevation"
]


occurrences_df = occurrences_df[interestingColumns]

occurrences_df.to_csv("../data/processed/occurrences_data.csv")
