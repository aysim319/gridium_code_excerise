from bs4 import BeautifulSoup
import json
import requests
from typing import Optional

BASE_URL="https://www.tide-forecast.com"

'''
script to map US cities into url
'''

def get_page_content(path) -> Optional[BeautifulSoup]:
    full_url = f"{BASE_URL}{path}"
    response = requests.get(full_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup

def parse_sub_soup(soup: BeautifulSoup):
    location_dict = dict()
    list = soup.find("ul", attrs={"class": "columns-list is-2 countries-list"})
    if not list:
        return location_dict
    else:
        points = list.find_all("li")
        for point in points:
            url_path = point.find("a").attrs.get("href")
            name = point.find("a").find("div", {"class": "countries-li"}).text.strip()
            location_dict[name] = url_path
    return location_dict

def get_all_location_page(soup: BeautifulSoup):
    div = soup.find("div", {"class": "buttons is-centered has-addons"})
    return [a.get("href") for a in div.find_all("a", "button is-tiny is-outlined")]


if __name__ == "__main__":
    soup = get_page_content("/countries/United-States/locations/")
    locations_url = get_all_location_page(soup)
    location_url_dict = dict()
    for location in locations_url:
        soup = get_page_content(location)
        locations = parse_sub_soup(soup)
        location_url_dict.update(locations)
    with open("us_location_mapping.json", "w") as f:
        f.write(json.dumps(location_url_dict, indent=4))