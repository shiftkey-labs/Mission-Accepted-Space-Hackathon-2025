"""
Terrain Analysis Module

Processes DEM (Digital Elevation Model) data to calculate slope, flow direction,
and create terrain visualizations.

Functions:
- process_terrain_tiff(input_path="elevation.tif") - Process a DEM TIFF file
- fetch_and_process_terrain(bbox, output_dir="./") - Fetch DEM and process terrain
"""

import rasterio
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import logging
import tempfile
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


def calculate_flow_direction(dem: np.ndarray) -> np.ndarray:
    """Simple D8 flow direction calculation"""
    rows, cols = dem.shape
    flow_dir = np.zeros_like(dem, dtype=int)
    
    # Direction encoding: 1=E, 2=SE, 4=S, 8=SW, 16=W, 32=NW, 64=N, 128=NE
    directions = [
        (0, 1, 1),    # East
        (1, 1, 2),    # Southeast
        (1, 0, 4),    # South
        (1, -1, 8),   # Southwest
        (0, -1, 16),  # West
        (-1, -1, 32), # Northwest
        (-1, 0, 64),  # North
        (-1, 1, 128)  # Northeast
    ]
    
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if np.isnan(dem[i, j]):
                continue
            
            max_slope = -np.inf
            flow_direction = 0
            
            for di, dj, code in directions:
                neighbor = dem[i+di, j+dj]
                if not np.isnan(neighbor):
                    slope_to_neighbor = (dem[i, j] - neighbor)
                    if slope_to_neighbor > max_slope:
                        max_slope = slope_to_neighbor
                        flow_direction = code
            
            flow_dir[i, j] = flow_direction
    
    return flow_dir


def process_terrain_from_bytes(
    tiff_bytes: bytes,
    output_png: str = "terrain_analysis.png",
    dem_resolution: float = 30.0,
    show_plot: bool = False
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Process terrain directly from TIFF bytes (no file I/O).
    
    Args:
        tiff_bytes: Raw TIFF data as bytes
        output_png: Path for output visualization PNG
        dem_resolution: DEM resolution in meters
        show_plot: Whether to display the plot
        
    Returns:
        Tuple of (elevation, slope, flow_direction) numpy arrays
    """
    from rasterio.io import MemoryFile
    
    logger.info("Processing terrain from TIFF bytes")
    
    with MemoryFile(tiff_bytes) as mem:
        with mem.open() as src:
            elevation = src.read(1).astype(float)
            
    logger.info(f"Loaded DEM from bytes: {elevation.shape} pixels")
    
    # Calculate Slope (in degrees)
    dx = dem_resolution
    dy = dem_resolution
    
    gradient_x = ndimage.sobel(elevation, axis=1) / (8 * dx)
    gradient_y = ndimage.sobel(elevation, axis=0) / (8 * dy)
    
    slope = np.degrees(np.arctan(np.sqrt(gradient_x**2 + gradient_y**2)))
    
    # Calculate Flow Direction
    flow_direction = calculate_flow_direction(elevation)
    
    # Log statistics
    logger.info(f"Elevation range: {np.nanmin(elevation):.1f}m to {np.nanmax(elevation):.1f}m")
    logger.info(f"Slope range: {np.nanmin(slope):.1f}° to {np.nanmax(slope):.1f}°")
    
    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Elevation plot
    im1 = axes[0].imshow(elevation, cmap='terrain')
    axes[0].set_title("Elevation (DEM)")
    axes[0].set_xlabel("Pixel X")
    axes[0].set_ylabel("Pixel Y")
    plt.colorbar(im1, ax=axes[0], label="Elevation (m)")
    
    # Slope plot
    im2 = axes[1].imshow(slope, cmap='YlOrRd', vmin=0, vmax=15)
    axes[1].set_title("Slope (degrees)")
    axes[1].set_xlabel("Pixel X")
    axes[1].set_ylabel("Pixel Y")
    plt.colorbar(im2, ax=axes[1], label="Slope (°)")
    
    plt.tight_layout()
    plt.savefig(output_png, dpi=150, bbox_inches='tight')
    logger.info(f"Saved terrain visualization to {output_png}")
    
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    
    return elevation, slope, flow_direction


def fetch_and_process_terrain_memory(
    bbox: List[float],
    output_png: str = "terrain_analysis.png",
    access_token: Optional[str] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fetch DEM and process terrain entirely in memory (no temp files at all).
    
    Args:
        bbox: Bounding box [min_lng, min_lat, max_lng, max_lat]
        output_png: Path for output visualization PNG
        access_token: Sentinel Hub access token
        
    Returns:
        Tuple of (elevation, slope, flow_direction) numpy arrays
    """
    from app.main.get_elevation import fetch_elevation_tiff
    
    logger.info(f"Fetching DEM data for bbox: {bbox} (memory-only)")
    
    # Create a temporary file just to get the bytes, then immediately delete it
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=True) as temp_file:
        # Fetch to temp file
        tiff_bytes = fetch_elevation_tiff(
            bbox=bbox,
            output_path=temp_file.name,
            access_token=access_token
        )
        
        # Read the file content back as bytes
        temp_file.seek(0)
        tiff_bytes = temp_file.read()
    
    # Process entirely from bytes
    return process_terrain_from_bytes(tiff_bytes, output_png)


