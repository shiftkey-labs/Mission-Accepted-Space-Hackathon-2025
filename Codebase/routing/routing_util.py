import rasterio
from rasterio.transform import xy
from pyproj import Transformer
import numpy as np
from shapely.geometry import LineString, MultiLineString, mapping
from PIL import Image

import json

def export_navmap(navmap, out_png="navmap.png"):
    """Export binary navigation map as GeoTIFF and PNG for visualization."""
    # Simple grayscale PNG
    img = Image.fromarray((navmap * 255).astype(np.uint8))
    img.save(out_png)
    print(f"Saved navmap PNG → {out_png}")

def export_route_geojson(path_pixels, src_path, output_path="pixel_route_wgs84.geojson"):
    """
    Export a pixel-based path to GeoJSON in WGS84,
    automatically splitting at the antimeridian to avoid lines across the globe.
    """
    # --- Open raster and setup transformer ---
    with rasterio.open(src_path) as src:
        transform_affine = src.transform
        crs_src = src.crs
        transformer = Transformer.from_crs(crs_src, "EPSG:4326", always_xy=True)

        # Convert pixel (row, col) to geographic coordinates
        coords = []
        for row, col in path_pixels:
            x, y = xy(transform_affine, row, col, offset='center')
            lon, lat = transformer.transform(x, y)
            coords.append((lon, lat))

    # --- Unwrap longitudes for smooth continuity ---
    longitudes = np.array([c[0] for c in coords])
    lats = np.array([c[1] for c in coords])
    unwrapped_lons = np.unwrap(np.radians(longitudes))
    unwrapped_lons = np.degrees(unwrapped_lons)
    unwrapped_lons = ((unwrapped_lons + 180) % 360) - 180
    coords_unwrapped = list(zip(unwrapped_lons, lats))

    # --- Split at antimeridian ---
    def split_antimeridian(coords):
        segments = []
        current_segment = [coords[0]]
        for prev, curr in zip(coords[:-1], coords[1:]):
            lon_prev, _ = prev
            lon_curr, _ = curr
            if abs(lon_curr - lon_prev) > 180:
                segments.append(current_segment)
                current_segment = [prev, curr]
            else:
                current_segment.append(curr)
        segments.append(current_segment)
        return segments

    segments = split_antimeridian(coords_unwrapped)
    multiline = MultiLineString([LineString(seg) for seg in segments])

    # --- Build GeoJSON ---
    geojson = {
        "type": "FeatureCollection",
        "name": "pixel_route_wgs84",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
        },
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": mapping(multiline),
            }
        ],
    }

    # --- Save to file ---
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)

    print(f"Route GeoJSON exported to {output_path}")


def read_rgb_from_tiff(path):
    """Read TIFF and return an (H, W, 3) uint8 RGB image.
       Handles:
         - 3-band RGB
         - 4-band RGBA (drops alpha)
         - 1-band with palette (colormap)
    """
    with rasterio.open(path) as src:
        if src.count >= 3:
            # read first 3 bands (assume R,G,B)
            r = src.read(1)
            g = src.read(2)
            b = src.read(3)
            # if bands are floats, scale to 0-255
            def to_uint8(x):
                if np.issubdtype(x.dtype, np.floating):
                    x = x - np.nanmin(x)
                    maxv = np.nanmax(x)
                    if maxv == 0:
                        return (x * 0).astype(np.uint8)
                    else:
                        return (np.clip(x / maxv, 0, 1) * 255).astype(np.uint8)
                else:
                    # already integer; if >255, rescale
                    maxv = x.max()
                    if maxv > 255:
                        return (x.astype(np.float32) / maxv * 255).astype(np.uint8)
                    return x.astype(np.uint8)
            r8 = to_uint8(r)
            g8 = to_uint8(g)
            b8 = to_uint8(b)
            img = np.stack([r8, g8, b8], axis=-1)
            return img, src
        else:
            # single-band with possible colormap
            arr = src.read(1)
            cmap = None
            try:
                cmap = src.colormap(1)  # dict {value:(r,g,b,a)}
            except Exception:
                cmap = None

            if cmap:
                # build palette -> rgb array
                h, w = arr.shape
                img = np.zeros((h, w, 3), dtype=np.uint8)
                for val, rgba in cmap.items():
                    r, g, b, *_ = rgba
                    mask = (arr == val)
                    if np.any(mask):
                        img[mask] = [r, g, b]
                return img, src
            else:
                # fallback: normalize single band to grayscale RGB
                a = arr.astype(np.float32)
                a = a - np.nanmin(a)
                maxv = np.nanmax(a)
                if maxv != 0:
                    a = (a / maxv * 255)
                a8 = np.clip(a, 0, 255).astype(np.uint8)
                img = np.stack([a8, a8, a8], axis=-1)
                return img, src


