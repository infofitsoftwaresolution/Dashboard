# Deploy Lambda with Layers (For Large Packages)

Since your deployment package exceeds 50 MB, we'll use **Lambda Layers** to handle the dependencies.

## Solution: Lambda Layers

- **Lambda Function ZIP:** Small (< 1 MB) - Contains only your code
- **Lambda Layer ZIP:** Large (~80 MB) - Contains dependencies (pandas, pyarrow, psycopg2)
- Lambda Layers can be up to **250 MB unzipped** (50 MB zipped per layer)

---

## Step 1: Build the Packages

### Option A: Use Pre-built Scripts (Recommended)

```powershell
# Build Lambda Layer (dependencies)
.\build_layer.ps1

# Build Lambda Function (code only)
.\build_function_only.ps1
```

### Option B: Manual Build

**Build Layer:**
```powershell
mkdir layer\python\lib\python3.11\site-packages -Force
python -m pip install pandas==2.1.4 pyarrow==14.0.2 psycopg2-binary==2.9.9 -t layer\python\lib\python3.11\site-packages
Compress-Archive -Path layer\* -DestinationPath lambda-layer.zip -Force
```

**Build Function:**
```powershell
mkdir function-package
copy lambda_function.py function-package\
Compress-Archive -Path function-package\* -DestinationPath lambda-function.zip -Force
```

---

## Step 2: Create Lambda Layer

### 2.1: Upload Layer to S3 (Required for layers > 50 MB)

1. **Upload layer ZIP to S3:**
   ```bash
   aws s3 cp lambda-layer.zip s3://your-bucket-name/lambda-layers/lambda-layer.zip
   ```

   Or use AWS Console:
   - Go to S3 → Your bucket
   - Create folder: `lambda-layers/`
   - Upload `lambda-layer.zip`

### 2.2: Create Lambda Layer

**Option A: Using AWS Console**

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Click **"Layers"** in left sidebar
3. Click **"Create layer"**
4. Configure:
   - **Name:** `parquet-to-rds-dependencies`
   - **Upload a .zip file:** (if < 50 MB) OR
   - **Upload from Amazon S3:** `s3://your-bucket-name/lambda-layers/lambda-layer.zip`
   - **Compatible runtimes:** Select `Python 3.11`
5. Click **"Create"**
6. **Note the Layer ARN** (you'll need it in Step 3)

**Option B: Using AWS CLI**

```bash
aws lambda publish-layer-version \
  --layer-name parquet-to-rds-dependencies \
  --description "Dependencies for parquet-to-rds Lambda (pandas, pyarrow, psycopg2)" \
  --zip-file fileb://lambda-layer.zip \
  --compatible-runtimes python3.11
```

Or from S3:
```bash
aws lambda publish-layer-version \
  --layer-name parquet-to-rds-dependencies \
  --description "Dependencies for parquet-to-rds Lambda" \
  --content S3Bucket=your-bucket-name,S3Key=lambda-layers/lambda-layer.zip \
  --compatible-runtimes python3.11
```

---

## Step 3: Create Lambda Function

### 3.1: Create Function

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Click **"Create function"**
3. Configure:
   - **Author from scratch**
   - **Function name:** `parquet-to-rds-processor`
   - **Runtime:** `Python 3.11`
   - **Architecture:** `x86_64`
4. Click **"Create function"**

### 3.2: Upload Function Code

1. Scroll to **"Code source"**
2. Click **"Upload from"** → **".zip file"**
3. Upload: `lambda-function.zip` (this is small, < 1 MB)
4. Click **"Save"**

### 3.3: Attach Lambda Layer

1. Scroll down to **"Layers"** section
2. Click **"Add a layer"**
3. Select **"Custom layers"**
4. Choose: `parquet-to-rds-dependencies`
5. Select the latest version
6. Click **"Add"**

### 3.4: Configure Function Settings

1. Click **"Configuration"** tab
2. **General configuration:**
   - Timeout: `15 min 0 sec`
   - Memory: `1024 MB`
3. **Environment variables:**
   - `DB_HOST` = `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
   - `DB_PORT` = `5432`
   - `DB_NAME` = `audit_trail_db`
   - `DB_USER` = `postgres`
   - `DB_PASSWORD` = `Dashboard6287`
   - `TABLE_NAME` = `audit_trail_data`

### 3.5: Configure IAM Permissions

1. **Configuration** → **Permissions**
2. Click on Execution role
3. Attach policies:
   - `AmazonS3ReadOnlyAccess`
   - `CloudWatchLogsFullAccess`
   - `AWSLambdaVPCAccessExecutionRole` (if RDS in VPC)

### 3.6: Configure VPC (If RDS is in VPC)

1. **Configuration** → **VPC**
2. Select same VPC as RDS
3. Select 2 subnets
4. Select security group
5. Update RDS security group to allow Lambda

### 3.7: Add S3 Trigger

1. **Configuration** → **Triggers**
2. **Add trigger:**
   - Source: `S3`
   - Bucket: Your bucket
   - Event: `All object create events`
   - Prefix: `audit-trail-data/raw/`
   - Suffix: `.parquet`

---

## Step 4: Test

1. Upload test parquet file to S3
2. Check CloudWatch Logs
3. Verify data in PostgreSQL

---

## Alternative: Upload Large ZIP via S3

If you prefer to use the original large ZIP file:

### Step 1: Upload to S3

```bash
aws s3 cp parquet-to-rds.zip s3://your-bucket-name/lambda-deployments/parquet-to-rds.zip
```

### Step 2: Create Function with S3 Code

**Using AWS CLI:**
```bash
aws lambda create-function \
  --function-name parquet-to-rds-processor \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --code S3Bucket=your-bucket-name,S3Key=lambda-deployments/parquet-to-rds.zip \
  --handler lambda_function.lambda_handler \
  --timeout 900 \
  --memory-size 1024
```

**Using AWS Console:**
1. Create function (without uploading code)
2. Go to **Code** tab
3. Click **"Actions"** → **"Upload a file from Amazon S3"**
4. Enter S3 URL: `s3://your-bucket-name/lambda-deployments/parquet-to-rds.zip`
5. Click **"Save"**

---

## Summary

**Recommended Approach: Lambda Layers**
- ✅ Function code: `lambda-function.zip` (< 1 MB) - Upload directly
- ✅ Dependencies: `lambda-layer.zip` (~80 MB) - Upload as Layer
- ✅ Attach layer to function
- ✅ Easier to update function code (smaller uploads)

**Alternative: S3 Upload**
- Upload large ZIP to S3 first
- Reference S3 location when creating/updating function

---

## Quick Commands

```powershell
# Build packages
.\build_layer.ps1
.\build_function_only.ps1

# Upload layer to S3
aws s3 cp lambda-layer.zip s3://your-bucket-name/lambda-layers/

# Create layer
aws lambda publish-layer-version --layer-name parquet-to-rds-dependencies --zip-file fileb://lambda-layer.zip --compatible-runtimes python3.11
```

---

## Troubleshooting

**Layer not found:**
- Verify layer name matches
- Check layer version is selected
- Ensure compatible runtime (Python 3.11)

**Import errors:**
- Verify layer is attached
- Check layer contains dependencies in correct path: `python/lib/python3.11/site-packages/`
- Test locally with same structure

**Size still too large:**
- Use S3 upload method
- Or split into multiple layers (max 5 layers per function)







