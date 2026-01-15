#!/bin/bash
# Bash script to build Lambda deployment package
# Run this script to create parquet-to-rds.zip ready for Lambda upload

echo "Building Lambda deployment package..."

# Clean up previous builds
if [ -d "package" ]; then
    echo "Cleaning up previous package directory..."
    rm -rf package
fi

if [ -f "parquet-to-rds.zip" ]; then
    echo "Removing old ZIP file..."
    rm -f parquet-to-rds.zip
fi

# Create package directory
echo "Creating package directory..."
mkdir -p package

# Copy Lambda function
echo "Copying Lambda function..."
cp lambda_function.py package/

# Install dependencies
echo "Installing Python dependencies..."
echo "This may take a few minutes..."

# Check Python version
python3 --version

# Install dependencies into package directory
python3 -m pip install -r requirements.txt -t package/ --quiet

# Create ZIP file
echo "Creating ZIP file..."
cd package
zip -r ../parquet-to-rds.zip . -q
cd ..

# Get file size
ZIP_SIZE=$(du -h parquet-to-rds.zip | cut -f1)
echo ""
echo "Package created successfully!"
echo "File: parquet-to-rds.zip"
echo "Size: $ZIP_SIZE"
echo ""
echo "Ready to upload to AWS Lambda!"







