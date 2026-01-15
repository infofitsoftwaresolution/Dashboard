# PowerShell script to build Lambda Layer for Linux (Lambda environment)
# This uses Docker to build Linux-compatible packages

Write-Host "Building Lambda Layer for Linux environment..." -ForegroundColor Green
Write-Host "This requires Docker to be installed and running" -ForegroundColor Yellow

# Check if Docker is available
$dockerAvailable = $false
try {
    docker --version | Out-Null
    $dockerAvailable = $true
} catch {
    Write-Host "Docker not found. Please install Docker Desktop." -ForegroundColor Red
    Write-Host "Alternative: Use AWS SAM build or EC2 Linux instance" -ForegroundColor Yellow
}

if (-not $dockerAvailable) {
    Write-Host "`nSkipping Docker build. Use alternative method below." -ForegroundColor Yellow
    exit 1
}

# Clean up previous builds
if (Test-Path "layer-linux") {
    Write-Host "Cleaning up previous layer directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "layer-linux"
}

if (Test-Path "lambda-layer-linux.zip") {
    Write-Host "Removing old layer ZIP file..." -ForegroundColor Yellow
    Remove-Item -Force "lambda-layer-linux.zip"
}

# Create layer directory structure
Write-Host "Creating layer directory structure..." -ForegroundColor Green
$layerPath = "layer-linux\python\lib\python3.11\site-packages"
New-Item -ItemType Directory -Path $layerPath -Force | Out-Null

# Use Docker to install Linux-compatible packages
Write-Host "Installing Linux-compatible packages using Docker..." -ForegroundColor Green
Write-Host "This may take 5-10 minutes..." -ForegroundColor Yellow

# Create requirements file
$requirements = @"
pandas==2.1.4
pyarrow==14.0.2
psycopg2-binary==2.9.9
"@
$requirements | Out-File -FilePath "requirements-layer.txt" -Encoding utf8

# Build using Docker (Amazon Linux 2 - matches Lambda runtime)
docker run --rm -v "${PWD}:/var/task" -w /var/task public.ecr.aws/lambda/python:3.11 pip install -r requirements-layer.txt -t layer-linux/python/lib/python3.11/site-packages/

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed. Trying alternative method..." -ForegroundColor Red
    Write-Host "Please use AWS SAM build or EC2 Linux instance" -ForegroundColor Yellow
    exit 1
}

# Create ZIP file for layer
Write-Host "Creating layer ZIP file..." -ForegroundColor Green
Compress-Archive -Path "layer-linux\*" -DestinationPath "lambda-layer-linux.zip" -Force

# Get file size
$zipSize = (Get-Item "lambda-layer-linux.zip").Length / 1MB
Write-Host "`nLayer package created successfully!" -ForegroundColor Green
Write-Host "File: lambda-layer-linux.zip" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
Write-Host "`nReady to upload as Lambda Layer!" -ForegroundColor Green







