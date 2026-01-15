"""
AWS Lambda function to process parquet files from S3 and save to RDS PostgreSQL
Triggered when a new parquet file is uploaded to S3
"""
import json
import os
import boto3
import pandas as pd
import pyarrow.parquet as pq
import psycopg2
from psycopg2 import errors as psycopg2_errors
from psycopg2.extras import execute_batch
from io import BytesIO
import logging
from typing import Dict, Any, List

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client('s3')

# RDS PostgreSQL connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST', 'database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'audit_trail_db')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Table name
TABLE_NAME = os.environ.get('TABLE_NAME', 'audit_trail_data')


def get_db_connection():
    """Create and return a PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=10
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise


def read_parquet_from_s3(bucket: str, key: str) -> pd.DataFrame:
    """Read parquet file from S3 and return as pandas DataFrame"""
    try:
        logger.info(f"Reading parquet file from s3://{bucket}/{key}")
        
        # Get object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        
        # Read parquet file into memory
        parquet_file = BytesIO(response['Body'].read())
        df = pd.read_parquet(parquet_file)
        
        logger.info(f"Successfully read {len(df)} rows from parquet file")
        return df
    except Exception as e:
        logger.error(f"Error reading parquet file from S3: {str(e)}")
        raise


def prepare_data_for_insert(df: pd.DataFrame) -> list:
    """Prepare DataFrame data for batch insert into PostgreSQL"""
    # Replace NaN/None values with None (NULL in SQL)
    df = df.where(pd.notnull(df), None)
    
    # Convert DataFrame to list of tuples
    records = [tuple(row) for row in df.values]
    return records


def get_table_columns(conn) -> List[str]:
    """Get column names from the PostgreSQL table (excluding auto-generated columns)"""
    try:
        cursor = conn.cursor()
        # Query to get column names excluding id, created_at, updated_at
        query = f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{TABLE_NAME}'
            AND column_name NOT IN ('id', 'created_at', 'updated_at')
            ORDER BY ordinal_position
        """
        cursor.execute(query)
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return columns
    except Exception as e:
        logger.error(f"Error getting table columns: {str(e)}")
        raise


def align_dataframe_to_table(df: pd.DataFrame, table_columns: list) -> pd.DataFrame:
    """Align DataFrame columns with table columns, handling missing/extra columns"""
    # Create a new DataFrame with table column structure
    aligned_df = pd.DataFrame()
    
    for col in table_columns:
        if col in df.columns:
            aligned_df[col] = df[col]
        else:
            # Column not in parquet file, fill with None
            logger.warning(f"Column '{col}' not found in parquet file, filling with NULL")
            aligned_df[col] = None
    
    # Log any extra columns in parquet that aren't in table
    extra_cols = set(df.columns) - set(table_columns)
    if extra_cols:
        logger.warning(f"Extra columns in parquet file (will be ignored): {', '.join(extra_cols)}")
    
    return aligned_df


def insert_data_to_rds(conn, df: pd.DataFrame):
    """Insert DataFrame data into PostgreSQL table"""
    try:
        cursor = conn.cursor()
        
        # Get table columns from database
        table_columns = get_table_columns(conn)
        logger.info(f"Table columns: {', '.join(table_columns)}")
        logger.info(f"DataFrame columns: {', '.join(df.columns)}")
        
        # Align DataFrame with table columns
        df_aligned = align_dataframe_to_table(df, table_columns)
        
        # Create placeholders for INSERT statement
        placeholders = ', '.join(['%s'] * len(table_columns))
        column_names = ', '.join([f'"{col}"' for col in table_columns])
        
        # Prepare data
        records = prepare_data_for_insert(df_aligned)
        
        # Check if conflict columns exist in the aligned DataFrame
        conflict_cols = ['pk', 'sk', 'audit_datetime']
        has_conflict_cols = all(col in table_columns for col in conflict_cols)
        
        # Prepare INSERT statement with optional ON CONFLICT handling
        if has_conflict_cols:
            conflict_clause = "ON CONFLICT (pk, sk, audit_datetime) DO NOTHING"
        else:
            conflict_clause = ""
            logger.warning("Conflict columns (pk, sk, audit_datetime) not all present, skipping conflict handling")
        
        insert_query = f"""
            INSERT INTO {TABLE_NAME} ({column_names})
            VALUES ({placeholders})
            {conflict_clause}
        """
        
        # Batch insert for better performance
        logger.info(f"Inserting {len(records)} records into {TABLE_NAME}")
        try:
            execute_batch(cursor, insert_query, records, page_size=1000)
        except (psycopg2_errors.UniqueViolation, psycopg2_errors.SyntaxError) as e:
            # If ON CONFLICT clause fails, try without it
            if has_conflict_cols:
                logger.warning(f"ON CONFLICT clause failed: {str(e)}, retrying without conflict handling")
                conn.rollback()
                cursor.close()
                cursor = conn.cursor()
                insert_query = f"""
                    INSERT INTO {TABLE_NAME} ({column_names})
                    VALUES ({placeholders})
                """
                execute_batch(cursor, insert_query, records, page_size=1000)
            else:
                raise
        
        # Commit transaction
        conn.commit()
        cursor.close()
        
        logger.info(f"Successfully inserted {len(records)} records into PostgreSQL")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error inserting data to RDS: {str(e)}")
        raise


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler function
    Triggered by S3 event when a new parquet file is uploaded
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Validate environment variables
        if not all([DB_USER, DB_PASSWORD]):
            error_msg = "DB_USER and DB_PASSWORD environment variables must be set"
            logger.error(error_msg)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': error_msg})
            }
        
        # Process each S3 record in the event
        processed_files = []
        errors = []
        
        for record in event.get('Records', []):
            try:
                # Extract S3 bucket and key from event
                bucket = record['s3']['bucket']['name']
                key = record['s3']['object']['key']
                
                # Skip if not a parquet file
                if not key.endswith('.parquet'):
                    logger.info(f"Skipping non-parquet file: {key}")
                    continue
                
                logger.info(f"Processing file: s3://{bucket}/{key}")
                
                # Read parquet file from S3
                df = read_parquet_from_s3(bucket, key)
                
                if df.empty:
                    logger.warning(f"Parquet file {key} is empty, skipping")
                    continue
                
                # Connect to RDS PostgreSQL
                conn = get_db_connection()
                
                try:
                    # Insert data into PostgreSQL
                    insert_data_to_rds(conn, df)
                    processed_files.append(key)
                    logger.info(f"Successfully processed file: {key}")
                finally:
                    conn.close()
                    
            except Exception as e:
                error_msg = f"Error processing file {key}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        # Return response
        response = {
            'statusCode': 200 if not errors else 207,  # 207 Multi-Status if partial failures
            'body': json.dumps({
                'message': 'Processing completed',
                'processed_files': processed_files,
                'errors': errors,
                'total_processed': len(processed_files),
                'total_errors': len(errors)
            })
        }
        
        logger.info(f"Processing complete. Processed: {len(processed_files)}, Errors: {len(errors)}")
        return response
        
    except Exception as e:
        error_msg = f"Lambda execution failed: {str(e)}"
        logger.error(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_msg})
        }

