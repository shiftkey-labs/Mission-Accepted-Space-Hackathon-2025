"""
Unified Analysis Module

Comprehensive geospatial analysis combining:
- Satellite imagery processing
- Elevation data analysis  
- Algae bloom detection with severity levels
- Land cover classification
- Terrain analysis (slope, flow direction)
- Buffer strip site selection visualization
"""

import rasterio
import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from io import BytesIO
import logging
import tempfile
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)


def classify_land_cover(B02, B03, B04, B08, B11, B12):
    """
    Classify land cover from Sentinel-2 bands
    
    Returns:
        land_cover: Classification array (0=unclassified, 1=water, 2=urban, 3=bare, 4=agriculture, 5=forest)
        agricultural_mask: Boolean mask for agricultural areas
    """
    # Calculate spectral indices
    ndvi = np.where((B08 + B04) == 0, np.nan, (B08 - B04) / (B08 + B04))
    ndwi = np.where((B03 + B08) == 0, np.nan, (B03 - B08) / (B03 + B08))
    ndbi = np.where((B11 + B08) == 0, np.nan, (B11 - B08) / (B11 + B08))
    
    # Initialize land cover classification
    land_cover = np.zeros_like(ndvi, dtype=int)
    
    # Classify land cover types
    land_cover[ndwi > 0] = 1  # Water
    land_cover[(ndbi > 0) & (ndvi < 0.3) & (ndwi <= 0)] = 2  # Urban/Built-up
    land_cover[(ndvi >= 0) & (ndvi < 0.2) & (ndwi <= 0) & (ndbi <= 0)] = 3  # Bare soil
    land_cover[(ndvi >= 0.3) & (ndvi < 0.5) & (ndwi <= 0)] = 4  # Agriculture
    land_cover[(ndvi >= 0.6) & (ndwi <= 0)] = 5  # Forest
    
    agricultural_mask = (land_cover == 4)
    
    return land_cover, agricultural_mask


def detect_algae_with_severity(B02, B03, B04, B08):
    """
    Detect algae blooms with severity classification using the improved algorithm
    
    Returns:
        ndwi: Water detection index
        ndvi_algae_clipped: Flipped NDVI for algae highlighting
        algae_severity: Severity classification (1=Low, 2=Medium, 3=High)
    """
    # Compute NDWI and NDVI
    ndwi = np.where((B03 + B08) == 0, np.nan, (B03 - B08) / (B03 + B08))
    ndvi = np.where((B08 + B04) == 0, np.nan, (B08 - B04) / (B08 + B04))
    
    # Water mask and NDVI over water
    water_mask = ndwi > 0
    ndvi_over_water = np.where(water_mask, ndvi, np.nan)
    
    # Flip NDVI over water to highlight algae
    ndvi_algae = np.where(water_mask, -ndvi_over_water, np.nan)
    
    # Clip outliers (top 1%)
    ndvi_water_values = ndvi_algae[~np.isnan(ndvi_algae)]
    if len(ndvi_water_values) > 0:
        upper_clip = np.nanpercentile(ndvi_water_values, 99)
        ndvi_algae_clipped = np.where(ndvi_algae > upper_clip, upper_clip, ndvi_algae)
        
        # Adaptive thresholds for severity classification
        ndvi_values_clipped = ndvi_algae_clipped[~np.isnan(ndvi_algae_clipped)]
        if len(ndvi_values_clipped) > 0:
            low_thresh = np.nanpercentile(ndvi_values_clipped, 70)
            medium_thresh = np.nanpercentile(ndvi_values_clipped, 85)
            high_thresh = np.nanpercentile(ndvi_values_clipped, 95)
            
            # Classify algae severity
            algae_severity = np.full_like(ndvi_algae_clipped, np.nan)
            algae_severity = np.where((ndvi_algae_clipped >= low_thresh) & (ndvi_algae_clipped < medium_thresh), 1, algae_severity)
            algae_severity = np.where((ndvi_algae_clipped >= medium_thresh) & (ndvi_algae_clipped < high_thresh), 2, algae_severity)
            algae_severity = np.where(ndvi_algae_clipped >= high_thresh, 3, algae_severity)
        else:
            algae_severity = np.full_like(ndvi_algae_clipped, np.nan)
    else:
        ndvi_algae_clipped = np.full_like(ndvi_algae, np.nan)
        algae_severity = np.full_like(ndvi_algae, np.nan)
    
    return ndwi, ndvi_algae_clipped, algae_severity


