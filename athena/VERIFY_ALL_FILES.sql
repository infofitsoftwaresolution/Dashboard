-- Verify All Parquet Files Are Being Read
-- Run these queries in Athena to ensure all files are accessible

USE audit_trail_db;

-- Step 1: Repair table metadata (IMPORTANT - run this after adding new files)
-- This ensures Athena detects all Parquet files in S3
MSCK REPAIR TABLE audit_trail_data;

-- Step 2: Get total count of records from ALL Parquet files
SELECT COUNT(*) as total_records FROM audit_trail_data;

-- Step 3: Get count by file (if partition information is available)
-- Note: This may not work if files aren't partitioned
SELECT COUNT(*) as record_count 
FROM audit_trail_data;

-- Step 4: Get date range to verify all files are included
SELECT 
    MIN(audit_datetime) as earliest_record,
    MAX(audit_datetime) as latest_record,
    COUNT(*) as total_records
FROM audit_trail_data;

-- Step 5: Get sample of records from different time periods
SELECT 
    DATE(audit_datetime) as date,
    COUNT(*) as records_per_day
FROM audit_trail_data
WHERE audit_datetime IS NOT NULL
GROUP BY DATE(audit_datetime)
ORDER BY date DESC
LIMIT 30;

-- Step 6: Verify all columns are accessible
SELECT * FROM audit_trail_data LIMIT 10;

