# ✅ Solution: File Too Large (50 MB Limit)

Your original ZIP was **82.73 MB**, which exceeds Lambda's 50 MB direct upload limit.

## ✅ Solution: Use Lambda Layers

I've created **two smaller packages**:

1. **`lambda-function.zip`** - **2.98 KB** ✅ (Your code only)
2. **`lambda-layer.zip`** - **65.98 MB** (Dependencies - upload via S3)

---

## 🚀 Quick Deployment Steps

### Step 1: Upload Layer to S3 (Required - Layer is 65.98 MB)

```bash
# Upload layer to S3
aws s3 cp lambda-layer.zip s3://your-bucket-name/lambda-layers/lambda-layer.zip
```

**Or via AWS Console:**
1. Go to S3 → Your bucket
2. Create folder: `lambda-layers/`
3. Upload `lambda-layer.zip`

### Step 2: Create Lambda Layer

**Option A: AWS Console**
1. Go to Lambda → **Layers** → **Create layer**
2. **Name:** `parquet-to-rds-dependencies`
3. **Upload from S3:** `s3://your-bucket-name/lambda-layers/lambda-layer.zip`
4. **Compatible runtimes:** `Python 3.11`
5. Click **Create**
6. **Copy the Layer ARN** (you'll need it)

**Option B: AWS CLI**
```bash
aws lambda publish-layer-version \
  --layer-name parquet-to-rds-dependencies \
  --content S3Bucket=your-bucket-name,S3Key=lambda-layers/lambda-layer.zip \
  --compatible-runtimes python3.11
```

### Step 3: Create Lambda Function

1. **Go to Lambda Console** → **Create function**
2. **Name:** `parquet-to-rds-processor`
3. **Runtime:** `Python 3.11`
4. **Upload code:** `lambda-function.zip` (only 2.98 KB - uploads directly!)
5. **Add Layer:**
   - Scroll to **Layers** section
   - Click **Add a layer**
   - Select: `parquet-to-rds-dependencies`
   - Select latest version
   - Click **Add**

### Step 4: Configure Function

1. **Timeout:** 15 minutes
2. **Memory:** 1024 MB
3. **Environment Variables:**
   ```
   DB_HOST = database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com
   DB_PORT = 5432
   DB_NAME = audit_trail_db
   DB_USER = postgres
   DB_PASSWORD = Dashboard6287
   TABLE_NAME = audit_trail_data
   ```
4. **IAM Permissions:** S3 read, CloudWatch logs
5. **VPC:** Configure if RDS is in VPC
6. **S3 Trigger:** Add trigger for parquet files

---

## 📦 Files Ready

✅ **`lambda-function.zip`** (2.98 KB) - Upload directly to Lambda  
✅ **`lambda-layer.zip`** (65.98 MB) - Upload to S3, then create Layer

---

## 🔄 Alternative: Upload Large ZIP via S3

If you prefer to use the original large ZIP:

```bash
# Upload to S3
aws s3 cp parquet-to-rds.zip s3://your-bucket-name/lambda-deployments/parquet-to-rds.zip
```

Then in Lambda Console:
1. Create function
2. **Actions** → **Upload a file from Amazon S3**
3. Enter: `s3://your-bucket-name/lambda-deployments/parquet-to-rds.zip`

---

## ✅ Recommended: Use Layers

**Why Layers?**
- ✅ Function code is tiny (2.98 KB) - fast uploads
- ✅ Easy to update function without re-uploading dependencies
- ✅ Can reuse layer for multiple functions
- ✅ Better separation of concerns

**Files:**
- `lambda-function.zip` → Upload to Lambda directly
- `lambda-layer.zip` → Upload to S3, create Layer, attach to function

---

## 📋 Checklist

- [ ] Upload `lambda-layer.zip` to S3
- [ ] Create Lambda Layer from S3
- [ ] Create Lambda Function
- [ ] Upload `lambda-function.zip` to function
- [ ] Attach Layer to function
- [ ] Configure environment variables
- [ ] Add S3 trigger
- [ ] Test!

---

**See `DEPLOY_WITH_LAYERS.md` for detailed instructions.**







