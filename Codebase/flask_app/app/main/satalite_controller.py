"""
Satellite Controller
Handles satellite imagery requests from Sentinel Hub API for algae detection
"""
import requests
import os
from typing import Dict, List, Optional, Tuple
import logging
from .tif_to_algae_map import bytes_to_algae_png


class SatelliteController:
    """Controller for satellite imagery operations using Sentinel Hub API"""
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize the satellite controller
        
        Args:
            access_token: Sentinel Hub access token. If not provided, will look for TOKEN env var
        """
        self.access_token = access_token or os.getenv('TOKEN')
        self.base_url = "https://services.sentinel-hub.com/api/v1/process"
        
        if not self.access_token:
            logging.warning("No Sentinel Hub access token provided. Set TOKEN environment variable or pass token to constructor.")
    
    def fetch_satellite_imagery(
        self,
        bbox: List[float],
        time_range: Dict[str, str],
        width: int = 1000,
        height: int = 1000,
        output_format: str = "image/tiff",
        mosaicking_order: str = "mostRecent"
    ) -> requests.Response:
        """
        Fetch satellite imagery from Sentinel Hub API
        
        Args:
            bbox: Bounding box coordinates [min_lng, min_lat, max_lng, max_lat]
            time_range: Dictionary with 'from' and 'to' datetime strings
            width: Output image width in pixels
            height: Output image height in pixels
            output_format: Image format (e.g., 'image/tiff', 'image/png')
            mosaicking_order: Mosaicking order for multiple images
            
        Returns:
            requests.Response object containing the satellite imagery
            
        Raises:
            ValueError: If access token is not provided
            requests.RequestException: If API request fails
        """
        if not self.access_token:
            raise ValueError("Access token is required. Set SENTINEL_HUB_TOKEN environment variable or provide token.")
        
        # Evalscript for multi-spectral data extraction (B02, B03, B04, B08, B11, B12)
        evalscript = """//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04", "B08", "B11", "B12", "dataMask"],
    output: { id: "default", bands: 6, sampleType: "FLOAT32" }
  };
}

function evaluatePixel(sample) {
  if (sample.dataMask == 0) return [NaN, NaN, NaN, NaN, NaN, NaN];
  return [sample.B02, sample.B03, sample.B04, sample.B08, sample.B11, sample.B12];
}"""
        
        # Request payload
        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": time_range,
                        "mosaickingOrder": mosaicking_order
                    },
                    "processing": {"harmonizeValues": True}
                }]
            },
            "output": {
                "width": width,
                "height": height,
                "responses": [{
                    "identifier": "default",
                    "format": {"type": output_format}
                }]
            },
            "evalscript": evalscript
        }
        
        # Headers
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response
            
        except requests.RequestException as e:
            logging.error(f"Failed to fetch satellite imagery: {e}")
            raise
    
    def fetch_algae_detection_imagery(
        self,
        bbox: List[float],
        start_date: str,
        end_date: str,
        output_path: Optional[str] = None
    ) -> bytes:
        """
        Fetch satellite imagery specifically for algae detection
        
        Args:
            bbox: Bounding box coordinates [min_lng, min_lat, max_lng, max_lat]
            start_date: Start date in format "YYYY-MM-DDTHH:MM:SSZ"
            end_date: End date in format "YYYY-MM-DDTHH:MM:SSZ"
            output_path: Optional path to save the image file
            
        Returns:
            Raw image data as bytes
        """
        time_range = {
            "from": start_date,
            "to": end_date
        }
        
        response = self.fetch_satellite_imagery(bbox, time_range)
        tiff_bytes = response.content

        # Convert TIFF bytes to a matplotlib PNG image (three-panel visualization)
        try:
            png_bytes = bytes_to_algae_png(tiff_bytes)

            if output_path:
                # If user provided a path, ensure it's a .png (append if necessary)
                out_path = output_path
                if not out_path.lower().endswith('.png'):
                    out_path = out_path + '.png'
                with open(out_path, 'wb') as f:
                    f.write(png_bytes)
                logging.info(f"Algae detection PNG saved to {out_path}")

            return png_bytes

        except Exception as e:
            logging.error(f"Failed to convert TIFF to PNG plot: {e}")
            # Fall back to returning the raw TIFF bytes so callers don't lose data
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(tiff_bytes)
                logging.info(f"Satellite imagery (TIFF) saved to {output_path}")
            return tiff_bytes
    
    def fetch_lake_winnipeg_imagery(self, output_path: Optional[str] = None) -> bytes:
        """
        Convenience method to fetch imagery for Lake Winnipeg area (matching your curl example)
        
        Args:
            output_path: Optional path to save the image file
            
        Returns:
            Raw image data as bytes
        """
        # Coordinates from your curl example (Lake Winnipeg area)
        bbox = [-101.273432, 50.075155, -96.060934, 54.171428]
        start_date = "2022-08-01T10:00:00Z"
        end_date = "2022-08-31T22:00:00Z"
        
        return self.fetch_algae_detection_imagery(bbox, start_date, end_date, output_path)

    def fetch_raw_satellite_image(
        self,
        bbox: List[float],
        time_range: Dict[str, str],
        width: int = 1000,
        height: int = 1000,
        mosaicking_order: str = "leastCC"
    ) -> bytes:
        """
        Fetch raw RGB satellite imagery as PNG without any processing
        
        Args:
            bbox: Bounding box coordinates [min_lng, min_lat, max_lng, max_lat]
            time_range: Dictionary with 'from' and 'to' datetime strings
            width: Output image width in pixels
            height: Output image height in pixels
            mosaicking_order: Mosaicking order for multiple images
            
        Returns:
            bytes: Raw PNG image data
            
        Raises:
            ValueError: If access token is not provided
            requests.RequestException: If API request fails
        """
        if not self.access_token:
            raise ValueError("Access token is required. Set SENTINEL_HUB_TOKEN environment variable or provide token.")
        
        # Evalscript for RGB true color image
        evalscript = """//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04", "dataMask"],
    output: { bands: 3, sampleType: "AUTO" }
  };
}

