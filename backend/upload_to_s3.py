"""
Script to upload Parquet files to S3 bucket
This script uploads local Parquet files to S3 for Athena to query
"""
import boto3
import os
from pathlib import Path
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "athena-data-bucket-data")
S3_PREFIX = os.getenv("S3_PREFIX", "audit-trail-data/raw/")

def upload_parquet_files(local_directory=".", s3_bucket=None, s3_prefix=None):
    """
    Upload all Parquet files from local directory to S3
    
    Args:
        local_directory: Local directory containing Parquet files
        s3_bucket: S3 bucket name (if None, uses env variable)
        s3_prefix: S3 prefix/path (if None, uses env variable)
    """
    if not s3_bucket:
        s3_bucket = S3_BUCKET_NAME
    if not s3_prefix:
        s3_prefix = S3_PREFIX
    
    if not s3_bucket:
        raise ValueError("S3_BUCKET_NAME must be set in environment variables or passed as parameter")
    
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables")
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    # Find all Parquet files
    parquet_files = glob.glob(os.path.join(local_directory, "*.parquet"))
    
    if not parquet_files:
        print(f"No Parquet files found in {local_directory}")
        return
    
    print(f"Found {len(parquet_files)} Parquet file(s)")
    print(f"Uploading to: s3://{s3_bucket}/{s3_prefix}")
    print("-" * 60)
    
    uploaded_count = 0
    for file_path in parquet_files:
        file_name = os.path.basename(file_path)
        s3_key = f"{s3_prefix}{file_name}"
        
        try:
            print(f"Uploading {file_name}...")
            s3_client.upload_file(file_path, s3_bucket, s3_key)
            print(f"✅ Successfully uploaded: {file_name}")
            print(f"   S3 Location: s3://{s3_bucket}/{s3_key}")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ Failed to upload {file_name}: {str(e)}")
    
    print("-" * 60)
    print(f"Upload complete! {uploaded_count}/{len(parquet_files)} files uploaded")
    print(f"\nS3 Location: s3://{s3_bucket}/{s3_prefix}")
    print(f"\nNext steps:")
    print(f"1. Create Athena table using: athena/create_table.sql")
    print(f"2. Query data using: athena/query_all_data.sql")

if __name__ == "__main__":
    import sys
    
    # Get project root directory (parent of backend)
    project_root = Path(__file__).parent.parent
    
    # Upload Parquet files from project root
    try:
        upload_parquet_files(
            local_directory=str(project_root),
            s3_bucket=S3_BUCKET_NAME,
            s3_prefix=S3_PREFIX
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

