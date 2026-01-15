# Fix: Linux Compatibility Issue

## Problem
The error `module 'os' has no attribute 'add_dll_directory'` occurs because:
- Dependencies were built on Windows
- Lambda runs on Linux (Amazon Linux 2)
- Windows-built packages don't work on Linux

## Solution: Rebuild Layer for Linux

You have 3 options:

---

## Option 1: Use AWS SAM Build (Recommended - Easiest)

AWS SAM automatically builds Linux-compatible packages.

### Steps:

1. **Install AWS SAM CLI** (if not installed):
   ```bash
   # Windows (Chocolatey)
   choco install aws-sam-cli
   ```

2. **Build using SAM:**
   ```bash
   cd lambda/parquet_to_rds
   sam build
   ```

3. **Deploy:**
   ```bash
   sam deploy --guided
   ```

SAM will automatically:
- Build Linux-compatible packages
- Create the layer correctly
- Deploy everything

---

## Option 2: Use Docker (If you have Docker Desktop)

1. **Make sure Docker Desktop is running**

2. **Run the build script:**
   ```powershell
   .\build_layer_linux.ps1
   ```

3. **Upload the new layer:**
   - Upload `lambda-layer-linux.zip` to S3
   - Create new layer version in Lambda
   - Attach to your function

---

## Option 3: Use EC2 Linux Instance (Most Reliable)

1. **Launch an EC2 instance:**
   - AMI: Amazon Linux 2
   - Instance type: t2.micro (free tier)
   - Region: ap-south-1

2. **SSH into the instance:**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install Python and pip:**
   ```bash
   sudo yum update -y
   sudo yum install python3.11 python3.11-pip -y
   ```

4. **Build the layer:**
   ```bash
   mkdir -p layer/python/lib/python3.11/site-packages
   pip3.11 install pandas==2.1.4 pyarrow==14.0.2 psycopg2-binary==2.9.9 -t layer/python/lib/python3.11/site-packages/
   cd layer
   zip -r ../lambda-layer-linux.zip .
   ```

5. **Download the ZIP:**
   ```bash
   # From your local machine, use SCP:
   scp -i your-key.pem ec2-user@your-instance-ip:~/lambda-layer-linux.zip .
   ```

---

## Option 4: Use Pre-built Public Layers (Quick Fix)

Use publicly available layers for pandas and pyarrow:

1. **Add these layers to your function:**
   - Layer 1: `arn:aws:lambda:ap-south-1:336392948345:layer:AWSSDKPandas-Python311:2`
     (AWS Data Wrangler layer - includes pandas, pyarrow)
   - Layer 2: Create custom layer for psycopg2 only (much smaller)

2. **Create small layer for psycopg2 only:**
   ```bash
   # On Linux/EC2:
   mkdir -p layer/python/lib/python3.11/site-packages
   pip3.11 install psycopg2-binary==2.9.9 -t layer/python/lib/python3.11/site-packages/
   zip -r psycopg2-layer.zip layer/
   ```

---

## Quick Fix: Use AWS Data Wrangler Layer

This is the fastest solution:

1. **Go to Lambda → Your Function → Layers**

2. **Remove the current layer**

3. **Add AWS Data Wrangler Layer:**
   - Click "Add a layer"
   - Select "Specify an ARN"
   - Enter: `arn:aws:lambda:ap-south-1:336392948345:layer:AWSSDKPandas-Python311:2`
   - Click "Add"

4. **Create small layer for psycopg2:**
   - Use Option 3 (EC2) or Option 2 (Docker) to build just psycopg2
   - Or use this smaller requirements:
     ```
     psycopg2-binary==2.9.9
     ```
   - This will be much smaller (~5-10 MB)

---

## Recommended: Use AWS SAM

The easiest and most reliable method is to use AWS SAM:

```bash
# Install SAM CLI
choco install aws-sam-cli

# Build (automatically creates Linux-compatible packages)
cd lambda/parquet_to_rds
sam build

# Deploy
sam deploy --guided
```

This handles everything automatically!

---

## After Fixing

1. Update the layer in your Lambda function
2. Test again
3. Should work without the `add_dll_directory` error







