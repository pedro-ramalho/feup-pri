import csv
import os
import requests
import json
import re

from xml.etree import ElementTree

MAX_ARTICLES = 10

# API key
api_key = '20dfcbbfef207ff7715129eae64107620d09'

# create the output directory
output_directory = 'unprocessed'
os.makedirs(output_directory, exist_ok=True)

# read the list of species
with open('processed/species.csv', 'r') as file:
    species_list = list(csv.reader(file))


def format_species_name(species_name: str) -> str:
    return '_'.join(re.sub(r'[^a-zA-Z0-9 ]', '', species_name).split())


def get_pubmed_url(species_name: str) -> str:
    return f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={species_name}&rettype=abstract&api_key={api_key}"


def get_abstract_url(pmid: str) -> str:
    return f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract&api_key={api_key}"


def get_wikipedia_url(species_name: str) -> str:
    return f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={species_name}"


def extract_abstracts(species_name: str) -> dict:
    url = get_pubmed_url(species_name=species_name)
    response = requests.get(url)

    abstracts = dict()

    if response.status_code == 200:
        root = ElementTree.fromstring(response.content)
        pmids = [element.text for element in root.findall(".//Id")]

        num_articles = 1
        for pmid in pmids:
            if num_articles > MAX_ARTICLES:
                break

            abstract_url = get_abstract_url(pmid=pmid)
            abstract_response = requests.get(abstract_url)

            if abstract_response.status_code == 200:
                abstract = abstract_response.text
                abstracts[f'abstract_{num_articles}'] = abstract
                num_articles += 1
            else:
                print(
                    f'Error: Could not fetch the abstract from the article no. {num_articles}')

    return abstracts


for species in species_list:
    species_name = species[0]
    formatted_name = format_species_name(species_name=species_name)
    first_letter = formatted_name[0].upper()

    letter_directory = os.path.join(output_directory, first_letter)
    os.makedirs(letter_directory, exist_ok=True)

    species_data = {}

    # extract abstracts from articles

    # extract content from wikipedia

    print(f'species_name = {species_name}')
    print(f'formatted_name = {formatted_name}')
    print(f'first_letter = {first_letter}')
    # exit(0)

    abstracts = extract_abstracts(species_name=species_name)

    # wikipedia_url = get_wikipedia_url(species_name=formatted_name)
    # wikipedia_response = requests.get(wikipedia_url)

    # if wikipedia_response.status_code == 200:
    #     data = wikipedia_response.json()
    #     page_id = list(data["query"]["pages"].keys())[0]

    #     if "extract" in data["query"]["pages"][page_id]:
    #         content = data["query"]["pages"][page_id]["extract"]
    #         species_data["wikipedia_content"] = content

    json_filename = os.path.join(letter_directory, f"{species_name}.json")
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(abstracts, json_file, ensure_ascii=False, indent=4)
