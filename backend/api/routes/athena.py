"""
Athena API routes
All endpoints related to AWS Athena queries and S3 Parquet file operations
"""
from fastapi import APIRouter
import traceback

from athena_service import AthenaService

router = APIRouter()

@router.get("/data")
async def get_athena_data(
    start_date: str = None,
    end_date: str = None,
    status: str = None,
    user_id: str = None,
    patient_id: str = None,
    limit: int = 100
):
    """
    Get processed data from Athena (S3 Parquet files)
    Supports filtering by date range, status, user_id, and patient_id
    """
    try:
        athena = AthenaService()
        
        data = athena.get_data_with_filters(
            start_date=start_date,
            end_date=end_date,
            status=status,
            user_id=user_id,
            patient_id=patient_id,
            limit=limit
        )
        
        return {
            "success": True,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/summary")
async def get_athena_summary():
    """
    Get summary statistics from ALL Parquet files in Athena
    """
    try:
        athena = AthenaService()
        
        stats = athena.get_data_statistics()
        
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "stats": {}
        }

@router.post("/query")
async def execute_athena_query(query: str):
    """
    Execute a custom Athena query
    Note: Use with caution, only allow trusted queries in production
    """
    try:
        athena = AthenaService()
        
        result = athena.execute_query(query)
        
        return {
            "success": True,
            "query_execution_id": result.get("query_execution_id"),
            "status": result.get("status"),
            "results": result.get("results", [])
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/all-data")
async def get_all_athena_data(
    start_date: str = None,
    end_date: str = None,
    status: str = None,
    user_id: str = None
):
    """
    Get ALL data from ALL Parquet files through Athena (NO LIMIT)
    Fetches complete dataset from S3
    """
    try:
        athena = AthenaService()
        
        data = athena.get_all_data_from_athena(
            start_date=start_date,
            end_date=end_date,
            status=status,
            user_id=user_id
        )
        
        return {
            "success": True,
            "count": len(data),
            "data": data,
            "message": f"Fetched {len(data)} records from all Parquet files"
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "count": 0,
            "data": []
        }

@router.get("/verify-files")
async def verify_s3_parquet_files():
    """
    Verify all Parquet files in S3 are accessible
    Lists all .parquet files in the configured S3 location
    """
    try:
        athena = AthenaService()
        
        verification = athena.verify_s3_files()
        
        return {
            "success": True,
            "verification": verification
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "verification": {}
        }

@router.get("/repair-table")
async def repair_athena_table():
    """
    Repair Athena table metadata to ensure all Parquet files are detected
    Run this after uploading new Parquet files to S3
    """
    try:
        athena = AthenaService()
        
        repair_result = athena.repair_table_metadata()
        
        return {
            "success": True,
            "repair": repair_result
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "repair": {}
        }

@router.get("/dashboard")
async def get_athena_dashboard_data(
    limit: int = None,
    start_date: str = None,
    end_date: str = None,
    status: str = None,
    user_id: str = None
):
    """
    Get dashboard data from Athena view
    If limit is None, returns ALL data
    """
    try:
        athena = AthenaService()
        
        # Use dashboard view method with filters
        data = athena.get_dashboard_data(
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            status=status,
            user_id=user_id
        )
        
        return {
            "success": True,
            "count": len(data),
            "data": data,
            "limit_applied": limit is not None
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "count": 0,
            "data": []
        }

