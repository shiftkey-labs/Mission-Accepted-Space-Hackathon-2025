import ee
from datetime import datetime
ee.Authenticate()
ee.Initialize(project = "ndvi-hackathon-476220")

def getSlope(centre):
    region = ee.Geometry.Point(centre).buffer(4000)

    collection = ee.ImageCollection('COPERNICUS/DEM/GLO30') \
    
    dem = collection.mosaic()

    slope = ee.Terrain.slope(dem)

    meanSlope = slope.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=30
    )

    if meanSlope.get('slope').getInfo() is None:
        return 0

    return meanSlope.get('slope').getInfo()