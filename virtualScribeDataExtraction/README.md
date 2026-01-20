# Parquet to PostgreSQL Data Pipeline

A production-ready AWS Lambda function that automatically processes Parquet files from S3 and loads them into RDS PostgreSQL. The solution uses container-based deployment for reliable dependency management.

## 📖 Table of Contents

- [Architecture](#-architecture)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Complete Step-by-Step Setup Guide](#-complete-step-by-step-setup-guide)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Monitoring](#-monitoring)

## 🏗️ Architecture

```
┌─────────────┐
│  S3 Bucket  │
│ (Parquet)   │
└──────┬──────┘
       │ Upload Event
       │ Triggers
       ▼
┌─────────────────────────┐
│   AWS Lambda Function   │
│   (Container Image)     │
│                         │
│  1. Download Parquet   │
│  2. Analyze Schema     │
│  3. Create Table       │
│  4. Load Data          │
└──────┬──────────────────┘
       │
       ▼
┌─────────────┐
│ RDS         │
│ PostgreSQL  │
└─────────────┘
```

## ✨ Features

- **Automatic Processing**: Triggers automatically on S3 Parquet file uploads
- **Schema Detection**: Automatically analyzes and maps Parquet schemas to PostgreSQL
- **Type Mapping**: Intelligent conversion of Arrow/Parquet types to PostgreSQL types
- **Table Creation**: Auto-creates PostgreSQL tables if they don't exist
- **Batch Loading**: Efficient batch inserts for large files (1000 rows per batch)
- **Error Handling**: Comprehensive error handling with detailed logging
- **CloudWatch Integration**: Full logging and monitoring capabilities
- **Container Deployment**: Uses Docker for reliable dependency management

## 📋 Prerequisites

Before you begin, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
   - Download from: https://aws.amazon.com/cli/
   - Configure with: `aws configure`
3. **Docker Desktop** installed and running
   - Download from: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version`
4. **RDS PostgreSQL Instance** (or create one during setup)
5. **S3 Bucket** (or create one during setup)

### Get Your AWS Account ID

You'll need your AWS Account ID for several steps. Get it using:

```powershell
aws sts get-caller-identity --query Account --output text
```

Save this number - you'll use it as `YOUR-ACCOUNT-ID` in commands below.

## 🚀 Complete Step-by-Step Setup Guide

Follow these steps in order to set up the complete solution.

### Step 1: Create ECR Repository

Amazon Elastic Container Registry (ECR) stores your Docker images.

1. **Open AWS Console** → Go to ECR: https://console.aws.amazon.com/ecr
2. **Select Region**: Make sure you're in `ap-south-1` (Mumbai)
3. **Create Repository**:
   - Click "Create repository"
   - Repository name: `parquet-processor`
   - Visibility: Private
   - Tag immutability: Disabled (or Enabled if preferred)
   - Encryption: AWS managed encryption key
   - Click "Create repository"

**Verify:**
```powershell
aws ecr describe-repositories --repository-names parquet-processor --region ap-south-1
```

### Step 2: Create IAM Role for Lambda

The Lambda function needs permissions to access S3 and write logs.

1. **Open AWS Console** → Go to IAM: https://console.aws.amazon.com/iam
2. **Create Role**:
   - Click "Roles" → "Create role"
   - Trusted entity: AWS service
   - Service: Lambda
   - Click "Next"
3. **Add Permissions**:
   - Search and select: `AmazonS3ReadOnlyAccess`
   - Search and select: `CloudWatchLogsFullAccess`
   - Click "Next"
4. **Name the Role**:
   - Role name: `parquet-processor-lambda-role`
   - Description: "Role for Lambda function to process Parquet files"
   - Click "Create role"
5. **Note the Role ARN**:
   - It will look like: `arn:aws:iam::YOUR-ACCOUNT-ID:role/parquet-processor-lambda-role`
   - Save this for Step 5

**Alternative: Create via CLI:**
```powershell
# Create trust policy file
$trustPolicy = @{
    Version = "2012-10-17"
    Statement = @(
        @{
            Effect = "Allow"
            Principal = @{
                Service = "lambda.amazonaws.com"
            }
            Action = "sts:AssumeRole"
        }
    )
} | ConvertTo-Json

# Create role
aws iam create-role `
    --role-name parquet-processor-lambda-role `
    --assume-role-policy-document $trustPolicy

# Attach policies
aws iam attach-role-policy `
    --role-name parquet-processor-lambda-role `
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

aws iam attach-role-policy `
    --role-name parquet-processor-lambda-role `
    --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
```

### Step 3: Create S3 Bucket (if needed)

If you don't have an S3 bucket yet:

1. **Open AWS Console** → Go to S3: https://console.aws.amazon.com/s3
2. **Create Bucket**:
   - Click "Create bucket"
   - Bucket name: Choose a unique name (e.g., `my-parquet-files-123456789`)
   - Region: `ap-south-1` (Mumbai)
   - Block Public Access: Keep enabled
   - Click "Create bucket"

**Note the bucket name** - you'll need it later.

### Step 4: Prepare RDS PostgreSQL

Ensure your RDS PostgreSQL instance is ready:

1. **RDS Endpoint**: Note your RDS endpoint (e.g., `database-1.c3easrmf.ap-south-1.rds.amazonaws.com`)
2. **Database Name**: Usually `postgres`
3. **Credentials**: Have your database username and password ready
4. **Security Group**: Ensure it allows inbound connections from Lambda (or your IP for testing)

**If RDS is in a VPC:**
- Lambda must be in the same VPC
- Security group must allow Lambda's security group
- Consider VPC endpoints for S3 access

### Step 5: Build and Push Docker Image

This step creates the container image and uploads it to ECR.

#### 5.1 Navigate to Project Directory

```powershell
cd D:\Dashboard\virtualScribeDataExtraction
```

#### 5.2 Login to ECR

Replace `YOUR-ACCOUNT-ID` with your actual account ID:

```powershell
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com
```

**Expected output:** `Login Succeeded`

#### 5.3 Build and Push Image

**Important:** Use this exact command to ensure OCI format (required for Lambda):

```powershell
docker buildx build `
    --platform linux/amd64 `
    --provenance=false `
    --sbom=false `
    --output type=image,oci-mediatypes=true,name=YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/parquet-processor:latest `
    --push .
```

**What this does:**
- `--platform linux/amd64`: Builds for Lambda's architecture
- `--provenance=false --sbom=false`: Disables extra metadata (not needed)
- `--output type=image,oci-mediatypes=true`: Ensures OCI format (required for Lambda)
- `--push`: Pushes directly to ECR

**This will take 5-10 minutes** - it's downloading and installing dependencies.

**Verify the image:**
```powershell
aws ecr describe-images `
    --repository-name parquet-processor `
    --region ap-south-1 `
    --image-ids imageTag=latest `
    --query 'imageDetails[0].imageManifestMediaType' `
    --output text
```

**Expected output:** `application/vnd.oci.image.manifest.v1+json`

If you see `application/vnd.docker.distribution.manifest.v2+json`, the image is in Docker format and won't work with Lambda. Rebuild using the command above.

### Step 6: Create Lambda Function

Now create the Lambda function using the container image.

#### 6.1 Get Your IAM Role ARN

```powershell
aws iam get-role --role-name parquet-processor-lambda-role --query 'Role.Arn' --output text
```

Save this ARN - it looks like: `arn:aws:iam::YOUR-ACCOUNT-ID:role/parquet-processor-lambda-role`

#### 6.2 Create Lambda Function

Replace `YOUR-ACCOUNT-ID` and `YOUR-ROLE-ARN`:

```powershell
aws lambda create-function `
    --function-name parquet-to-postgres-processor `
    --region ap-south-1 `
    --package-type Image `
    --code ImageUri=YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/parquet-processor:latest `
    --role YOUR-ROLE-ARN `
    --timeout 900 `
    --memory-size 3008 `
    --ephemeral-storage Size=10240
```

**Parameters explained:**
- `--function-name`: Name of your Lambda function
- `--package-type Image`: Uses container image (not zip)
- `--code ImageUri`: Points to your ECR image
- `--role`: IAM role ARN from Step 6.1
- `--timeout 900`: 15 minutes (maximum)
- `--memory-size 3008`: Maximum memory (recommended for large files)
- `--ephemeral-storage Size=10240`: 10 GB temporary storage

**Wait 1-2 minutes** for the function to be created.

**Verify:**
```powershell
aws lambda get-function --function-name parquet-to-postgres-processor --region ap-south-1 --query 'Configuration.State' --output text
```

**Expected output:** `Active`

### Step 7: Configure Environment Variables

Set database connection details as environment variables.

Replace the values with your actual RDS details:

```powershell
aws lambda update-function-configuration `
    --function-name parquet-to-postgres-processor `
    --region ap-south-1 `
    --environment "Variables={DB_HOST=your-rds-endpoint.rds.amazonaws.com,DB_NAME=postgres,DB_PORT=5432,DB_USER=postgres,DB_PASSWORD=your-password,TABLE_NAME=audittrail_firehose}"
```

**Example:**
```powershell
aws lambda update-function-configuration `
    --function-name parquet-to-postgres-processor `
    --region ap-south-1 `
    --environment "Variables={DB_HOST=database-1.c3easrmf.ap-south-1.rds.amazonaws.com,DB_NAME=postgres,DB_PORT=5432,DB_USER=postgres,DB_PASSWORD=Dashboard6287,TABLE_NAME=audittrail_firehose}"
```

**Verify:**
```powershell
aws lambda get-function-configuration `
    --function-name parquet-to-postgres-processor `
    --region ap-south-1 `
    --query 'Environment.Variables' `
    --output json
```

### Step 8: Configure S3 Event Trigger

Set up S3 to automatically trigger Lambda when Parquet files are uploaded.

#### Option A: Using AWS Console (Recommended for beginners)

1. **Go to S3 Console**: https://console.aws.amazon.com/s3
2. **Select Your Bucket**: Click on your bucket name
3. **Go to Properties Tab**: Click "Properties" at the top
4. **Scroll to Event Notifications**: Find "Event notifications" section
5. **Create Event Notification**:
   - Click "Create event notification"
   - **Event name**: `parquet-upload-trigger`
   - **Prefix** (optional): `parquet/` (only trigger for files in this folder)
   - **Suffix**: `.parquet` (only trigger for .parquet files)
   - **Event types**: Check `PUT` (when files are uploaded)
   - **Destination**: Select "Lambda function"
   - **Lambda function**: Select `parquet-to-postgres-processor`
   - Click "Save changes"

#### Option B: Using AWS CLI

Replace `YOUR-BUCKET-NAME` with your actual bucket name:

```powershell
aws s3api put-bucket-notification-configuration `
    --bucket YOUR-BUCKET-NAME `
    --notification-configuration '{
        "LambdaFunctionConfigurations": [{
            "Id": "parquet-upload-trigger",
            "LambdaFunctionArn": "arn:aws:lambda:ap-south-1:YOUR-ACCOUNT-ID:function:parquet-to-postgres-processor",
            "Events": ["s3:ObjectCreated:Put"],
            "Filter": {
                "Key": {
                    "FilterRules": [{
                        "Name": "Suffix",
                        "Value": ".parquet"
                    }]
                }
            }
        }]
    }'
