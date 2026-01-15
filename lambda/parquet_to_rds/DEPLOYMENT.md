# Quick Deployment Guide

## Option 1: Using AWS SAM (Recommended)

### Prerequisites
```bash
# Install AWS SAM CLI
# Windows: choco install aws-sam-cli
# Or download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

# Install AWS CLI and configure credentials
aws configure
```

### Steps

1. **Navigate to Lambda directory**
   ```bash
   cd lambda/parquet_to_rds
   ```

2. **Build the function**
   ```bash
   sam build
   ```

3. **Deploy (guided mode)**
   ```bash
   sam deploy --guided
   ```
   
   Enter the following when prompted:
   - Stack Name: `parquet-to-rds-stack`
   - AWS Region: `ap-south-1`
   - Parameter S3BucketName: `athena-data-bucket-data`
   - Parameter S3Prefix: `audit-trail-data/raw/`
   - Parameter DBHost: `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
   - Parameter DBPort: `5432`
   - Parameter DBName: `audit_trail_db`
   - Parameter DBUser: `[your_db_username]`
   - Parameter DBPassword: `[your_db_password]`
   - Confirm changes: `Y`
   - Allow SAM CLI IAM role creation: `Y`
   - Disable rollback: `N`
   - Save arguments to configuration file: `Y`

4. **Verify deployment**
   - Check AWS Lambda Console for the function
   - Verify S3 trigger is configured
   - Check CloudWatch Logs

## Option 2: Manual Deployment via AWS Console

### Step 1: Create Deployment Package

```bash
cd lambda/parquet_to_rds

# Create package directory
mkdir package
cd package

# Copy function code
cp ../lambda_function.py .

# Install dependencies
pip install -r ../requirements.txt -t .

# Create ZIP (Windows PowerShell)
Compress-Archive -Path * -DestinationPath ../parquet-to-rds.zip

# Or on Linux/Mac
# zip -r ../parquet-to-rds.zip .
```

### Step 2: Create Lambda Function

1. Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Click **Create function**
3. Select **Author from scratch**
4. Configure:
   - **Function name**: `parquet-to-rds-processor`
   - **Runtime**: `Python 3.11`
   - **Architecture**: `x86_64`
5. Click **Create function**

### Step 3: Upload Code

1. In the function, scroll to **Code source**
2. Click **Upload from** → **.zip file**
3. Upload `parquet-to-rds.zip`
4. Click **Save**

### Step 4: Configure Environment Variables

1. Go to **Configuration** → **Environment variables**
2. Click **Edit**
3. Add:
   - `DB_HOST` = `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
   - `DB_PORT` = `5432`
   - `DB_NAME` = `audit_trail_db`
   - `DB_USER` = `[your_db_username]`
   - `DB_PASSWORD` = `[your_db_password]`
   - `TABLE_NAME` = `audit_trail_data`
4. Click **Save**

### Step 5: Configure Function Settings

1. Go to **Configuration** → **General configuration**
2. Click **Edit**
3. Set:
   - **Timeout**: `15 min 0 sec` (900 seconds)
   - **Memory**: `1024 MB`
4. Click **Save**

### Step 6: Add S3 Trigger

1. Go to **Configuration** → **Triggers**
2. Click **Add trigger**
3. Select **S3**
4. Configure:
   - **Bucket**: `athena-data-bucket-data` (or your bucket)
   - **Event types**: Select `All object create events`
   - **Prefix**: `audit-trail-data/raw/`
   - **Suffix**: `.parquet`
   - **Enable trigger**: ✓ (checked)
5. Click **Add**

### Step 7: Configure IAM Permissions

1. Go to **Configuration** → **Permissions**
2. Click on the **Execution role**
3. Ensure the role has:
   - S3 read permissions for your bucket
   - CloudWatch Logs permissions
   - VPC access (if RDS is in VPC)

If needed, attach these policies:
- `AmazonS3ReadOnlyAccess` (or custom policy for your bucket)
- `AWSLambdaVPCAccessExecutionRole` (if RDS is in VPC)

## Step 8: Create PostgreSQL Table

Before testing, ensure the table exists in your RDS database:

```bash
# Connect to RDS
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U your_username -d audit_trail_db

# Run the table creation script
\i create_rds_table.sql

# Or copy and paste the SQL from create_rds_table.sql
```

## Testing

1. **Upload a test parquet file to S3:**
   ```bash
   aws s3 cp test.parquet s3://athena-data-bucket-data/audit-trail-data/raw/
   ```

2. **Check Lambda execution:**
   - Go to Lambda function → **Monitor** → **View CloudWatch logs**
   - Check for successful execution

3. **Verify data in PostgreSQL:**
   ```sql
   SELECT COUNT(*) FROM audit_trail_data;
   SELECT * FROM audit_trail_data LIMIT 10;
   ```

## Troubleshooting

### Lambda can't connect to RDS
- Ensure Lambda is in the same VPC as RDS (if RDS is in VPC)
- Check security group allows inbound connections from Lambda
- Verify RDS endpoint and credentials

### Permission errors
- Check Lambda execution role has S3 read permissions
- Verify database user has INSERT permissions

### Timeout errors
- Increase Lambda timeout (max 15 minutes)
- Increase memory allocation
- Check if parquet file is too large







