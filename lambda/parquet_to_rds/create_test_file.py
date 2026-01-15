"""
Create a test parquet file for testing Lambda function
This creates sample data matching the audit_trail_data schema
"""
import pandas as pd
from datetime import datetime, timedelta
import os

# Create sample data matching your schema
data = {
    'event_name': ['appointment_created', 'appointment_completed', 'note_signed'],
    'pk': ['pk-test-001', 'pk-test-002', 'pk-test-003'],
    'sk': ['sk-test-001', 'sk-test-002', 'sk-test-003'],
    'app': ['healthcare-app', 'healthcare-app', 'healthcare-app'],
    'tenant_id': ['tenant-123', 'tenant-123', 'tenant-123'],
    'user_id': ['user-456', 'user-456', 'user-789'],
    'appt_datetime': [
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(hours=2),
        datetime.now() - timedelta(hours=1)
    ],
    'status': ['scheduled', 'completed', 'signed'],
    'status_reason': [None, 'Patient attended', None],
    'care_record_id': ['care-001', 'care-001', 'care-002'],
    'patient_id': ['patient-001', 'patient-001', 'patient-002'],
    'patient_name': ['John Doe', 'John Doe', 'Jane Smith'],
    'audio_uri': ['s3://bucket/audio1.mp3', 's3://bucket/audio2.mp3', None],
    'summary_uri': ['s3://bucket/summary1.txt', 's3://bucket/summary2.txt', 's3://bucket/summary3.txt'],
    'edited_summary_uri': [None, 's3://bucket/edited1.txt', None],
    'transcript_uri': ['s3://bucket/transcript1.txt', 's3://bucket/transcript2.txt', None],
    'after_visit_summary_uri': [None, 's3://bucket/avs1.txt', 's3://bucket/avs2.txt'],
    'audio_duration': ['300', '450', '600'],
    'expireat': [1735689600, 1735776000, 1735862400],
    'similarity': ['0.95', '0.92', '0.88'],
    'note_format': ['standard', 'standard', 'detailed'],
    'session_id': ['session-001', 'session-001', 'session-002'],
    'internal_record': ['internal-001', 'internal-001', 'internal-002'],
    'creation_userid': ['creator-001', 'creator-001', 'creator-002'],
    'creation_datetime': [
        datetime.now() - timedelta(days=1, hours=1),
        datetime.now() - timedelta(hours=3),
        datetime.now() - timedelta(hours=2)
    ],
    'completed_datetime': [
        None,
        datetime.now() - timedelta(hours=1),
        datetime.now() - timedelta(minutes=30)
    ],
    'lastupdated_datetime': [
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(hours=2),
        datetime.now() - timedelta(hours=1)
    ],
    'lastupdated_userid': ['updater-001', 'updater-001', 'updater-002'],
    'lastupdated_reason': [None, 'Status updated', 'Note signed'],
    'audit_datetime': [
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(hours=2),
        datetime.now() - timedelta(hours=1)
    ],
    'submitted_datetime': [
        None,
        datetime.now() - timedelta(hours=1, minutes=30),
        datetime.now() - timedelta(minutes=45)
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as parquet file
output_file = 'test.parquet'
df.to_parquet(output_file, index=False, engine='pyarrow')

print(f"✅ Test parquet file created: {output_file}")
print(f"📊 Records: {len(df)}")
print(f"📁 File size: {os.path.getsize(output_file) / 1024:.2f} KB")
print(f"\n📋 Sample data:")
print(df[['event_name', 'patient_name', 'status', 'appt_datetime']].head())
print(f"\n✅ Ready to upload to S3!")
print(f"   Upload to: s3://your-bucket-name/audit-trail-data/raw/test.parquet")







