"""
Main Routes
Contains the main application routes including the home page and health check.
"""
from flask import render_template, request, jsonify, send_file
from app.main import bp
from app.main.satalite_controller import SatelliteController
from app.main.get_elevation import fetch_elevation_tiff
from app.main.terrain import process_terrain_tiff
from app.main.tif_to_algae_map import process_tiff_file
from app.main.combined_visualization import create_combined_plot_from_controller
from app.main.unified_analysis import create_unified_analysis_from_controller
from app.main.precipitation_api import PrecipitationAnalyzer
from app.main.water_temperature_api import WaterTemperatureAnalyzer
import os
import tempfile
import logging
import zipfile
from io import BytesIO
import numpy as np
import json


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle NumPy data types and NaN values"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            if np.isnan(obj):
                return None  # or 0.0, depending on your preference
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


@bp.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@bp.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return {'status': 'healthy', 'message': 'Flask app is running'}


@bp.route('/api/satellite/fetch', methods=['POST'])
def fetch_satellite_imagery():
    """
    API endpoint to fetch satellite imagery
    
    Expected JSON payload:
    {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
        "start_date": "2022-08-01T10:00:00Z",
        "end_date": "2022-08-31T22:00:00Z",
        "format": "tiff" (optional, defaults to "tiff"),
        "use_topography": false (optional, set to true to use topography instead of slope)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['bbox', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get optional use_topography flag (defaults to False for terrain/slope)
        use_topography = data.get('use_topography', False)
        
        # Initialize satellite controller
        controller = SatelliteController()
        
        # Create unified analysis visualization
        # To use topography instead of terrain, set use_topography=True
        unified_image_data = create_unified_analysis_from_controller(
            satellite_controller=controller,
            bbox=data['bbox'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            title="Comprehensive Geospatial Analysis: Buffer Strip Site Selection",
            use_topography=True  # Toggle between terrain and topography
        )
        
        # Create temporary file to send as PNG
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(unified_image_data)
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name='unified_geospatial_analysis.png',
            mimetype='image/png'
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Error fetching satellite imagery: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/api/satellite/raw-image', methods=['POST'])
def fetch_raw_satellite_image():
    """
    API endpoint to fetch raw RGB satellite imagery without processing
    
    Expected JSON payload:
    {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
        "start_date": "2022-08-01T10:00:00Z",
        "end_date": "2022-08-31T22:00:00Z",
        "width": 1000 (optional, defaults to 1000),
        "height": 1000 (optional, defaults to 1000)
    }
    
    Returns:
        Raw PNG image of satellite data (RGB true color)
    """
    try:
        # Debug logging
        logging.info(f"Request Content-Type: {request.content_type}")
        logging.info(f"Request Headers: {dict(request.headers)}")
        
        data = request.get_json(force=True)  # Force JSON parsing
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['bbox', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        bbox = data['bbox']
        start_date = data['start_date']
        end_date = data['end_date']
        width = data.get('width', 1000)
        height = data.get('height', 1000)
        
        # Validate bbox format
        if not isinstance(bbox, list) or len(bbox) != 4:
            return jsonify({'error': 'bbox must be a list of 4 coordinates [min_lng, min_lat, max_lng, max_lat]'}), 400
        
        controller = SatelliteController()
        
        # Prepare time range for controller
        time_range = {
            "from": start_date,
            "to": end_date
        }
        
        # Fetch raw satellite image
        image_data = controller.fetch_raw_satellite_image(
            bbox=bbox,
            time_range=time_range,
            width=width,
            height=height
        )
        
        # Create temporary file to send as PNG
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(image_data)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name='raw_satellite_image.png',
            mimetype='image/png'
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Error fetching raw satellite image: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/api/satellite/lake-winnipeg')
def fetch_lake_winnipeg():
    """
    Unified Lake Winnipeg analysis - combines satellite imagery, elevation data,
    algae detection with severity levels, land cover classification, and terrain analysis
    for comprehensive buffer strip site selection.
    """
    try:
        # Lake Winnipeg coordinates and date range
        bbox = [-101.273432, 50.075155, -96.060934, 54.171428]
        start_date = "2022-08-01T10:00:00Z"
        end_date = "2022-08-31T22:00:00Z"
        
        controller = SatelliteController()
        
        # Create unified analysis visualization
        unified_image_data = create_unified_analysis_from_controller(
            satellite_controller=controller,
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            title="Lake Winnipeg: Comprehensive Geospatial Analysis & Buffer Strip Site Selection"
        )

        # Create temporary file to send as PNG
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(unified_image_data)
        temp_file.close()

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name='lake_winnipeg_unified_analysis.png',
            mimetype='image/png'
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Error in Lake Winnipeg unified analysis: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/api/satellite/comprehensive', methods=['POST'])
def fetch_comprehensive_analysis():
    """
    Comprehensive endpoint that fetches satellite data, elevation data, 
    and generates both algae detection and terrain visualization images.
    
    Expected JSON payload:
    {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
        "start_date": "2022-08-01T10:00:00Z",
        "end_date": "2022-08-31T22:00:00Z"
    }
    
    Returns a ZIP file containing:
    - algae_detection.png (NDWI, NDVI, algae mask visualization)
    - terrain_analysis.png (elevation and slope visualization)
    - ndvi_water.txt (numeric NDVI data over water)
    - algae_mask.txt (numeric algae mask data)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['bbox', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        bbox = data['bbox']
        
        # Create temporary directory for all processing
        with tempfile.TemporaryDirectory() as temp_dir:
            satellite_tiff = os.path.join(temp_dir, "satellite.tif")
            elevation_tiff = os.path.join(temp_dir, "elevation.tif")
            algae_png = os.path.join(temp_dir, "algae_detection.png")
            terrain_png = os.path.join(temp_dir, "terrain_analysis.png")
            ndvi_txt = os.path.join(temp_dir, "ndvi_water.txt")
            algae_txt = os.path.join(temp_dir, "algae_mask.txt")
            
            # 1. Fetch satellite imagery
            logging.info("Fetching satellite imagery...")
            satellite_controller = SatelliteController()
            satellite_data = satellite_controller.fetch_algae_detection_imagery(
                bbox=bbox,
                start_date=data['start_date'],
                end_date=data['end_date'],
                output_path=satellite_tiff
            )
            
            # 2. Process algae detection
            logging.info("Processing algae detection...")
            process_tiff_file(
                input_path=satellite_tiff,
                png_output=algae_png,
                ndvi_output=ndvi_txt,
                algae_output=algae_txt,
                show_plot=False
            )
            
            # 3. Fetch elevation data
            logging.info("Fetching elevation data...")
            fetch_elevation_tiff(
                bbox=bbox,
                output_path=elevation_tiff
            )
            
            # 4. Process terrain analysis
            logging.info("Processing terrain analysis...")
            process_terrain_tiff(
                input_path=elevation_tiff,
                output_png=terrain_png,
                save_arrays=False,
                show_plot=False
            )
            
            # 5. Create ZIP file with all outputs
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add visualization images
                zip_file.write(algae_png, "algae_detection.png")
                zip_file.write(terrain_png, "terrain_analysis.png")
                
                # Add numeric data files
                zip_file.write(ndvi_txt, "ndvi_water.txt")
                zip_file.write(algae_txt, "algae_mask.txt")
            
            zip_buffer.seek(0)
            
            # Create temporary file for the ZIP
            temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
            temp_zip.write(zip_buffer.getvalue())
            temp_zip.close()
            
            logging.info("✅ Comprehensive analysis complete!")
            
            return send_file(
                temp_zip.name,
                as_attachment=True,
                download_name='satellite_terrain_analysis.zip',
                mimetype='application/zip'
            )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Error in comprehensive analysis: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/api/satellite/lake-winnipeg-comprehensive')
def fetch_lake_winnipeg_comprehensive():
    """
    Comprehensive analysis for Lake Winnipeg area - satellite + elevation + processing.
    Returns ZIP with algae detection and terrain analysis.
    """
    try:
        # Use Lake Winnipeg coordinates and date range
        bbox = [-101.273432, 50.075155, -96.060934, 54.171428]
        start_date = "2022-08-01T10:00:00Z"
        end_date = "2022-08-31T22:00:00Z"
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            satellite_tiff = os.path.join(temp_dir, "lake_winnipeg_satellite.tif")
            elevation_tiff = os.path.join(temp_dir, "lake_winnipeg_elevation.tif")
            algae_png = os.path.join(temp_dir, "lake_winnipeg_algae.png")
            terrain_png = os.path.join(temp_dir, "lake_winnipeg_terrain.png")
            ndvi_txt = os.path.join(temp_dir, "lake_winnipeg_ndvi_water.txt")
            algae_txt = os.path.join(temp_dir, "lake_winnipeg_algae_mask.txt")
            
            # Process satellite and elevation data
            satellite_controller = SatelliteController()
            
            # Fetch and process satellite imagery
            satellite_controller.fetch_algae_detection_imagery(
                bbox=bbox,
                start_date=start_date,
                end_date=end_date,
                output_path=satellite_tiff
            )
            
            process_tiff_file(
                input_path=satellite_tiff,
                png_output=algae_png,
                ndvi_output=ndvi_txt,
                algae_output=algae_txt,
                show_plot=False
            )
            
            # Fetch and process elevation data
            fetch_elevation_tiff(bbox=bbox, output_path=elevation_tiff)
            process_terrain_tiff(
                input_path=elevation_tiff,
                output_png=terrain_png,
                save_arrays=False,
                show_plot=False
            )
            
            # Create ZIP with all results
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(algae_png, "lake_winnipeg_algae_detection.png")
                zip_file.write(terrain_png, "lake_winnipeg_terrain_analysis.png")
                zip_file.write(ndvi_txt, "lake_winnipeg_ndvi_water.txt")
                zip_file.write(algae_txt, "lake_winnipeg_algae_mask.txt")
            
            zip_buffer.seek(0)
            
            temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
            temp_zip.write(zip_buffer.getvalue())
            temp_zip.close()
            
            return send_file(
                temp_zip.name,
                as_attachment=True,
                download_name='lake_winnipeg_comprehensive_analysis.zip',
                mimetype='application/zip'
            )
        
    except Exception as e:
        logging.error(f"Error in Lake Winnipeg comprehensive analysis: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/api/precipitation/analyze', methods=['POST'])
def analyze_precipitation():
    """
    API endpoint to analyze precipitation data for a specific location and time
    
    Expected JSON payload:
    {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
        "year": "2024",
        "month": "04",
        "location_name": "Lake Winnipeg" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['bbox', 'year', 'month']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        bbox = data['bbox']
        year = data['year']
        month = data['month']
        location_name = data.get('location_name', 'Unknown Location')
        
        # Validate bbox format
        if not isinstance(bbox, list) or len(bbox) != 4:
            return jsonify({'error': 'bbox must be an array of 4 coordinates [north, west, south, east]'}), 400
        
        # Validate year and month
        try:
            int(year)
            int(month)
        except ValueError:
            return jsonify({'error': 'year and month must be valid integers'}), 400
        
        # Ensure month has leading zero if needed
        month = f"{int(month):02d}"
        
        # Initialize precipitation analyzer
        analyzer = PrecipitationAnalyzer()
        
        # Perform analysis
        result = analyzer.analyze_precipitation_for_location(
            bbox=bbox,
            year=year,
            month=month,
            location_name=location_name
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except ValueError as e:
        # Handle validation errors and CDS API specific errors
        logging.warning(f"Validation error in precipitation analysis: {e}")
        return jsonify({
            'error': 'Invalid request parameters',
            'message': str(e),
            'suggestion': 'Please try a different date range (1940-2024) or check your location coordinates.'
        }), 400
        
    except Exception as e:
        logging.error(f"Unexpected error in precipitation analysis: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while processing your request.',
            'details': str(e) if logging.getLogger().isEnabledFor(logging.DEBUG) else 'Enable debug logging for details'
        }), 500


@bp.route('/api/water-temperature/analyze', methods=['POST'])
def analyze_water_temperature():
    """
    API endpoint to analyze water temperature data for a specific location and time
    
    Expected JSON payload:
    {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
        "start_date": "2022-08-01T10:00:00Z",
        "end_date": "2022-08-31T22:00:00Z",
        "location_name": "Lake Winnipeg" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['bbox', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        bbox = data['bbox']
        start_date = data['start_date']
        end_date = data['end_date']
        location_name = data.get('location_name', 'Unknown Location')
        
        # Validate bbox format
        if not isinstance(bbox, list) or len(bbox) != 4:
            return jsonify({'error': 'bbox must be an array of 4 coordinates [west, south, east, north]'}), 400
        
        # Validate date formats (basic check)
        if not all('T' in date and 'Z' in date for date in [start_date, end_date]):
            return jsonify({'error': 'Dates must be in ISO format (YYYY-MM-DDTHH:MM:SSZ)'}), 400
        
        # Initialize water temperature analyzer
        analyzer = WaterTemperatureAnalyzer()
        
        # Perform analysis
        result = analyzer.analyze_water_temperature(
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            location_name=location_name
        )
        
        # Ensure all numeric values are JSON serializable
        def clean_for_json(obj):
            if isinstance(obj, dict):
                return {k: clean_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_for_json(v) for v in obj]
            elif isinstance(obj, (np.floating, float)):
                return None if np.isnan(obj) else float(obj)
            elif isinstance(obj, (np.integer, int)):
                return int(obj)
            else:
                return obj
        
        clean_result = clean_for_json(result)
        
        return jsonify({
            'success': True,
            'data': clean_result
        })
        
    except ValueError as e:
        # Handle validation errors and API specific errors
        logging.warning(f"Validation error in water temperature analysis: {e}")
        return jsonify({
            'error': 'Invalid request parameters',
            'message': str(e),
            'suggestion': 'Please check your date range and location coordinates, and verify API token is valid.'
        }), 400
        
    except Exception as e:
        logging.error(f"Unexpected error in water temperature analysis: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while processing your request.',
            'details': str(e) if logging.getLogger().isEnabledFor(logging.DEBUG) else 'Enable debug logging for details'
        }), 500


@bp.route('/api/satellite/info')
def satellite_info():
    """Get information about unified geospatial analysis capabilities"""
    return jsonify({
        'service': 'Unified Geospatial Analysis API',
        'description': 'Comprehensive analysis combining satellite imagery, elevation data, and multiple analytical layers',
        'data_sources': {
            'satellite': 'Sentinel-2 L2A (6 bands: B02, B03, B04, B08, B11, B12)',
            'elevation': 'Copernicus DEM 30m resolution',
            'precipitation': 'ERA5-Land Monthly Means',
            'water_temperature': 'Sentinel-3 SLSTR (Sea/Land Surface Temperature)'
        },
        'analysis_components': [
            'Algae bloom detection with severity classification (Low/Medium/High)',
            'Land cover classification (Water, Urban, Bare soil, Agriculture, Forest)',
            'Terrain analysis (slope, flow direction)',
            'Buffer strip site selection visualization',
            'Precipitation analysis and visualization',
            'Water temperature analysis and mapping'
        ],
        'endpoints': {
            'custom_analysis': 'POST /api/satellite/fetch - Custom bbox and date range',
            'raw_satellite_image': 'POST /api/satellite/raw-image - Raw RGB satellite imagery without processing',
            'lake_winnipeg': 'GET /api/satellite/lake-winnipeg - Pre-configured Lake Winnipeg analysis',
            'comprehensive_zip': 'POST /api/satellite/comprehensive - Returns ZIP with individual components',
            'lake_winnipeg_zip': 'GET /api/satellite/lake-winnipeg-comprehensive - ZIP for Lake Winnipeg',
            'precipitation_analysis': 'POST /api/precipitation/analyze - Precipitation data analysis and visualization',
            'water_temperature_analysis': 'POST /api/water-temperature/analyze - Water temperature analysis and mapping'
        },
        'output_format': 'Single PNG image with main visualization (buffer strip site selection) plus 6 supporting analytical views',
        'example_bbox': [-101.273432, 50.075155, -96.060934, 54.171428],
        'date_format': 'YYYY-MM-DDTHH:MM:SSZ'
    })