function evaluatePixel(sample) {
  if (sample.dataMask == 0) return [0, 0, 0];
  // True color RGB (Red: B04, Green: B03, Blue: B02)
  // Apply gamma correction for better visualization
  let gain = 2.5;
  let gamma = 1.8;
  return [
    Math.pow(sample.B04 * gain, 1/gamma),
    Math.pow(sample.B03 * gain, 1/gamma), 
    Math.pow(sample.B02 * gain, 1/gamma)
  ];
}"""
        
        # Request payload for RGB PNG output
        payload = {
            "input": {
                "bounds": {
                    "bbox": bbox
                },
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": time_range,
                        "mosaickingOrder": mosaicking_order
                    },
                    "processing": {"harmonizeValues": True}
                }]
            },
            "output": {
                "width": width,
                "height": height,
                "responses": [{
                    "identifier": "default",
                    "format": {"type": "image/png"}
                }]
            },
            "evalscript": evalscript
        }
        
        # Headers
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.content
            
        except requests.RequestException as e:
            logging.error(f"Failed to fetch raw satellite image: {e}")
            raise


# Convenience function for direct usage
def fetch_satellite_data(
    bbox: List[float],
    start_date: str,
    end_date: str,
    access_token: Optional[str] = None,
    output_path: Optional[str] = None
) -> bytes:
    """
    Convenience function to fetch satellite data
    
    Args:
        bbox: Bounding box coordinates [min_lng, min_lat, max_lng, max_lat]
        start_date: Start date in format "YYYY-MM-DDTHH:MM:SSZ"
        end_date: End date in format "YYYY-MM-DDTHH:MM:SSZ"
        access_token: Sentinel Hub access token
        output_path: Optional path to save the image file
        
    Returns:
        Raw image data as bytes
    """
    controller = SatelliteController(access_token)
    return controller.fetch_algae_detection_imagery(bbox, start_date, end_date, output_path)


# Example usage matching your curl command
if __name__ == "__main__":
    # Set your access token (better to use environment variable)
    ACCESS_TOKEN = "your_access_token_here"
    
    # Initialize controller
    controller = SatelliteController(ACCESS_TOKEN)
    
    try:
        # Fetch Lake Winnipeg imagery (matches your curl example)
        image_data = controller.fetch_lake_winnipeg_imagery("output.tif")
        print(f"Successfully downloaded {len(image_data)} bytes of satellite imagery")
        
    except Exception as e:
        print(f"Error fetching satellite imagery: {e}")
