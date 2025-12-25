# PowerShell script to help configure AWS credentials
# Run this script to set up your .env file interactively

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AWS Credentials Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$envFile = ".env"

# Check if .env exists, if not copy from env.example
if (-not (Test-Path $envFile)) {
    if (Test-Path "env.example") {
        Copy-Item "env.example" $envFile
        Write-Host "✅ Created .env file from env.example" -ForegroundColor Green
    } else {
        Write-Host "❌ env.example not found" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Please enter your AWS credentials:" -ForegroundColor Yellow
Write-Host ""

# Get AWS Access Key ID
$accessKey = Read-Host "AWS Access Key ID"
if ([string]::IsNullOrWhiteSpace($accessKey)) {
    Write-Host "❌ Access Key ID cannot be empty" -ForegroundColor Red
    exit 1
}

# Get AWS Secret Access Key
$secretKey = Read-Host "AWS Secret Access Key" -AsSecureString
$secretKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretKey)
)
if ([string]::IsNullOrWhiteSpace($secretKeyPlain)) {
    Write-Host "❌ Secret Access Key cannot be empty" -ForegroundColor Red
    exit 1
}

# Get AWS Region (with default)
$region = Read-Host "AWS Region (default: us-east-1)"
if ([string]::IsNullOrWhiteSpace($region)) {
    $region = "us-east-1"
}

Write-Host ""
Write-Host "Updating .env file..." -ForegroundColor Yellow

# Read current .env file
$envContent = Get-Content $envFile -Raw

# Update AWS credentials
$envContent = $envContent -replace "AWS_ACCESS_KEY_ID=.*", "AWS_ACCESS_KEY_ID=$accessKey"
$envContent = $envContent -replace "AWS_SECRET_ACCESS_KEY=.*", "AWS_SECRET_ACCESS_KEY=$secretKeyPlain"
$envContent = $envContent -replace "AWS_REGION=.*", "AWS_REGION=$region"

# Ensure S3 and Athena configs are set
if ($envContent -notmatch "S3_BUCKET_NAME=") {
    $envContent += "`nS3_BUCKET_NAME=athena-data-bucket-data`n"
}
if ($envContent -notmatch "ATHENA_DATABASE_NAME=") {
    $envContent += "`nATHENA_DATABASE_NAME=audit_trail_db`n"
}

# Write back to file
Set-Content -Path $envFile -Value $envContent -NoNewline

Write-Host "✅ .env file updated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: python test_aws_credentials.py" -ForegroundColor White
Write-Host "2. If test passes, restart your backend server" -ForegroundColor White
Write-Host ""

