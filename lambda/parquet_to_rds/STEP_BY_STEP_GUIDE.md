# Step-by-Step Guide: Create and Configure Lambda Function

This guide will walk you through creating and configuring the Lambda function to process parquet files from S3 and save to RDS PostgreSQL.

## Prerequisites

Before starting, ensure you have:
- ✅ AWS Account with appropriate permissions
- ✅ RDS PostgreSQL database running
- ✅ S3 bucket with parquet files
- ✅ AWS CLI installed and configured (`aws configure`)
- ✅ PostgreSQL client (psql) or database management tool

---

## Part 1: Prepare PostgreSQL Database

### Step 1.1: Connect to RDS Database

Open your terminal/command prompt and connect to your RDS PostgreSQL:

```bash
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U your_username -d audit_trail_db
```

**Note:** Replace `your_username` with your actual PostgreSQL username. You'll be prompted for the password.

### Step 1.2: Create the Table

Once connected, run the table creation script:

```sql
-- Copy and paste the contents of create_rds_table.sql
-- Or run it directly:
\i create_rds_table.sql
```

Or manually execute the SQL from `lambda/parquet_to_rds/create_rds_table.sql`.

### Step 1.3: Verify Table Creation

```sql
-- Check if table exists
\dt audit_trail_data

-- Check table structure
\d audit_trail_data

-- Exit psql
\q
```

---

## Part 2: Create Lambda Deployment Package

### Step 2.1: Navigate to Lambda Directory

Open terminal/command prompt and navigate to the Lambda directory:

```bash
cd lambda/parquet_to_rds
```

### Step 2.2: Create Package Directory

```bash
# Windows PowerShell
mkdir package
cd package

# Or Windows CMD
mkdir package
cd package

# Linux/Mac
mkdir -p package
cd package
```

### Step 2.3: Copy Lambda Function

```bash
# Windows
copy ..\lambda_function.py .

# Linux/Mac
cp ../lambda_function.py .
```

### Step 2.4: Install Python Dependencies

**Important:** Use Python 3.11 (same as Lambda runtime)

```bash
# Install dependencies into the package directory
pip install -r ../requirements.txt -t .

# This will install:
# - boto3
# - pandas
# - pyarrow
# - psycopg2-binary
```

**Note:** If you have multiple Python versions, use:
```bash
python3.11 -m pip install -r ../requirements.txt -t .
```

### Step 2.5: Create ZIP File

```bash
# Windows PowerShell
cd ..
Compress-Archive -Path package\* -DestinationPath parquet-to-rds.zip

# Windows CMD (if you have 7-Zip)
cd ..
7z a parquet-to-rds.zip package\*

# Linux/Mac
cd ..
zip -r parquet-to-rds.zip package/
```

**Verify the ZIP file was created:**
```bash
# Windows
dir parquet-to-rds.zip

# Linux/Mac
ls -lh parquet-to-rds.zip
```

---

## Part 3: Create Lambda Function via AWS Console

### Step 3.1: Open AWS Lambda Console

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Make sure you're in the correct region: **ap-south-1** (Mumbai)
3. Click **"Create function"** button (top right)

### Step 3.2: Configure Basic Settings

1. **Author from scratch** (should be selected by default)
2. **Function name:** `parquet-to-rds-processor`
3. **Runtime:** Select `Python 3.11`
4. **Architecture:** `x86_64` (default)
5. Click **"Create function"** button

### Step 3.3: Upload Code

1. Scroll down to **"Code source"** section
2. Click **"Upload from"** dropdown
3. Select **".zip file"**
4. Click **"Upload"** button
5. Select the `parquet-to-rds.zip` file you created
6. Click **"Save"** button
7. Wait for upload to complete (may take 1-2 minutes)

### Step 3.4: Configure Function Settings

1. Click **"Configuration"** tab (top menu)
2. Click **"General configuration"** in left sidebar
3. Click **"Edit"** button
4. Update settings:
   - **Timeout:** Change to `15 min 0 sec` (900 seconds)
   - **Memory:** Change to `1024 MB`