```

**Grant S3 Permission to Invoke Lambda:**
```powershell
aws lambda add-permission `
    --function-name parquet-to-postgres-processor `
    --statement-id s3-trigger-permission `
    --action lambda:InvokeFunction `
    --principal s3.amazonaws.com `
    --source-arn arn:aws:s3:::YOUR-BUCKET-NAME `
    --source-account YOUR-ACCOUNT-ID `
    --region ap-south-1
```

### Step 9: Test the Solution

Now test if everything works!

#### 9.1 Upload a Test Parquet File

**Option 1: Using AWS Console**
1. Go to S3 → Your bucket
2. Click "Upload"
3. Select a `.parquet` file
4. Click "Upload"

**Option 2: Using AWS CLI**
```powershell
aws s3 cp test.parquet s3://YOUR-BUCKET-NAME/
```

#### 9.2 Check CloudWatch Logs

Watch the logs in real-time:

```powershell
aws logs tail /aws/lambda/parquet-to-postgres-processor --follow --region ap-south-1
```

**Look for these success messages:**
- `✓ Connected to PostgreSQL successfully!`
- `✓ Successfully loaded X rows`
- `Table created successfully`

#### 9.3 Verify Data in PostgreSQL

Connect to your RDS database and check:

```sql
-- Count rows
SELECT COUNT(*) FROM audittrail_firehose;

-- View sample data
SELECT * FROM audittrail_firehose LIMIT 10;

-- Check table structure
\d audittrail_firehose
```

