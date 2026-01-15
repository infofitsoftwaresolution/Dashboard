# PowerShell script to build Lambda function package (code only, no dependencies)
# This will be small enough to upload directly (< 50 MB)

Write-Host "Building Lambda function package (code only)..." -ForegroundColor Green

# Clean up previous builds
if (Test-Path "function-package") {
    Write-Host "Cleaning up previous function package directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "function-package"
}

if (Test-Path "lambda-function.zip") {
    Write-Host "Removing old function ZIP file..." -ForegroundColor Yellow
    Remove-Item -Force "lambda-function.zip"
}

# Create function package directory
Write-Host "Creating function package directory..." -ForegroundColor Green
New-Item -ItemType Directory -Path "function-package" | Out-Null

# Copy only Lambda function (boto3 is already in Lambda runtime)
Write-Host "Copying Lambda function..." -ForegroundColor Green
Copy-Item "lambda_function.py" -Destination "function-package\"

# Create ZIP file
Write-Host "Creating ZIP file..." -ForegroundColor Green
Compress-Archive -Path "function-package\*" -DestinationPath "lambda-function.zip" -Force

# Get file size
$zipSize = (Get-Item "lambda-function.zip").Length / 1MB
Write-Host "`nFunction package created successfully!" -ForegroundColor Green
Write-Host "File: lambda-function.zip" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor Cyan
Write-Host "`nReady to upload to Lambda (will use Layer for dependencies)!" -ForegroundColor Green







