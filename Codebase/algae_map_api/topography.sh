curl -X POST https://services.sentinel-hub.com/api/v1/process \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3NjE0NDQ1MzgsImlhdCI6MTc2MTQ0MDkzOCwianRpIjoiNTY1N2M4MWMtNmExNi00YTczLTkzNjgtZjcyY2JiOTk3MDA0IiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJhdWQiOiJodHRwczovL2FwaS5wbGFuZXQuY29tLyIsInN1YiI6ImYyNmM1NWM4LTU3NTgtNGJkYy1iYWZkLTE0YWQzNjMxYzE1NiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImE4MGU2MWQxLTNiNTQtNDRkYi05NzNmLWM5N2I4M2NmOThmMCIsInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjEzNC4xOTAuMjUxLjE1NyIsInBsX3Byb2plY3QiOiI2YTAxYzZhMy0xNjM5LTRmNWMtYTEzNi05ZTM1ZTVmOThlZGQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtYTgwZTYxZDEtM2I1NC00NGRiLTk3M2YtYzk3YjgzY2Y5OGYwIiwiY2xpZW50QWRkcmVzcyI6IjEzNC4xOTAuMjUxLjE1NyIsImNsaWVudF9pZCI6ImE4MGU2MWQxLTNiNTQtNDRkYi05NzNmLWM5N2I4M2NmOThmMCIsImFjY291bnQiOiI2YTAxYzZhMy0xNjM5LTRmNWMtYTEzNi05ZTM1ZTVmOThlZGQiLCJwbF93b3Jrc3BhY2UiOiJkZGU2MDVlYi1lMGQ3LTQwMWEtYTM3ZC1lYTA5NmYxNDhiNzgifQ.Ms97teOVUhWct1BQtkFD4egqkkr-pCN_G6dnvLOL1S8oeEAYJn6vAFy6MWTOQOqHZLqlka-Pcj3KGaySABWswhi8DP-KmV65p9SFCB40Yye_EV8ylwtRodsX_VoJMOt1ldAnb5h2GZB-Jx7AgJ6BkRuu4_7PxYWj_cX-9lxYb1VmeQ8uKoLcNJP8G9wLrKc1IqXvkITjs5QwPT3sAjFH7T9zEno_i4pPylzu5z8xKDNljuHPuO_mseKP1BgulTY4h1pJxlUIyFA4HnnVeUotHxCdj1lGBzBgFTwhyPlR7EwhDTulQr_2wUbtnDSeCCN_AZ6WliWaWKqNNQuRIgQc5w" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "bounds": {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428]
      },
      "data": [{
        "type": "DEM",
        "dataFilter": {
          "demInstance": "COPERNICUS_30"
        }
      }]
    },
    "output": {
      "width": 1000,
      "height": 1000,
      "responses": [{
        "identifier": "default",
        "format": { "type": "image/tiff" }
      }]
    },
    "evalscript": "//VERSION=3\nfunction setup() {\n  return {\n    input: [\"DEM\"],\n    output: { bands: 1, sampleType: \"FLOAT32\" }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  return [sample.DEM];\n}"
  }' -o elevation.tif
