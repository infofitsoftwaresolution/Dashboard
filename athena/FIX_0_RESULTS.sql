-- QUICK FIX for 0 Results Issue
-- Run these queries in order in Athena Console

-- Step 1: Make sure you're in the correct database
USE audit_trail_db;

-- Step 2: Check if table exists
SHOW TABLES;

-- Step 3: Check table location (verify it matches your S3 path)
DESCRIBE audit_trail_data;

-- Step 4: REPAIR TABLE - This refreshes metadata (MOST IMPORTANT!)
MSCK REPAIR TABLE audit_trail_data;

-- Step 5: Wait 5-10 seconds, then check count
SELECT COUNT(*) as total_records FROM audit_trail_data;

-- Step 6: If count > 0, get all data
SELECT * FROM audit_trail_data 
ORDER BY audit_datetime DESC;

-- If still 0 results after repair, check:
-- 1. Files are actually in s3://athena-data-bucket-data/audit-trail-data/raw/
-- 2. Table LOCATION matches exactly: s3://athena-data-bucket-data/audit-trail-data/raw/
-- 3. IAM permissions allow Athena to read S3

