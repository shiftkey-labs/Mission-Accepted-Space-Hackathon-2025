from iceChange import calculateIceChange
from ndviChange import getNdviChange
from ndwiChange import getNdwiChange
from slope import getSlope
import numpy as np


def getRiskFactors():
    coastal_locations = [
        {"name": "Iqaluit, NU", "coordinates": [-68.5197, 63.7467], "groundTemp": 267.787, "isPermaFrost": False, "population": 7429},
        {"name": "Belcher Islands, NU", "coordinates": [-79.0, 56.0], "groundTemp": 275.668, "isPermaFrost": False, "population": 1010},
        {"name": "Sanikiluaq, NU", "coordinates": [-79.2333, 56.5333], "groundTemp": 274.69, "isPermaFrost": False, "population": 1010},
        {"name": "Grise Fiord, NU", "coordinates": [-82.3, 76.4], "groundTemp": 265.06, "isPermaFrost": True, "population": 144},
        {"name": "Southampton Island, NU", "coordinates": [-85.0, 63.0], "groundTemp": 266.24, "isPermaFrost": True, "population": 1035},
        {"name": "Coats Island, NU", "coordinates": [-86.0, 64.0], "groundTemp": 267.79, "isPermaFrost": False, "population": 0},
        {"name": "Rankin Inlet, NU", "coordinates": [-92.0831, 62.8083], "groundTemp": 276.45, "isPermaFrost": False, "population": 2975},
        {"name": "Arviat, NU", "coordinates": [-94.0586, 61.1083], "groundTemp": 277.4, "isPermaFrost": False, "population": 2061},
        {"name": "Baker Lake, NU", "coordinates": [-96.0208, 64.3167], "groundTemp": 266.40, "isPermaFrost": False, "population": 2060},
        {"name": "Bathurst Inlet, NU", "coordinates": [-108.03, 66.84], "groundTemp": 266.28, "isPermaFrost": True, "population": 0},
        {"name": "Kugluktuk, NU", "coordinates": [-115.09, 67.825], "groundTemp": 265.03, "isPermaFrost": True, "population": 1382},
        {"name": "Paulatuk, NW", "coordinates": [-124.07, 69.35], "groundTemp": 273.21, "isPermaFrost": False, "population": 298},
        {"name": "Sachs Harbour, NW", "coordinates": [-125.247, 71.985], "groundTemp": 261.36, "isPermaFrost": True, "population": 104},
        {"name": "Atlin area, YT", "coordinates": [-132.7333, 59.5667], "groundTemp": 276.80, "isPermaFrost": False, "population": 547},
        {"name": "Tagish, YT", "coordinates": [-134.2533, 60.0875], "groundTemp": 269.49, "isPermaFrost": False, "population": 249},
        {"name": "Whitehorse, YT", "coordinates": [-135.0568, 60.7212], "groundTemp": 275.14, "isPermaFrost": False, "population": 30970},
        {"name": "Carcross, YT", "coordinates": [-136.2569, 60.7169], "groundTemp": 276.15, "isPermaFrost": False, "population": 317},
        {"name": "Destruction Bay, YT", "coordinates": [-136.5, 59.75], "groundTemp": 272.41, "isPermaFrost": False, "population": 40},
        {"name": "Haines border area, YT", "coordinates": [-137.0103, 60.1722], "groundTemp": 278.72, "isPermaFrost": False, "population": 688},
        {"name": "Kluane Lake, YT", "coordinates": [-137.5833, 59.25], "groundTemp": 274.12, "isPermaFrost": False, "population": 64},
        {"name": "Dalton Post, YT", "coordinates": [-138.8, 59.5167], "groundTemp": 273.01, "isPermaFrost": False, "population": 100},
        {"name": "Burwash Landing, YT", "coordinates": [-139.0394, 61.3714], "groundTemp": 267.71, "isPermaFrost": False, "population": 64},
        {"name": "Haines Junction area, YT", "coordinates": [-139.4333, 59.55], "groundTemp": 273.93, "isPermaFrost": False, "population": 688}
        #name | coordinates | groundTemp | isPermaFrost | population | iceChange | slope | ndviChange | ndwiChange | iceChangeIndex | slopeIndex | ndviChangeIndex 
        #     | ndwiChangeIndex | groundTempIndex | riskFactorIndex
    ]

    index = 1
    for loc in coastal_locations: 
        name = loc["name"]
        coords = loc["coordinates"]
        iceChange = calculateIceChange(coords)  
        slope = getSlope(coords)
        ndviChange = getNdviChange(coords)
        ndwiChange = getNdwiChange(coords)
        loc["iceChange"] = iceChange
        loc["slope"] = slope
        loc["ndviChange"] = ndviChange
        loc["ndwiChange"] = ndwiChange
        
        index += 1

    def findIndices(indexType, positiveCorrelation):
        max = coastal_locations[0][indexType]
        min = coastal_locations[0][indexType]
        for loc in coastal_locations: 
            if (loc[indexType] > max):
                max = loc[indexType]
            if (loc[indexType] < min):
                min = loc[indexType]

        for loc in coastal_locations:
            if(positiveCorrelation):
                slopeIndex = ((loc[indexType] - min) / (max - min) * 5)
            else:
                slopeIndex = 5 - ((loc[indexType] - min) / (max - min) * 5)
            loc[indexType + 'Index'] = slopeIndex

    findIndices("iceChange", False)
    findIndices("slope", True)
    findIndices("ndviChange", False)
    findIndices("ndwiChange", True)
    findIndices("groundTemp", True)

    for loc in coastal_locations: 
        finalIndex = (0.15 * loc["slopeIndex"]) + (0.25 * loc["ndwiChangeIndex"]) + (0.15 * loc["ndviChangeIndex"]) + (0.15 * loc["iceChangeIndex"]) + (0.30 * loc["groundTempIndex"])
        loc["riskIndex"] = finalIndex
        
    return coastal_locations