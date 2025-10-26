import cdsapi

c = cdsapi.Client(
    url="https://cds.climate.copernicus.eu/api",
    key="8d98e02f-a9db-4c39-a201-931f7aa0437b"
)


c.retrieve(
    'reanalysis-era5-land-monthly-means',
    {
        'variable': 'total_precipitation',
        'year': '2024',
        'month': '04',
        'area': [54.171428, -101.273432, 50.075155, -96.060934],  # [N, W, S, E]
        'format': 'netcdf',
        'grid': [0.01, 0.01]
    },
    'April2024_precip.nc'
)