def calculate_terrain_metrics(elevation):
    """
    Calculate terrain metrics from elevation data
    
    Returns:
        slope: Slope in degrees
        flow_direction: Flow direction using D8 algorithm
    """
    # Calculate slope
    dx = dy = 30  # Copernicus DEM resolution in meters
    gradient_x = ndimage.sobel(elevation, axis=1) / (8 * dx)
    gradient_y = ndimage.sobel(elevation, axis=0) / (8 * dy)
    slope = np.degrees(np.arctan(np.sqrt(gradient_x**2 + gradient_y**2)))
    
    # Calculate flow direction using D8 algorithm
    rows, cols = elevation.shape
    flow_direction = np.zeros_like(elevation, dtype=int)
    
    directions = [
        (0, 1, 1), (1, 1, 2), (1, 0, 4), (1, -1, 8),
        (0, -1, 16), (-1, -1, 32), (-1, 0, 64), (-1, 1, 128)
    ]
    
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if np.isnan(elevation[i, j]):
                continue
            
            max_slope_val = -np.inf
            flow_dir = 0
            
            for di, dj, code in directions:
                neighbor = elevation[i+di, j+dj]
                if not np.isnan(neighbor):
                    slope_to_neighbor = elevation[i, j] - neighbor
                    if slope_to_neighbor > max_slope_val:
                        max_slope_val = slope_to_neighbor
                        flow_dir = code
            
            flow_direction[i, j] = flow_dir
    
    return slope, flow_direction


def create_unified_analysis_plot(
    satellite_tiff_path: str,
    elevation_tiff_path: str,
    title: str = "Unified Geospatial Analysis: Buffer Strip Site Selection"
) -> bytes:
    """
    Create comprehensive analysis plot combining all components
    
    Args:
        satellite_tiff_path: Path to satellite TIFF file
        elevation_tiff_path: Path to elevation TIFF file
        title: Plot title
        
    Returns:
        PNG image as bytes
    """
    logger.info("Creating unified geospatial analysis visualization...")
    
    # Load satellite data
    with rasterio.open(satellite_tiff_path) as src:
        B02 = src.read(1).astype(float)  # Blue
        B03 = src.read(2).astype(float)  # Green
        B04 = src.read(3).astype(float)  # Red
        B08 = src.read(4).astype(float)  # NIR
        B11 = src.read(5).astype(float)  # SWIR1
        B12 = src.read(6).astype(float)  # SWIR2
    
    # Load elevation data
    with rasterio.open(elevation_tiff_path) as src:
        elevation = src.read(1).astype(float)
    
    logger.info("Processing land cover classification...")
    land_cover, agricultural_mask = classify_land_cover(B02, B03, B04, B08, B11, B12)
    
    logger.info("Processing algae detection with severity...")
    ndwi, ndvi_algae_clipped, algae_severity = detect_algae_with_severity(B02, B03, B04, B08)
    
    logger.info("Processing terrain analysis...")
    slope, flow_direction = calculate_terrain_metrics(elevation)
    
    # Create single focused visualization - slope + agriculture + algae severity
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Base layer: Slope for terrain context
    im_slope = ax.imshow(slope, cmap='YlOrRd', vmin=0, vmax=15, alpha=0.7)
    
    # Overlay: Agricultural land (target areas for buffer strips)
    ag_display = np.where(agricultural_mask, 1, np.nan)
    ax.imshow(ag_display, cmap='Oranges', alpha=0.6, vmin=0, vmax=1, interpolation='nearest')
    
    # Overlay: Algae severity levels
    algae_severity_display = np.where(algae_severity > 0, algae_severity, np.nan)
    severity_colors = ['lightgreen', 'green', 'darkgreen']
    severity_cmap = ListedColormap(severity_colors)
    ax.imshow(algae_severity_display, cmap=severity_cmap, alpha=0.8, vmin=1, vmax=3, interpolation='nearest')
    
    # Add elevation contours for additional context
    if not np.all(np.isnan(elevation)):
        contours = ax.contour(elevation, levels=10, colors='black', alpha=0.3, linewidths=0.8)
        ax.clabel(contours, inline=True, fontsize=10, fmt='%d m')
    
    # Add colorbar for slope (shorter to avoid legend overlap)
    cbar = fig.colorbar(im_slope, ax=ax, shrink=0.5, pad=0.02, aspect=20)
    cbar.set_label('Slope (degrees)', fontsize=10)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Pixel X", fontsize=12)
    ax.set_ylabel("Pixel Y", fontsize=12)
    
    # Create comprehensive legend
    legend_elements = [
        Patch(facecolor='lightgreen', alpha=0.8, label='Low Algae Severity'),
        Patch(facecolor='green', alpha=0.8, label='Medium Algae Severity'),  
        Patch(facecolor='darkgreen', alpha=0.8, label='High Algae Severity'),
        Patch(facecolor='brown', alpha=0.6, label='Agricultural Land'),
        Patch(facecolor='yellow', alpha=0.7, label='Slope (Background)'),
        Patch(facecolor='black', alpha=0.3, label='Elevation Contours')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.25, 1), fontsize=10)
    
    plt.tight_layout()
    
    # Convert to bytes with proper error handling
    try:
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info("✅ Unified analysis visualization created successfully")
        return image_bytes
    
    except Exception as e:
        logger.error(f"Error saving figure: {e}")
        raise
    finally:
        # Always close the figure to free memory
        plt.close(fig)