5. Click **"Save"** button

### Step 3.5: Set Environment Variables

1. Still in **"Configuration"** tab
2. Click **"Environment variables"** in left sidebar
3. Click **"Edit"** button
4. Click **"Add environment variable"** for each:

   | Key | Value |
   |-----|-------|
   | `DB_HOST` | `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com` |
   | `DB_PORT` | `5432` |
   | `DB_NAME` | `audit_trail_db` |
   | `DB_USER` | `[Your PostgreSQL username]` |
   | `DB_PASSWORD` | `[Your PostgreSQL password]` |
   | `TABLE_NAME` | `audit_trail_data` |

5. Click **"Save"** button

**Security Note:** The password is stored as plain text. For production, consider using AWS Secrets Manager.

### Step 3.6: Configure IAM Permissions

1. In **"Configuration"** tab
2. Click **"Permissions"** in left sidebar
3. Click on the **Execution role** name (e.g., `parquet-to-rds-processor-role-xxxxx`)
4. This opens IAM Console in a new tab
5. Click **"Add permissions"** → **"Attach policies"**
6. Search and attach:
   - `AmazonS3ReadOnlyAccess` (or create custom policy for your specific bucket)
   - `CloudWatchLogsFullAccess` (or `AWSLambdaBasicExecutionRole`)
7. If RDS is in VPC, also attach:
   - `AWSLambdaVPCAccessExecutionRole`
8. Go back to Lambda Console tab

### Step 3.7: Configure VPC (If RDS is in VPC)

**Skip this step if your RDS has public access enabled.**

1. In **"Configuration"** tab
2. Click **"VPC"** in left sidebar
3. Click **"Edit"** button
4. Configure:
   - **VPC:** Select the same VPC as your RDS instance
   - **Subnets:** Select at least 2 private subnets (for high availability)
   - **Security groups:** Select a security group that allows outbound connections
5. Click **"Save"** button
6. **Important:** This will take 1-2 minutes to apply

**To find RDS VPC:**
- Go to RDS Console → Your database → Connectivity & security → VPC

**Update RDS Security Group:**
- Go to RDS → Your database → Connectivity & security → VPC security groups
- Click on the security group
- Edit inbound rules → Add rule:
  - Type: PostgreSQL (port 5432)
  - Source: Select Lambda's security group
  - Save rules

### Step 3.8: Add S3 Trigger

1. Still in Lambda function page
2. Click **"Configuration"** tab
3. Click **"Triggers"** in left sidebar (or scroll to "Function overview" → "Add trigger")
4. Click **"Add trigger"** button
5. Configure trigger:
   - **Source:** Select `S3`
   - **Bucket:** Select your S3 bucket (e.g., `athena-data-bucket-data`)
   - **Event types:** Check `All object create events`
   - **Prefix:** `audit-trail-data/raw/` (or your prefix)
   - **Suffix:** `.parquet`
   - **Enable trigger:** ✓ (checked)
6. Click **"Add"** button

**Note:** You may see a warning about permissions. Click "Add" to allow Lambda to access S3.

---

## Part 4: Test the Lambda Function

### Step 4.1: Test with Sample Event

1. In Lambda function page
2. Click **"Test"** tab (next to "Code" tab)
3. Click **"Create new test event"**
4. Select **"Create new test event"**
5. **Event name:** `test-s3-parquet`
6. **Event JSON:** Copy and paste from `events/s3-event.json`, but update the bucket name and key:

```json
{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "ap-south-1",
      "eventTime": "2024-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "s3": {
        "bucket": {
          "name": "athena-data-bucket-data"
        },
        "object": {
          "key": "audit-trail-data/raw/test-file.parquet",
          "size": 1024
        }
      }
    }
  ]
}
```

7. Click **"Save"** button
8. Click **"Test"** button
9. Wait for execution (may take 30-60 seconds)
10. Check **"Execution result"**:
    - ✅ Success: Green banner with execution results
    - ❌ Error: Red banner with error details

