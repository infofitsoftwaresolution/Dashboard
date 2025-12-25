-- Create a view for dashboard data from Athena
-- This view provides a clean, optimized query for the dashboard

USE audit_trail_db;

-- Create view for dashboard data
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

-- Query the view (this is what the dashboard will use)
-- SELECT * FROM audit_trail_dashboard_view 
-- ORDER BY audit_datetime DESC 
-- LIMIT 100;

-- Alternative: If you have a processed table, use that instead
-- CREATE OR REPLACE VIEW audit_trail_dashboard_view AS
-- SELECT * FROM audit_trail_processed
-- ORDER BY audit_datetime DESC;

