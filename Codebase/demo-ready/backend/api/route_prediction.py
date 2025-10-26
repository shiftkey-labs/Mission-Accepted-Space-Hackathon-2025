from fastapi import APIRouter

from models import RouteRequest

router = APIRouter(tags=["route_prediction"])


@router.post("/route_prediction")
def route_prediction(request_body: RouteRequest):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [request_body.start, request_body.end],
                },
                "properties": {
                    "source": "stubbed",
                },
            }
        ],
    }
