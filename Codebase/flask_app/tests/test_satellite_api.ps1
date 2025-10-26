# PowerShell Test script for Satellite API endpoints
# Run this script to test all endpoints using Invoke-RestMethod and Invoke-WebRequest

param(
    [string]$BaseUrl = "http://127.0.0.1:5000",
    [string]$OutputDir = "test_outputs"
)

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Write-Host "🛰️ Testing Satellite API Endpoints" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "`n1️⃣ Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$BaseUrl/health" -Method GET
    Write-Host "✅ Health check passed" -ForegroundColor Green
    $healthResponse | ConvertTo-Json | Write-Host
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Satellite Info
Write-Host "`n2️⃣ Testing Satellite Info..." -ForegroundColor Yellow
try {
    $infoResponse = Invoke-RestMethod -Uri "$BaseUrl/api/satellite/info" -Method GET
    Write-Host "✅ Satellite info retrieved" -ForegroundColor Green
    $infoResponse | ConvertTo-Json | Write-Host
} catch {
    Write-Host "❌ Satellite info failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Lake Winnipeg Imagery
Write-Host "`n3️⃣ Downloading Lake Winnipeg Imagery..." -ForegroundColor Yellow
try {
    $lakeOutputFile = Join-Path $OutputDir "lake_winnipeg.tif"
    Invoke-WebRequest -Uri "$BaseUrl/api/satellite/lake-winnipeg" -OutFile $lakeOutputFile
    $fileInfo = Get-Item $lakeOutputFile
    Write-Host "✅ Lake Winnipeg imagery saved to $lakeOutputFile" -ForegroundColor Green
    Write-Host "   File size: $($fileInfo.Length) bytes" -ForegroundColor Gray
} catch {
    Write-Host "❌ Lake Winnipeg imagery download failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Custom Satellite Fetch
Write-Host "`n4️⃣ Testing Custom Satellite Fetch..." -ForegroundColor Yellow
try {
    $customPayload = @{
        bbox = @(-101.273432, 50.075155, -96.060934, 54.171428)
        start_date = "2022-08-01T10:00:00Z"
        end_date = "2022-08-31T22:00:00Z"
    } | ConvertTo-Json

    $customOutputFile = Join-Path $OutputDir "custom_satellite.tif"
    
    Invoke-WebRequest -Uri "$BaseUrl/api/satellite/fetch" `
        -Method POST `
        -ContentType "application/json" `
        -Body $customPayload `
        -OutFile $customOutputFile
    
    $fileInfo = Get-Item $customOutputFile
    Write-Host "✅ Custom satellite imagery saved to $customOutputFile" -ForegroundColor Green
    Write-Host "   File size: $($fileInfo.Length) bytes" -ForegroundColor Gray
} catch {
    Write-Host "❌ Custom satellite imagery download failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Error Handling - Missing Fields
Write-Host "`n5️⃣ Testing Error Handling (Missing Fields)..." -ForegroundColor Yellow
try {
    $invalidPayload = @{
        bbox = @(-101.273432, 50.075155, -96.060934, 54.171428)
    } | ConvertTo-Json

    $errorResponse = Invoke-RestMethod -Uri "$BaseUrl/api/satellite/fetch" `
        -Method POST `
        -ContentType "application/json" `
        -Body $invalidPayload
    
    Write-Host "❌ Expected error but got success: $($errorResponse | ConvertTo-Json)" -ForegroundColor Red
} catch {
    $errorDetails = $_.Exception.Response
    if ($errorDetails.StatusCode -eq 400) {
        Write-Host "✅ Correctly returned 400 Bad Request for missing fields" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Unexpected error status: $($errorDetails.StatusCode)" -ForegroundColor Yellow
    }
    
    # Try to get error message
    try {
        $errorStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorStream)
        $errorBody = $reader.ReadToEnd()
        Write-Host "   Error response: $errorBody" -ForegroundColor Gray
    } catch {
        Write-Host "   Could not read error response" -ForegroundColor Gray
    }
}

# Test 6: Error Handling - Invalid JSON
Write-Host "`n6️⃣ Testing Error Handling (Invalid JSON)..." -ForegroundColor Yellow
try {
    Invoke-RestMethod -Uri "$BaseUrl/api/satellite/fetch" `
        -Method POST `
        -ContentType "application/json" `
        -Body "invalid json"
    
    Write-Host "❌ Expected error but got success" -ForegroundColor Red
} catch {
    $errorDetails = $_.Exception.Response
    if ($errorDetails.StatusCode -eq 400) {
        Write-Host "✅ Correctly returned 400 Bad Request for invalid JSON" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Unexpected error status: $($errorDetails.StatusCode)" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "`n🏁 Test completed!" -ForegroundColor Cyan
Write-Host "Output files saved in: $OutputDir" -ForegroundColor Gray

if (Test-Path $OutputDir) {
    Get-ChildItem $OutputDir | Format-Table Name, Length, LastWriteTime
}

Write-Host "`n📋 Test Summary:" -ForegroundColor Cyan
Write-Host "- Health Check: Test basic API connectivity" -ForegroundColor Gray
Write-Host "- Satellite Info: Get API capabilities and supported formats" -ForegroundColor Gray
Write-Host "- Lake Winnipeg: Download preset imagery (matches original curl)" -ForegroundColor Gray
Write-Host "- Custom Fetch: Download imagery with custom parameters" -ForegroundColor Gray
Write-Host "- Error Tests: Verify proper error handling" -ForegroundColor Gray