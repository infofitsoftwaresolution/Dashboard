# Quick Start Guide

## Prerequisites Checklist

- [ ] AWS Account with appropriate permissions
- [ ] RDS PostgreSQL database running at `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
- [ ] PostgreSQL database `audit_trail_db` created
- [ ] PostgreSQL user credentials with INSERT permissions
- [ ] S3 bucket with parquet files (e.g., `athena-data-bucket-data`)
- [ ] AWS CLI configured (`aws configure`)
- [ ] AWS SAM CLI installed (optional, for easier deployment)

## 5-Minute Setup

### Step 1: Create PostgreSQL Table (2 minutes)

Connect to your RDS database and run:

```bash
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U your_username -d audit_trail_db -f create_rds_table.sql
```

Or manually execute the SQL in `create_rds_table.sql` via your database client.

### Step 2: Deploy Lambda Function (3 minutes)

#### Option A: Using SAM (Recommended)

```bash
cd lambda/parquet_to_rds
sam build
sam deploy --guided
```

Follow the prompts and enter:
- Stack name: `parquet-to-rds-stack`
- Region: `ap-south-1`
- S3 Bucket: `athena-data-bucket-data` (or your bucket)
- S3 Prefix: `audit-trail-data/raw/`
- DB credentials: Your PostgreSQL username and password

#### Option B: Manual Deployment

1. Create deployment package:
   ```bash
   cd lambda/parquet_to_rds
   mkdir package && cd package
   cp ../lambda_function.py .
   pip install -r ../requirements.txt -t .
   zip -r ../parquet-to-rds.zip .
   ```

2. Create Lambda function in AWS Console:
   - Function name: `parquet-to-rds-processor`
   - Runtime: Python 3.11
   - Upload `parquet-to-rds.zip`
   - Set timeout: 15 minutes
   - Set memory: 1024 MB

3. Add environment variables:
   - `DB_HOST`: `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
   - `DB_PORT`: `5432`
   - `DB_NAME`: `audit_trail_db`
   - `DB_USER`: Your username
   - `DB_PASSWORD`: Your password
   - `TABLE_NAME`: `audit_trail_data`

4. Add S3 trigger:
   - Bucket: Your S3 bucket
   - Event: All object create events
   - Prefix: `audit-trail-data/raw/`
   - Suffix: `.parquet`

### Step 3: Test (1 minute)

1. Upload a test parquet file to S3:
   ```bash
   aws s3 cp test.parquet s3://athena-data-bucket-data/audit-trail-data/raw/
   ```

2. Check Lambda logs:
   - Go to CloudWatch → Log groups → `/aws/lambda/parquet-to-rds-processor`
   - Verify successful execution

3. Verify data in PostgreSQL:
   ```sql
   SELECT COUNT(*) FROM audit_trail_data;
   ```

## Troubleshooting

### Lambda can't connect to RDS
- **If RDS is in VPC**: Configure Lambda VPC settings (see `VPC_SETUP.md`)
- Check security group allows Lambda connections
- Verify RDS endpoint is correct

### Permission errors
- Lambda execution role needs S3 read permissions
- Database user needs INSERT permissions

### Timeout errors
- Increase Lambda timeout (max 15 minutes)
- Increase memory allocation
- Check parquet file size

## Next Steps

- Monitor CloudWatch Logs for processing status
- Set up CloudWatch Alarms for errors
- Configure VPC if RDS is in private subnet (see `VPC_SETUP.md`)
- Review `README.md` for detailed documentation

## Support

Check CloudWatch Logs for detailed error messages and processing status.







