# Satellite API Test Suite

This folder contains various HTTP REST clients and test tools for testing the Satellite Imagery API endpoints.

## Test Files

### 1. `test_satellite_rest_client.py`
**Comprehensive Python test client**
- Full test suite with detailed logging
- Automatic file downloads and validation
- Error handling tests
- JSON output with test results
- Usage: `python test_satellite_rest_client.py`

### 2. `satellite_api.http`
**VS Code REST Client format**
- Simple HTTP file for manual testing
- Works with VS Code REST Client extension
- Easy to modify and run individual tests
- Usage: Open in VS Code and click "Send Request"

### 3. `test_satellite_api.sh`
**Bash script for Linux/Mac**
- Command-line testing using curl
- Automatic file downloads
- JSON parsing with jq
- Usage: `chmod +x test_satellite_api.sh && ./test_satellite_api.sh`

### 4. `test_satellite_api.ps1`
**PowerShell script for Windows**
- Windows-native testing using Invoke-RestMethod
- Automatic file downloads
- Detailed error handling
- Usage: `.\test_satellite_api.ps1`

## API Endpoints Tested

### `GET /health`
Basic health check to verify the Flask app is running.

### `GET /api/satellite/info`
Get information about satellite API capabilities, supported formats, and example parameters.

### `GET /api/satellite/lake-winnipeg`
Download satellite imagery for Lake Winnipeg area (matches the original curl command).

### `POST /api/satellite/fetch`
Download custom satellite imagery with specified parameters:
```json
{
    "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
    "start_date": "2022-08-01T10:00:00Z",
    "end_date": "2022-08-31T22:00:00Z"
}
```

## Prerequisites

### For Python Tests
```bash
pip install requests
```

### For Bash Tests
- `curl` (usually pre-installed)
- `jq` for JSON parsing: `sudo apt install jq` (Linux) or `brew install jq` (Mac)

### For PowerShell Tests
- PowerShell 5.1+ (built-in on Windows)
- No additional dependencies required

### For VS Code HTTP Tests
- Install the "REST Client" extension in VS Code

## Usage Examples

### Quick Start
1. Start the Flask app: `python run.py`
2. Run any test client:
   ```bash
   # Python (most comprehensive)
   python tests/test_satellite_rest_client.py
   
   # PowerShell (Windows)
   .\tests\test_satellite_api.ps1
   
   # Bash (Linux/Mac)
   ./tests/test_satellite_api.sh
   ```

### Manual Testing
Use the `satellite_api.http` file with VS Code REST Client extension for interactive testing.

## Test Output

All tests create output files in the `test_outputs/` directory:
- `lake_winnipeg.tif` - Imagery from Lake Winnipeg endpoint
- `custom_satellite.tif` - Imagery from custom fetch endpoint
- `test_results.json` - Detailed test results (Python client only)

## Environment Variables

Set your Sentinel Hub token as an environment variable:
```bash
export TOKEN="your_sentinel_hub_token_here"
```

Or it will use the token configured in the satellite controller.

## Expected Test Results

✅ **Successful Tests:**
- Health check returns 200 with JSON response
- Satellite info returns API capabilities
- File downloads complete with valid TIFF files
- Error handling returns appropriate HTTP status codes

❌ **Common Issues:**
- Flask app not running (connection refused)
- Missing or invalid Sentinel Hub token
- Network connectivity issues
- Invalid request parameters

## Original Curl Command Equivalent

The Lake Winnipeg endpoint (`/api/satellite/lake-winnipeg`) replicates this curl command:
```bash
curl -X POST https://services.sentinel-hub.com/api/v1/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...}' -o output.tif
```