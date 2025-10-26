"""
Topography Visualization Module

Creates contour-based topographic maps from DEM data.
Uses monotone colormap and Gaussian smoothing for aesthetic visualization.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from scipy import ndimage
from matplotlib.colors import LinearSegmentedColormap
import logging
from typing import Tuple
from rasterio.io import MemoryFile
from io import BytesIO
import rasterio
import os

logger = logging.getLogger(__name__)


def process_topography_from_bytes(
    tiff_bytes: bytes,
    n_levels: int = 40,
    sigma: float = 1.0
) -> bytes:
    """
    Create topographic contour map from DEM TIFF bytes.
    
    Args:
        tiff_bytes: Raw TIFF data as bytes
        n_levels: Number of contour levels (default 40)
        sigma: Gaussian smoothing sigma for clean contours (default 1.0)
        
    Returns:
        PNG image bytes
    """
    logger.info("Processing topography from TIFF bytes")
    
    # Load elevation data from bytes
    with MemoryFile(tiff_bytes) as mem:
        with mem.open() as src:
            elevation = src.read(1).astype(float)
    
    logger.info(f"Loaded DEM from bytes: {elevation.shape} pixels")
    
    # Handle invalid values
    elevation[elevation <= -1000] = np.nan
    
    # Smooth for clean contours
    elevation_smooth = ndimage.gaussian_filter(elevation, sigma=sigma)
    
    # Flip vertically so north is up
    elev_flipped = np.flipud(elevation_smooth)
    
    # Define contour levels
    min_elev, max_elev = np.nanmin(elev_flipped), np.nanmax(elev_flipped)
    levels = np.linspace(min_elev, max_elev, n_levels)
    
    logger.info(f"Elevation range: {min_elev:.1f}m to {max_elev:.1f}m")
    
    # Create custom monotone colormap (light tan → dark brown)
    colors = ["#f3e9d2", "#c0a16b", "#7a5a2a"]  # light → dark terrain
    mono_cmap = LinearSegmentedColormap.from_list("mono_terrain", colors)
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    
    # Filled contours with monotone gradient
    contourf = plt.contourf(
        elev_flipped,
        levels=levels,
        cmap=mono_cmap,
        alpha=1.0
    )
    
    # Thin contour lines for definition
    plt.contour(
        elev_flipped,
        levels=levels,
        colors="black",
        linewidths=0.4,
        alpha=0.4
    )
    
    plt.title("Topographic Map", fontsize=14, fontweight='bold')
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.colorbar(contourf, label="Elevation (m)")
    plt.tight_layout()
    
    # Save to bytes
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    image_bytes = buf.read()
    plt.close(fig)
    
    logger.info(f"✅ Topography map created successfully")
    
    return image_bytes


def process_topography_from_file(
    tiff_path: str,
    output_png: str = "topography.png",
    n_levels: int = 40,
    sigma: float = 1.0
) -> bytes:
    """
    Create topographic contour map from DEM TIFF file.
    
    Args:
        tiff_path: Path to elevation TIFF file
        output_png: Path for output PNG file
        n_levels: Number of contour levels (default 40)
        sigma: Gaussian smoothing sigma (default 1.0)
        
    Returns:
        PNG image bytes
    """
    if not os.path.exists(tiff_path):
        raise FileNotFoundError(f"DEM file not found: {tiff_path}")
    
    logger.info(f"Processing topography from {tiff_path}")
    
    # Load elevation data
    with rasterio.open(tiff_path) as src:
        elevation = src.read(1).astype(float)
    
    logger.info(f"Loaded DEM: {elevation.shape} pixels")
    
    # Handle invalid values
    elevation[elevation <= -1000] = np.nan
    
    # Smooth for clean contours
    elevation_smooth = ndimage.gaussian_filter(elevation, sigma=sigma)
    
    # Flip vertically so north is up
    elev_flipped = np.flipud(elevation_smooth)
    
    # Define contour levels
    min_elev, max_elev = np.nanmin(elev_flipped), np.nanmax(elev_flipped)
    levels = np.linspace(min_elev, max_elev, n_levels)
    
    logger.info(f"Elevation range: {min_elev:.1f}m to {max_elev:.1f}m")
    
    # Create custom monotone colormap
    colors = ["#f3e9d2", "#c0a16b", "#7a5a2a"]  # light → dark terrain
    mono_cmap = LinearSegmentedColormap.from_list("mono_terrain", colors)
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    
    # Filled contours
    contourf = plt.contourf(
        elev_flipped,
        levels=levels,
        cmap=mono_cmap,
        alpha=1.0
    )
    
    # Thin contour lines
    plt.contour(
        elev_flipped,
        levels=levels,
        colors="black",
        linewidths=0.4,
        alpha=0.4
    )
    
    plt.title("Topographic Map", fontsize=14, fontweight='bold')
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.colorbar(contourf, label="Elevation (m)")
    plt.tight_layout()
    
    # Save to file
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    logger.info(f"Saved topography to {output_png}")
    
    # Also return bytes
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    image_bytes = buf.read()
    plt.close(fig)
    
    return image_bytes


def get_smoothed_elevation(
    elevation: np.ndarray,
    sigma: float = 1.0,
    flip_vertical: bool = True
) -> Tuple[np.ndarray, float, float]:
    """
    Helper function to get smoothed elevation data for topographic visualization.
    
    Args:
        elevation: Raw elevation array
        sigma: Gaussian smoothing sigma
        flip_vertical: Whether to flip the array vertically (for north-up orientation)
        
    Returns:
        Tuple of (smoothed_elevation, min_elevation, max_elevation)
    """
    # Handle invalid values
    elevation_clean = np.copy(elevation)
    elevation_clean[elevation_clean <= -1000] = np.nan
    
    # Smooth for clean contours
    elevation_smooth = ndimage.gaussian_filter(elevation_clean, sigma=sigma)
    
    # Flip if requested
    if flip_vertical:
        elevation_smooth = np.flipud(elevation_smooth)
    
    min_elev = np.nanmin(elevation_smooth)
    max_elev = np.nanmax(elevation_smooth)
    
    return elevation_smooth, min_elev, max_elev


if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Create topographic visualization from DEM data")
    parser.add_argument("--input", "-i", default="elevation.tif", help="Input DEM TIFF file")
    parser.add_argument("--output", "-o", default="topography.png", help="Output PNG file")
    parser.add_argument("--levels", type=int, default=40, help="Number of contour levels")
    parser.add_argument("--sigma", type=float, default=1.0, help="Gaussian smoothing sigma")
    args = parser.parse_args()
    
    try:
        process_topography_from_file(
            tiff_path=args.input,
            output_png=args.output,
            n_levels=args.levels,
            sigma=args.sigma
        )
        print(f"✅ Topography visualization saved to {args.output}")
    except Exception as e:
        print(f"❌ Error: {e}")
