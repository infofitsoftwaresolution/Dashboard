# Lambda Function: Parquet to RDS PostgreSQL Processor

This Lambda function automatically processes parquet files uploaded to S3 and inserts the data into RDS PostgreSQL database.

## Architecture

```
S3 Bucket (parquet files)
    ↓ (S3 Event Trigger)
AWS Lambda Function
    ↓ (Read & Process)
RDS PostgreSQL Database
```

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **RDS PostgreSQL Database** running and accessible
   - Endpoint: `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
   - Database: `audit_trail_db`
   - User credentials with INSERT permissions
3. **S3 Bucket** with parquet files
4. **AWS CLI** and **SAM CLI** installed
5. **Python 3.11** (for local testing)

## Setup Instructions

### Step 1: Create PostgreSQL Table

1. Connect to your RDS PostgreSQL database:
   ```bash
   psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U your_username -d audit_trail_db
   ```

2. Run the table creation script:
   ```bash
   psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U your_username -d audit_trail_db -f create_rds_table.sql
   ```

   Or manually execute the SQL in `create_rds_table.sql`

### Step 2: Install Dependencies

Install AWS SAM CLI if not already installed:
```bash
# Windows (using Chocolatey)
choco install aws-sam-cli

# Or download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
```

### Step 3: Build Lambda Package

Navigate to the lambda function directory:
```bash
cd lambda/parquet_to_rds
```

Build the Lambda package:
```bash
sam build
```

This will:
- Install Python dependencies
- Create a deployment package in `.aws-sam/build/`

### Step 4: Deploy Lambda Function

Deploy using SAM:
```bash
sam deploy --guided
```

During guided deployment, you'll be prompted for:
- Stack name: `parquet-to-rds-stack`
- AWS Region: `ap-south-1`
- S3 Bucket Name: `athena-data-bucket-data` (or your bucket name)
- S3 Prefix: `audit-trail-data/raw/` (or your prefix)
- DB Host: `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
- DB Port: `5432`
- DB Name: `audit_trail_db`
- DB User: Your PostgreSQL username
- DB Password: Your PostgreSQL password

Or deploy with parameters file:
```bash
sam deploy --parameter-overrides \
  S3BucketName=athena-data-bucket-data \
  S3Prefix=audit-trail-data/raw/ \
  DBHost=database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com \
  DBPort=5432 \
  DBName=audit_trail_db \
  DBUser=your_db_user \
  DBPassword=your_db_password
```

### Step 5: Verify Deployment

1. Check Lambda function in AWS Console
2. Verify S3 trigger is configured
3. Test by uploading a parquet file to S3

## Manual Deployment (Alternative)

If you prefer to deploy manually without SAM:

### 1. Create Deployment Package

```bash
# Create package directory
mkdir lambda-package
cd lambda-package

# Copy Lambda function
cp ../lambda_function.py .

# Install dependencies
pip install -r ../requirements.txt -t .

# Create ZIP file
zip -r ../parquet-to-rds.zip .
```

### 2. Create Lambda Function via AWS Console

1. Go to AWS Lambda Console
2. Click "Create function"
3. Choose "Author from scratch"
4. Configure:
   - Function name: `parquet-to-rds-processor`
   - Runtime: Python 3.11
   - Architecture: x86_64
5. Upload the ZIP file
6. Set environment variables:
   - `DB_HOST`: `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
   - `DB_PORT`: `5432`
   - `DB_NAME`: `audit_trail_db`
   - `DB_USER`: Your PostgreSQL username
   - `DB_PASSWORD`: Your PostgreSQL password
   - `TABLE_NAME`: `audit_trail_data`
7. Set timeout to 15 minutes (900 seconds)
8. Set memory to 1024 MB

### 3. Add S3 Trigger

1. In Lambda function, go to "Configuration" → "Triggers"
2. Click "Add trigger"
3. Select "S3"
4. Configure:
   - Bucket: Your S3 bucket name
   - Event type: `All object create events`
   - Prefix: `audit-trail-data/raw/` (or your prefix)
   - Suffix: `.parquet`
5. Click "Add"

### 4. Configure IAM Permissions

Ensure Lambda execution role has:
- S3 read permissions for the bucket
- CloudWatch Logs permissions
- VPC access (if RDS is in VPC)

## Testing

### Local Testing

Test the function locally:
```bash
sam local invoke ParquetToRDSFunction -e events/s3-event.json
```

Create a test event file `events/s3-event.json`:
```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "athena-data-bucket-data"
        },
        "object": {
          "key": "audit-trail-data/raw/test-file.parquet"
        }
      }
    }
  ]
}
```

### Test with Real S3 File

1. Upload a test parquet file to S3:
   ```bash
   aws s3 cp test.parquet s3://athena-data-bucket-data/audit-trail-data/raw/
   ```

2. Check CloudWatch Logs for the Lambda function to see execution results

3. Verify data in PostgreSQL:
   ```sql
   SELECT COUNT(*) FROM audit_trail_data;
   SELECT * FROM audit_trail_data LIMIT 10;
   ```

## Monitoring

- **CloudWatch Logs**: View function logs in `/aws/lambda/parquet-to-rds-processor`
- **CloudWatch Metrics**: Monitor invocations, errors, duration
- **RDS Monitoring**: Check database connections and query performance

## Troubleshooting

### Common Issues

1. **Connection Timeout to RDS**
   - Ensure Lambda is in the same VPC as RDS (if RDS is in VPC)
   - Check security group rules allow Lambda to connect
   - Verify RDS endpoint is correct

2. **Permission Errors**
   - Check Lambda execution role has S3 read permissions
   - Verify RDS credentials are correct
   - Ensure database user has INSERT permissions

3. **Memory/Timeout Issues**
   - Increase Lambda memory allocation
   - Increase timeout for large files
   - Consider processing files in chunks

4. **Data Type Mismatches**
   - Check parquet file schema matches PostgreSQL table schema
   - Verify data types are compatible

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DB_HOST` | RDS PostgreSQL host | Yes |
| `DB_PORT` | RDS PostgreSQL port | Yes |
| `DB_NAME` | Database name | Yes |
| `DB_USER` | Database username | Yes |
| `DB_PASSWORD` | Database password | Yes |
| `TABLE_NAME` | Target table name | No (default: audit_trail_data) |

## Cost Optimization

- Lambda charges per invocation and compute time
- Consider batching multiple files if possible
- Use appropriate memory allocation (not too high)
- Monitor and optimize database connection pooling if needed

## Security Best Practices

1. Store database credentials in AWS Secrets Manager (recommended)
2. Use VPC endpoints for S3 access (if in VPC)
3. Enable encryption at rest for RDS
4. Use least privilege IAM roles
5. Enable CloudWatch Logs encryption

## Support

For issues or questions, check:
- CloudWatch Logs for error messages
- RDS connection logs
- Lambda function metrics







