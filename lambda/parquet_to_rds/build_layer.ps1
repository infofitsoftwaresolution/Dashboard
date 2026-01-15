# PowerShell script to build Lambda Layer with dependencies
# Lambda Layers can be up to 250 MB (unzipped)

Write-Host "Building Lambda Layer package..." -ForegroundColor Green

# Clean up previous builds
if (Test-Path "layer") {
    Write-Host "Cleaning up previous layer directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "layer"
}

if (Test-Path "lambda-layer.zip") {
    Write-Host "Removing old layer ZIP file..." -ForegroundColor Yellow
    Remove-Item -Force "lambda-layer.zip"
}

# Create layer directory structure (python/lib/python3.11/site-packages)
Write-Host "Creating layer directory structure..." -ForegroundColor Green
$layerPath = "layer\python\lib\python3.11\site-packages"
New-Item -ItemType Directory -Path $layerPath -Force | Out-Null

# Install dependencies into layer directory
Write-Host "Installing Python dependencies into layer..." -ForegroundColor Green
Write-Host "This may take a few minutes..." -ForegroundColor Yellow

python -m pip install pandas==2.1.4 pyarrow==14.0.2 psycopg2-binary==2.9.9 -t $layerPath --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing dependencies. Trying with pip directly..." -ForegroundColor Red
    pip install pandas==2.1.4 pyarrow==14.0.2 psycopg2-binary==2.9.9 -t $layerPath --quiet
}

# Create ZIP file for layer
Write-Host "Creating layer ZIP file..." -ForegroundColor Green
Compress-Archive -Path "layer\*" -DestinationPath "lambda-layer.zip" -Force

# Get file size
$zipSize = (Get-Item "lambda-layer.zip").Length / 1MB
Write-Host "`nLayer package created successfully!" -ForegroundColor Green
Write-Host "File: lambda-layer.zip" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
Write-Host "`nReady to upload as Lambda Layer!" -ForegroundColor Green