## 📁 Project Structure

```
virtualScribeDataExtraction/
├── lambda_function.py          # Main Lambda handler
├── Dockerfile                  # Container image definition
├── requirements.txt            # Local development dependencies
├── requirements-lambda.txt     # Lambda dependencies (reference)
├── analyze_parquet_schema.py   # Local utility: Schema analysis
├── load_parquet_to_postgres.py # Local utility: Data loading
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## ⚙️ Configuration Reference

### Lambda Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DB_HOST` | RDS endpoint | Yes | `database-1.c3easrmf.ap-south-1.rds.amazonaws.com` |
| `DB_NAME` | Database name | Yes | `postgres` |
| `DB_PORT` | Database port | Yes | `5432` |
| `DB_USER` | Database user | Yes | `postgres` |
| `DB_PASSWORD` | Database password | Yes | `your-secure-password` |
| `TABLE_NAME` | Target table name | Yes | `audittrail_firehose` |

### Lambda Function Settings

| Setting | Value | Reason |
|---------|-------|--------|
| **Runtime** | Container Image | Uses Docker image |
| **Memory** | 3008 MB | Maximum for large files |
| **Timeout** | 900 seconds | 15 minutes (maximum) |
| **Ephemeral Storage** | 10240 MB | 10 GB for large Parquet files |

