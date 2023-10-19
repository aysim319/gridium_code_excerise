# Coding Accessment

## Description
This coding exercise is intended to help us get to know each other through code. You get to see a small example of the types of problems our new backend engineer will solve, and we get to see if your approach to coding is a fit for us. We expect this should take no more than 1-2 hours; if it takes much longer, stop and send what you have.

Write a simple Python web scraper to help us visit the tide pools.

Go to https://www.tide-forecast.com/ to get tide forecasts for these locations:

Half Moon Bay, California

Huntington Beach, California

Providence, Rhode Island

Wrightsville Beach, North Carolina

Load the tide forecast page for each location and extract information on low tides that occur after sunrise and before sunset. Return the time and height for each daylight low tide.

# Setup
## prerequisite 
setting up virtual environment
```angular2html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# How to run
# running script
```
python3 src/main.py [file containing cities] --output_path=[path]

# eg) in the project root directory
python3 src/main.py cities.txt out/
```

# Known Limitation
- html content must be consistent from the format shown in the [test/data/providence-tide.html](tests%2Fdata%2Fprovidence-tide.html)
- the location must be within us and with the format specified in the [us_location_mapping.json](src%2Fus_location_mapping.json)
  - the mapping is accurate as of 2023-10-19 and may be subject to change
- locations outside of US is not guaranteed to work unless gotten subdomain that matches the url
  - eg) Venezia, Italy -> Venezia-Italy
  - eg) Villa San Giovanni, Italy -> Villa-San-Giovanni
  