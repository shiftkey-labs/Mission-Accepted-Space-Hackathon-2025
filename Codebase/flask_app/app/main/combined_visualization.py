"""
Combined Visualization Module

Creates combined matplotlib plots showing both algae detection and terrain analysis
in a single side-by-side image.
"""

import rasterio
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO
import logging
from .tif_to_algae_map import _compute_indices
from .terrain import process_terrain_tiff
import tempfile
import os

logger = logging.getLogger(__name__)


def create_combined_algae_terrain_plot(
    satellite_tiff_path: str,
    elevation_tiff_path: str,
    title: str = "Lake Analysis: Algae Detection & Terrain"
) -> bytes:
    """
    Create a combined plot showing algae detection (left) and terrain analysis (right).
    
    Args:
        satellite_tiff_path: Path to satellite TIFF file
        elevation_tiff_path: Path to elevation TIFF file  
        title: Main title for the combined plot
        
    Returns:
        PNG image as bytes
    """
    logger.info("Creating combined algae + terrain visualization")
    
    # 1. Process algae detection from satellite data
    with rasterio.open(satellite_tiff_path) as src:
        # Read bands: B02 (Blue), B03 (Green), B04 (Red), B08 (NIR)
        blue = src.read(1).astype(float)   # B02
        green = src.read(2).astype(float)  # B03
        red = src.read(3).astype(float)    # B04
        nir = src.read(4).astype(float)    # B08
    
    # Compute indices using the correct function signature
    ndwi, ndvi_over_water, algae_mask = _compute_indices(blue, green, red, nir)
    
    # Calculate full NDVI for visualization
    ndvi = np.where((nir + red) == 0, np.nan, (nir - red) / (nir + red))
    
    # Water mask (NDWI > 0) - already computed by _compute_indices
    water_mask = ndwi > 0
    
    # 2. Process terrain from elevation data
    with rasterio.open(elevation_tiff_path) as src:
        elevation = src.read(1).astype(float)
    
    # Calculate slope using same method as terrain.py
    from scipy import ndimage
    dx = dy = 30  # Copernicus DEM resolution
    gradient_x = ndimage.sobel(elevation, axis=1) / (8 * dx)
    gradient_y = ndimage.sobel(elevation, axis=0) / (8 * dy)
    slope = np.degrees(np.arctan(np.sqrt(gradient_x**2 + gradient_y**2)))
    
    # 3. Create combined visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # Top left: NDWI (Water detection)
    im1 = axes[0, 0].imshow(ndwi, cmap='RdYlBu', vmin=-1, vmax=1)
    axes[0, 0].set_title("NDWI (Water Detection)")
    axes[0, 0].set_xlabel("Pixel X")
    axes[0, 0].set_ylabel("Pixel Y")
    plt.colorbar(im1, ax=axes[0, 0], label="NDWI")
    
    # Top right: NDVI over Water + Algae Mask
    im2 = axes[0, 1].imshow(ndvi_over_water, cmap='RdYlGn', vmin=-1, vmax=1)
    axes[0, 1].contour(algae_mask, levels=[0.5], colors=['red'], linewidths=2)
    axes[0, 1].set_title("NDVI over Water + Algae Mask (Red)")
    axes[0, 1].set_xlabel("Pixel X")
    axes[0, 1].set_ylabel("Pixel Y")
    plt.colorbar(im2, ax=axes[0, 1], label="NDVI")
    
    # Bottom left: Elevation
    im3 = axes[1, 0].imshow(elevation, cmap='terrain')
    axes[1, 0].set_title("Elevation (DEM)")
    axes[1, 0].set_xlabel("Pixel X")
    axes[1, 0].set_ylabel("Pixel Y")
    plt.colorbar(im3, ax=axes[1, 0], label="Elevation (m)")
    
    # Bottom right: Slope
    im4 = axes[1, 1].imshow(slope, cmap='YlOrRd', vmin=0, vmax=15)
    axes[1, 1].set_title("Slope (degrees)")
    axes[1, 1].set_xlabel("Pixel X")
    axes[1, 1].set_ylabel("Pixel Y")
    plt.colorbar(im4, ax=axes[1, 1], label="Slope (°)")
    
    plt.tight_layout()
    
    # Convert to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close(fig)
    
    logger.info("✅ Combined visualization created successfully")
    return image_bytes


def create_combined_plot_from_controller(
    satellite_controller,
    bbox: list,
    start_date: str,
    end_date: str,
    title: str = "Satellite Analysis: Algae Detection & Terrain"
) -> bytes:
    """
    Create combined plot by fetching both satellite and elevation data.
    
    Args:
        satellite_controller: SatelliteController instance
        bbox: Bounding box [min_lng, min_lat, max_lng, max_lat]
        start_date: Start date string
        end_date: End date string
        title: Plot title
        
    Returns:
        PNG image as bytes
    """
    from .get_elevation import fetch_elevation_tiff
    
    # Use temporary files for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        satellite_tiff = os.path.join(temp_dir, "satellite.tif")
        elevation_tiff = os.path.join(temp_dir, "elevation.tif")
        
        # Fetch satellite imagery - need to get raw TIFF data, not processed PNG
        logger.info("Fetching satellite imagery for combined plot...")
        time_range = {
            "from": start_date,
            "to": end_date
        }
        
        # Get raw TIFF data from satellite controller
        response = satellite_controller.fetch_satellite_imagery(bbox, time_range)
        tiff_bytes = response.content
        
        # Save raw TIFF to file
        with open(satellite_tiff, 'wb') as f:
            f.write(tiff_bytes)
        
        # Fetch elevation data
        logger.info("Fetching elevation data for combined plot...")
        fetch_elevation_tiff(bbox=bbox, output_path=elevation_tiff)
        
        # Create combined visualization
        return create_combined_algae_terrain_plot(
            satellite_tiff_path=satellite_tiff,
            elevation_tiff_path=elevation_tiff,
            title=title
        )