### IAM Permissions Required

The Lambda execution role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

## 📊 Data Type Mapping

The function automatically maps Parquet/Arrow types to PostgreSQL types:

| Parquet/Arrow Type | PostgreSQL Type |
|-------------------|-----------------|
| `int8`, `int16`, `int32` | `INTEGER` |
| `int64`, `uint32` | `BIGINT` |
| `uint64` | `NUMERIC(20)` |
| `float32` | `REAL` |
| `float64`, `double` | `DOUBLE PRECISION` |
| `string`, `utf8`, `large_string` | `TEXT` |
| `bool`, `boolean` | `BOOLEAN` |
| `timestamp[ns/us/ms/s]` | `TIMESTAMP` |
| `date32`, `date64` | `DATE` |
| `time32`, `time64` | `TIME` |
| `decimal128`, `decimal256` | `NUMERIC` |
| `binary`, `large_binary` | `BYTEA` |

Unknown types default to `TEXT`.

## 🧪 Testing

### Test Locally (Before Deploying)

1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Analyze Parquet schema:**
   ```powershell
   python analyze_parquet_schema.py
   ```

3. **Load data to local PostgreSQL:**
   ```powershell
   python load_parquet_to_postgres.py
   ```

### Test Lambda Function

1. **Upload test file to S3:**
   ```powershell
   aws s3 cp test.parquet s3://YOUR-BUCKET-NAME/
   ```

2. **Check CloudWatch Logs:**
   ```powershell
   aws logs tail /aws/lambda/parquet-to-postgres-processor --follow --region ap-south-1
   ```

3. **Verify data in PostgreSQL:**
   ```sql
   SELECT COUNT(*) FROM audittrail_firehose;
   SELECT * FROM audittrail_firehose LIMIT 10;
   ```

## 🔧 Local Development

### Setup

```powershell
# Install dependencies
pip install -r requirements.txt
```

### Utility Scripts

- **`analyze_parquet_schema.py`**: Analyze Parquet file schema locally
- **`load_parquet_to_postgres.py`**: Load Parquet data to local PostgreSQL

