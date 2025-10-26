# Data Processing Workflow

This document outlines the steps taken to process RADARSAT Constellation Mission (RCM) satellite data using SNAP and QGIS software to detect shoreline changes along the coast of **northeastern New Brunswick, near Kouchibouguac National Park and Baie-Sainte-Anne**.

---

## 1. Data Acquisition

* **Source:** Natural Resources Canada (NRCan) Earth Observation Data Management System (EODMS) Portal (`https://www.eodms-sgdot.nrcan-rncan.gc.ca/`)
* **Satellite:** RADARSAT Constellation Mission (RCM)
* **Product Type:** Ground Range Detected (GRD)
* **Area of Interest:** Coastal region of northeastern New Brunswick, specifically including areas adjacent to **Kouchibouguac National Park and Baie-Sainte-Anne**.
* **Images Acquired:**
    * One RCM GRD image from late 2019 or 2020 (representing the "Before" shoreline).
    * One RCM GRD image from 2023 or 2024 (representing the "After" shoreline).
        *(You can optionally add the exact filenames here if you have them).*

---

## 2. SNAP Processing Workflow

The following steps were performed using the ESA SNAP Desktop software (version 12 used, though other recent versions should work) for *each* RCM image:

1.  **Open Product:** Imported the RCM data by opening the `manifest.safe` file within the product folder (`File -> Open Product`).
2.  **Radiometric Calibration:** Converted pixel values to calibrated backscatter.
    * Tool: `Radar -> Radiometric -> Calibrate`
    * Parameters: Checked **Output sigma0 band**.
3.  **Speckle Filtering:** Reduced inherent SAR speckle noise.
    * Tool: `Radar -> Speckle Filtering -> Single Product Speckle Filter`
    * Parameters: Filter = **Lee Sigma**, Window Size = **5x5**.
4.  **Terrain Correction:** Corrected geometric distortions using a Digital Elevation Model (DEM) and projected the image into a standard map coordinate system.
    * Tool: `Radar -> Geometric -> Terrain Correction -> Range-Doppler Terrain Correction`
    * Parameters:
        * DEM: **SRTM 1Sec HGT (AutoDownload)**
        * Map Projection: **WGS84 / UTM (Auto)**
        * Pixel Spacing: **20 meters**
5.  **Export Raster:** Saved the final terrain-corrected image.
    * Tool: Right-click product -> `Export -> GeoTIFF`. Saved as `[filename]_TC.tif`.

---

## 3. QGIS Analysis Workflow

The following steps were performed using QGIS software (version 3.x) for *each* exported GeoTIFF:

1.  **Load Raster:** Added the processed GeoTIFF (`[filename]_TC.tif`) to a QGIS project.
2.  **Polygonize (Raster to Vector):** Converted the raster image into vector polygons based on pixel values (land vs. water).
    * Tool: `Raster -> Conversion -> Polygonize (Raster to Vector)...`
    * Output saved temporarily.
3.  **Polygons to Lines:** Converted the filtered land polygons into boundary lines representing the shoreline.
    * Tool: `Vector -> Geometry Tools -> Polygons to Lines...`
4.  **Export Shoreline:** Saved the resulting line layer.
    * Tool: Right-click layer -> `Export -> Save Features As...`
    * Format: **ESRI Shapefile (.shp)**
    * Saved as `Shoreline_Before_LINE.shp` and `Shoreline_After_LINE.shp`.

These final Shapefiles represent the extracted shorelines for the two different dates and were used for the comparative analysis and map creation.