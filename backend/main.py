from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union
from datetime import datetime, timedelta

app = FastAPI(title="Dashboard API", version="1.0.0")

# Database initialization removed - using Athena only

# Configure CORS - Allow all localhost ports for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SalesData(BaseModel):
    date: str
    sales: float
    orders: int

class RevenueData(BaseModel):
    month: str
    revenue: float
    profit: float

class UserActivity(BaseModel):
    hour: int
    active_users: int

class Metric(BaseModel):
    label: str
    value: Union[float, str]
    change: float
    trend: str

class TopUser(BaseModel):
    name: str
    visits: int
    totalTime: str = None

class ActiveUsersData(BaseModel):
    active: int
    enabled: int

class StaffSpeakingData(BaseModel):
    staff: int
    nonStaff: int

class TimesData(BaseModel):
    month: str
    recording: float
    processing: float
    createdToSign: float

class ConsentsData(BaseModel):
    listening: int
    dictation: int

class AuditItem(BaseModel):
    date: str
    action: str
    user: str
    status: str
    details: str

class PatientAccessItem(BaseModel):
    patientId: str
    patientName: str
    accessDate: str
    accessType: str
    duration: str

class ServiceUsageItem(BaseModel):
    serviceName: str
    usageCount: int
    totalTime: str
    lastUsed: str

class RecommendationItem(BaseModel):
    id: str
    type: str
    priority: str
    status: str
    createdDate: str

class DeliveryScheduleItem(BaseModel):
    reportName: str
    frequency: str
    nextDelivery: str
    status: str

class SignedNoteItem(BaseModel):
    noteId: str
    patientName: str
    practitioner: str
    signedDate: str
    status: str

class PractitionerUsageItem(BaseModel):
    practitionerName: str
    visits: int
    totalTime: str
    lastActive: str

class SyncIssueItem(BaseModel):
    id: str
    type: str
    severity: str
    status: str
    reportedDate: str

class UnsignedNoteItem(BaseModel):
    noteId: str
    patientName: str
    practitioner: str
    createdDate: str
    daysPending: int

@app.get("/")
async def root():
    return {"message": "Dashboard API is running"}

