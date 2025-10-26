import ee
from datetime import datetime
ee.Authenticate()
ee.Initialize(project = "ndvi-hackathon-476220")

def getNdviForYear(year, centre):
    region = ee.Geometry.Point(centre).buffer(25000)

    collection = ee.ImageCollection('MODIS/061/MOD13Q1') \
        .filterDate(f'{year}-11-01', f'{year}-11-30') \
        .select('NDVI') \
        .filterBounds(region)

    meanNdvi = collection.mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=250
    )

    ndviValue = meanNdvi.get('NDVI')
    if ndviValue:
        return ndviValue.getInfo()
    else:
        return 0

def getNdviChange(centre):
    currentYear = datetime.now().year
    year1 = currentYear - 1
    year2 = currentYear - 2

    ndviLastYear = getNdviForYear(year1, centre)
    ndviPreviousYear = getNdviForYear(year2, centre)

    if not ndviLastYear or not ndviPreviousYear:
        return 0

    ndviChange = (ndviLastYear / 10000 - ndviPreviousYear / 10000)
    return ndviChange