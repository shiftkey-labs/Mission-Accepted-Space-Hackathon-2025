curl -X POST 'https://sh.dataspace.copernicus.eu/api/v1/process' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
  -d '{
    "input": {
      "bounds": {
        "bbox": [13.0, 45.0, 14.0, 46.0],
        "properties": {
          "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        }
      },
      "data": [
        {
          "dataFilter": {
            "timeRange": {
              "from": "2023-08-01T00:00:00Z",
              "to": "2023-08-31T23:59:59Z"
            }
          },
          "type": "SENTINEL_3_SLSTR_WST"
        }
      ]
    },
    "output": {
      "width": 512,
      "height": 512,
      "responses": [
        {
          "identifier": "default",
          "format": {
            "type": "image/tiff"
          }
        }
      ]
    },
    "evalscript": "//VERSION=3\nfunction setup() {\n  return {\n    input: [\"WST\"], \n    output: { \n      bands: 1, \n      sampleType: \"FLOAT32\"\n    }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  return [sample.WST];\n}"
  }' > water_temp_image.tiff