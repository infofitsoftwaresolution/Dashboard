"""
Data API routes - Get all data from PostgreSQL
"""
from fastapi import APIRouter
from typing import List, Dict, Optional
from database_service import DatabaseService

router = APIRouter()

@router.get("/all-data")
async def get_all_data(
    limit: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    user_id: Optional[str] = None
):
    """Get all data from PostgreSQL audit_trail_data table"""
    try:
        db = DatabaseService()
        data = db.get_all_data(
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            status=status,
            user_id=user_id
        )
        return {
            "success": True,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "count": 0,
            "data": []
        }

@router.get("/count")
async def get_count():
    """Get total count of records"""
    try:
        db = DatabaseService()
        count = db.get_count()
        return {
            "success": True,
            "count": count
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "count": 0
        }

