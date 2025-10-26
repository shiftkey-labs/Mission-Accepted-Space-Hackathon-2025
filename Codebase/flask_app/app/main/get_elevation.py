"""
Elevation fetcher for Sentinel Hub DEM (COPERNICUS_30)

Provides a simple function to call Sentinel Hub's /api/v1/process endpoint
and retrieve a DEM (Digital Elevation Model) as a GeoTIFF (FLOAT32).

Usage:
    from app.main.get_elevation import fetch_elevation_tiff
    fetch_elevation_tiff(bbox=[-101.27,50.07,-96.06,54.17], output_path="elevation.tif")

By default the function reads the access token from the environment variable `TOKEN`.
"""

import os
import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in the Flask app root (two directories up)
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    load_dotenv(env_path)
except ImportError:
    logger.warning("python-dotenv not installed. Environment variables must be set manually.")

API_URL = "https://services.sentinel-hub.com/api/v1/process"
DEFAULT_TOKEN_ENVVAR = "TOKEN"


def fetch_elevation_tiff(
    bbox: List[float],
    output_path: str = "elevation.tif",
    dem_instance: str = "COPERNICUS_30",
    width: int = 1000,
    height: int = 1000,
    access_token: Optional[str] = None,
    timeout: int = 300
) -> bytes:
    """
    Fetch DEM (elevation) GeoTIFF from Sentinel Hub and save to disk.

    Args:
        bbox: [min_lng, min_lat, max_lng, max_lat]
        output_path: local file path to save the returned TIFF
        dem_instance: DEM instance name (default: "COPERNICUS_30")
        width: output image width in pixels
        height: output image height in pixels
        access_token: optional bearer token; if not provided, read from env var `TOKEN`
        timeout: request timeout in seconds

    Returns:
        The raw response content (bytes) containing the TIFF data

    Raises:
        ValueError: when token is not available or bbox is invalid
        requests.RequestException: when the HTTP request fails
    """
    # Basic validation
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        raise ValueError("bbox must be a list of four coordinates: [min_lng, min_lat, max_lng, max_lat]")

    token = access_token or os.getenv(DEFAULT_TOKEN_ENVVAR) or os.getenv("TOKEN")
    if not token:
        raise ValueError(f"Access token required. Provide access_token or set environment variable '{DEFAULT_TOKEN_ENVVAR}' or 'SENTINEL_HUB_TOKEN'")

    evalscript = """//VERSION=3
function setup() {
  return {
    input: ["DEM"],
    output: { bands: 1, sampleType: "FLOAT32" }
  };
}

function evaluatePixel(sample) {
  return [sample.DEM];
}"""

    payload: Dict = {
        "input": {
            "bounds": { "bbox": bbox },
            "data": [
                {
                    "type": "DEM",
                    "dataFilter": {
                        "demInstance": dem_instance
                    }
                }
            ]
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [
                { "identifier": "default", "format": { "type": "image/tiff" } }
            ]
        },
        "evalscript": evalscript
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    logger.info("Sending DEM request to Sentinel Hub")

    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=timeout, stream=True)
        resp.raise_for_status()

        # Collect content while writing to file
        content_bytes = b""
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    content_bytes += chunk

        logger.info(f"Elevation TIFF saved to: {output_path}")
        return content_bytes

    except requests.RequestException as exc:
        logger.error(f"Failed to fetch elevation data: {exc}")
        # Optionally include more debugging info
        if exc.response is not None:
            try:
                logger.debug(f"Response body: {exc.response.text}")
            except Exception:
                pass
        raise


