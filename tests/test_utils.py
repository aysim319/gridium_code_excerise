from freezegun import freeze_time
from unittest import mock
from pathlib import Path
import pytest
from src.utils import find_sun_rise_and_sun_set_time, map_city_to_url, generate_mapping

BASE_URL = "https://www.tide-forecast.com"

TEST_PROJECT_DIR = Path(__file__).resolve().parent


def test_valid_map_city_to_url():
    generate_mapping()
    with open(f"{TEST_PROJECT_DIR}/data/valid_cities.txt") as f:
        result = map_city_to_url(f)
        expected = [('San Diego, California', '/locations/San-Diego-California/tides/latest'), ('Huntington, New York', '/locations/Huntington-2/tides/latest')]
        assert (expected == result)

def test_invalid_map_city_to_url():
    with open(f"{TEST_PROJECT_DIR}/data/invalid_cities.txt") as f:
        result = map_city_to_url(f)
        expected = [('FooBar, BarBar', '/locations/FooBar/tides/latest'), ('Chicago, Illinois', '/locations/Chicago/tides/latest'), ('St.Louis, Missouri', '/locations/St.Louis/tides/latest'), ('Venezia, Italy', '/locations/Venezia/tides/latest'), ('Villa San Giovanni, Italy', '/locations/Villa-San-Giovanni/tides/latest')]
        assert (expected == result)

@freeze_time('2023-10-18')
def test_find_sun_rise_and_sun_set_time(tide_page_soup):
    result = find_sun_rise_and_sun_set_time(tide_page_soup)
    expected = ('7:00am','5:59pm')
    assert (expected == result)

