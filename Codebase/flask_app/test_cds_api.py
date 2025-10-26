"""
Test script to verify CDS API connection and credentials
"""
import cdsapi
import logging

logging.basicConfig(level=logging.INFO)

def test_cds_api():
    try:
        # Initialize CDS client
        c = cdsapi.Client(
            url="https://cds.climate.copernicus.eu/api",
            key="8d98e02f-a9db-4c39-a201-931f7aa0437b"
        )
        
        print("CDS API client initialized successfully")
        
        # Try a simple request for Lake Winnipeg area
        bbox = [54.171428, -101.273432, 50.075155, -96.060934]  # [N, W, S, E]
        
        print(f"Testing data request for bbox: {bbox}")
        print("Year: 2024, Month: 04")
        
        # Make the request
        result = c.retrieve(
            'reanalysis-era5-land-monthly-means',
            {
                'variable': 'total_precipitation',
                'year': '2024',
                'month': '04',
                'area': bbox,  # [N, W, S, E]
                'format': 'netcdf',
                'grid': [0.01, 0.01]
            },
            'test_precip.nc'
        )
        
        print("Request submitted successfully!")
        print("Downloading...")
        
        # The download happens automatically when using the retrieve method
        print("Download completed successfully!")
        
        # Clean up
        import os
        if os.path.exists('test_precip.nc'):
            os.remove('test_precip.nc')
            print("Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"Error testing CDS API: {e}")
        return False

if __name__ == "__main__":
    test_cds_api()