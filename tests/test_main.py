from freezegun import freeze_time
from unittest import mock
from pathlib import Path
import pytest
from src.main import parse_soup, get_page_content

BASE_URL="https://www.tide-forecast.com"

TEST_PROJECT_DIR = Path(__file__).resolve().parent


@mock.patch("requests.get")
def test_get_page_content(mock_requests, tide_page):
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.content = tide_page
    soup = get_page_content("Providence-Rhode-Island", "providence")

@mock.patch("logging.error")
@mock.patch("requests.get")
def test_get_page_content_failed(mock_requests, mock_logging, page_not_found_page):
    mock_requests.return_value.status_code = 404
    mock_requests.return_value.content = page_not_found_page
    soup = get_page_content("Providence-Rhode-Island", "providence")
    assert (soup is None)
    mock_logging.assert_called_once()

@freeze_time('2023-10-18')
def test_parse_soup(tide_page_soup):
    result = parse_soup(tide_page_soup, "providence")
    expected = [{'date': '2023-10-18', 'height_in_ft': 0.13, 'location': 'providence', 'low_tide_time': '4:38 PM', 'sunrise': '7:00am', 'sunset': '5:59pm'}]
    assert(expected == result)

