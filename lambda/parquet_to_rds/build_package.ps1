# PowerShell script to build Lambda deployment package
# Run this script to create parquet-to-rds.zip ready for Lambda upload

Write-Host "Building Lambda deployment package..." -ForegroundColor Green

# Clean up previous builds
if (Test-Path "package") {
    Write-Host "Cleaning up previous package directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "package"
}

if (Test-Path "parquet-to-rds.zip") {
    Write-Host "Removing old ZIP file..." -ForegroundColor Yellow
    Remove-Item -Force "parquet-to-rds.zip"
}

# Create package directory
Write-Host "Creating package directory..." -ForegroundColor Green
New-Item -ItemType Directory -Path "package" | Out-Null

# Copy Lambda function
Write-Host "Copying Lambda function..." -ForegroundColor Green
Copy-Item "lambda_function.py" -Destination "package\"

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "Using: $pythonVersion" -ForegroundColor Cyan

# Install dependencies into package directory
python -m pip install -r requirements.txt -t package\ --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing dependencies. Trying with pip directly..." -ForegroundColor Red
    pip install -r requirements.txt -t package\ --quiet
}

# Create ZIP file
Write-Host "Creating ZIP file..." -ForegroundColor Green
Compress-Archive -Path "package\*" -DestinationPath "parquet-to-rds.zip" -Force

# Get file size
$zipSize = (Get-Item "parquet-to-rds.zip").Length / 1MB
Write-Host "`nPackage created successfully!" -ForegroundColor Green
Write-Host "File: parquet-to-rds.zip" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
Write-Host "`nReady to upload to AWS Lambda!" -ForegroundColor Green







