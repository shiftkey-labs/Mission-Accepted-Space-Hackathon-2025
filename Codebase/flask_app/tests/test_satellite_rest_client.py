"""
HTTP REST Client for testing Satellite Imagery API endpoints
This test client can be used to test all satellite-related endpoints
"""

import requests
import json
import os
import time
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SatelliteAPITestClient:
    """REST client for testing satellite imagery API endpoints"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        """
        Initialize the test client
        
        Args:
            base_url: Base URL of the Flask application
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
    def test_health_endpoint(self) -> Dict[str, Any]:
        """Test the health check endpoint"""
        logger.info("Testing health endpoint...")
        
        url = f"{self.base_url}/health"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            result = {
                "endpoint": "/health",
                "method": "GET",
                "status_code": response.status_code,
                "response": response.json(),
                "success": True
            }
            
            logger.info(f"✅ Health check passed: {result['response']}")
            return result
            
        except Exception as e:
            result = {
                "endpoint": "/health",
                "method": "GET",
                "status_code": getattr(response, 'status_code', None),
                "error": str(e),
                "success": False
            }
            logger.error(f"❌ Health check failed: {e}")
            return result
    
    def test_satellite_info_endpoint(self) -> Dict[str, Any]:
        """Test the satellite info endpoint"""
        logger.info("Testing satellite info endpoint...")
        
        url = f"{self.base_url}/api/satellite/info"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            result = {
                "endpoint": "/api/satellite/info",
                "method": "GET",
                "status_code": response.status_code,
                "response": response.json(),
                "success": True
            }
            
            logger.info(f"✅ Satellite info retrieved successfully")
            logger.info(f"📡 Supported satellites: {result['response'].get('supported_satellites', [])}")
            return result
            
        except Exception as e:
            result = {
                "endpoint": "/api/satellite/info",
                "method": "GET",
                "status_code": getattr(response, 'status_code', None),
                "error": str(e),
                "success": False
            }
            logger.error(f"❌ Satellite info failed: {e}")
            return result
    
    def test_lake_winnipeg_endpoint(self, output_file: str = "test_lake_winnipeg.tif") -> Dict[str, Any]:
        """Test the Lake Winnipeg imagery endpoint"""
        logger.info("Testing Lake Winnipeg imagery endpoint...")
        
        url = f"{self.base_url}/api/satellite/lake-winnipeg"
        
        try:
            response = self.session.get(url, stream=True)
            
            if response.status_code == 200:
                # Save the file
                with open(output_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = os.path.getsize(output_file)
                
                result = {
                    "endpoint": "/api/satellite/lake-winnipeg",
                    "method": "GET",
                    "status_code": response.status_code,
                    "file_saved": output_file,
                    "file_size_bytes": file_size,
                    "content_type": response.headers.get('Content-Type'),
                    "success": True
                }
                
                logger.info(f"✅ Lake Winnipeg imagery downloaded successfully")
                logger.info(f"📁 File saved: {output_file} ({file_size} bytes)")
                return result
                
            else:
                # Try to get error response as JSON
                try:
                    error_response = response.json()
                except:
                    error_response = response.text
                
                result = {
                    "endpoint": "/api/satellite/lake-winnipeg",
                    "method": "GET",
                    "status_code": response.status_code,
                    "error": error_response,
                    "success": False
                }
                
                logger.error(f"❌ Lake Winnipeg imagery failed: {error_response}")
                return result
                
        except Exception as e:
            result = {
                "endpoint": "/api/satellite/lake-winnipeg",
                "method": "GET",
                "status_code": getattr(response, 'status_code', None),
                "error": str(e),
                "success": False
            }
            logger.error(f"❌ Lake Winnipeg imagery failed: {e}")
            return result
    
    def test_custom_satellite_fetch(
        self, 
        bbox: list = [-101.273432, 50.075155, -96.060934, 54.171428],
        start_date: str = "2022-08-01T10:00:00Z",
        end_date: str = "2022-08-31T22:00:00Z",
        output_file: str = "test_custom_satellite.tif"
    ) -> Dict[str, Any]:
        """Test the custom satellite fetch endpoint"""
        logger.info("Testing custom satellite fetch endpoint...")
        
        url = f"{self.base_url}/api/satellite/fetch"
        
        payload = {
            "bbox": bbox,
            "start_date": start_date,
            "end_date": end_date
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = self.session.post(url, json=payload, headers=headers, stream=True)
            
            if response.status_code == 200:
                # Save the file
                with open(output_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = os.path.getsize(output_file)
                
                result = {
                    "endpoint": "/api/satellite/fetch",
                    "method": "POST",
                    "status_code": response.status_code,
                    "request_payload": payload,
                    "file_saved": output_file,
                    "file_size_bytes": file_size,
                    "content_type": response.headers.get('Content-Type'),
                    "success": True
                }
                
                logger.info(f"✅ Custom satellite imagery downloaded successfully")
                logger.info(f"📁 File saved: {output_file} ({file_size} bytes)")
                logger.info(f"📍 Bbox: {bbox}")
                return result
                
            else:
                # Try to get error response as JSON
                try:
                    error_response = response.json()
                except:
                    error_response = response.text
                
                result = {
                    "endpoint": "/api/satellite/fetch",
                    "method": "POST",
                    "status_code": response.status_code,
                    "request_payload": payload,
                    "error": error_response,
                    "success": False
                }
                
                logger.error(f"❌ Custom satellite fetch failed: {error_response}")
                return result
                
        except Exception as e:
            result = {
                "endpoint": "/api/satellite/fetch",
                "method": "POST",
                "status_code": getattr(response, 'status_code', None),
                "request_payload": payload,
                "error": str(e),
                "success": False
            }
            logger.error(f"❌ Custom satellite fetch failed: {e}")
            return result
    
    def test_invalid_requests(self) -> Dict[str, Any]:
        """Test invalid requests to ensure proper error handling"""
        logger.info("Testing invalid requests...")
        
        tests = []
        
        # Test 1: Missing required fields in POST
        url = f"{self.base_url}/api/satellite/fetch"
        invalid_payload = {"bbox": [-101, 50, -96, 54]}  # Missing dates
        
        try:
            response = self.session.post(url, json=invalid_payload)
            error_response = response.json() if response.headers.get('Content-Type', '').startswith('application/json') else response.text
            
            tests.append({
                "test": "Missing required fields",
                "endpoint": "/api/satellite/fetch",
                "method": "POST",
                "status_code": response.status_code,
                "expected_status": 400,
                "response": error_response,
                "success": response.status_code == 400
            })
        except Exception as e:
            tests.append({
                "test": "Missing required fields",
                "error": str(e),
                "success": False
            })
        
        # Test 2: Invalid JSON
        try:
            response = self.session.post(url, data="invalid json", headers={"Content-Type": "application/json"})
            error_response = response.json() if response.headers.get('Content-Type', '').startswith('application/json') else response.text
            
            tests.append({
                "test": "Invalid JSON",
                "endpoint": "/api/satellite/fetch",
                "method": "POST",
                "status_code": response.status_code,
                "expected_status": 400,
                "response": error_response,
                "success": response.status_code == 400
            })
        except Exception as e:
            tests.append({
                "test": "Invalid JSON",
                "error": str(e),
                "success": False
            })
        
        # Test 3: Non-existent endpoint
        try:
            response = self.session.get(f"{self.base_url}/api/satellite/nonexistent")
            
            tests.append({
                "test": "Non-existent endpoint",
                "endpoint": "/api/satellite/nonexistent",
                "method": "GET",
                "status_code": response.status_code,
                "expected_status": 404,
                "success": response.status_code == 404
            })
        except Exception as e:
            tests.append({
                "test": "Non-existent endpoint",
                "error": str(e),
                "success": False
            })
        
        result = {
            "endpoint": "Invalid request tests",
            "tests": tests,
            "success": all(test.get('success', False) for test in tests)
        }
        
        if result['success']:
            logger.info("✅ All invalid request tests passed")
        else:
            logger.error("❌ Some invalid request tests failed")
        
        return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        logger.info("🧪 Starting comprehensive API tests...")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        test_results = {
            "health_check": self.test_health_endpoint(),
            "satellite_info": self.test_satellite_info_endpoint(),
            "lake_winnipeg": self.test_lake_winnipeg_endpoint(),
            "custom_fetch": self.test_custom_satellite_fetch(),
            "invalid_requests": self.test_invalid_requests()
        }
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate summary
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result.get('success', False))
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": (passed_tests / total_tests) * 100,
            "duration_seconds": duration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info("=" * 60)
        logger.info(f"🏁 Test Summary:")
        logger.info(f"   Total Tests: {summary['total_tests']}")
        logger.info(f"   Passed: {summary['passed_tests']}")
        logger.info(f"   Failed: {summary['failed_tests']}")
        logger.info(f"   Success Rate: {summary['success_rate']:.1f}%")
        logger.info(f"   Duration: {summary['duration_seconds']:.2f} seconds")
        
        return {
            "summary": summary,
            "test_results": test_results
        }


def main():
    """Main function to run the tests"""
    print("🛰️ Satellite API REST Client Test")
    print("=" * 60)
    
    # Initialize client
    client = SatelliteAPITestClient()
    
    # Check if Flask app is running
    try:
        response = requests.get(f"{client.base_url}/health", timeout=5)
        print(f"✅ Flask app is running at {client.base_url}")
    except requests.exceptions.RequestException:
        print(f"❌ Flask app is not running at {client.base_url}")
        print("Please start the Flask app with: python run.py")
        return
    
    # Run all tests
    results = client.run_all_tests()
    
    # Save results to file
    output_file = "test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {output_file}")
    
    # Return exit code based on success
    if results['summary']['success_rate'] == 100:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️ {results['summary']['failed_tests']} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())