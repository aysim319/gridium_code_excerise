from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from pathlib import Path
import pytest
import requests

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

TEST_PROJECT_DIR = Path(__file__).resolve().parent

@pytest.fixture(autouse=True)
def tide_page_soup():
    with open(f"{TEST_PROJECT_DIR}/data/providence-tide.html") as f:
        huntington_soup = BeautifulSoup(f, "html.parser")
        return huntington_soup

@pytest.fixture(autouse=True)
def tide_page():
    with open(f"{TEST_PROJECT_DIR}/data/providence-tide.html") as f:
        html = f.read()
        return html

@pytest.fixture(autouse=True)
def page_not_found_page():
    with open(f"{TEST_PROJECT_DIR}/data/page_not_found.html") as f:
        html = f.read()
        return html


@pytest.fixture(autouse=True)
def invalid_cities():
    with open(f"{TEST_PROJECT_DIR}/data/invalid_cities.txt") as f:
        lines = f.read()
        return lines.split("\n")