@app.get("/api/metrics", response_model=List[Metric])
async def get_metrics(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get dashboard metrics from Athena data"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        # Convert month range to date range if provided
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            # Get last day of end month
            from datetime import datetime
            try:
                year, month = end_month.split('-')
                if month == '12':
                    last_day = 31
                else:
                    next_month = datetime(int(year), int(month) + 1, 1)
                    last_day = (next_month - timedelta(days=1)).day
                end_date = f"{end_month}-{last_day:02d}"
            except:
                end_date = f"{end_month}-31"
        
        metrics = athena.get_metrics_from_athena(start_date=start_date, end_date=end_date)
        return metrics
    except Exception as e:
        # Fallback to empty metrics on error
        return [
            {"label": "Visits", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Notes from Scribe", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Notes without Scribe", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Note Content from Scribe", "value": 0.0, "change": 0.0, "trend": "neutral"},
            {"label": "Total Time", "value": "0 min", "change": 0.0, "trend": "neutral"}
        ]

@app.get("/api/top-users", response_model=List[TopUser])
async def get_top_users(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get top users data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        users = athena.get_top_users_from_athena(limit=8)
        return users
    except Exception as e:
        return []

@app.get("/api/active-users", response_model=ActiveUsersData)
async def get_active_users(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get active vs enabled users from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        return athena.get_active_users_from_athena()
    except Exception as e:
        return {"active": 0, "enabled": 0}

@app.get("/api/staff-speaking", response_model=StaffSpeakingData)
async def get_staff_speaking(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get staff speaking data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        return athena.get_staff_speaking_from_athena()
    except Exception as e:
        return {"staff": 0, "nonStaff": 0}

@app.get("/api/times", response_model=List[TimesData])
async def get_times(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get times data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        times = athena.get_times_data_from_athena()
        return times
    except Exception as e:
        return []

@app.get("/api/consents", response_model=ConsentsData)
async def get_consents(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get consents data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        return athena.get_consents_from_athena()
    except Exception as e:
        return {"listening": 0, "dictation": 0}

@app.get("/api/sales", response_model=List[SalesData])
async def get_sales_data():
    """Get sales data for the last 30 days"""
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "sales": round(random.uniform(1000, 5000), 2),
            "orders": random.randint(50, 200)
        })
    
    return data

@app.get("/api/revenue", response_model=List[RevenueData])
async def get_revenue_data():
    """Get monthly revenue data"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data = []
    
    for month in months:
        data.append({
            "month": month,
            "revenue": round(random.uniform(20000, 60000), 2),
            "profit": round(random.uniform(5000, 20000), 2)
        })
    
    return data

@app.get("/api/activity", response_model=List[UserActivity])
async def get_user_activity():
    """Get hourly user activity"""
    data = []
    for hour in range(24):
        data.append({
            "hour": hour,
            "active_users": random.randint(100, 500)
        })
    
    return data

@app.get("/api/filter-options")
async def get_filter_options():
    """Get unique values for filters from Athena data"""
    try:
        athena = AthenaService()
        return athena.get_filter_options_from_athena()
    except Exception as e:
        print(f"Error in get_filter_options: {e}")
        return {
            "practitioners": [],
            "programs": [],
            "locations": []
        }

@app.get("/api/audit-summary", response_model=List[AuditItem])
async def get_audit_summary(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get audit summary data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        # Convert month to date if needed
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{end_month}-31"
        
        # Build query
        query = f"SELECT * FROM {athena.athena_table} WHERE 1=1"
        
        if start_date:
            query += f" AND audit_datetime >= TIMESTAMP '{start_date} 00:00:00'"
        if end_date:
            query += f" AND audit_datetime <= TIMESTAMP '{end_date} 23:59:59'"
        if practitioner:
            query += f" AND user_id = '{practitioner}'"
        if program:
            query += f" AND tenant_id = '{program}'"
        if location:
            query += f" AND tenant_id = '{location}'"
        
        query += " ORDER BY audit_datetime DESC LIMIT 100"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        return [
            {
                "date": d.get('audit_datetime', ''),
                "action": d.get('event_name', ''),
                "user": d.get('user_id', ''),
                "status": d.get('status', ''),
                "details": f"Patient: {d.get('patient_name', 'N/A')}"
            }
            for d in data
        ]
    except Exception as e:
        return []

@app.get("/api/patient-access", response_model=List[PatientAccessItem])
async def get_patient_access(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get patient access data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{end_month}-31"
        
        query = f"SELECT * FROM {athena.athena_table} WHERE patient_id IS NOT NULL"
        
        if start_date:
            query += f" AND audit_datetime >= TIMESTAMP '{start_date} 00:00:00'"
        if end_date:
            query += f" AND audit_datetime <= TIMESTAMP '{end_date} 23:59:59'"
        if practitioner:
            query += f" AND user_id = '{practitioner}'"
        if program:
            query += f" AND tenant_id = '{program}'"
        if location:
            query += f" AND tenant_id = '{location}'"
        
        query += " ORDER BY audit_datetime DESC LIMIT 100"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        return [
            {
                "patientId": d.get('patient_id', ''),
                "patientName": d.get('patient_name', ''),
                "accessDate": d.get('audit_datetime', ''),
                "accessType": d.get('event_name', 'Access'),
                "duration": f"{float(d.get('audio_duration', 0) or 0) / 60:.1f} min"
            }
            for d in data
        ]
    except Exception as e:
        return []

@app.get("/api/patient-service-usage", response_model=List[ServiceUsageItem])
async def get_patient_service_usage():
    """Get patient service usage data from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        query = f"""
        SELECT 
            note_format as service_name,
            COUNT(*) as usage_count,
            SUM(CAST(audio_duration AS double)) as total_duration,
            MAX(audit_datetime) as last_used
        FROM {athena.athena_table}
        WHERE note_format IS NOT NULL
        GROUP BY note_format
        ORDER BY usage_count DESC
        """
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        services = []
        for d in data:
            duration_sec = float(d.get('total_duration', 0) or 0)
            hours = int(duration_sec / 3600)
            mins = int((duration_sec % 3600) / 60)
            total_time = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
            
            services.append({
                "serviceName": d.get('service_name', 'Unknown'),
                "usageCount": int(d.get('usage_count', 0) or 0),
                "totalTime": total_time,
                "lastUsed": d.get('last_used', '')
            })
        
        return services
    except Exception as e:
        return []

@app.get("/api/recommendation-summary", response_model=List[RecommendationItem])
async def get_recommendation_summary(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get recommendation summary from Athena (based on similarity scores)"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{end_month}-31"
        
        # Get records with low similarity (needs attention)
        query = f"""
        SELECT 
            care_record_id as id,
            'Low Similarity' as type,
            CASE 
                WHEN CAST(similarity AS double) < 0.1 THEN 'high'
                WHEN CAST(similarity AS double) < 0.3 THEN 'medium'
                ELSE 'low'
            END as priority,
            status,
            creation_datetime as created_date
        FROM {athena.athena_table}
        WHERE similarity IS NOT NULL
        """
        
        if start_date:
            query += f" AND creation_datetime >= TIMESTAMP '{start_date} 00:00:00'"
        if end_date:
            query += f" AND creation_datetime <= TIMESTAMP '{end_date} 23:59:59'"
        
        query += " ORDER BY CAST(similarity AS double) ASC LIMIT 100"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        return [
            {
                "id": d.get('id', ''),
                "type": d.get('type', 'Recommendation'),
                "priority": d.get('priority', 'medium'),
                "status": d.get('status', 'pending'),
                "createdDate": d.get('created_date', '')
            }
            for d in data
        ]
    except Exception as e:
        return []

@app.get("/api/delivery-schedules", response_model=List[DeliveryScheduleItem])
async def get_delivery_schedules():
    """Get report delivery schedules (static data - can be enhanced)"""
    # This is a static endpoint - can be enhanced to pull from Athena if needed
    return [
        {
            "reportName": "Audit Summary",
            "frequency": "Daily",
            "nextDelivery": "Tomorrow",
            "status": "Active"
        },
        {
            "reportName": "Patient Access Report",
            "frequency": "Weekly",
            "nextDelivery": "Next Monday",
            "status": "Active"
        }
    ]

@app.get("/api/signed-notes", response_model=List[SignedNoteItem])
async def get_signed_notes(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get signed notes data from Athena (FINALIZED status)"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{end_month}-31"
        
        query = f"SELECT * FROM {athena.athena_table} WHERE status = 'FINALIZED'"
        
        if start_date:
            query += f" AND completed_datetime >= TIMESTAMP '{start_date} 00:00:00'"
        if end_date:
            query += f" AND completed_datetime <= TIMESTAMP '{end_date} 23:59:59'"
        if practitioner:
            query += f" AND user_id = '{practitioner}'"
        if program:
            query += f" AND tenant_id = '{program}'"
        if location:
            query += f" AND tenant_id = '{location}'"
        
        query += " ORDER BY completed_datetime DESC LIMIT 100"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        return [
            {
                "noteId": d.get('care_record_id', ''),
                "patientName": d.get('patient_name', ''),
                "practitioner": d.get('user_id', ''),
                "signedDate": d.get('completed_datetime', ''),
                "status": d.get('status', 'FINALIZED')
            }
            for d in data
        ]
    except Exception as e:
        return []

@app.get("/api/practitioner-service-usage", response_model=List[PractitionerUsageItem])
async def get_practitioner_service_usage(
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get practitioner service usage from Athena"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        query = f"""
        SELECT 
            user_id,
            COUNT(*) as visits,
            SUM(CAST(audio_duration AS double)) as total_duration,
            MAX(audit_datetime) as last_active
        FROM {athena.athena_table}
        WHERE user_id IS NOT NULL
        """
        
        if practitioner:
            query += f" AND user_id = '{practitioner}'"
        if program:
            query += f" AND tenant_id = '{program}'"
        if location:
            query += f" AND tenant_id = '{location}'"
        
        query += " GROUP BY user_id ORDER BY visits DESC LIMIT 50"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        practitioners = []
        for d in data:
            duration_sec = float(d.get('total_duration', 0) or 0)
            hours = int(duration_sec / 3600)
            mins = int((duration_sec % 3600) / 60)
            total_time = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
            
            practitioners.append({
                "practitionerName": f"User {d.get('user_id', 'Unknown')}",
                "visits": int(d.get('visits', 0) or 0),
                "totalTime": total_time,
                "lastActive": d.get('last_active', '')
            })
        
        return practitioners
    except Exception as e:
        return []

@app.get("/api/sync-issues", response_model=List[SyncIssueItem])
async def get_sync_issues(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get sync issues from Athena (sessions with errors or issues)"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{end_month}-31"
        
        # Find records with potential issues (no completion, missing data, etc.)
        query = f"""
        SELECT 
            care_record_id as id,
            event_name as type,
            status,
            audit_datetime as reported_date
        FROM {athena.athena_table}
        WHERE (completed_datetime IS NULL 
           OR status != 'FINALIZED'
           OR audio_duration IS NULL)
        """
        
        if start_date:
            query += f" AND audit_datetime >= TIMESTAMP '{start_date} 00:00:00'"
        if end_date:
            query += f" AND audit_datetime <= TIMESTAMP '{end_date} 23:59:59'"
        
        query += " ORDER BY audit_datetime DESC LIMIT 100"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        return [
            {
                "id": d.get('id', ''),
                "type": d.get('type', 'Sync Issue'),
                "severity": "medium",
                "status": d.get('status', 'pending'),
                "reportedDate": d.get('reported_date', '')
            }
            for d in data
        ]
    except Exception as e:
        return []

@app.get("/api/unsigned-notes", response_model=List[UnsignedNoteItem])
async def get_unsigned_notes(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get unsigned notes data from Athena (non-FINALIZED status)"""
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{end_month}-31"
        
        query = f"SELECT * FROM {athena.athena_table} WHERE status != 'FINALIZED' OR status IS NULL"
        
        if start_date:
            query += f" AND creation_datetime >= TIMESTAMP '{start_date} 00:00:00'"
        if end_date:
            query += f" AND creation_datetime <= TIMESTAMP '{end_date} 23:59:59'"
        if practitioner:
            query += f" AND user_id = '{practitioner}'"
        if program:
            query += f" AND tenant_id = '{program}'"
        if location:
            query += f" AND tenant_id = '{location}'"
        
        query += " ORDER BY creation_datetime DESC LIMIT 100"
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        # Calculate days pending
        unsigned_notes = []
        for d in data:
            created = d.get('creation_datetime', '')
            days_pending = 0
            if created:
                try:
                    from datetime import datetime
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    days_pending = (datetime.now(created_dt.tzinfo) - created_dt).days
                except:
                    pass
            
            unsigned_notes.append({
                "noteId": d.get('care_record_id', ''),
                "patientName": d.get('patient_name', ''),
                "practitioner": d.get('user_id', ''),
                "createdDate": created,
                "daysPending": days_pending
            })
        
        return sorted(unsigned_notes, key=lambda x: x['daysPending'], reverse=True)
    except Exception as e:
        return []

# Athena endpoints for querying processed data from S3
@app.get("/api/athena/data")
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
        from athena_service import AthenaService
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

@app.get("/api/athena/summary")
async def get_athena_summary():
    """
    Get summary statistics from ALL Parquet files in Athena
    """
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        stats = athena.get_data_statistics()
        
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "stats": {}
        }

@app.post("/api/athena/query")
async def execute_athena_query(query: str):
    """
    Execute a custom Athena query
    Note: Use with caution, only allow trusted queries in production
    """
    try:
        from athena_service import AthenaService
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

@app.get("/api/athena/all-data")
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
        from athena_service import AthenaService
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
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "count": 0,
            "data": []
        }

@app.get("/api/athena/verify-files")
async def verify_s3_parquet_files():
    """
    Verify all Parquet files in S3 are accessible
    Lists all .parquet files in the configured S3 location
    """
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        verification = athena.verify_s3_files()
        
        return {
            "success": True,
            "verification": verification
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "verification": {}
        }

@app.get("/api/athena/repair-table")
async def repair_athena_table():
    """
    Repair Athena table metadata to ensure all Parquet files are detected
    Run this after uploading new Parquet files to S3
    """
    try:
        from athena_service import AthenaService
        athena = AthenaService()
        
        repair_result = athena.repair_table_metadata()
        
        return {
            "success": True,
            "repair": repair_result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "repair": {}
        }

@app.get("/api/athena/dashboard")
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
        from athena_service import AthenaService
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
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "count": 0,
            "data": []
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

