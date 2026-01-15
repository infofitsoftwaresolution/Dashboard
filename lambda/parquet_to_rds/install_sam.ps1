# Install AWS SAM CLI using Chocolatey
# If you don't have Chocolatey, install it first: https://chocolatey.org/install

Write-Host "Installing AWS SAM CLI..." -ForegroundColor Green

# Check if Chocolatey is installed
$chocoInstalled = Get-Command choco -ErrorAction SilentlyContinue

if (-not $chocoInstalled) {
    Write-Host "Chocolatey not found. Installing Chocolatey first..." -ForegroundColor Yellow
    Write-Host "Run PowerShell as Administrator and execute:" -ForegroundColor Yellow
    Write-Host 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))' -ForegroundColor Cyan
    Write-Host "`nOr download SAM CLI manually from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html" -ForegroundColor Yellow
} else {
    Write-Host "Installing AWS SAM CLI via Chocolatey..." -ForegroundColor Green
    choco install aws-sam-cli -y
    Write-Host "`nSAM CLI installed! Restart your terminal and run: sam --version" -ForegroundColor Green
}