## 🐛 Troubleshooting

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Timeout Error** | Function times out before completing | Increase Lambda timeout to 900 seconds (15 minutes) |
| **Memory Error** | Out of memory errors in logs | Increase Lambda memory to 3008 MB |
| **RDS Connection Failed** | "Failed to connect to PostgreSQL" | Check security group allows Lambda VPC access. If Lambda is in VPC, ensure VPC endpoints for S3. |
| **InvalidImage Error** | "Image manifest media type not supported" | Rebuild image with OCI format: `oci-mediatypes=true` |
| **S3 Access Denied** | "Access Denied" when reading from S3 | Verify IAM role has `s3:GetObject` and `s3:ListBucket` permissions |
| **Table Creation Failed** | "Permission denied" when creating table | Check database user has `CREATE TABLE` permissions |
| **Function Not Triggered** | No logs when uploading file | Check S3 event notification is configured correctly and Lambda has permission |

### Step-by-Step Debugging

#### 1. Check CloudWatch Logs

```powershell
aws logs tail /aws/lambda/parquet-to-postgres-processor --follow --region ap-south-1
```

Look for error messages and stack traces.

#### 2. Verify Environment Variables

```powershell
aws lambda get-function-configuration `
    --function-name parquet-to-postgres-processor `
    --region ap-south-1 `
    --query 'Environment.Variables' `
    --output json
```

Ensure all required variables are set correctly.

#### 3. Test Database Connection

If RDS connection fails:

1. **Check Security Group:**
   - RDS security group must allow inbound from Lambda's security group
   - If Lambda is in VPC, ensure VPC configuration is correct

2. **Test from Lambda:**
   - Create a simple test function to verify connectivity
   - Or check CloudWatch logs for connection errors

#### 4. Verify Image Format

```powershell
aws ecr describe-images `
    --repository-name parquet-processor `
    --region ap-south-1 `
    --image-ids imageTag=latest `
    --query 'imageDetails[0].imageManifestMediaType' `
    --output text
```

**Must return:** `application/vnd.oci.image.manifest.v1+json`

If it returns `application/vnd.docker.distribution.manifest.v2+json`, rebuild with OCI format.

#### 5. Check IAM Permissions

```powershell
# Check role policies
aws iam list-attached-role-policies --role-name parquet-processor-lambda-role

# Check S3 permissions
aws iam get-role-policy --role-name parquet-processor-lambda-role --policy-name YourPolicyName
```

#### 6. Verify S3 Event Trigger

```powershell
# Check bucket notification configuration
aws s3api get-bucket-notification-configuration --bucket YOUR-BUCKET-NAME

# Check Lambda permissions
aws lambda get-policy --function-name parquet-to-postgres-processor --region ap-south-1
```

## 📈 Monitoring

### CloudWatch Metrics

Monitor these key metrics in CloudWatch:

- **Invocations**: Number of function invocations
- **Duration**: Execution time (should be < 15 minutes)
- **Errors**: Number of errors (should be 0)
- **Throttles**: Number of throttled invocations
- **ConcurrentExecutions**: Number of concurrent executions

**View metrics:**
```powershell
aws cloudwatch get-metric-statistics `
    --namespace AWS/Lambda `
    --metric-name Invocations `
    --dimensions Name=FunctionName,Value=parquet-to-postgres-processor `
    --start-time 2025-01-20T00:00:00Z `
    --end-time 2025-01-20T23:59:59Z `
    --period 3600 `
    --statistics Sum `
    --region ap-south-1
```

### CloudWatch Logs

Logs are automatically sent to:
```
/aws/lambda/parquet-to-postgres-processor
```

**Key log messages to look for:**
- `✓ Connected to PostgreSQL successfully!` - Database connection successful
- `✓ Successfully loaded X rows` - Data loaded successfully
- `Table created successfully` - Table was created
- `Error:` - Any error messages

**View recent logs:**
```powershell
aws logs tail /aws/lambda/parquet-to-postgres-processor --since 1h --region ap-south-1
```

### Set Up Alarms

Create CloudWatch alarms for:

1. **Error Rate:**
   ```powershell
   aws cloudwatch put-metric-alarm `
       --alarm-name lambda-parquet-errors `
       --alarm-description "Alert on Lambda errors" `
       --metric-name Errors `
       --namespace AWS/Lambda `
       --statistic Sum `
       --period 300 `
       --threshold 1 `
       --comparison-operator GreaterThanThreshold `
       --dimensions Name=FunctionName,Value=parquet-to-postgres-processor `
       --evaluation-periods 1 `
       --region ap-south-1
   ```

