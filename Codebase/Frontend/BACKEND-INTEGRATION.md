# Backend Integration Guide

## For Backend Team Member

This document explains what the frontend expects from the Flask API.

## Required API Endpoint

### `GET /api/satellite-positions`

The frontend needs a single endpoint that returns an array of satellite objects with TLE data.

### Expected Response Format

```json
[
  {
    "name": "SAPPHIRE",
    "norad_id": 39088,
    "tle1": "1 39088U 13009C   25297.72717685  .00000254  00000-0  10395-3 0  9991",
    "tle2": "2 39088  98.4172 117.8868 0010342 226.4031 133.6297 14.35131764662806",
    "operator": "DND/CAF",
    "launch_date": "Feb 25, 2013",
    "mission": "Space surveillance in MEO/GEO",
    "status": "Active"
  },
  {
    "name": "RADARSAT-2",
    "norad_id": 32382,
    "tle1": "1 32382U 07061A   25297.86575773  .00000116  00000+0  61896-4 0  9996",
    "tle2": "2 32382  98.5813 303.1603 0001129  89.7632 270.3680 14.29982529932324",
    "operator": "MDA Space",
    "launch_date": "Dec 14, 2007",
    "mission": "C-band Synthetic Aperture Radar (SAR) Earth Observation",
    "status": "Active"
  }
]
```

## Critical Fields

The frontend **requires** these fields for orbit calculation:
- `norad_id` (integer) - Unique satellite identifier
- `tle1` (string) - First line of TLE data
- `tle2` (string) - Second line of TLE data

## Optional Display Fields

These fields are displayed in the UI but not required for orbit calculation:
- `name` (string) - Satellite name
- `operator` (string) - Operating organization
- `launch_date` (string) - Launch date
- `mission` (string) - Mission description
- `status` (string) - Current status

## Flask Implementation Example

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/api/satellite-positions')
def get_satellite_positions():
    # Load your satellite data (from JSON file, database, etc.)
    satellites = load_satellite_data()  # Your implementation
    
    # Ensure each satellite has tle1 and tle2 strings
    return jsonify(satellites)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## CORS Configuration

The frontend runs on `http://localhost:3000` (Next.js default).
Your Flask API needs to allow CORS from this origin:

```python
from flask_cors import CORS

# Option 1: Allow all origins (development)
CORS(app)

# Option 2: Specific origin (production)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
```

## Testing the Integration

1. Start your Flask backend: `python app.py` (typically on port 5000)
2. Update frontend API URL in `app/page.js`:

```javascript
// Change this line:
fetch('/data/Satellite-TLE-Data.json')

// To this:
fetch('http://localhost:5000/api/satellite-positions')
```

3. Test in browser console:
```javascript
fetch('http://localhost:5000/api/satellite-positions')
  .then(r => r.json())
  .then(console.log)
```

## TLE Data Sources

If you need to fetch TLE data, here are some options:

### 1. CelesTrak API (Recommended)
```python
import requests

def fetch_tle_data():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
    response = requests.get(url)
    return response.json()
```

### 2. Space-Track.org
- Requires free account
- More comprehensive data
- Rate limited

### 3. N2YO API
- Real-time tracking
- Requires API key

## Data Validation

Ensure TLE strings are valid:
- Line 1 starts with "1 "
- Line 2 starts with "2 "
- Each line is 69 characters
- Contains valid checksum

```python
def validate_tle(tle1, tle2):
    if not tle1.startswith('1 ') or not tle2.startswith('2 '):
        return False
    if len(tle1) != 69 or len(tle2) != 69:
        return False
    return True
```

## Environment Variables

Recommended `.env` structure:

```
FLASK_ENV=development
API_PORT=5000
CORS_ORIGINS=http://localhost:3000
TLE_UPDATE_INTERVAL=3600  # Update TLE data every hour
```

## Error Handling

Return appropriate HTTP status codes:

```python
@app.route('/api/satellite-positions')
def get_satellite_positions():
    try:
        satellites = load_satellite_data()
        return jsonify(satellites), 200
    except FileNotFoundError:
        return jsonify({'error': 'Satellite data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Next Steps

1. Set up Flask project with CORS
2. Load satellite TLE data (from JSON or API)
3. Create `/api/satellite-positions` endpoint
4. Test with curl or Postman
5. Update frontend to use your API
6. Test integration

## Questions?

If the frontend needs additional fields or different formatting, let me know and I can adjust the code.

## Sample curl Test

```bash
curl http://localhost:5000/api/satellite-positions
```

Expected output: JSON array with satellite objects including `tle1` and `tle2`.

