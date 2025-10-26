curl -X POST "https://sh.dataspace.copernicus.eu/api/v1/process" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYVUh3VWZKaHVDVWo0X3k4ZF8xM0hxWXBYMFdwdDd2anhob2FPLUxzREZFIn0.eyJleHAiOjE3NjE0MzgyMTAsImlhdCI6MTc2MTQzNzYxMCwianRpIjoiMDZhOWE3ZDMtYTVkMy00NGU1LTk3ZmYtZDgzMDA3NTgwYWEyIiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5kYXRhc3BhY2UuY29wZXJuaWN1cy5ldS9hdXRoL3JlYWxtcy9DRFNFIiwic3ViIjoiYTViY2E3ZjktZDZjZi00ODg0LWIwOTktNTcxMTc3OTkxMjM0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2gtYTBhOTNjMjUtYzZlYy00NmNmLWIwMTMtZTU5MDA0N2JiNjBiIiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIHVzZXItY29udGV4dCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjEzNC4xOTAuMTY3LjE4MCIsIm9yZ2FuaXphdGlvbnMiOlsiZGVmYXVsdC0wMDQ1MDdlMC03NTU3LTQ4NmYtYTVjZC1lZmU3ZWViMmUzMDMiXSwidXNlcl9jb250ZXh0X2lkIjoiNTM2MzBhMzAtMDlmOC00YjM3LTk1NTAtNzNkY2FkN2VlMjMwIiwiY29udGV4dF9yb2xlcyI6e30sImNvbnRleHRfZ3JvdXBzIjpbIi9hY2Nlc3NfZ3JvdXBzL3VzZXJfdHlwb2xvZ3kvY29wZXJuaWN1c19nZW5lcmFsLyIsIi9vcmdhbml6YXRpb25zL2RlZmF1bHQtMDA0NTA3ZTAtNzU1Ny00ODZmLWE1Y2QtZWZlN2VlYjJlMzAzLyJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtc2gtYTBhOTNjMjUtYzZlYy00NmNmLWIwMTMtZTU5MDA0N2JiNjBiIiwidXNlcl9jb250ZXh0IjoiZGVmYXVsdC0wMDQ1MDdlMC03NTU3LTQ4NmYtYTVjZC1lZmU3ZWViMmUzMDMiLCJjbGllbnRBZGRyZXNzIjoiMTM0LjE5MC4xNjcuMTgwIiwiY2xpZW50X2lkIjoic2gtYTBhOTNjMjUtYzZlYy00NmNmLWIwMTMtZTU5MDA0N2JiNjBiIn0.PH9x012LvjCWiqc_bpSR_nbqsB1D4-cJmjVX8MTbSNW76XK6ZUp96oVohc7FMajGhGolsgo36YH9Z5e9W06_VNHuB4PJwxBk1PXmKJqOXfHg1Ckl2Rxc_TfOIjr2ESQalrXrub79--lB8s4Ug8OvMqkCg62w5ReVYsX3PeML-JZDp-YSnSQINiAp1PMbabdDlCMtOsiyrYtWX4L9oOK_pQVViQEHApUTnVGQxO6WVjG7ohZ1cJ0i2ngRq-1P6Dyu9sqITO5Kw83QlP3KcYnC3SUuoXU-w_J8HnpwxrKnQIsV_gDoBxHFTnu21jXej-JbO2dLnLMSIrk0tgqKE3oiAA" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "bounds": {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428],
        "properties": {
          "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
        }
      },
      "data": [
        {
          "type": "sentinel-2-l2a",
          "dataFilter": {
            "timeRange": {
              "from": "2022-08-01T00:00:00Z",
              "to": "2022-08-25T00:00:00Z"
            },
            "mosaickingOrder": "leastCC",
            "maxCloudCoverage": 30
          }
        }
      ]
    },
    "evalscript": "//VERSION=3\nfunction setup() {\n  return {\n    input: [\"B03\", \"B08\", \"SCL\"],\n    output: { bands: 1, sampleType: \"UINT8\" }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  // Use Scene Classification Layer (SCL)\n  // SCL value 6 = water\n  if (sample.SCL === 6) {\n    return [1];\n  }\n  \n  // Backup: NDWI-based water detection\n  // NDWI = (Green - NIR) / (Green + NIR)\n  let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08);\n  \n  // Water typically has NDWI > 0.3\n  if (ndwi > 0.3) {\n    return [1];\n  }\n  \n  return [0];\n}",
    "output": {
      "width": 512,
      "height": 512,
      "responses": [
        {
          "identifier": "default",
          "format": { "type": "image/tiff" }
        }
      ]
    }
  }' \
  --output water_mask.tiff