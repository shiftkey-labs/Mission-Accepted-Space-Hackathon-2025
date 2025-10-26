import math
import csv

EARTH_RADIUS_KM = 6371.0

cities = []

def load_cities(file_path="data/cities500.txt"):
    global cities
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 7:
                continue
            try:
                cities.append({
                    "name": parts[1],
                    "lat": float(parts[4]),
                    "lon": float(parts[5]),
                    "country": parts[8] if len(parts) > 8 else ""
                })
            except ValueError:
                continue
    print(f"Loaded {len(cities)} cities into memory.")


def haversine_distance(lat1, lon1, lat2, lon2):
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def get_nearest_city(lat, lon, max_distance_km=300):
    if not cities:
        raise ValueError("City list not loaded. Call load_cities() first.")

    nearest = None
    min_dist = float("inf")

    for c in cities:
        dist = haversine_distance(lat, lon, c["lat"], c["lon"])
        if dist < min_dist:
            nearest = c
            min_dist = dist

    if min_dist <= max_distance_km:
        return {
            "name": nearest["name"],
            "country": nearest["country"],
            "distance_km": round(min_dist, 1)
        }
    else:
        return None