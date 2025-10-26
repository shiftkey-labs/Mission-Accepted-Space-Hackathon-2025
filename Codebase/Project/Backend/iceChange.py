import requests, json
import numpy as np
from datetime import datetime

def get_planet_data(start_date, end_date, centre):

    cornerA = [centre[0] - 0.5, centre[1] + 0.5]
    cornerB = [centre[0] - 0.5, centre[1] - 0.5]
    cornerC = [centre[0] + 0.5, centre[1] + 0.5]
    cornerD = [centre[0] + 0.5, centre[1] - 0.5]
    API_KEY = "PLAK0a31a8458a904cc792c6889ba19d0f72"
    AOI = {
        "type": "Polygon",
        "coordinates": [
            [
                cornerA, cornerB, cornerC, cornerD, cornerA
            ]
        ]
    }

    url = "https://api.planet.com/data/v1/quick-search"

    payload = {
        "item_types": ["PSScene"],
        "filter": {
            "type": "AndFilter",
            "config": [
                {"type": "GeometryFilter", "field_name": "geometry", "config": AOI},
                {"type": "DateRangeFilter", "field_name": "acquired", "config": {"gte": start_date, "lte": end_date}},
                {"type": "RangeFilter", "field_name": "cloud_cover", "config": {"lte": 0.3}}
            ]
        }
    }

    response = requests.post(url, auth=(API_KEY, ""), json=payload)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    return response.json().get("features", [])

def extract_snow_ice_metadata(features):
    ice_data = []
    for f in features:
        ice = f.get("properties", {}).get("snow_ice_percent")
        ice_data.append(ice)
    return ice_data

def calculateIceChange(centre):
    currentYear = datetime.now().year
    year1 = currentYear - 1
    year2 = currentYear - 2

    dataLastYear = get_planet_data(f"{year1}-11-01T00:00:00Z", f"{year1}-11-30T23:59:59Z", centre)
    dataPreviousYear = get_planet_data(f"{year2}-11-01T00:00:00Z", f"{year2}-11-30T23:59:59Z", centre)

    if not dataLastYear or not dataPreviousYear:
        return 0

    iceLastYear = extract_snow_ice_metadata(dataLastYear)
    icePreviousYear = extract_snow_ice_metadata(dataPreviousYear)

    refinedIceLastYear = [ice for ice in iceLastYear if ice is not None]
    refinedIcePreviousYear = [ice for ice in icePreviousYear if ice is not None]

    if len(refinedIceLastYear) == 0 or len(refinedIcePreviousYear) == 0:
        return 0

    meanLastYear = np.mean(refinedIceLastYear)
    meanPreviousYear = np.mean(refinedIcePreviousYear)
    stdDevLastYear = np.std(refinedIceLastYear)
    stdDevPreviousYear = np.std(refinedIcePreviousYear)

    filteredIceLastYear = []
    filteredIcePreviousYear = []

    for ice in refinedIceLastYear:
            if ice > meanLastYear - 2 * stdDevLastYear and ice < meanLastYear + 2 * stdDevLastYear:
                filteredIceLastYear.append(ice)

    averageIceLastYear = np.mean(filteredIceLastYear)

    for ice in refinedIcePreviousYear:
        if ice > meanPreviousYear - 2 * stdDevPreviousYear and ice < meanPreviousYear + 2 * stdDevPreviousYear:
            filteredIcePreviousYear.append(ice)

    averageIcePreviousYear = np.mean(filteredIcePreviousYear)

    iceChange = averageIcePreviousYear - averageIceLastYear
    return iceChange