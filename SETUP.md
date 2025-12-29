# Setup Guide - AWS Athena & S3 Data Pipeline Dashboard

Complete guide for setting up S3, Athena, and running the dashboard application.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [AWS S3 Setup](#aws-s3-setup)
4. [AWS Athena Setup](#aws-athena-setup)
5. [SQL Queries Reference](#sql-queries-reference)
6. [Application Setup](#application-setup)
7. [API Endpoints](#api-endpoints)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **AWS Account** with:
  - S3 bucket access
  - Athena access
  - IAM user with appropriate permissions

---

## Project Structure

```
Dashboard/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── athena_service.py       # Athena query service
│   ├── requirements.txt        # Python dependencies
│   ├── env.example             # Environment variables template
│   └── venv/                   # Python virtual environment (created on setup)
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── AthenaDataView.jsx
│   │   │   ├── FilterBar.jsx
│   │   │   ├── Dashboard components...
│   │   ├── App.jsx             # Main React app
│   │   └── main.jsx            # React entry point
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Vite configuration
│
├── athena/
│   ├── create_table_ACTUAL.sql      # Create Athena table
│   ├── create_view.sql              # Create dashboard view
│   ├── FIX_0_RESULTS.sql            # Fix metadata issues
│   ├── GET_ALL_DATA_ACTUAL.sql      # Query all data
│   ├── save_results_to_s3_ACTUAL.sql # Process and save to S3
│   └── VERIFY_ALL_FILES.sql         # Verify all files are read
│
├── README.md                   # Project overview
└── SETUP.md                    # This file
```

---

## AWS S3 Setup

### Step 1: Create S3 Bucket

1. Go to [AWS S3 Console](https://console.aws.amazon.com/s3/)
2. Click **"Create bucket"**
3. Configure:
   - **Bucket name**: `athena-data-bucket-data` (or your preferred name)
   - **Region**: `ap-south-1` (or your preferred region)
   - **Block Public Access**: Keep default settings
4. Click **"Create bucket"**

### Step 2: Create S3 Folder Structure

Create the following folder structure in your S3 bucket:

```
s3://athena-data-bucket-data/
├── audit-trail-data/
│   ├── raw/                    # Raw Parquet files go here
│   └── processed/              # Processed results (optional)
└── athena-results/             # Athena query results
```

### Step 3: Upload Parquet Files

Upload your Parquet files to:
```
s3://athena-data-bucket-data/audit-trail-data/raw/
```

**Methods to upload:**
- AWS Console: Drag and drop files
- AWS CLI: `aws s3 cp file.parquet s3://athena-data-bucket-data/audit-trail-data/raw/`
- Python script: Use `boto3` to upload programmatically

### Step 4: Configure S3 Permissions

Ensure your IAM user has these S3 permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::athena-data-bucket-data/*",
        "arn:aws:s3:::athena-data-bucket-data"
      ]
    }
  ]
}
```

---

## AWS Athena Setup

### Step 1: Create IAM User with Athena Permissions

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Create a new user or use existing user
3. Attach the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::athena-data-bucket-data/*",
        "arn:aws:s3:::athena-data-bucket-data"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "athena:*",
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Create **Access Key** for the user:
   - Go to user → Security credentials → Create access key
   - Save `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### Step 2: Configure Athena Workgroup

1. Go to [AWS Athena Console](https://console.aws.amazon.com/athena/)
2. Go to **Workgroups** → **primary** (or create new)
3. Configure **Query result location**:
   ```
   s3://athena-data-bucket-data/athena-results/
   ```
4. Set **Encryption**: SSE_S3 (default)

### Step 3: Create Athena Database

Run this query in Athena Console:

```sql
CREATE DATABASE IF NOT EXISTS audit_trail_db;
```

### Step 4: Create Athena Table

Run the SQL from `athena/create_table_ACTUAL.sql` (see SQL Queries section below).

**Important:** Update the `LOCATION` in the SQL to match your S3 bucket:
```sql
LOCATION 's3://YOUR_BUCKET_NAME/audit-trail-data/raw/'
```

### Step 5: Repair Table Metadata

After creating the table, run:

```sql
MSCK REPAIR TABLE audit_trail_data;
```

This refreshes metadata so Athena can detect all Parquet files.

### Step 6: Verify Table

```sql
SELECT COUNT(*) as total_records FROM audit_trail_data;
```

If count > 0, your setup is working!

---

## SQL Queries Reference

All SQL queries used in this application:

### 1. Create Database

```sql
CREATE DATABASE IF NOT EXISTS audit_trail_db;
USE audit_trail_db;
```

### 2. Create External Table

**File:** `athena/create_table_ACTUAL.sql`

```sql
USE audit_trail_db;

CREATE EXTERNAL TABLE IF NOT EXISTS audit_trail_data (
    event_name string,
    pk string,
    sk string,
    app string,
    tenant_id string,
    user_id string,
    appt_datetime timestamp,
    status string,
    status_reason string,
    care_record_id string,
    patient_id string,
    patient_name string,
    audio_uri string,
    summary_uri string,
    edited_summary_uri string,
    transcript_uri string,
    after_visit_summary_uri string,
    audio_duration string,
    expireat bigint,
    similarity string,
    note_format string,
    session_id string,
    internal_record string,
    creation_userid string,
    creation_datetime timestamp,
    completed_datetime timestamp,
    lastupdated_datetime timestamp,
    lastupdated_userid string,
    lastupdated_reason string,
    audit_datetime timestamp,
    submitted_datetime timestamp
)
STORED AS PARQUET
LOCATION 's3://athena-data-bucket-data/audit-trail-data/raw/'
TBLPROPERTIES (
    'projection.enabled'='false',
    'parquet.compress'='SNAPPY'
);
```

### 3. Create Dashboard View

**File:** `athena/create_view.sql`

```sql
USE audit_trail_db;

CREATE OR REPLACE VIEW audit_trail_dashboard_view AS
SELECT 
    event_name,
    tenant_id,
    user_id,
    patient_id,
    patient_name,
    status,
    appt_datetime,
    creation_datetime,
    completed_datetime,
    lastupdated_datetime,
    audit_datetime,
    CAST(audio_duration AS double) as audio_duration,
    CAST(similarity AS double) as similarity,
    note_format,
    creation_userid,
    lastupdated_userid,
    lastupdated_reason,
    care_record_id
FROM audit_trail_data
WHERE status IS NOT NULL
  AND patient_id IS NOT NULL;
```

### 4. Repair Table (Fix 0 Results)

**File:** `athena/FIX_0_RESULTS.sql`

```sql
USE audit_trail_db;

-- Repair table metadata (run after adding new files)
MSCK REPAIR TABLE audit_trail_data;

-- Verify count
SELECT COUNT(*) as total_records FROM audit_trail_data;
```

### 5. Get All Data

**File:** `athena/GET_ALL_DATA_ACTUAL.sql`

```sql
USE audit_trail_db;

-- Get all data
SELECT * FROM audit_trail_data 
ORDER BY audit_datetime DESC;

-- Get with limit
SELECT * FROM audit_trail_data 
ORDER BY audit_datetime DESC 
LIMIT 100;

-- Get specific columns
SELECT 
    event_name,
    tenant_id,
    user_id,
    patient_id,
    patient_name,
    status,
    audit_datetime
FROM audit_trail_data
ORDER BY audit_datetime DESC
LIMIT 10;
```

### 6. Process and Save Results to S3

**File:** `athena/save_results_to_s3_ACTUAL.sql`

```sql
USE audit_trail_db;

-- Create processed table
CREATE EXTERNAL TABLE IF NOT EXISTS audit_trail_processed (
    event_name string,
    tenant_id string,
    user_id string,
    patient_id string,
    patient_name string,
    status string,
    appt_datetime timestamp,
    creation_datetime timestamp,
    completed_datetime timestamp,
    lastupdated_datetime timestamp,
    audit_datetime timestamp,
    audio_duration double,
    similarity double,
    note_format string
)
STORED AS PARQUET
LOCATION 's3://athena-data-bucket-data/audit-trail-data/processed/'
TBLPROPERTIES (
    'projection.enabled'='false',
    'parquet.compress'='SNAPPY'
);

-- Insert processed data (saves to S3)
INSERT INTO audit_trail_processed
SELECT 
    event_name,
    tenant_id,
    user_id,
    patient_id,
    patient_name,
    status,
    appt_datetime,
    creation_datetime,
    completed_datetime,
    lastupdated_datetime,
    audit_datetime,
    CAST(audio_duration AS double) as audio_duration,
    CAST(similarity AS double) as similarity,
    note_format
FROM audit_trail_data
WHERE status IS NOT NULL
  AND patient_id IS NOT NULL;
```

### 7. Verify All Files Are Read

**File:** `athena/VERIFY_ALL_FILES.sql`

```sql
USE audit_trail_db;

-- Repair metadata
MSCK REPAIR TABLE audit_trail_data;

-- Get total count
SELECT COUNT(*) as total_records FROM audit_trail_data;

-- Get date range
SELECT 
    MIN(audit_datetime) as earliest_record,
    MAX(audit_datetime) as latest_record,
    COUNT(*) as total_records
FROM audit_trail_data;

-- Get records per day
SELECT 
    DATE(audit_datetime) as date,
    COUNT(*) as records_per_day
FROM audit_trail_data
WHERE audit_datetime IS NOT NULL
GROUP BY DATE(audit_datetime)
ORDER BY date DESC
LIMIT 30;
```

### 8. Common Filter Queries

```sql
-- Filter by status
SELECT * FROM audit_trail_data 
WHERE status = 'FINALIZED'
ORDER BY audit_datetime DESC;

-- Filter by date range
SELECT * FROM audit_trail_data 
WHERE audit_datetime >= TIMESTAMP '2025-10-01 00:00:00'
  AND audit_datetime <= TIMESTAMP '2025-12-31 23:59:59'
ORDER BY audit_datetime DESC;

-- Filter by user
SELECT * FROM audit_trail_data 
WHERE user_id = '500065'
ORDER BY audit_datetime DESC;

-- Filter by tenant
SELECT * FROM audit_trail_data 
WHERE tenant_id = 'OUTP_NY!LIVE:PROD'
ORDER BY audit_datetime DESC;

-- Combined filters
SELECT * FROM audit_trail_data 
WHERE status = 'FINALIZED'
  AND tenant_id = 'OUTP_NY!LIVE:PROD'
  AND audit_datetime >= TIMESTAMP '2025-10-01 00:00:00'
ORDER BY audit_datetime DESC;
```

---

## Application Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
```

### Step 2: Backend Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   # Copy example file
   copy env.example .env  # Windows
   cp env.example .env    # Linux/Mac
   ```

5. **Edit `.env` file:**
   ```env
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION=ap-south-1
   S3_BUCKET_NAME=athena-data-bucket-data
   S3_PREFIX=audit-trail-data/raw/
   S3_RESULTS_BUCKET=athena-data-bucket-data
   S3_RESULTS_PREFIX=athena-results/
   ATHENA_DATABASE_NAME=audit_trail_db
   ATHENA_TABLE_NAME=audit_trail_data
   ATHENA_WORKGROUP=primary
   ```

6. **Start backend:**
   ```bash
   python main.py
   ```

   Backend runs at: `http://localhost:8000`

### Step 3: Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend runs at: `http://localhost:5173`

### Step 4: Access Dashboard

Open browser: `http://localhost:5173`

---

## API Endpoints

### Health Check

- **GET** `/`
  - Returns: `{"message": "Dashboard API is running"}`

### Dashboard Metrics

- **GET** `/api/metrics`
  - Returns: List of dashboard metrics (visits, notes, time, similarity)

- **GET** `/api/top-users`
  - Returns: Top users by session count

- **GET** `/api/active-users`
  - Returns: Active user statistics

- **GET** `/api/staff-speaking`
  - Returns: Staff speaking statistics

- **GET** `/api/times`
  - Returns: Time-related data grouped by month

- **GET** `/api/consents`
  - Returns: Consent data statistics

### Filter Options

- **GET** `/api/filter-options`
  - Returns: Available filter options (practitioners, programs, locations)
  - Query params: None

### Reports (All support filters)

- **GET** `/api/audit-summary`
  - Query params: `practitioner`, `program`, `location`, `startDate`, `endDate`

- **GET** `/api/patient-access`
  - Query params: `practitioner`, `program`, `location`, `startDate`, `endDate`

- **GET** `/api/signed-notes`
  - Query params: `practitioner`, `program`, `location`, `startDate`, `endDate`

- **GET** `/api/unsigned-notes`
  - Query params: `practitioner`, `program`, `location`, `startDate`, `endDate`

- **GET** `/api/practitioner-service-usage`
  - Query params: `practitioner`, `program`, `location`, `startDate`, `endDate`

- **GET** `/api/sync-issues`
  - Query params: `practitioner`, `program`, `location`, `startDate`, `endDate`

### Athena Endpoints

- **GET** `/api/athena/data`
  - Returns: Data from Athena with filters
  - Query params: `limit`, `status`, `user_id`, `patient_id`, `start_date`, `end_date`

- **GET** `/api/athena/summary`
  - Returns: Summary statistics from Athena

- **POST** `/api/athena/query`
  - Body: `{"query": "SELECT * FROM audit_trail_data LIMIT 10"}`
  - Returns: Custom query results

- **GET** `/api/athena/all-data`
  - Returns: All data from all Parquet files (no limit)

- **GET** `/api/athena/dashboard`
  - Returns: Optimized dashboard data
  - Query params: `limit` (use `limit=None` for all data), `status`, `user_id`, `patient_id`, `start_date`, `end_date`

- **GET** `/api/athena/verify-files`
  - Returns: List of all Parquet files in S3 with size and last modified date

- **GET** `/api/athena/repair-table`
  - Executes `MSCK REPAIR TABLE` to refresh Athena metadata
  - Returns: Repair status

### API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Troubleshooting

### Backend Issues

**Problem:** Backend won't start
- **Solution:**
  1. Check Python version: `python --version` (need 3.8+)
  2. Activate virtual environment
  3. Install dependencies: `pip install -r requirements.txt`
  4. Check `.env` file exists and has correct AWS credentials

**Problem:** "AWS credentials must be set"
- **Solution:** Configure `.env` file with AWS credentials (see Application Setup)

**Problem:** "InvalidRequestException: Unable to verify/create output bucket"
- **Solution:**
  1. Check S3 bucket exists and is in the same region as `AWS_REGION`
  2. Verify IAM user has `s3:GetBucketLocation` permission
  3. Check `S3_RESULTS_BUCKET` in `.env` matches your bucket name

### Frontend Issues

**Problem:** Frontend won't start
- **Solution:**
  1. Check Node.js version: `node --version` (need 16+)
  2. Delete `node_modules`: `rm -rf node_modules` (Linux/Mac) or `rmdir /s node_modules` (Windows)
  3. Reinstall: `npm install`
  4. Check if port 5173 is available

**Problem:** CORS errors
- **Solution:**
  1. Ensure backend is running on port 8000
  2. Check `backend/main.py` CORS configuration
  3. Verify frontend is calling correct API URL

### Athena Issues

**Problem:** 0 results from Athena queries
- **Solution:**
  1. Run `MSCK REPAIR TABLE audit_trail_data;` in Athena Console
  2. Verify Parquet files are in correct S3 location
  3. Check table `LOCATION` matches S3 path exactly
  4. Verify IAM permissions allow Athena to read S3

**Problem:** "Table not found"
- **Solution:**
  1. Verify database exists: `SHOW DATABASES;`
  2. Use correct database: `USE audit_trail_db;`
  3. Check table exists: `SHOW TABLES;`
  4. Recreate table using `athena/create_table_ACTUAL.sql`

**Problem:** Query timeout
- **Solution:**
  1. Add `LIMIT` to queries
  2. Use filters to reduce data scanned
  3. Check S3 bucket region matches Athena region
  4. Verify Parquet files are not corrupted

### Data Issues

**Problem:** Missing columns in results
- **Solution:**
  1. Verify Parquet file schema matches table schema
  2. Check column names match exactly (case-sensitive)
  3. Run `DESCRIBE audit_trail_data;` to see table structure

**Problem:** Date/time format issues
- **Solution:**
  1. Athena expects timestamps in format: `TIMESTAMP '2025-10-31 21:00:00'`
  2. Use `CAST()` for type conversions
  3. Check Parquet file timestamp format

---

## Next Steps

1. ✅ S3 bucket created and Parquet files uploaded
2. ✅ Athena database and table created
3. ✅ Backend configured and running
4. ✅ Frontend configured and running
5. ✅ Dashboard accessible at `http://localhost:5173`

**You're all set!** 🎉

For more information, see `README.md` for project overview.
