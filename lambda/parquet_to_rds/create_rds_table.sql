-- PostgreSQL Table Creation Script for Audit Trail Data
-- Run this script on your RDS PostgreSQL database before deploying the Lambda function
-- Database: audit_trail_db
-- Table: audit_trail_data

-- Create database if it doesn't exist (run as superuser)
-- CREATE DATABASE audit_trail_db;

-- Connect to the database
-- \c audit_trail_db;

-- Create the table
CREATE TABLE IF NOT EXISTS audit_trail_data (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255),
    pk VARCHAR(255),
    sk VARCHAR(255),
    app VARCHAR(255),
    tenant_id VARCHAR(255),
    user_id VARCHAR(255),
    appt_datetime TIMESTAMP,
    status VARCHAR(255),
    status_reason VARCHAR(255),
    care_record_id VARCHAR(255),
    patient_id VARCHAR(255),
    patient_name VARCHAR(255),
    audio_uri TEXT,
    summary_uri TEXT,
    edited_summary_uri TEXT,
    transcript_uri TEXT,
    after_visit_summary_uri TEXT,
    audio_duration VARCHAR(255),
    expireat BIGINT,
    similarity VARCHAR(255),
    note_format VARCHAR(255),
    session_id VARCHAR(255),
    internal_record VARCHAR(255),
    creation_userid VARCHAR(255),
    creation_datetime TIMESTAMP,
    completed_datetime TIMESTAMP,
    lastupdated_datetime TIMESTAMP,
    lastupdated_userid VARCHAR(255),
    lastupdated_reason VARCHAR(255),
    audit_datetime TIMESTAMP,
    submitted_datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_tenant_id ON audit_trail_data(tenant_id);
CREATE INDEX IF NOT EXISTS idx_user_id ON audit_trail_data(user_id);
CREATE INDEX IF NOT EXISTS idx_patient_id ON audit_trail_data(patient_id);
CREATE INDEX IF NOT EXISTS idx_status ON audit_trail_data(status);
CREATE INDEX IF NOT EXISTS idx_appt_datetime ON audit_trail_data(appt_datetime);
CREATE INDEX IF NOT EXISTS idx_audit_datetime ON audit_trail_data(audit_datetime);

-- Create unique constraint on combination of key fields to prevent duplicates
-- Adjust based on your actual unique key requirements
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_record 
ON audit_trail_data(pk, sk, audit_datetime) 
WHERE pk IS NOT NULL AND sk IS NOT NULL AND audit_datetime IS NOT NULL;

-- Verify table creation
SELECT COUNT(*) FROM audit_trail_data;







