-- Query to get ALL data from the Parquet files
-- Bucket: athena-data-bucket-data
-- Make sure you're using the correct database: USE audit_trail_db;

-- Get all data
SELECT * FROM audit_trail_data 
ORDER BY audit_datetime DESC;

-- If you get 0 results, try these troubleshooting queries:

-- 1. Check if table exists and has data
SELECT COUNT(*) as total_records FROM audit_trail_data;

-- 2. Check first few records
SELECT * FROM audit_trail_data LIMIT 10;

-- 3. Check specific columns
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

-- 4. If still 0 results, repair the table
-- MSCK REPAIR TABLE audit_trail_data;

