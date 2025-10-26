curl -X POST "https://sh.dataspace.copernicus.eu/api/v1/process" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYVUh3VWZKaHVDVWo0X3k4ZF8xM0hxWXBYMFdwdDd2anhob2FPLUxzREZFIn0.eyJleHAiOjE3NjE0Mzc1NzcsImlhdCI6MTc2MTQzNjk3NywianRpIjoiMjdlOTM0NzUtN2FjOC00OTY3LWEzNjEtMjBlYzYzZTk4NWUzIiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5kYXRhc3BhY2UuY29wZXJuaWN1cy5ldS9hdXRoL3JlYWxtcy9DRFNFIiwic3ViIjoiYTViY2E3ZjktZDZjZi00ODg0LWIwOTktNTcxMTc3OTkxMjM0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2gtYTBhOTNjMjUtYzZlYy00NmNmLWIwMTMtZTU5MDA0N2JiNjBiIiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIHVzZXItY29udGV4dCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjEzNC4xOTAuMTY3LjE4MCIsIm9yZ2FuaXphdGlvbnMiOlsiZGVmYXVsdC0wMDQ1MDdlMC03NTU3LTQ4NmYtYTVjZC1lZmU3ZWViMmUzMDMiXSwidXNlcl9jb250ZXh0X2lkIjoiNTM2MzBhMzAtMDlmOC00YjM3LTk1NTAtNzNkY2FkN2VlMjMwIiwiY29udGV4dF9yb2xlcyI6e30sImNvbnRleHRfZ3JvdXBzIjpbIi9hY2Nlc3NfZ3JvdXBzL3VzZXJfdHlwb2xvZ3kvY29wZXJuaWN1c19nZW5lcmFsLyIsIi9vcmdhbml6YXRpb25zL2RlZmF1bHQtMDA0NTA3ZTAtNzU1Ny00ODZmLWE1Y2QtZWZlN2VlYjJlMzAzLyJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtc2gtYTBhOTNjMjUtYzZlYy00NmNmLWIwMTMtZTU5MDA0N2JiNjBiIiwidXNlcl9jb250ZXh0IjoiZGVmYXVsdC0wMDQ1MDdlMC03NTU3LTQ4NmYtYTVjZC1lZmU3ZWViMmUzMDMiLCJjbGllbnRBZGRyZXNzIjoiMTM0LjE5MC4xNjcuMTgwIiwiY2xpZW50X2lkIjoic2gtYTBhOTNjMjUtYzZlYy00NmNmLWIwMTMtZTU5MDA0N2JiNjBiIn0.ACv53frVuxJlRItZpWJz8fXGuXL4Vi-vHW3B6mZtBPAzBD1vs7KRoGMvrOO1xzpC_S-az2Xi_fBWAbNgwJUQlsgmGWsyimihgg54bW_OfVitoYA5IQUWZsgiuXO2MRF7A-a6S_QfzQz32lrHUFybyJ9QVaxt2Wt6KLhZRJ0FVmSwUBvVyL5BL9QTHFwyk-q1JQqIxpMLSmYIhb_t-3RN8NNIdO-acx4HVVf2wCNYSnIuBpPVJxzcZdPV3dOm-RgJ3MV1MXoP5CmNIrsK3dcFTbqJwtzk43-HiWftygrbY0et56MmMrGdQBTd34y-IEyPbMYp6vix6im1XAzQdHknyA" \
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
          "type": "sentinel-3-slstr",
          "dataFilter": {
            "timeRange": {
              "from": "2022-08-01T00:00:00Z",
              "to": "2022-08-25T00:00:00Z"
            },
            "mosaickingOrder": "mostRecent",
            "orbitDirection": "DESCENDING"
          }
        }
      ]
    },
    "evalscript": "//VERSION=3\nfunction setup() {\n  return {\n    input: [{ bands: [\"S8\"] }],\n    output: { bands: 1, sampleType: \"FLOAT32\" }\n  };\n}\nfunction evaluatePixel(sample) {\n  return [sample.S8];\n}",
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
  --output slstr_sst.tiff
