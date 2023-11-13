import pandas as pd
from constants import *
import sqlite3
import matplotlib.pyplot as plt
import math

conn = sqlite3.connect(DATABASE_FUNGI)

observations = pd.read_sql_query('''
                               SELECT
                               *
                               FROM observations
                               ''', conn)

species = pd.read_sql_query('''
                               SELECT
                               *
                               FROM species
                               ''', conn)

images = pd.read_sql_query('''
                               SELECT
                               *
                               FROM images
                               ''', conn)

observations_df = pd.DataFrame(observations, columns=["index", "species", "gbif_id", "year", "month",
                               "day", "country_code", "district", "county", "parish", "longitude", "latitude", "author"])

species_df = df = pd.DataFrame(species, columns=["index", "species", "infraspecificEpithet", "class", "iucnRedListCategory", "kingdom", "sex",
                               "phylum", "specificEpithet", "vernacularName", "genericName", "family", "datasetName", "higherClassification", "subgenus", "organismName"])

images_df = pd.DataFrame(images, columns=["index", "gbif_id", "type", "format", "identifier", "image_link", "title",
                         "description", "source", "audience", "created", "creator", "contributor", "publisher", "license", "rightsHolder"])

observations_null_percentages = []
species_null_percentages = []

for col in [x for x in observations_df.columns if x != "index"]:
    null_percentage = 100 * \
        observations_df[col].isnull().sum() / len(observations_df[col])
    observations_null_percentages.append((col, null_percentage))

for col in [x for x in species_df.columns if x != "index"]:
    null_percentage = 100 * \
        species_df[col].isnull().sum() / len(species_df[col])
    species_null_percentages.append((col, null_percentage))


plt.bar([x[0] for x in observations_null_percentages], [x[1]
        for x in observations_null_percentages], color='skyblue', edgecolor='black')
plt.title('Data completeness in Observations')
plt.xlabel('Attribute')
plt.ylabel('Percentage of missing values')
plt.xticks(rotation=90, fontsize='x-small')
plt.tight_layout()
plt.savefig(fname="data/characterization/observation_completeness.png",
            format="png", transparent=False)
plt.clf()

plt.bar([x[0] for x in species_null_percentages], [x[1]
        for x in species_null_percentages], color='skyblue', edgecolor='black')
plt.title('Data completeness in Species')
plt.xlabel('Attribute')
plt.ylabel('Percentage of missing values')
plt.xticks(rotation=90, fontsize='x-small')
plt.tight_layout()
plt.savefig(fname="data/characterization/species_completeness.png",
            format="png", transparent=False)
plt.clf()

species_observations = []
for species in species_df['species']:
    species_observations.append(
        (species, len(observations_df[observations_df['species'] == species])))

species_observations.sort(key=lambda x: x[1], reverse=True)

top_15_species = species_observations[:15]

plt.bar([x[0] for x in top_15_species], [x[1]
        for x in top_15_species], color='skyblue', edgecolor='black')
plt.title('Most observed species')
plt.xlabel('Species name')
plt.ylabel('Number of observations')
plt.xticks(rotation=90, fontsize='x-small')
plt.tight_layout()
plt.savefig(fname="data/characterization/species_observations.png",
            format="png", transparent=False)
plt.clf()

portugal_district_observations = []
spain_district_observations = []

for district in observations_df[observations_df['country_code'] == "PT"]['district'].unique():
    portugal_district_observations.append((district, len(
        observations_df[observations_df['country_code'] == "PT"][observations_df['district'] == district]['district'])))

for district in observations_df[observations_df['country_code'] == "ES"]['district'].unique():
    spain_district_observations.append((district, len(
        observations_df[observations_df['country_code'] == "ES"][observations_df['district'] == district]['district'])))

portugal_district_observations.sort(key=lambda x: x[1], reverse=True)
spain_district_observations.sort(key=lambda x: x[1], reverse=True)

top_5_portugal = portugal_district_observations[:min(
    5, len(portugal_district_observations))]
top_5_spain = spain_district_observations[:min(
    5, len(spain_district_observations))]

bars = plt.bar(["ES - " + x[0] for x in top_5_spain] + ["PT - " + x[0]
               for x in top_5_portugal], [x[1] for x in top_5_spain + top_5_portugal], edgecolor='black')

# yes the name implies top 5 but there could be less
for i in range(len(top_5_spain)):
    bars[i].set_color('tab:orange')

for i in range(len(top_5_spain), len(top_5_spain) + len(top_5_portugal)):
    bars[i].set_color('tab:blue')

plt.title('Districts with most observations')
plt.xlabel('Country and district')
plt.ylabel('Number of observations')
plt.xticks(rotation=90, fontsize='x-small')
plt.tight_layout()
plt.savefig(fname="data/characterization/district_observations.png",
            format="png", transparent=False)
plt.clf()

portugal_observations = len(
    observations_df[observations_df['country_code'] == "PT"])
spain_observations = len(
    observations_df[observations_df['country_code'] == "ES"])

total = portugal_observations + spain_observations

plt.pie([portugal_observations, spain_observations], labels=["Portugal", "Spain"],
        autopct=lambda x: f"{math.trunc(total * x/100000)}k ({round(x, 1)}%)")
plt.tight_layout()
plt.savefig(fname="data/characterization/observation_distribution_by_country.png",
            format="png", transparent=False)
plt.clf()

plt.hist(observations_df['year'].dropna(), bins=30,
         color='skyblue', edgecolor='black')
plt.xlabel('Year')
plt.ylabel('Count of Observations')
plt.title('Distribution of Observations by Year')
plt.tight_layout()
plt.savefig('data/characterization/observation_distribution_by_year.png',
            format="png", transparent=False)
plt.clf()

phylum_counts = species_df[species_df['phylum'].notna()
                           ]['phylum'].value_counts()

plt.tight_layout()
phylum_counts.plot(kind='bar')
plt.xlabel('Phylum')
plt.ylabel('Count of Species')
plt.title('Distribution of Species by Phylum')
plt.savefig('data/characterization/species_distribution_by_phylum.png',
            format="png", transparent=False)
plt.clf()

class_counts = species_df[species_df['class'].notna()]['class'].value_counts()

phylum_counts.plot(kind='bar')
plt.xlabel('Class')
plt.ylabel('Count of Species')
plt.title('Distribution of Species by Class')
plt.tight_layout()
plt.savefig('data/characterization/species_distribution_by_class.png',
            format="png", transparent=False)
plt.clf()


plt.scatter(observations_df['longitude'],
            observations_df['latitude'], alpha=0.5, color='blue')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical Distribution of Observations')
plt.tight_layout()
plt.savefig('data/characterization/geographical_distribution.png',
            format="png", transparent=False)
plt.clf()
