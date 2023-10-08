import requests
from xml.etree import ElementTree

MAX_ARTICLES = 10

api_endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
api_key = "20dfcbbfef207ff7715129eae64107620d09"
search_term = "Leccinum scabrum"

url = f"{api_endpoint}?db=pubmed&term={search_term}&rettype=abstract&api_key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    root = ElementTree.fromstring(response.content)

    pmids = [element.text for element in root.findall(".//Id")]

    num_articles = 0
    for pmid in pmids:
        if num_articles > MAX_ARTICLES:
            break

        abstract_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract&api_key={api_key}"

        abstract_response = requests.get(abstract_url)

        if abstract_response.status_code == 200:
            abstract = abstract_response.text
            print(abstract)

            num_articles += 1
        else:
            print(f"Error retrieving abstract for PMID {pmid}")
else:
    print(f"Error: {response.status_code} - {response.text}")
