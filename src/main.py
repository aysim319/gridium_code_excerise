from bs4 import BeautifulSoup
import click
from datetime import date, datetime
import logging
from pathlib import Path
import requests
from typing import Optional
import csv

from src.utils import generate_mapping, map_city_to_url, find_sun_rise_and_sun_set_time

BASE_URL="https://www.tide-forecast.com"

PROJECT_DIR = Path(__file__).resolve().parent

def get_page_content(mapped_city_url: str, city_name: str) -> Optional[BeautifulSoup]:
    full_url = f"{BASE_URL}{mapped_city_url}"
    response = requests.get(full_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup
    else:
        logging.error(f"{city_name}: request failed: {response}")


def parse_soup(soup: BeautifulSoup, city: str):
    sunrise, sunset = find_sun_rise_and_sun_set_time(soup)
    today = date.today().strftime('%Y-%m-%d')
    results = []
    if sunrise and sunset:
        table = soup.find("table", {"class": "tide-day-tides"})
        if table:
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")
            try:
                for row in rows:
                    tide_info_dict = {"location": city}
                    tide_info_dict["date"] = today
                    tide_info_dict["sunrise"] = sunrise
                    tide_info_dict["sunset"] = sunset
                    row_data = row.find_all("td")
                    if row_data:
                        first_cell = row_data[0].get_text()

                        if first_cell in ("Low Tide"):
                            second_cell = row_data[1].get_text().split("(")[0].strip(" ")

                            low_tide_time = datetime.strptime(f"{today} {second_cell}", '%Y-%m-%d %I:%M %p')
                            sunrise_time = datetime.strptime(f"{today} {sunrise}", '%Y-%m-%d %I:%M%p')
                            sunset_time = datetime.strptime(f"{today} {sunset}", '%Y-%m-%d %I:%M%p')
                            if low_tide_time > sunrise_time and low_tide_time < sunset_time:
                                tide_info_dict["low_tide_time"] = second_cell
                                third_cell = row_data[2].get_text()
                                third_cell_ft = float(third_cell.split(" ")[0])
                                tide_info_dict["height_in_ft"] = third_cell_ft

                    if tide_info_dict.get("low_tide_time"):
                        results.append(tide_info_dict)
            except Exception as e:
                logging.error(e, stack_info=True)
        return results


@click.command()
@click.argument("cities_file",
                type=click.File("r"))
@click.option("--output_path",
              type=click.Path(),
              help="output path to save the result"
              )
def main(cities_file, output_path):
    generate_mapping()
    cleaned_cities = map_city_to_url(cities_file)
    full_result = []
    for city_name, city_url in cleaned_cities:
        soup = get_page_content(city_url, city_name)
        if soup:
            result = parse_soup(soup, city_name)
            full_result.extend(result)

    if output_path:
        filepath = Path(output_path)
        with open(f"{filepath}/output.csv", "a+") as f:
            fc = csv.DictWriter(f,
                                fieldnames=["location", "date", "sunrise", "sunset", "low_tide_time", "height_in_ft"])
            fc.writeheader()
            fc.writerows(full_result)
    else:
        print(full_result)


if __name__ == "__main__":
    main()