def color_to_binary_navigability(img_rgb,
                                 blue_ratio_threshold=1.2,
                                 blue_min=80,
                                 ice_brightness_threshold=220,
                                 gray_tolerance=15):
    """
    Classify an (H,W,3) uint8 RGB image into water/ice/land.

    Heuristics:
      - water: blue channel significantly greater than red & green (blue_ratio_threshold)
               and blue channel above blue_min intensity.
      - ice: very bright pixels (all channels > ice_brightness_threshold)
      - land: otherwise (including dark/gray)
    Returns:
       navmap: uint8 2D array (1 = water/traversable, 0 = blocked)
       masks: dict with boolean masks for 'water','ice','land'
    """
    r = img_rgb[..., 0].astype(np.float32)
    g = img_rgb[..., 1].astype(np.float32)
    b = img_rgb[..., 2].astype(np.float32)

    # water mask: blue stronger than others
    # add small epsilon to denom to avoid div by zero
    eps = 1e-6
    mean_rg = (r + g) / 2.0 + eps
    blue_ratio = (b / mean_rg)
    water_mask = (blue_ratio >= blue_ratio_threshold) & (b >= blue_min)

    # ice mask: very bright (white)
    ice_mask = (r >= ice_brightness_threshold) & (g >= ice_brightness_threshold) & (b >= ice_brightness_threshold)

    # land mask: gray/dark (or anything not water or ice)
    land_mask = ~(water_mask | ice_mask)

    # But some shallow water near coast might be light blue; adjust if desired
    navmap = np.zeros(img_rgb.shape[:2], dtype=np.uint8)
    navmap[water_mask] = 1  # traversable
    navmap[ice_mask] = 0
    navmap[land_mask] = 0

    masks = {"water": water_mask, "ice": ice_mask, "land": land_mask}
    return navmap, masks


def preprocess_color_tiff_to_binary(tif_path,
                                    water_blue_ratio=1.2,
                                    blue_min=80,
                                    ice_brightness=220,
                                    debug_counts=True):
    """
    High-level wrapper: read TIFF color, classify pixels, return binary map (1=water).
    """
    img, src = read_rgb_from_tiff(tif_path)
    navmap, masks = color_to_binary_navigability(img,
                                                 blue_ratio_threshold=water_blue_ratio,
                                                 blue_min=blue_min,
                                                 ice_brightness_threshold=ice_brightness)
    if debug_counts:
        n_water = masks["water"].sum()
        n_ice = masks["ice"].sum()
        n_land = masks["land"].sum()
        total = img.shape[0] * img.shape[1]
        print(f"Pixels: total={total}, water={n_water}, ice={n_ice}, land={n_land}")
    return navmap, img, src  # return original image and rasterio src if you need geotransform


def get_pixel_value_from_latlon(tif_path: str, lat: float, lon: float, src_epsg="EPSG:4326"):
    """
    Converts a latitude/longitude coordinate to raster pixel coordinates
    and returns the corresponding pixel value.

    Args:
        tif_path (str): Path to the GeoTIFF file.
        lat (float): Latitude in decimal degrees.
        lon (float): Longitude in decimal degrees.
        src_epsg (str): CRS of input coordinates (default WGS84).

    Returns:
        dict: {
            "row": int,
            "col": int,
            "inside_bounds": bool
        }
    """
    with rasterio.open(tif_path) as src:
        # Prepare transformer from input CRS to raster CRS
        transformer = Transformer.from_crs(src_epsg, src.crs, always_xy=True)

        # Convert lon/lat to raster projection (x, y)
        x, y = transformer.transform(lon, lat)

        # Check if within raster extent
        inside = (
            src.bounds.left <= x <= src.bounds.right and
            src.bounds.bottom <= y <= src.bounds.top
        )

        # Clamp to bounds if outside (optional safety)
        x_clamped = min(max(x, src.bounds.left), src.bounds.right)
        y_clamped = min(max(y, src.bounds.bottom), src.bounds.top)

        # Convert to pixel coordinates
        row, col = src.index(x_clamped, y_clamped)

    return (row, col)