def process_terrain_tiff(
    input_path: str = "elevation.tif",
    output_png: str = "terrain_analysis.png",
    save_arrays: bool = True,
    show_plot: bool = False,
    dem_resolution: float = 30.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Process a DEM TIFF file to calculate terrain metrics and create visualization.
    
    Args:
        input_path: Path to elevation TIFF file
        output_png: Path for output visualization PNG
        save_arrays: Whether to save numpy arrays (.npy files)
        show_plot: Whether to display the plot
        dem_resolution: DEM resolution in meters (default 30m for COPERNICUS_30)
        
    Returns:
        Tuple of (elevation, slope, flow_direction) numpy arrays
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"DEM file not found: {input_path}")
    
    logger.info(f"Processing terrain from {input_path}")
    
    # Load DEM
    with rasterio.open(input_path) as src:
        elevation = src.read(1).astype(float)
        transform = src.transform
        crs = src.crs
        
    logger.info(f"Loaded DEM: {elevation.shape} pixels, CRS: {crs}")
    
    # Calculate Slope (in degrees)
    dx = dem_resolution  # meters per pixel
    dy = dem_resolution
    
    gradient_x = ndimage.sobel(elevation, axis=1) / (8 * dx)
    gradient_y = ndimage.sobel(elevation, axis=0) / (8 * dy)
    
    slope = np.degrees(np.arctan(np.sqrt(gradient_x**2 + gradient_y**2)))
    
    # Calculate Flow Direction
    flow_direction = calculate_flow_direction(elevation)
    
    # Log statistics
    logger.info(f"Elevation range: {np.nanmin(elevation):.1f}m to {np.nanmax(elevation):.1f}m")
    logger.info(f"Slope range: {np.nanmin(slope):.1f}° to {np.nanmax(slope):.1f}°")
    
    # Save arrays if requested
    if save_arrays:
        base_name = os.path.splitext(input_path)[0]
        np.save(f"{base_name}_elevation.npy", elevation)
        np.save(f"{base_name}_slope.npy", slope)
        np.save(f"{base_name}_flow_direction.npy", flow_direction)
        logger.info(f"Saved arrays: {base_name}_*.npy")
    
    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Elevation plot
    im1 = axes[0].imshow(elevation, cmap='terrain')
    axes[0].set_title("Elevation (DEM)")
    axes[0].set_xlabel("Pixel X")
    axes[0].set_ylabel("Pixel Y")
    plt.colorbar(im1, ax=axes[0], label="Elevation (m)")
    
    # Slope plot
    im2 = axes[1].imshow(slope, cmap='YlOrRd', vmin=0, vmax=15)
    axes[1].set_title("Slope (degrees)")
    axes[1].set_xlabel("Pixel X")
    axes[1].set_ylabel("Pixel Y")
    plt.colorbar(im2, ax=axes[1], label="Slope (°)")
    
    plt.tight_layout()
    plt.savefig(output_png, dpi=150, bbox_inches='tight')
    logger.info(f"Saved terrain visualization to {output_png}")
    
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    
    return elevation, slope, flow_direction


