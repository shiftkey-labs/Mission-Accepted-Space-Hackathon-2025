import ee
from datetime import datetime
ee.Authenticate()
ee.Initialize(project = "ndvi-hackathon-476220")

def getNdwiForYear(year, centre):
    region = ee.Geometry.Point(centre).buffer(2000)

    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterDate(f'{year}-06-01', f'{year}-08-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 25)) \
        .filterBounds(region)

    def addNdwi(image):
        ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
        return image.addBands(ndwi)
    
    ndwiCollection = collection.map(addNdwi)

    meanNdwi = ndwiCollection.select('NDWI').mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=100
    )

    if collection.size().getInfo() == 0:
        return 0

    if meanNdwi.get('NDWI').getInfo() is None:
        return 0

    ndwiValue = meanNdwi.get('NDWI')
    if ndwiValue:
        return ndwiValue.getInfo()
    else:
        return 0

def getNdwiChange(centre):
    currentYear = datetime.now().year
    year1 = currentYear - 1
    year2 = currentYear - 2
    year3 = currentYear - 4
    year4 = currentYear - 5

    ndwi1 = getNdwiForYear(year1, centre)
    ndwi2 = getNdwiForYear(year2, centre)
    ndwi3 = getNdwiForYear(year3, centre)
    ndwi4 = getNdwiForYear(year4, centre)

    recentAvg = (ndwi1 + ndwi2) / 2
    baseAvg = (ndwi3 + ndwi4) / 2

    ndwiChange = recentAvg - baseAvg
    return ndwiChange