### Step 4.2: Check CloudWatch Logs

1. In Lambda function page
2. Click **"Monitor"** tab
3. Click **"View CloudWatch logs"** button
4. Click on the latest log stream
5. Review logs for:
   - Connection to database
   - Reading parquet file
   - Inserting records
   - Any errors

### Step 4.3: Test with Real S3 File

1. Upload a test parquet file to S3:

```bash
aws s3 cp your-test-file.parquet s3://athena-data-bucket-data/audit-trail-data/raw/
```

2. Wait 1-2 minutes
3. Check CloudWatch Logs to see if Lambda was triggered
4. Verify data in PostgreSQL:

```bash
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U your_username -d audit_trail_db

# Check record count
SELECT COUNT(*) FROM audit_trail_data;

# View sample data
SELECT * FROM audit_trail_data LIMIT 10;
```

---

## Part 5: Verify and Monitor

### Step 5.1: Verify Configuration

Check all settings are correct:

- ✅ Function code uploaded
- ✅ Timeout: 15 minutes
- ✅ Memory: 1024 MB
- ✅ Environment variables set (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME)
- ✅ IAM permissions configured
- ✅ VPC configured (if needed)
- ✅ S3 trigger added

### Step 5.2: Set Up Monitoring

1. Go to **"Monitor"** tab in Lambda
2. Review metrics:
   - **Invocations:** Number of times function was called
   - **Duration:** Execution time
   - **Errors:** Any failures
   - **Throttles:** If function is being throttled

3. Set up CloudWatch Alarms (optional):
   - Go to CloudWatch → Alarms
   - Create alarm for Lambda errors
   - Set notification (email/SNS)

---

## Troubleshooting Common Issues

### Issue 1: "Unable to connect to database"

**Solutions:**
- Verify RDS endpoint is correct
- Check if RDS is in VPC (configure Lambda VPC settings)
- Verify security group allows Lambda connections
- Check database credentials

### Issue 2: "Permission denied" errors

**Solutions:**
- Check Lambda execution role has S3 read permissions
- Verify database user has INSERT permissions
- Check VPC permissions if RDS is in VPC

### Issue 3: "Timeout" errors

**Solutions:**
- Increase Lambda timeout (max 15 minutes)
- Increase memory allocation
- Check if parquet file is too large
- Verify network connectivity to RDS

### Issue 4: "Module not found" errors

**Solutions:**
- Ensure all dependencies are in the ZIP file
- Check Python version matches (3.11)
- Rebuild the deployment package

### Issue 5: Lambda not triggered by S3

**Solutions:**
- Verify S3 trigger is enabled
- Check file prefix/suffix matches
- Verify bucket name is correct
- Check CloudWatch Logs for trigger events

---

## Alternative: Deploy Using AWS SAM CLI

If you prefer using SAM CLI (easier for updates):

### Step 1: Install SAM CLI

```bash
# Windows (Chocolatey)
choco install aws-sam-cli

# Or download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
```

### Step 2: Build and Deploy

```bash
cd lambda/parquet_to_rds

# Build
sam build

# Deploy (guided mode - will ask for parameters)
sam deploy --guided
```

Follow the prompts and enter your configuration values.

---

## Next Steps

1. ✅ Lambda function is created and configured
2. ✅ S3 trigger is set up
3. ✅ Test with a real parquet file
4. ✅ Monitor CloudWatch Logs
5. ✅ Set up alerts for errors (optional)

Your Lambda function is now ready to automatically process parquet files uploaded to S3 and save them to RDS PostgreSQL!

---

## Quick Reference

**Lambda Function Name:** `parquet-to-rds-processor`  
**Runtime:** Python 3.11  
**Timeout:** 15 minutes  
**Memory:** 1024 MB  
**Trigger:** S3 Object Created events  
**RDS Endpoint:** `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`  
**Database:** `audit_trail_db`  
**Table:** `audit_trail_data`







