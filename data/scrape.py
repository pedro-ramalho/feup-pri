import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

url = "https://cdnsciencepub.com/doi/abs/10.1139/b61-100"

os.environ['MOZ_HEADLESS'] = '1'

driver = webdriver.Firefox()

try:
    driver.get(url)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    abstract_elements = soup.find_all(class_="abstract")

    if not abstract_elements:
        abstract_elements = soup.find_all(id="abstract")

    for element in abstract_elements:
        abstract_text = element.get_text().lstrip("Abstract").strip()
        print(abstract_text)

finally:
    driver.quit()
