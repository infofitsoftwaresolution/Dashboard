# Build Linux-compatible Lambda Layer using Docker
Write-Host "Building Linux-compatible Lambda Layer..." -ForegroundColor Green

# Clean up
if (Test-Path "layer-linux") {
    Remove-Item -Recurse -Force "layer-linux"
}
if (Test-Path "lambda-layer-linux.zip") {
    Remove-Item -Force "lambda-layer-linux.zip"
}

# Create directory structure
New-Item -ItemType Directory -Path "layer-linux\python\lib\python3.11\site-packages" -Force | Out-Null

Write-Host "Installing dependencies in Linux container (this will take 5-10 minutes)..." -ForegroundColor Yellow
Write-Host "Please wait, Docker is building Linux-compatible packages..." -ForegroundColor Cyan

# Build using Docker - Lambda Python 3.11 image
docker run --rm `
    --entrypoint="" `
    -v "${PWD}:/var/task" `
    -w /var/task `
    public.ecr.aws/lambda/python:3.11 `
    /var/lang/bin/pip install pandas==2.1.4 pyarrow==14.0.2 psycopg2-binary==2.9.9 -t layer-linux/python/lib/python3.11/site-packages/

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nBuild failed. Please check Docker is running." -ForegroundColor Red
    exit 1
}

Write-Host "`nCreating ZIP file..." -ForegroundColor Green
Compress-Archive -Path "layer-linux\*" -DestinationPath "lambda-layer-linux.zip" -Force

$zipSize = (Get-Item "lambda-layer-linux.zip").Length / 1MB
Write-Host "`n✅ Layer created successfully!" -ForegroundColor Green
Write-Host "File: lambda-layer-linux.zip" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
Write-Host "`nNext: Upload to S3 and create Lambda Layer" -ForegroundColor Yellow



