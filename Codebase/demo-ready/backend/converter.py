"""
Utilities for converting sea-ice GeoTIFF rasters into GeoJSON point clouds.

The heavy lifting is done with rasterio, NumPy, and GeoPandas.  Converted
feature collections can be cached in-memory so repeated requests for the same
file are fast.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, Tuple

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import xy as transform_xy
from shapely.geometry import Point


class GeoDataConversionError(RuntimeError):
    """Raised when we fail to convert a GeoTIFF into GeoJSON."""


def _load_raster(path: Path) -> Tuple[np.ndarray, rasterio.Affine, rasterio.crs.CRS]:
    try:
        with rasterio.open(path) as src:
            data = src.read(1)
            transform = src.transform
            crs = src.crs
    except Exception as exc:  # pragma: no cover - rasterio emits complex errors
        raise GeoDataConversionError(f"Failed to read raster '{path}': {exc}") from exc

    if data is None or transform is None or crs is None:
        raise GeoDataConversionError(f"Raster '{path}' is missing required metadata.")

    return data, transform, crs


def _pixel_coordinates(
    transform: rasterio.Affine, width: int, height: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the projected coordinates for every pixel center in the raster.
    """
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs = transform.c + cols * transform.a + rows * transform.b
    ys = transform.f + cols * transform.d + rows * transform.e
    return xs, ys


def _filter_points(
    data: np.ndarray,
    xs: np.ndarray,
    ys: np.ndarray,
    radius_km: float,
    transform: rasterio.Affine,
) -> Iterable[Point]:
    """
    Mask the raster to keep only pixels whose value indicates ice presence
    and whose distance from the origin exceeds the desired radius.
    """
    if data.shape != xs.shape or xs.shape != ys.shape:
        raise GeoDataConversionError("Raster dimensions mismatch while generating coordinates.")

    dist_km = np.sqrt(xs**2 + ys**2) / 1000
    mask = (data == 1) & (dist_km > radius_km)
    rows, cols = np.where(mask)
    xs_filtered, ys_filtered = transform_xy(transform, rows, cols)
    for x, y in zip(xs_filtered, ys_filtered):
        yield Point(x, y)


def _to_feature_collection(points: Iterable[Point], crs) -> Dict:
    gdf = gpd.GeoDataFrame(geometry=list(points), crs=crs)
    if gdf.empty:
        return {"type": "FeatureCollection", "features": []}

    gdf = gdf.to_crs(epsg=4326)
    return gdf.__geo_interface__


@lru_cache(maxsize=128)
def convert_tif_to_geojson(path: str, radius_km: float = 500) -> Dict:
    """
    Convert a GeoTIFF file into a GeoJSON FeatureCollection (as a dict).

    Results are cached in-memory keyed by the file path and radius.
    """
    tif_path = Path(path)
    if not tif_path.exists():
        raise FileNotFoundError(f"GeoTIFF not found at {tif_path}")

    data, transform, crs = _load_raster(tif_path)
    xs, ys = _pixel_coordinates(transform, data.shape[1], data.shape[0])
    points = list(_filter_points(data, xs, ys, radius_km, transform))
    return _to_feature_collection(points, crs)