def fetch_elevation_with_terrain(
    bbox: List[float],
    output_path: str = "elevation.tif",
    terrain_png: str = "terrain_analysis.png",
    access_token: Optional[str] = None,
    cleanup_tiff: bool = False
) -> bytes:
    """
    Fetch DEM elevation data and automatically generate terrain visualization.
    
    Args:
        bbox: [min_lng, min_lat, max_lng, max_lat]
        output_path: Path to save the DEM TIFF file
        terrain_png: Path to save the terrain visualization PNG
        access_token: Sentinel Hub access token
        cleanup_tiff: Whether to delete the TIFF file after creating terrain image
        
    Returns:
        Raw TIFF bytes
    """
    # Fetch elevation data
    tiff_bytes = fetch_elevation_tiff(
        bbox=bbox,
        output_path=output_path,
        access_token=access_token
    )
    
    try:
        # Import terrain processing (avoiding circular imports)
        from terrain import process_terrain_tiff
        
        logger.info(f"Processing terrain analysis from {output_path}")
        
        # Generate terrain visualization
        elevation, slope, flow_direction = process_terrain_tiff(
            input_path=output_path,
            output_png=terrain_png,
            save_arrays=False,
            show_plot=False
        )
        
        logger.info(f"✅ Terrain visualization saved to {terrain_png}")
        
        # Optionally clean up the TIFF file
        if cleanup_tiff:
            try:
                os.remove(output_path)
                logger.info(f"Cleaned up DEM file: {output_path}")
            except OSError as e:
                logger.warning(f"Could not remove {output_path}: {e}")
        
        return tiff_bytes
        
    except ImportError:
        logger.warning("terrain.py not found - only DEM TIFF was created")
        return tiff_bytes
    except Exception as e:
        logger.error(f"Failed to process terrain: {e}")
        return tiff_bytes


def fetch_lake_winnipeg_elevation(output_path: str = "elevation_lake_winnipeg.tif", access_token: Optional[str] = None) -> bytes:
    """
    Convenience function to fetch elevation for the bbox used in the example curl command.
    """
    bbox = [-101.273432, 50.075155, -96.060934, 54.171428]
    return fetch_elevation_tiff(bbox=bbox, output_path=output_path, access_token=access_token)


def fetch_lake_winnipeg_with_terrain(
    output_dir: str = "./",
    cleanup_tiff: bool = False,
    access_token: Optional[str] = None
) -> bytes:
    """
    Fetch Lake Winnipeg elevation and generate terrain visualization in one step.
    """
    bbox = [-101.273432, 50.075155, -96.060934, 54.171428]
    
    tiff_path = os.path.join(output_dir, "lake_winnipeg_elevation.tif")
    png_path = os.path.join(output_dir, "lake_winnipeg_terrain.png")
    
    return fetch_elevation_with_terrain(
        bbox=bbox,
        output_path=tiff_path,
        terrain_png=png_path,
        access_token=access_token,
        cleanup_tiff=cleanup_tiff
    )


if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Fetch DEM elevation data with optional terrain analysis")
    parser.add_argument("--terrain", action="store_true", help="Generate terrain visualization")
    parser.add_argument("--cleanup", action="store_true", help="Delete TIFF file after creating terrain image")
    parser.add_argument("--output", "-o", default="elevation.tif", help="Output TIFF file path")
    parser.add_argument("--png", default="terrain_analysis.png", help="Terrain PNG output path")
    parser.add_argument("--bbox", nargs=4, type=float, help="Bounding box: min_lng min_lat max_lng max_lat")
    args = parser.parse_args()
    
    token = os.getenv(DEFAULT_TOKEN_ENVVAR) or os.getenv("SENTINEL_HUB_TOKEN")
    bbox = args.bbox or [-101.273432, 50.075155, -96.060934, 54.171428]

    print("Get elevation TIFF example")
    
    if not token:
        print(f"Environment variable '{DEFAULT_TOKEN_ENVVAR}' or 'SENTINEL_HUB_TOKEN' not set.")
        print("Set it to your Sentinel Hub token or pass access_token to the function.")
    else:
        try:
            if args.terrain:
                # Fetch elevation + generate terrain visualization
                print(f"Fetching DEM and generating terrain visualization...")
                fetch_elevation_with_terrain(
                    bbox=bbox,
                    output_path=args.output,
                    terrain_png=args.png,
                    cleanup_tiff=args.cleanup
                )
                if args.cleanup:
                    print(f"✅ Terrain visualization saved to {args.png}")
                else:
                    print(f"✅ DEM saved to {args.output}")
                    print(f"✅ Terrain visualization saved to {args.png}")
            else:
                # Just fetch elevation TIFF
                fetch_elevation_tiff(bbox=bbox, output_path=args.output)
                print(f"✅ DEM saved to {args.output}")
                print("💡 Use --terrain flag to also generate terrain visualization")
        except Exception as e:
            print(f"❌ Error: {e}")
