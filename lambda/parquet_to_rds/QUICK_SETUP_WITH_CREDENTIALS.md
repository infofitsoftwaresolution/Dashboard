# Quick Setup Guide - Ready to Deploy

## ✅ Package Ready!

Your Lambda deployment package has been created:
- **File:** `parquet-to-rds.zip`
- **Size:** ~79 MB
- **Location:** `lambda/parquet_to_rds/parquet-to-rds.zip`

---

## 🚀 Deployment Steps

### Step 1: Create PostgreSQL Table (5 minutes)

Connect to your RDS database and create the table:

```bash
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U postgres -d audit_trail_db
```

Then run:
```sql
-- Copy and paste the SQL from create_rds_table.sql
-- Or execute the file directly
\i create_rds_table.sql
```

Or manually execute the SQL in `create_rds_table.sql`.

---

### Step 2: Create Lambda Function in AWS Console (10 minutes)

1. **Go to AWS Lambda Console**
   - URL: https://console.aws.amazon.com/lambda/
   - Make sure region is: **ap-south-1** (Mumbai)

2. **Create Function**
   - Click **"Create function"**
   - Select **"Author from scratch"**
   - **Function name:** `parquet-to-rds-processor`
   - **Runtime:** `Python 3.11`
   - **Architecture:** `x86_64`
   - Click **"Create function"**

3. **Upload Code**
   - Scroll to **"Code source"** section
   - Click **"Upload from"** → **".zip file"**
   - Click **"Upload"** and select: `parquet-to-rds.zip`
   - Click **"Save"**
   - Wait for upload (1-2 minutes)

4. **Configure Settings**
   - Click **"Configuration"** tab
   - Click **"General configuration"** → **"Edit"**
   - Set **Timeout:** `15 min 0 sec`
   - Set **Memory:** `1024 MB`
   - Click **"Save"**

5. **Add Environment Variables**
   - Click **"Environment variables"** → **"Edit"**
   - Add these variables:

| Key | Value |
|-----|-------|
| `DB_HOST` | `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `audit_trail_db` |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | `Dashboard6287` |
| `TABLE_NAME` | `audit_trail_data` |

   - Click **"Save"**

6. **Configure IAM Permissions**
   - Click **"Permissions"** in Configuration tab
   - Click on the **Execution role** name
   - Click **"Add permissions"** → **"Attach policies"**
   - Attach:
     - `AmazonS3ReadOnlyAccess`
     - `CloudWatchLogsFullAccess`
   - If RDS is in VPC, also attach:
     - `AWSLambdaVPCAccessExecutionRole`

7. **Configure VPC (If RDS is in VPC)**
   - Click **"VPC"** in Configuration tab
   - Click **"Edit"**
   - Select same VPC as RDS
   - Select 2 subnets
   - Select security group
   - Click **"Save"**
   - **Update RDS Security Group** to allow Lambda connections (port 5432)

8. **Add S3 Trigger**
   - Click **"Triggers"** in Configuration tab
   - Click **"Add trigger"**
   - **Source:** `S3`
   - **Bucket:** Your S3 bucket (e.g., `athena-data-bucket-data`)
   - **Event types:** `All object create events`
   - **Prefix:** `audit-trail-data/raw/`
   - **Suffix:** `.parquet`
   - **Enable trigger:** ✓
   - Click **"Add"**

---

### Step 3: Test the Function (5 minutes)

1. **Upload a test parquet file to S3:**
   ```bash
   aws s3 cp test.parquet s3://your-bucket-name/audit-trail-data/raw/
   ```

2. **Check CloudWatch Logs:**
   - Go to Lambda → **Monitor** → **View CloudWatch logs**
   - Check for successful execution

3. **Verify data in PostgreSQL:**
   ```bash
   psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U postgres -d audit_trail_db
   ```
   ```sql
   SELECT COUNT(*) FROM audit_trail_data;
   SELECT * FROM audit_trail_data LIMIT 10;
   ```

---

## 📋 Your Configuration Summary

- **Database Host:** `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
- **Database Port:** `5432`
- **Database Name:** `audit_trail_db`
- **Database User:** `postgres`
- **Database Password:** `Dashboard6287`
- **Table Name:** `audit_trail_data`
- **Lambda Function:** `parquet-to-rds-processor`
- **Runtime:** Python 3.11
- **Timeout:** 15 minutes
- **Memory:** 1024 MB

---

## ✅ Checklist

- [ ] PostgreSQL table created
- [ ] Lambda function created
- [ ] Code uploaded (parquet-to-rds.zip)
- [ ] Environment variables set
- [ ] IAM permissions configured
- [ ] VPC configured (if needed)
- [ ] S3 trigger added
- [ ] Test file uploaded
- [ ] Data verified in PostgreSQL

---

## 🆘 Troubleshooting

**Can't connect to database:**
- Check if RDS is in VPC (configure Lambda VPC)
- Verify security group allows Lambda connections
- Check database credentials

**Permission errors:**
- Verify Lambda role has S3 read permissions
- Check database user has INSERT permissions

**Timeout errors:**
- Increase Lambda timeout
- Increase memory allocation

---

## 📁 Files Ready

- ✅ `parquet-to-rds.zip` - Ready to upload to Lambda
- ✅ `create_rds_table.sql` - Run this on PostgreSQL
- ✅ `lambda_function.py` - Lambda function code
- ✅ `ENVIRONMENT_VARIABLES.txt` - Your credentials reference

**You're all set! Upload the ZIP file and configure as above.**







