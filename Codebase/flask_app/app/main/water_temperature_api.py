"""
Water Temperature Analysis API
Handles water temperature data fetching and visualization using Sentinel-3 SLSTR data.
"""
import requests
import rasterio
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from rasterio.warp import reproject, Resampling
import tempfile
import os
from io import BytesIO
import base64
import logging
from typing import List, Optional, Dict, Any
import json

class WaterTemperatureAnalyzer:
    def __init__(self, copernicus_token=None):
        """
        Initialize the water temperature analyzer
        
        Args:
            copernicus_token: Copernicus Dataspace token for API access
        """
        self.copernicus_token = copernicus_token or os.getenv('COPERNICUS_TOKEN')
        if not self.copernicus_token:
            # Try to get token from the water_mask.sh file format
            raise ValueError("Copernicus Dataspace token not provided. Set COPERNICUS_TOKEN environment variable or pass token to constructor.")
        
        self.base_url = "https://sh.dataspace.copernicus.eu/api/v1/process"
        
    def fetch_water_mask(self, bbox: List[float], start_date: str, end_date: str) -> bytes:
        """
        Fetch water mask using Sentinel-2 data for water detection
        
        Args:
            bbox: Bounding box [west, south, east, north]
            start_date: Start date in ISO format
            end_date: End date in ISO format
            
        Returns:
            Water mask TIFF data as bytes
        """
        
        headers = {
            "Authorization": f"Bearer {self.copernicus_token}",
            "Content-Type": "application/json"
        }
        
        # Water detection evalscript from water_mask.sh
        evalscript = """//VERSION=3
function setup() {
  return {
    input: ["B03", "B08", "SCL"],
    output: { bands: 1, sampleType: "UINT8" }
  };
}

function evaluatePixel(sample) {
  // Use Scene Classification Layer (SCL)
  // SCL value 6 = water
  if (sample.SCL === 6) {
    return [1];
  }
  
  // Backup: NDWI-based water detection
  // NDWI = (Green - NIR) / (Green + NIR)
  let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08);
  
  // Water typically has NDWI > 0.3
  if (ndwi > 0.3) {
    return [1];
  }
  
  return [0];
}"""
        
        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox,
                    "properties": {
                        "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                    }
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": start_date,
                                "to": end_date
                            },
                            "mosaickingOrder": "leastCC",
                            "maxCloudCoverage": 30
                        }
                    }
                ]
            },
            "evalscript": evalscript,
            "output": {
                "width": 512,
                "height": 512,
                "responses": [
                    {
                        "identifier": "default",
                        "format": {"type": "image/tiff"}
                    }
                ]
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logging.error(f"Error fetching water mask: {e}")
            raise
    
    def fetch_water_temperature(self, bbox: List[float], start_date: str, end_date: str) -> bytes:
        """
        Fetch water temperature using Sentinel-3 SLSTR data
        
        Args:
            bbox: Bounding box [west, south, east, north]
            start_date: Start date in ISO format
            end_date: End date in ISO format
            
        Returns:
            Temperature TIFF data as bytes
        """
        
        headers = {
            "Authorization": f"Bearer {self.copernicus_token}",
            "Content-Type": "application/json"
        }
        
        # Temperature extraction evalscript from water_temp.sh
        evalscript = """//VERSION=3
function setup() {
  return {
    input: [{ bands: ["S8"] }],
    output: { bands: 1, sampleType: "FLOAT32" }
  };
}
function evaluatePixel(sample) {
  return [sample.S8];
}"""
        
        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox,
                    "properties": {
                        "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                    }
                },
                "data": [
                    {
                        "type": "sentinel-3-slstr",
                        "dataFilter": {
                            "timeRange": {
                                "from": start_date,
                                "to": end_date
                            },
                            "mosaickingOrder": "mostRecent",
                            "orbitDirection": "DESCENDING"
                        }
                    }
                ]
            },
            "evalscript": evalscript,
            "output": {
                "width": 512,
                "height": 512,
                "responses": [
                    {
                        "identifier": "default",
                        "format": {"type": "image/tiff"}
                    }
                ]
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logging.error(f"Error fetching water temperature: {e}")
            raise
    
    def process_water_temperature(self, temp_tiff_bytes: bytes, mask_tiff_bytes: Optional[bytes] = None) -> Dict[str, Any]:
        """
        Process water temperature data and create visualization
        
        Args:
            temp_tiff_bytes: Temperature TIFF data as bytes
            mask_tiff_bytes: Optional water mask TIFF data as bytes
            
        Returns:
            Dictionary with temperature statistics and base64 encoded image
        """
        try:
            # Save temp data to temporary files for processing
            with tempfile.NamedTemporaryFile(suffix='.tiff', delete=False) as temp_file:
                temp_file.write(temp_tiff_bytes)
                temp_path = temp_file.name
            
            mask_path = None
            if mask_tiff_bytes:
                with tempfile.NamedTemporaryFile(suffix='.tiff', delete=False) as mask_file:
                    mask_file.write(mask_tiff_bytes)
                    mask_path = mask_file.name
            
            # Read the temperature TIFF
            with rasterio.open(temp_path) as src:
                temp_data = src.read(1)
                temp_transform = src.transform
                temp_crs = src.crs
                temp_shape = temp_data.shape
            
            logging.info(f"Temperature data shape: {temp_shape}")
            logging.info(f"Value range: {np.nanmin(temp_data)} - {np.nanmax(temp_data)}")
            
            # Create or load water mask
            if mask_path and os.path.exists(mask_path):
                logging.info("Using provided water mask")
                
                with rasterio.open(mask_path) as mask_src:
                    # Reproject water mask to match temperature data
                    water_mask = np.zeros(temp_shape, dtype=np.uint8)
                    
                    reproject(
                        source=rasterio.band(mask_src, 1),
                        destination=water_mask,
                        src_transform=mask_src.transform,
                        src_crs=mask_src.crs,
                        dst_transform=temp_transform,
                        dst_crs=temp_crs,
                        resampling=Resampling.nearest
                    )
                    
                    water_mask = water_mask > 0
            else:
                logging.info("No water mask provided, using temperature threshold")
                # Fallback: simple threshold
                water_mask = (
                    ~np.isnan(temp_data) &
                    (temp_data > 285) &  # > 12°C
                    (temp_data < 302)    # < 29°C
                )
            
            # Apply mask to temperature data
            masked_temp = np.ma.masked_where(~water_mask, temp_data)
            
            # Convert to Celsius
            masked_temp_celsius = masked_temp - 273.15
            
            # Calculate statistics
            valid_temps = masked_temp_celsius[~masked_temp_celsius.mask]
            if len(valid_temps) > 0:
                # Calculate statistics with NaN handling
                mean_temp = np.mean(valid_temps)
                min_temp = np.min(valid_temps)
                max_temp = np.max(valid_temps)
                std_temp = np.std(valid_temps)
                
                # Convert to float and handle NaN values
                stats = {
                    'mean_temperature': float(mean_temp) if not np.isnan(mean_temp) else 0.0,
                    'min_temperature': float(min_temp) if not np.isnan(min_temp) else 0.0,
                    'max_temperature': float(max_temp) if not np.isnan(max_temp) else 0.0,
                    'std_temperature': float(std_temp) if not np.isnan(std_temp) else 0.0,
                    'water_pixels': int(np.sum(water_mask)),
                    'units': '°C'
                }
            else:
                stats = {
                    'mean_temperature': 0.0,
                    'min_temperature': 0.0,
                    'max_temperature': 0.0,
                    'std_temperature': 0.0,
                    'water_pixels': 0,
                    'units': '°C'
                }
            
            # Create visualization
            plt.figure(figsize=(12, 10))
            im = plt.imshow(masked_temp_celsius, cmap='RdYlBu_r', vmin=10, vmax=20)
            plt.colorbar(im, label='Temperature (°C)')
            plt.title('Water Temperature Analysis')
            plt.xlabel('Pixel X')
            plt.ylabel('Pixel Y')
            plt.tight_layout()
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_b64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close()
            
            # Clean up temporary files
            try:
                os.unlink(temp_path)
                if mask_path:
                    os.unlink(mask_path)
            except:
                pass
            
            return {
                'statistics': stats,
                'image_base64': image_b64
            }
            
        except Exception as e:
            logging.error(f"Error processing water temperature: {e}")
            raise
    
    def analyze_water_temperature(self, bbox: List[float], start_date: str, end_date: str, location_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete water temperature analysis for a given location and time
        
        Args:
            bbox: Bounding box [west, south, east, north]
            start_date: Start date in ISO format
            end_date: End date in ISO format
            location_name: Optional name for the location
            
        Returns:
            Dictionary with analysis results and visualization
        """
        try:
            logging.info(f"Starting water temperature analysis for {location_name or 'location'}")
            
            # Fetch water mask and temperature data in parallel
            logging.info("Fetching water mask...")
            try:
                mask_data = self.fetch_water_mask(bbox, start_date, end_date)
            except Exception as e:
                logging.warning(f"Could not fetch water mask: {e}")
                mask_data = None
            
            logging.info("Fetching water temperature data...")
            temp_data = self.fetch_water_temperature(bbox, start_date, end_date)
            
            # Process the data
            result = self.process_water_temperature(temp_data, mask_data)
            
            # Add metadata
            result['metadata'] = {
                'bbox': bbox,
                'start_date': start_date,
                'end_date': end_date,
                'location_name': location_name or f"Location {bbox}",
                'data_source': 'Sentinel-3 SLSTR'
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Error in water temperature analysis: {e}")
            raise