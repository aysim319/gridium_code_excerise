from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path
from typing import Optional, List, Tuple

PROJECT_DIR = Path(__file__).resolve().parent

LOCATION_MAPPING = {}


def generate_mapping():
    try:
        with open(f"{PROJECT_DIR}/us_location_mapping.json", "r") as f:
            global LOCATION_MAPPING
            LOCATION_MAPPING = json.load(f)
    except FileNotFoundError:
        logging.error("please run map_us_cities_to_url.py to generate a mapping file")
        exit(1)

def parse_city_name(city: str) -> str:
    parsed_city = city.split(",")[0]
    global LOCATION_MAPPING
    url = LOCATION_MAPPING.get(parsed_city)
    if url is None:
        logging.warn("city name is malformed and/or not based in the US")
        simple_parsed = parsed_city.replace(" ", "-")
        return f"/locations/{simple_parsed}/tides/latest"
    return url

def map_city_to_url(cities_file) -> List[Tuple[str]]:
    cities = cities_file.read()
    cities = cities.split("\n")
    cleaned_cities = [(c, parse_city_name(c)) for c in cities if parse_city_name(c)]
    return cleaned_cities


def find_sun_rise_and_sun_set_time(soup: BeautifulSoup):
    text = soup.find("p", attrs={"class": "tide-header-summary"}).text
    sunrise_idx = text.find("Sunrise")
    sunrise_time = text[sunrise_idx + 15:sunrise_idx + 21]
    sunset_idx = text.find("sunset")
    sunset_time = text[sunset_idx + 14:sunset_idx + 20]
    return sunrise_time, sunset_time