def create_unified_analysis_with_topography(
    satellite_tiff_path: str,
    elevation_tiff_path: str,
    title: str = "Unified Geospatial Analysis: Buffer Strip Site Selection (Topographic)"
) -> bytes:
    """
    Create comprehensive analysis plot using topography with strong color contrast.
    Adds a blue water mask overlay and vivid highlights for algae and agriculture.
    Agriculture regions are smoothed to appear more solid.
    """
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import ndimage
    from io import BytesIO
    import logging
    from matplotlib.patches import Patch
    import rasterio

    logger = logging.getLogger(__name__)
    logger.info("Creating unified geospatial analysis with vivid color contrast and water overlay...")

    # --- Load satellite data ---
    with rasterio.open(satellite_tiff_path) as src:
        B02 = src.read(1).astype(float)
        B03 = src.read(2).astype(float)
        B04 = src.read(3).astype(float)
        B08 = src.read(4).astype(float)
        B11 = src.read(5).astype(float)
        B12 = src.read(6).astype(float)

    # --- Load elevation data ---
    with rasterio.open(elevation_tiff_path) as src:
        elevation = src.read(1).astype(float)

    # --- Process data ---
    land_cover, agricultural_mask = classify_land_cover(B02, B03, B04, B08, B11, B12)
    ndwi, ndvi_algae_clipped, algae_severity = detect_algae_with_severity(B02, B03, B04, B08)

    # --- Smooth agricultural mask to create solid shapes ---
    structure = np.ones((4, 4))
    agricultural_mask = ndimage.binary_closing(agricultural_mask, structure=structure)
    agricultural_mask = ndimage.binary_fill_holes(agricultural_mask)
    agricultural_mask = ndimage.gaussian_filter(agricultural_mask.astype(float), sigma=0.8) > 0.4



    # --- Create water mask ---
    water_mask = ndwi > 0.1  # threshold for detecting open water

    # --- Create figure ---
    fig, ax = plt.subplots(figsize=(14, 10))
    logger.info("Creating high-contrast topography base layer...")

    elevation_clean = np.copy(elevation)
    elevation_clean[elevation_clean <= -1000] = np.nan
    elevation_smooth = ndimage.gaussian_filter(elevation_clean, sigma=1)

    # --- Darker, higher-contrast grayscale base ---
    topo_cmap = LinearSegmentedColormap.from_list(
        "dark_gray_terrain",
        ["#dcdcdc", "#a0a0a0", "#5a5a5a", "#1f1f1f"]
    )

    n_levels = 40
    min_elev, max_elev = np.nanmin(elevation_smooth), np.nanmax(elevation_smooth)
    levels = np.linspace(min_elev, max_elev, n_levels)

    im_topo = ax.contourf(
        elevation_smooth,
        levels=levels,
        cmap=topo_cmap,
        alpha=0.65
    )

    # --- Contour lines ---
    ax.contour(
        elevation_smooth,
        levels=levels,
        colors="black",
        linewidths=0.3,
        alpha=0.25
    )

    # --- Blue water mask overlay ---
    water_display = np.where(water_mask, 1, np.nan)
    blue_cmap = LinearSegmentedColormap.from_list(
        "water_blue",
        ["#a3d9ff", "#007eff", "#003f91"]  # light → vivid → deep blue
    )
    ax.imshow(
        water_display,
        cmap=blue_cmap,
        alpha=0.8,
        vmin=0,
        vmax=1,
        interpolation='nearest'
    )

    # --- Brighter, smoother agriculture overlay ---
    ag_display = np.where(agricultural_mask, 1, np.nan)
    bright_orange_cmap = LinearSegmentedColormap.from_list(
        "vivid_orange",
        ["#ffd24d", "#ff8c00", "#ff5c00"]  # light gold → strong amber → vivid orange
    )
    ax.imshow(
        ag_display,
        cmap=bright_orange_cmap,
        alpha=0.7,
        vmin=0,
        vmax=1,
        interpolation='nearest'
    )

    # --- Neon-green algae overlay ---
    algae_severity_display = np.where(algae_severity > 0, algae_severity, np.nan)
    vivid_greens = ['#80ff99', "#006b24", "#001e0a"]  # bright → medium → dark green
    severity_cmap = ListedColormap(vivid_greens)
    ax.imshow(
        algae_severity_display,
        cmap=severity_cmap,
        alpha=0.9,
        vmin=1,
        vmax=3,
        interpolation='nearest'
    )

    # --- Colorbar ---
    cbar = fig.colorbar(im_topo, ax=ax, shrink=0.5, pad=0.02, aspect=20)
    cbar.set_label('Elevation (m)', fontsize=10)

    # --- Titles & Legend ---
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Pixel X", fontsize=12)
    ax.set_ylabel("Pixel Y", fontsize=12)

    legend_elements = [
        Patch(facecolor='#80ff99', alpha=1, label='Low Algae Severity'),
        Patch(facecolor="#006b24", alpha=1, label='Medium Algae Severity'),
        Patch(facecolor="#001e0a", alpha=1, label='High Algae Severity'),
        Patch(facecolor='#ff8c00', alpha=0.5, label='Agricultural Land'),
        Patch(facecolor='#007eff', alpha=0.8, label='Water'),
        Patch(facecolor='#a0a0a0', alpha=0.65, label='Topography (Background)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.25, 1), fontsize=10)

    plt.tight_layout()

    # --- Export ---
    try:
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_bytes = buffer.getvalue()
        buffer.close()

        logger.info("✅ Vivid unified analysis with smoothed agriculture and topography created successfully")
        return image_bytes

    except Exception as e:
        logger.error(f"Error saving figure: {e}")
        raise
    finally:
        plt.close(fig)







def create_unified_analysis_from_controller(
    satellite_controller,
    bbox: List[float],
    start_date: str,
    end_date: str,
    title: str = "Unified Geospatial Analysis: Lake Monitoring & Management",
    use_topography: bool = True
) -> bytes:
    """
    Create unified analysis by fetching satellite and elevation data
    
    Args:
        satellite_controller: SatelliteController instance
        bbox: Bounding box coordinates
        start_date: Start date string
        end_date: End date string
        title: Plot title
        use_topography: If True, use topography visualization instead of slope/terrain
        
    Returns:
        PNG image bytes
    """
    from .get_elevation import fetch_elevation_tiff
    
    with tempfile.TemporaryDirectory() as temp_dir:
        satellite_tiff = os.path.join(temp_dir, "satellite.tiff")
        elevation_tiff = os.path.join(temp_dir, "elevation.tiff")
        
        # Fetch satellite imagery (raw TIFF)
        logger.info("Fetching satellite imagery for unified analysis...")
        time_range = {"from": start_date, "to": end_date}
        response = satellite_controller.fetch_satellite_imagery(bbox, time_range)
        
        with open(satellite_tiff, 'wb') as f:
            f.write(response.content)
        
        # Fetch elevation data
        logger.info("Fetching elevation data for unified analysis...")
        fetch_elevation_tiff(bbox=bbox, output_path=elevation_tiff)
        
        # Create unified visualization (choose between terrain or topography)
        if use_topography:
            print("Creating unified analysis with topography...")
            return create_unified_analysis_with_topography(
                satellite_tiff_path=satellite_tiff,
                elevation_tiff_path=elevation_tiff,
                title=title
            )
        else:
            return create_unified_analysis_plot(
                satellite_tiff_path=satellite_tiff,
                elevation_tiff_path=elevation_tiff,
                title=title
            )