@echo off
REM Batch script to build Lambda deployment package for Windows
REM Run this script to create parquet-to-rds.zip ready for Lambda upload

echo Building Lambda deployment package...

REM Clean up previous builds
if exist package (
    echo Cleaning up previous package directory...
    rmdir /s /q package
)

if exist parquet-to-rds.zip (
    echo Removing old ZIP file...
    del /f parquet-to-rds.zip
)

REM Create package directory
echo Creating package directory...
mkdir package

REM Copy Lambda function
echo Copying Lambda function...
copy lambda_function.py package\

REM Install dependencies
echo Installing Python dependencies...
echo This may take a few minutes...
python -m pip install -r requirements.txt -t package\ --quiet

if errorlevel 1 (
    echo Error installing dependencies. Trying with pip directly...
    pip install -r requirements.txt -t package\ --quiet
)

REM Create ZIP file using PowerShell
echo Creating ZIP file...
powershell -Command "Compress-Archive -Path 'package\*' -DestinationPath 'parquet-to-rds.zip' -Force"

echo.
echo Package created successfully!
echo File: parquet-to-rds.zip
echo.
echo Ready to upload to AWS Lambda!
pause







