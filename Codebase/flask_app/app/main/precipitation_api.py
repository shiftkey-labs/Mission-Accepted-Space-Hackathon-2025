"""
Precipitation Analysis API
Handles precipitation data fetching and visualization for algae bloom analysis.
"""
import cdsapi
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os
import zipfile
from io import BytesIO
import base64
import logging

class PrecipitationAnalyzer:
    def __init__(self, api_key=None):
        try:
            # Use provided API key or default
            key = api_key or "8d98e02f-a9db-4c39-a201-931f7aa0437b"
            
            self.client = cdsapi.Client(
                url="https://cds.climate.copernicus.eu/api",
                key=key
            )
            self.cds_available = True
            logging.info("CDS API client initialized successfully")
        except Exception as e:
            logging.warning(f"CDS API not available: {e}")
            self.client = None
            self.cds_available = False
    

    
    def fetch_precipitation_data(self, bbox, year, month, output_path=None):
        """
        Fetch precipitation data from Copernicus Climate Data Store
        
        Args:
            bbox: [north, west, south, east] bounding box coordinates
            year: Year as string (e.g., '2024')
            month: Month as string with leading zero (e.g., '04')
            output_path: Optional path to save the NetCDF file
        
        Returns:
            Path to the downloaded NetCDF file
        """
        if not self.cds_available or self.client is None:
            raise ValueError("CDS API is not available. Please check your API key and internet connection.")
        
        if output_path is None:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.nc').name
        
        # Validate inputs
        try:
            year_int = int(year)
            month_int = int(month)
            if year_int < 1940 or year_int > 2024:
                raise ValueError(f"Year {year} is outside available range (1940-2024)")
            if month_int < 1 or month_int > 12:
                raise ValueError(f"Month {month} is invalid (must be 1-12)")
        except ValueError as e:
            logging.error(f"Invalid date parameters: {e}")
            raise
        
        # Validate and convert bbox format
        if len(bbox) != 4:
            raise ValueError("bbox must contain exactly 4 coordinates")
        
        # Frontend sends [West, South, East, North], but CDS API expects [North, West, South, East]
        west, south, east, north = bbox
        
        # Validate coordinates
        if north <= south:
            raise ValueError(f"Invalid bbox: north ({north}) must be > south ({south})")
        if east <= west:
            raise ValueError(f"Invalid bbox: east ({east}) must be > west ({west})")
        
        # Convert to CDS API format [North, West, South, East]
        cds_bbox = [north, west, south, east]
        
        try:
            # Format the request exactly like the working example
            logging.info(f"Requesting precipitation data for {year}-{month}")
            logging.info(f"Original bbox (W,S,E,N): {bbox}")
            logging.info(f"CDS bbox (N,W,S,E): {cds_bbox}")
            
            # Ensure proper formatting for CDS API
            request_params = {
                'variable': 'total_precipitation',
                'year': str(year),
                'month': f"{int(month):02d}",  # Ensure two-digit month
                'area': [float(coord) for coord in cds_bbox],  # [N, W, S, E] - ensure float
                'format': 'netcdf',
                'grid': [0.01, 0.01]  # Use same resolution as working example
            }
            
            logging.info(f"CDS API request parameters: {request_params}")
            
            result = self.client.retrieve(
                'reanalysis-era5-land-monthly-means',
                request_params,
                output_path
            )
            
            # Wait for the request to complete
            if hasattr(result, 'download'):
                result.download(output_path)
            
            # Verify the file was created
            if not os.path.exists(output_path):
                raise ValueError("Precipitation data file was not created")
                
            logging.info(f"Successfully downloaded precipitation data to {output_path}")
            return output_path
            
        except Exception as e:
            error_msg = str(e)
            logging.error(f"CDS API error: {error_msg}")
            
            # Clean up any partial file
            if os.path.exists(output_path):
                try:
                    os.unlink(output_path)
                except:
                    pass
            
            if "MultiAdaptorNoDataError" in error_msg:
                raise ValueError(f"No precipitation data available for {year}-{month:02d} in the specified region. Try a different time period or location.")
            elif "400 Client Error" in error_msg or "Bad Request" in error_msg:
                raise ValueError(f"Invalid request parameters for CDS API. Date: {year}-{month:02d}, Region: {bbox}")
            elif "401" in error_msg or "Unauthorized" in error_msg:
                raise ValueError("CDS API authentication failed. Please check your API key and CDS account status.")
            elif "403" in error_msg or "Forbidden" in error_msg:
                raise ValueError("Access denied to CDS API. Please verify your account has the necessary permissions.")
            elif "timeout" in error_msg.lower():
                raise ValueError("CDS API request timed out. The service may be busy, please try again later.")
            else:
                raise ValueError(f"CDS API error: {error_msg}")
    
    def process_precipitation_file(self, nc_path, show_plot=False, save_png=None):
        """
        Process precipitation NetCDF file and create visualization
        
        Args:
            nc_path: Path to NetCDF file
            show_plot: Whether to display the plot
            save_png: Path to save PNG visualization
        
        Returns:
            Dictionary with precipitation statistics and base64 encoded image
        """
        try:
            # Handle both regular .nc files and zipped files
            if nc_path.endswith('.nc') and zipfile.is_zipfile(nc_path):
                # Extract from zip
                temp_dir = tempfile.mkdtemp()
                with zipfile.ZipFile(nc_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                # Find the actual .nc file
                extracted_files = os.listdir(temp_dir)
                nc_file = None
                for file in extracted_files:
                    if file.endswith('.nc'):
                        nc_file = os.path.join(temp_dir, file)
                        break
                if not nc_file:
                    raise ValueError("No .nc file found in the zip archive")
            else:
                nc_file = nc_path
            
            # Open the dataset with proper context management
            with xr.open_dataset(nc_file, engine='netcdf4') as ds:
                # Select first (and only) timestep along valid_time
                precip = ds['tp'].isel(valid_time=0)
                
                # Convert to mm (from m)
                precip_mm = precip * 1000
                
                # Load data into memory to avoid file access issues
                precip_data = precip_mm.load()
                
                # Calculate statistics
                stats = {
                    'mean_precipitation': float(precip_data.mean().values),
                    'max_precipitation': float(precip_data.max().values),
                    'min_precipitation': float(precip_data.min().values),
                    'total_precipitation': float(precip_data.sum().values),
                    'units': 'mm'
                }
                
                # Get title for plot
                plot_title = ds.attrs.get('title', 'Monthly Precipitation')
            
            # Create visualization (dataset is now closed)
            plt.figure(figsize=(10, 8))
            im = precip_data.plot(cmap='Blues', add_colorbar=False) #type: ignore
            plt.colorbar(im, label='Precipitation (mm)', shrink=0.8)
            plt.title(f"Total Precipitation - {plot_title} [mm]")
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            
            # Save or return as base64
            if save_png:
                plt.savefig(save_png, dpi=300, bbox_inches='tight')
                image_b64 = None
            else:
                # Convert to base64
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                buffer.seek(0)
                image_b64 = base64.b64encode(buffer.getvalue()).decode()
                buffer.close()
            
            if show_plot:
                plt.show()
            else:
                plt.close()
            
            # Clean up temporary files
            if nc_file != nc_path and os.path.exists(temp_dir):
                import shutil
                import time
                # Wait a moment for file handles to be released
                time.sleep(0.1)
                try:
                    shutil.rmtree(temp_dir)
                except Exception as cleanup_error:
                    logging.warning(f"Could not clean up temporary directory {temp_dir}: {cleanup_error}")
            
            return {
                'statistics': stats,
                'image_base64': image_b64,
                'image_path': save_png if save_png else None
            }
            
        except Exception as e:
            logging.error(f"Error processing precipitation file: {e}")
            # Try to cleanup temp files if they exist
            try:
                if 'temp_dir' in locals() and os.path.exists(temp_dir):
                    import shutil
                    import time
                    time.sleep(0.1)
                    shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                logging.warning(f"Could not clean up temp directory: {cleanup_error}")
            raise
    
    def analyze_precipitation_for_location(self, bbox, year, month, location_name=None):
        """
        Complete precipitation analysis for a given location and time
        
        Args:
            bbox: [north, west, south, east] bounding box coordinates
            year: Year as string
            month: Month as string with leading zero
            location_name: Optional name for the location
        
        Returns:
            Dictionary with analysis results and visualization
        """
        try:
            # Fetch precipitation data from CDS API
            nc_path = self.fetch_precipitation_data(bbox, year, month)
            
            # Process the data
            result = self.process_precipitation_file(nc_path)
            
            # Add metadata
            result['metadata'] = {
                'bbox': bbox,
                'year': year,
                'month': month,
                'location_name': location_name or f"Location {bbox}",
                'data_source': 'ERA5-Land Monthly Means'
            }
            
            # Clean up temporary file with better error handling
            if nc_path and os.path.exists(nc_path):
                try:
                    import time
                    time.sleep(0.1)  # Wait for file handles to be released
                    os.unlink(nc_path)
                    logging.info(f"Cleaned up temporary file: {nc_path}")
                except Exception as cleanup_error:
                    logging.warning(f"Could not clean up temporary file {nc_path}: {cleanup_error}")
            
            return result
            
        except Exception as e:
            logging.error(f"Error in precipitation analysis: {e}")
            # Try to cleanup temp file on error
            if 'nc_path' in locals() and nc_path and os.path.exists(nc_path):
                try:
                    import time
                    time.sleep(0.1)
                    os.unlink(nc_path)
                except:
                    pass
            raise
