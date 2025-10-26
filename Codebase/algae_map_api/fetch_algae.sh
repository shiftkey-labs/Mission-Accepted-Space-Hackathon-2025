curl -X POST https://services.sentinel-hub.com/api/v1/process \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3NjE0MjMyNjgsImlhdCI6MTc2MTQxOTY2OCwianRpIjoiM2NiMDNhZGYtN2Y0Yi00ZGNjLTkyZGItODYzYjEyYWU4NzI2IiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJhdWQiOiJodHRwczovL2FwaS5wbGFuZXQuY29tLyIsInN1YiI6ImYyNmM1NWM4LTU3NTgtNGJkYy1iYWZkLTE0YWQzNjMxYzE1NiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImE4MGU2MWQxLTNiNTQtNDRkYi05NzNmLWM5N2I4M2NmOThmMCIsInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjEzNC4xOTAuMjUxLjE1NyIsInBsX3Byb2plY3QiOiI2YTAxYzZhMy0xNjM5LTRmNWMtYTEzNi05ZTM1ZTVmOThlZGQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQtYTgwZTYxZDEtM2I1NC00NGRiLTk3M2YtYzk3YjgzY2Y5OGYwIiwiY2xpZW50QWRkcmVzcyI6IjEzNC4xOTAuMjUxLjE1NyIsImNsaWVudF9pZCI6ImE4MGU2MWQxLTNiNTQtNDRkYi05NzNmLWM5N2I4M2NmOThmMCIsImFjY291bnQiOiI2YTAxYzZhMy0xNjM5LTRmNWMtYTEzNi05ZTM1ZTVmOThlZGQiLCJwbF93b3Jrc3BhY2UiOiJkZGU2MDVlYi1lMGQ3LTQwMWEtYTM3ZC1lYTA5NmYxNDhiNzgifQ.bHbvgHaW3JhNq3qeK8jpK4Thb3ibTYvGTf6q4A9SBd_U5mYc21HgsIr-pFIEfqkNlApgj63BHi1com5kvXU7VhWlRdJPnVIQxSFKvzlsiDz1IdrQilf_p9PASS-JfwFUFgT-MlJX5hd-6DEW09ObJIOxxbed2K5vsrLxmyvJGrShzdCJr1awCXNPVkmJZlEtjbpgpxubM85TiikvDMvUR84g8u6qGLWXPHZnoe_u1fWht3t0RZKLJIN9bIAdcRPAw_MDsTFMGglzFIsu2_c2-EZ1VeN14aPIgM9UhA3z1CNNkWcufFEnmJGQRg1IveEZRHtIXf5TbtiaB3my93jAkA" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "bounds": {
        "bbox": [-101.273432, 50.075155, -96.060934, 54.171428]
      },
      "data": [{
        "type": "sentinel-2-l2a",
        "dataFilter": {
                    "timeRange": {
                        "from": "2022-08-01T10:00:00Z",
                        "to": "2022-08-31T22:00:00Z"
                    },
                     "mosaickingOrder": "mostRecent"
                },
        "processing": { "harmonizeValues": true }
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
    "evalscript": "//VERSION=3\nfunction setup() {\n  return {\n    input: [\"B02\", \"B03\", \"B04\", \"B08\", \"B11\", \"B12\", \"dataMask\"],\n    output: { id: \"default\", bands: 6, sampleType: \"FLOAT32\" }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  if (sample.dataMask == 0) return [NaN, NaN, NaN, NaN, NaN, NaN];\n  return [sample.B02, sample.B03, sample.B04, sample.B08, sample.B11, sample.B12];\n}"
  }' -o output.tif
