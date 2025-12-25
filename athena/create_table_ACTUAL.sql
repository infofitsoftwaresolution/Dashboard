-- Athena Table Creation Query - READY TO USE
-- Bucket: athena-data-bucket-data
-- Raw data location: s3://athena-data-bucket-data/audit-trail-data/raw/

-- Step 1: Create database (if not exists)
CREATE DATABASE IF NOT EXISTS audit_trail_db;

-- Step 2: Use the database
USE audit_trail_db;

-- Step 3: Create the external table
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

-- Step 4: Repair table to refresh metadata (IMPORTANT if you get 0 results)
MSCK REPAIR TABLE audit_trail_data;

-- Step 5: Verify table was created
SHOW TABLES;

-- Step 6: Check if data is accessible
SELECT COUNT(*) as total_records FROM audit_trail_data;

