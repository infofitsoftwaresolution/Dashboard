-- Process data and save results to S3
-- Bucket: athena-data-bucket-data
-- Processed data location: s3://athena-data-bucket-data/audit-trail-data/processed/

-- Step 1: Make sure you're using the correct database
USE audit_trail_db;

-- Step 2: Create processed results table
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

-- Step 3: Insert processed data (this saves to S3)
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

-- Step 4: Verify processed data
SELECT COUNT(*) FROM audit_trail_processed;
SELECT * FROM audit_trail_processed LIMIT 10;

