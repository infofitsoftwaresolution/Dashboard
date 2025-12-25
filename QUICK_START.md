# Quick Start Guide - Athena Data Pipeline

## 🚀 Quick Setup (5 Minutes)

### Step 1: Configure AWS Credentials

Edit `backend/.env`:
```env
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
S3_PREFIX=audit-trail-data/raw/
S3_RESULTS_BUCKET=your-bucket-name
S3_RESULTS_PREFIX=athena-results/
ATHENA_DATABASE_NAME=audit_trail_db
ATHENA_TABLE_NAME=audit_trail_processed
```

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Upload Parquet Files to S3

```bash
python backend/upload_to_s3.py
```

### Step 4: Create Athena Table

1. Go to [AWS Athena Console](https://console.aws.amazon.com/athena/)
2. Run this query (replace `YOUR_BUCKET_NAME`):

```sql
CREATE DATABASE IF NOT EXISTS audit_trail_db;

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
LOCATION 's3://YOUR_BUCKET_NAME/audit-trail-data/raw/'
TBLPROPERTIES (
    'projection.enabled'='false',
    'parquet.compress'='SNAPPY'
);
```

### Step 5: Query All Data

```sql
SELECT * FROM audit_trail_data ORDER BY audit_datetime DESC;
```

### Step 6: Start FastAPI Server

```bash
cd backend
python main.py
```

### Step 7: Test API

```bash
curl "http://localhost:8000/api/athena/data?limit=10"
```

---

## 📝 All Queries You Need

### Get All Data
```sql
SELECT * FROM audit_trail_data ORDER BY audit_datetime DESC;
```

### Get Data with Filters
```sql
SELECT * FROM audit_trail_data 
WHERE status = 'FINALIZED'
  AND audit_datetime >= TIMESTAMP '2025-10-01 00:00:00'
ORDER BY audit_datetime DESC;
```

### Process and Save to S3
```sql
-- First create processed table
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
LOCATION 's3://YOUR_BUCKET_NAME/audit-trail-data/processed/'
TBLPROPERTIES (
    'projection.enabled'='false',
    'parquet.compress'='SNAPPY'
);

-- Then insert processed data
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

---

## 📚 Full Documentation

See `ATHENA_PIPELINE_SETUP.md` for complete step-by-step instructions.

See `athena/QUERIES_REFERENCE.md` for all available queries.

