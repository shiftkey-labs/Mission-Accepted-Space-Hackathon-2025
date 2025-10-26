from shapely.geometry import Point
from shapely.ops import nearest_points
import geopandas as gpd

class ShippingCorridorHandler:
    def __init__(self, geojson_path: str, buffer_m=5000, crs="EPSG:4326"):
        """
        Initialize handler for shipping corridors.
        Args:
            geojson_path: Path to your GeoJSON file of shipping routes.
            buffer_m: Corridor buffer distance (in meters).
            crs: Target projection (e.g., EPSG:3413 for Arctic analysis).
        """
        self.routes = gpd.read_file(geojson_path)
        self.routes = self.routes.to_crs(crs)
        self.buffer_m = buffer_m
        self.corridors = self.routes.buffer(buffer_m)
        self.corridor_union = self.corridors.unary_union
        self.crs = crs

    def _to_crs(self, lon: float, lat: float):
        """Convert lat/lon to the target CRS if needed."""
        pt = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")
        if pt.crs != self.routes.crs:
            pt = pt.to_crs(self.routes.crs)
        return pt.iloc[0]

    def is_point_in_corridor(self, lon: float, lat: float, from_latlon=True) -> bool:
        """Check if a coordinate lies within the corridor buffer."""
        pt = self._to_crs(lon, lat) if from_latlon else Point(lon, lat)
        return self.corridor_union.contains(pt)

    def nearest_corridor_distance(self, lon: float, lat: float, from_latlon=True) -> float:
        """Compute distance from a coordinate to the nearest corridor line (in meters)."""
        pt = self._to_crs(lon, lat) if from_latlon else Point(lon, lat)
        nearest_geom = nearest_points(pt, self.routes.unary_union)[1]
        return pt.distance(nearest_geom)

    def corridor_bonus(self, lon: float, lat: float, max_bonus=0.5, from_latlon=True):
        """Return a cost multiplier based on proximity to a corridor."""
        dist = self.nearest_corridor_distance(lon, lat, from_latlon)
        if dist <= self.buffer_m:
            return max_bonus
        elif dist <= self.buffer_m * 3:
            decay = (dist - self.buffer_m) / (self.buffer_m * 2)
            return max_bonus + (1 - max_bonus) * decay
        else:
            return 1.0


# import geopandas as gpd
# from shapely.geometry import Point
# from shapely.ops import nearest_points
# import numpy as np 

# class ShippingCorridorHandler:
#     def __init__(self, geojson_path: str, buffer_m=5000, crs="EPSG:3413"):
#         """
#         Initialize handler for shipping corridors.
#         Args:
#             geojson_path: Path to your GeoJSON file of shipping routes.
#             buffer_m: Corridor buffer distance (in meters).
#             crs: Projected CRS for Arctic/Canadian analysis (EPSG:3413 works well).
#         """
#         # Load and reproject to working CRS (for distance operations)
#         self.routes = gpd.read_file(geojson_path)
#         self.routes = self.routes.to_crs(crs)
#         self.buffer_m = buffer_m

#         # Precompute buffered corridors and their union
#         self.corridors = self.routes.buffer(buffer_m)
#         self.corridor_union = self.corridors.unary_union
#         print(f"✅ Loaded {len(self.routes)} routes and created corridor buffer.")

#     def is_point_in_corridor(self, lon: float, lat: float) -> bool:
#         """Check if a coordinate lies within the buffered corridor area."""
#         pt = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326").to_crs(self.routes.crs)
#         return self.corridor_union.contains(pt.iloc[0])

#     def nearest_corridor_distance(self, x, y, from_latlon=True):
#         """
#         Compute distance from a coordinate to nearest corridor line (meters).
#         Set from_latlon=False if x,y are already in self.routes CRS.
#         """
#         if from_latlon:
#             pt = gpd.GeoSeries([Point(x, y)], crs="EPSG:4326").to_crs(self.routes.crs)
#         else:
#             pt = gpd.GeoSeries([Point(x, y)], crs=self.routes.crs)
            
#         # skip empty geometries
#         if self.routes.empty or self.routes.unary_union.is_empty:
#             return np.inf
        
#         # fix invalid geometry
#         routes_union = self.routes.unary_union
#         if not routes_union.is_valid:
#             routes_union = routes_union.buffer(0)
        
#         nearest_geom = nearest_points(pt.iloc[0], routes_union)[1]
#         return pt.distance(nearest_geom).iloc[0]

#     def corridor_bonus(self, lon, lat, max_bonus=0.5, from_latlon=True):
#         """
#         Return a cost multiplier based on proximity to a corridor.
#         If from_latlon=True, input coordinates are assumed in EPSG:4326 and converted.
#         """
#         if from_latlon:
#             pt = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326").to_crs(self.routes.crs)
#             lon, lat = pt.iloc[0].x, pt.iloc[0].y
        
#         dist = self.nearest_corridor_distance(lon, lat)
#         if dist <= self.buffer_m:
#             return max_bonus
#         elif dist <= self.buffer_m * 3:
#             decay = (dist - self.buffer_m) / (self.buffer_m * 2)
#             return max_bonus + (1 - max_bonus) * decay
#         else:
#             return 1.0


#     def route_points_near_corridor(self, start, end, threshold_m=10000):
#         """Check if both start & end are within a given distance of a corridor."""
#         s_dist = self.nearest_corridor_distance(*start)
#         e_dist = self.nearest_corridor_distance(*end)
#         return {
#             "start_near_corridor": s_dist <= threshold_m,
#             "end_near_corridor": e_dist <= threshold_m,
#             "start_dist_m": s_dist,
#             "end_dist_m": e_dist,
#         }

#     def export_corridor_buffer(self, output_geojson="corridors_buffered.geojson"):
#         """Export buffered corridors as GeoJSON in EPSG:4326 for Mapbox/Leaflet."""
#         # Create a GeoDataFrame for the buffered corridors
#         gdf = gpd.GeoDataFrame(geometry=self.corridors, crs=self.routes.crs)
#         # Reproject to WGS84 for web map display
#         gdf = gdf.to_crs("EPSG:4326")
#         gdf.to_file(output_geojson, driver="GeoJSON")
#         print(f"🗺️ Exported buffered corridors (Mapbox-ready) → {output_geojson}")