def fetch_and_process_terrain(
    bbox: List[float],
    output_dir: str = "./",
    terrain_png: str = "terrain_analysis.png",
    access_token: Optional[str] = None,
    save_arrays: bool = False
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fetch DEM data from Sentinel Hub and process terrain analysis in one step.
    Uses temporary files for DEM - automatically cleaned up after processing.
    
    Args:
        bbox: Bounding box [min_lng, min_lat, max_lng, max_lat]
        output_dir: Directory for output files
        terrain_png: Name of terrain visualization PNG to create
        access_token: Sentinel Hub access token
        save_arrays: Whether to save numpy arrays (default False for temp workflow)
        
    Returns:
        Tuple of (elevation, slope, flow_direction) numpy arrays
    """
    from app.main.get_elevation import fetch_elevation_tiff
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create temporary file for DEM
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as temp_tiff:
        temp_dem_path = temp_tiff.name
    
    try:
        logger.info(f"Fetching DEM data for bbox: {bbox}")
        
        # Fetch elevation data to temporary file
        fetch_elevation_tiff(
            bbox=bbox,
            output_path=temp_dem_path,
            access_token=access_token
        )
        
        logger.info(f"DEM saved to temporary file, processing terrain...")
        
        png_path = os.path.join(output_dir, terrain_png)
        
        # Process terrain from temporary file
        elevation, slope, flow_direction = process_terrain_tiff(
            input_path=temp_dem_path,
            output_png=png_path,
            save_arrays=save_arrays,
            show_plot=False
        )
        
        logger.info("✅ Terrain analysis complete!")
        
        return elevation, slope, flow_direction
        
    finally:
        # Clean up temporary DEM file
        try:
            os.unlink(temp_dem_path)
            logger.info(f"Temporary DEM file cleaned up: {temp_dem_path}")
        except OSError as e:
            logger.warning(f"Could not clean up temporary file {temp_dem_path}: {e}")


def fetch_lake_winnipeg_terrain(output_dir: str = "./", access_token: Optional[str] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convenience function to fetch and process Lake Winnipeg terrain.
    Uses temporary DEM file that gets automatically cleaned up.
    """
    bbox = [-101.273432, 50.075155, -96.060934, 54.171428]
    return fetch_and_process_terrain(
        bbox=bbox,
        output_dir=output_dir,
        terrain_png="lake_winnipeg_terrain.png",
        access_token=access_token
    )


# Keep the original script logic for backward compatibility
if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Process terrain from DEM data")
    parser.add_argument("--input", "-i", default="elevation.tif", help="Input DEM TIFF file")
    parser.add_argument("--output", "-o", default="terrain_analysis.png", help="Output PNG file")
    parser.add_argument("--fetch", action="store_true", help="Fetch DEM data first")
    parser.add_argument("--bbox", nargs=4, type=float, help="Bounding box: min_lng min_lat max_lng max_lat")
    parser.add_argument("--show", action="store_true", help="Display the plot")
    args = parser.parse_args()
    
    try:
        if args.fetch:
            if not args.bbox:
                # Use Lake Winnipeg as default
                elevation, slope, flow_direction = fetch_lake_winnipeg_terrain("./")
            else:
                elevation, slope, flow_direction = fetch_and_process_terrain(
                    bbox=args.bbox,
                    terrain_png=args.output
                )
        else:
            elevation, slope, flow_direction = process_terrain_tiff(
                input_path=args.input,
                output_png=args.output,
                show_plot=args.show
            )
        
        print("✅ Terrain analysis complete!")
        print(f"Elevation range: {np.nanmin(elevation):.1f}m to {np.nanmax(elevation):.1f}m")
        print(f"Slope range: {np.nanmin(slope):.1f}° to {np.nanmax(slope):.1f}°")
        
    except Exception as e:
        print(f"❌ Error: {e}")