2. **Duration:**
   - Alert if function takes > 10 minutes consistently

## 🔒 Security Best Practices

1. **Use AWS Secrets Manager** for database credentials instead of environment variables
   ```powershell
   # Store secret
   aws secretsmanager create-secret `
       --name parquet-processor/db-credentials `
       --secret-string '{"username":"postgres","password":"your-password"}'
   
   # Update Lambda to use secret
   # (Requires code changes to read from Secrets Manager)
   ```

2. **Enable VPC** for Lambda if RDS is in private subnet
   - Configure VPC, subnets, and security groups
   - Use VPC endpoints for S3 access

3. **Use IAM roles** with least privilege principle
   - Only grant necessary permissions
   - Regularly review and audit permissions

4. **Enable encryption** for S3 and RDS
   - Enable S3 bucket encryption
   - Enable RDS encryption at rest

5. **Regularly rotate** database passwords
   - Update environment variables when rotating

6. **Use VPC endpoints** for S3 access from Lambda in VPC
   - Reduces data transfer costs
   - Improves security

7. **Enable CloudWatch Logs encryption**
   - Encrypt log groups at rest

## 📦 Dependencies

### Container Image (Dockerfile)

- **Base Image**: `public.ecr.aws/lambda/python:3.11`
- **numpy**: `1.26.4`
- **pyarrow**: `14.0.1`
- **pandas**: `2.1.4`
- **psycopg2-binary**: `2.9.9`

### Local Development

- `pyarrow>=10.0.0`
- `pandas>=1.5.0`
- `psycopg2-binary>=2.9.0`

## 🔄 Updating the Function

When you make changes to `lambda_function.py`:

1. **Rebuild and push image:**
   ```powershell
   docker buildx build `
       --platform linux/amd64 `
       --provenance=false `
       --sbom=false `
       --output type=image,oci-mediatypes=true,name=YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/parquet-processor:latest `
       --push .
   ```

2. **Update Lambda function:**
   ```powershell
   aws lambda update-function-code `
       --function-name parquet-to-postgres-processor `
       --image-uri YOUR-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com/parquet-processor:latest `
       --region ap-south-1
   ```

3. **Wait for update:**
   ```powershell
   aws lambda wait function-updated `
       --function-name parquet-to-postgres-processor `
       --region ap-south-1
   ```

4. **Verify:**
   ```powershell
   aws lambda get-function `
       --function-name parquet-to-postgres-processor `
       --region ap-south-1 `
       --query 'Configuration.LastUpdateStatus' `
       --output text
   ```

   **Expected:** `Successful`

## 📝 How It Works

1. **S3 Event Trigger**: When a `.parquet` file is uploaded to S3, an event notification triggers Lambda
2. **Download**: Lambda downloads the Parquet file from S3 into memory
3. **Schema Analysis**: The function analyzes the Parquet schema and maps Arrow types to PostgreSQL types
4. **Table Creation**: If the table doesn't exist, it's created automatically based on the schema
5. **Data Loading**: Data is loaded in batches (1000 rows per batch) for efficiency
6. **Logging**: All operations are logged to CloudWatch for monitoring and debugging

## 🤝 Contributing

1. Test locally before deploying
2. Update documentation for any changes
3. Follow AWS Lambda best practices
4. Add comprehensive error handling
5. Include logging for debugging

## 📄 License

This project is provided as-is for internal use.

## 🆘 Getting Help

If you encounter issues:

1. **Check CloudWatch Logs** for detailed error messages
2. **Review Lambda function metrics** in CloudWatch
3. **Verify IAM permissions** and RDS security group settings
4. **Test database connectivity** separately
5. **Verify Docker image** is in OCI format
6. **Check this README's Troubleshooting section**

## 📚 Additional Resources

- [AWS Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS Lambda with S3](https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Last Updated:** January 2025  
**AWS Region:** ap-south-1 (Mumbai)  
**Lambda Runtime:** Container Image (Python 3.11)  
**Tested With:** AWS CLI 2.x, Docker Desktop 4.x
