import csv
import os
import requests
import json
import re
import shutil

from xml.etree import ElementTree

MAX_ARTICLES = 10

api_key = '20dfcbbfef207ff7715129eae64107620d09'

output_directory = '../data/unprocessed'

if os.path.exists(output_directory):
    shutil.rmtree(output_directory)

os.makedirs(output_directory, exist_ok=True)

with open('../data/processed/species.csv', 'r') as file:
    species_list = list(csv.reader(file))


def format_species_name(species_name: str) -> str: 
    return '_'.join(re.sub(r'[^a-zA-Z0-9 ]', '', species_name).split())


def get_pubmed_url(species_name: str) -> str:
    return f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={species_name}&rettype=abstract&api_key={api_key}"


def get_abstract_url(pmid: str) -> str:
    return f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract&api_key={api_key}"


def get_wikipedia_url(species_name: str) -> str:
    return f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={species_name}&redirects=1&exintro=true&explaintext=true"


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
                    f'Error: Could not fetch the abstract from article no. {num_articles}')

    return abstracts


def extract_wikipedia(species_name: str) -> dict:
    url = get_wikipedia_url(species_name=species_name)
    response = requests.get(url)

    wikipedia_content = dict()

    if response.status_code == 200:
        data = response.json()
        page_id = list(data["query"]["pages"].keys())[0]

        if "extract" in data["query"]["pages"][page_id]:
            wikipedia_content["summary"] = data["query"]["pages"][page_id]["extract"]

    return wikipedia_content


for species in species_list:
    species_name = species[0]
    formatted_name = format_species_name(species_name=species_name)
    first_letter = formatted_name[0].upper()

    letter_directory = os.path.join(output_directory, first_letter)
    os.makedirs(letter_directory, exist_ok=True)

    species_data = {}

    abstracts = extract_abstracts(species_name=species_name)
    species_data.update(abstracts)

    content = extract_wikipedia(species_name=formatted_name)
    species_data.update(content)

    json_filename = os.path.join(letter_directory, f"{species_name}.json")
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(species_data, json_file, ensure_ascii=False, indent=4)
