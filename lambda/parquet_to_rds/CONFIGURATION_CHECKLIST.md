# Lambda Configuration Checklist

Use this checklist to ensure all steps are completed correctly.

## Pre-Deployment Checklist

### Database Setup
- [ ] Connected to RDS PostgreSQL database
- [ ] Created `audit_trail_db` database (if not exists)
- [ ] Executed `create_rds_table.sql` to create table
- [ ] Verified table exists: `SELECT * FROM audit_trail_data LIMIT 1;`
- [ ] Confirmed database user has INSERT permissions
- [ ] Saved database credentials (username and password)

### Lambda Package Preparation
- [ ] Navigated to `lambda/parquet_to_rds` directory
- [ ] Created `package` directory
- [ ] Copied `lambda_function.py` to package directory
- [ ] Installed dependencies: `pip install -r requirements.txt -t .`
- [ ] Created ZIP file: `parquet-to-rds.zip`
- [ ] Verified ZIP file size (should be 50-100 MB with dependencies)

---

## AWS Lambda Console Configuration

### Function Creation
- [ ] Opened AWS Lambda Console (region: ap-south-1)
- [ ] Clicked "Create function"
- [ ] Selected "Author from scratch"
- [ ] Set function name: `parquet-to-rds-processor`
- [ ] Selected runtime: `Python 3.11`
- [ ] Selected architecture: `x86_64`
- [ ] Clicked "Create function"

### Code Upload
- [ ] Clicked "Upload from" → ".zip file"
- [ ] Selected `parquet-to-rds.zip`
- [ ] Clicked "Save"
- [ ] Waited for upload to complete

### General Configuration
- [ ] Clicked "Configuration" → "General configuration"
- [ ] Clicked "Edit"
- [ ] Set Timeout: `15 min 0 sec` (900 seconds)
- [ ] Set Memory: `1024 MB`
- [ ] Clicked "Save"

### Environment Variables
- [ ] Clicked "Configuration" → "Environment variables"
- [ ] Clicked "Edit"
- [ ] Added `DB_HOST` = `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
- [ ] Added `DB_PORT` = `5432`
- [ ] Added `DB_NAME` = `audit_trail_db`
- [ ] Added `DB_USER` = `[your_username]`
- [ ] Added `DB_PASSWORD` = `[your_password]`
- [ ] Added `TABLE_NAME` = `audit_trail_data`
- [ ] Clicked "Save"

### IAM Permissions
- [ ] Clicked "Configuration" → "Permissions"
- [ ] Clicked on Execution role name
- [ ] Added policy: `AmazonS3ReadOnlyAccess` (or custom S3 policy)
- [ ] Added policy: `CloudWatchLogsFullAccess` (or `AWSLambdaBasicExecutionRole`)
- [ ] If RDS in VPC: Added `AWSLambdaVPCAccessExecutionRole`

### VPC Configuration (If RDS is in VPC)
- [ ] Clicked "Configuration" → "VPC"
- [ ] Clicked "Edit"
- [ ] Selected VPC (same as RDS)
- [ ] Selected at least 2 subnets
- [ ] Selected security group (allows outbound)
- [ ] Clicked "Save"
- [ ] Updated RDS security group to allow Lambda connections (port 5432)

### S3 Trigger
- [ ] Clicked "Configuration" → "Triggers"
- [ ] Clicked "Add trigger"
- [ ] Selected source: `S3`
- [ ] Selected bucket: `athena-data-bucket-data` (or your bucket)
- [ ] Selected event type: `All object create events`
- [ ] Set prefix: `audit-trail-data/raw/`
- [ ] Set suffix: `.parquet`
- [ ] Enabled trigger: ✓
- [ ] Clicked "Add"

---

## Testing Checklist

### Test Event
- [ ] Clicked "Test" tab
- [ ] Created new test event: `test-s3-parquet`
- [ ] Pasted test event JSON (from `events/s3-event.json`)
- [ ] Updated bucket name and key in test event
- [ ] Clicked "Save"
- [ ] Clicked "Test"
- [ ] Verified execution result (success or identified errors)

### CloudWatch Logs
- [ ] Clicked "Monitor" → "View CloudWatch logs"
- [ ] Opened latest log stream
- [ ] Verified logs show:
  - [ ] Lambda function started
  - [ ] Database connection successful
  - [ ] Parquet file read (if test file exists)
  - [ ] Records inserted (if test file exists)
  - [ ] No errors

### Real S3 Test
- [ ] Uploaded test parquet file to S3:
  ```bash
  aws s3 cp test.parquet s3://athena-data-bucket-data/audit-trail-data/raw/
  ```
- [ ] Waited 1-2 minutes
- [ ] Checked CloudWatch Logs for trigger
- [ ] Verified Lambda was invoked
- [ ] Connected to PostgreSQL and verified data:
  ```sql
  SELECT COUNT(*) FROM audit_trail_data;
  SELECT * FROM audit_trail_data LIMIT 10;
  ```

---

## Verification Checklist

### Function Status
- [ ] Function shows "Active" status
- [ ] No errors in recent invocations
- [ ] Execution time is reasonable (< 5 minutes for typical files)

### Monitoring
- [ ] CloudWatch Logs accessible
- [ ] Metrics showing invocations
- [ ] No throttling errors
- [ ] No timeout errors

### Data Verification
- [ ] Data appears in PostgreSQL table
- [ ] Record counts match expected values
- [ ] Data types are correct
- [ ] No duplicate records (if unique constraint exists)

---

## Troubleshooting Checklist

If something doesn't work:

### Connection Issues
- [ ] Verified RDS endpoint is correct
- [ ] Checked if RDS is in VPC (configure Lambda VPC if needed)
- [ ] Verified security group allows Lambda connections
- [ ] Tested database credentials manually
- [ ] Checked RDS is accessible from your network

### Permission Issues
- [ ] Verified Lambda role has S3 read permissions
- [ ] Verified database user has INSERT permissions
- [ ] Checked VPC permissions (if applicable)
- [ ] Verified CloudWatch Logs permissions

### Execution Issues
- [ ] Checked CloudWatch Logs for detailed errors
- [ ] Verified all dependencies are in ZIP file
- [ ] Confirmed Python version is 3.11
- [ ] Checked timeout is sufficient (15 minutes)
- [ ] Verified memory allocation (1024 MB)

### Trigger Issues
- [ ] Verified S3 trigger is enabled
- [ ] Checked file prefix matches trigger prefix
- [ ] Verified file suffix is `.parquet`
- [ ] Confirmed bucket name is correct
- [ ] Checked S3 event notifications are working

---

## Final Verification

Before considering setup complete:

- [ ] All checkboxes above are checked
- [ ] Test file processed successfully
- [ ] Data appears correctly in PostgreSQL
- [ ] CloudWatch Logs show no errors
- [ ] Lambda function is active and ready
- [ ] S3 trigger is configured and enabled

**✅ Setup Complete!** Your Lambda function is now ready to automatically process parquet files.

---

## Quick Commands Reference

```bash
# Connect to RDS
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U username -d audit_trail_db

# Upload test file
aws s3 cp test.parquet s3://athena-data-bucket-data/audit-trail-data/raw/

# Check Lambda logs
aws logs tail /aws/lambda/parquet-to-rds-processor --follow

# Verify data in PostgreSQL
psql -h database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com -U username -d audit_trail_db -c "SELECT COUNT(*) FROM audit_trail_data;"
```







