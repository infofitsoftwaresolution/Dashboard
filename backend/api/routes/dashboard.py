"""
Dashboard API routes
All endpoints related to dashboard metrics, charts, and reports
"""
from fastapi import APIRouter
from typing import List
from datetime import datetime, timedelta

from api.models import (
    Metric, TopUser, ActiveUsersData, StaffSpeakingData, TimesData, ConsentsData,
    SalesData, RevenueData, UserActivity, AuditItem, PatientAccessItem,
    ServiceUsageItem, RecommendationItem, DeliveryScheduleItem, SignedNoteItem,
    PractitionerUsageItem, SyncIssueItem, UnsignedNoteItem
)
from database_service import DatabaseService

router = APIRouter()
db_service = DatabaseService()

@router.get("/metrics", response_model=List[Metric])
async def get_metrics(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get dashboard metrics from PostgreSQL database"""
    try:
        db = DatabaseService()
        
        # Convert month range to date range if provided
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
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
        
        data = db.get_all_data(start_date=start_date, end_date=end_date)
        total_count = len(data)
        completed = len([d for d in data if d.get('status') in ['completed', 'FINALIZED']])
        
        return [
            {"label": "Total Records", "value": total_count, "change": 0.0, "trend": "neutral"},
            {"label": "Completed Notes", "value": completed, "change": 0.0, "trend": "neutral"},
            {"label": "Pending Notes", "value": total_count - completed, "change": 0.0, "trend": "neutral"},
            {"label": "Unique Patients", "value": len(set([d.get('patient_id') for d in data if d.get('patient_id')])), "change": 0.0, "trend": "neutral"},
            {"label": "Total Records", "value": total_count, "change": 0.0, "trend": "neutral"}
        ]
    except Exception as e:
        print(f"Error in get_metrics: {e}")
        return [
            {"label": "Visits", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Notes from Scribe", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Notes without Scribe", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Note Content from Scribe", "value": 0.0, "change": 0.0, "trend": "neutral"},
            {"label": "Total Time", "value": "0 min", "change": 0.0, "trend": "neutral"}
        ]

@router.get("/top-users", response_model=List[TopUser])
async def get_top_users(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get top users data from PostgreSQL"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=1000)
        # Group by user_id and count visits
        user_counts = {}
        for record in data:
            user_id = record.get('user_id', 'Unknown')
            if user_id not in user_counts:
                user_counts[user_id] = 0
            user_counts[user_id] += 1
        
        # Sort and return top 8
        top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        return [
            {"name": f"User {user_id}", "visits": count, "totalTime": "0 min"}
            for user_id, count in top_users
        ]
    except Exception as e:
        print(f"Error in get_top_users: {e}")
        return []

@router.get("/active-users", response_model=ActiveUsersData)
async def get_active_users(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get active vs enabled users from Athena"""
    try:
        athena = AthenaService()
        return athena.get_active_users_from_athena()
    except Exception as e:
        return {"active": 0, "enabled": 0}

@router.get("/staff-speaking", response_model=StaffSpeakingData)
async def get_staff_speaking(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get staff speaking data from Athena"""
    try:
        athena = AthenaService()
        return athena.get_staff_speaking_from_athena()
    except Exception as e:
        return {"staff": 0, "nonStaff": 0}

@router.get("/times", response_model=List[TimesData])
async def get_times(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get times data from Athena"""
    try:
        athena = AthenaService()
        times = athena.get_times_data_from_athena()
        return times
    except Exception as e:
        return []

@router.get("/consents", response_model=ConsentsData)
async def get_consents(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get consents data from Athena"""
    try:
        athena = AthenaService()
        return athena.get_consents_from_athena()
    except Exception as e:
        return {"listening": 0, "dictation": 0}

@router.get("/sales", response_model=List[SalesData])
async def get_sales_data(
    start_date: str = None,
    end_date: str = None
):
    """Get sales data from Athena (daily session counts and orders)"""
    try:
        athena = AthenaService()
        
        # Default to last 30 days if no dates provided
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        query = f"""
        SELECT 
            date(audit_datetime) as date,
            COUNT(*) as orders,
            SUM(CAST(audio_duration AS double)) / 60.0 as sales
        FROM {athena.athena_table}
        WHERE audit_datetime >= TIMESTAMP '{start_date} 00:00:00'
          AND audit_datetime <= TIMESTAMP '{end_date} 23:59:59'
        GROUP BY date(audit_datetime)
        ORDER BY date ASC
        """
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        return [
            {
                "date": d.get('date', ''),
                "sales": round(float(d.get('sales', 0) or 0), 2),
                "orders": int(d.get('orders', 0) or 0)
            }
            for d in data
        ]
    except Exception as e:
        return []

@router.get("/revenue", response_model=List[RevenueData])
async def get_revenue_data(
    start_date: str = None,
    end_date: str = None
):
    """Get monthly revenue data from Athena"""
    try:
        athena = AthenaService()
        
        # Default to last 12 months if no dates provided
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        query = f"""
        SELECT 
            date_format(date(audit_datetime), '%Y-%m') as month_key,
            COUNT(*) as revenue,
            SUM(CASE WHEN status = 'FINALIZED' THEN 1 ELSE 0 END) as profit
        FROM {athena.athena_table}
        WHERE audit_datetime >= TIMESTAMP '{start_date} 00:00:00'
          AND audit_datetime <= TIMESTAMP '{end_date} 23:59:59'
        GROUP BY date_format(date(audit_datetime), '%Y-%m')
        ORDER BY month_key ASC
        """
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        revenue_data = []
        for d in data:
            month_key = d.get('month_key', '')
            if month_key:
                try:
                    year, month = month_key.split('-')
                    month_name = month_names[int(month) - 1]
                    revenue_data.append({
                        "month": f"{month_name} {year}",
                        "revenue": round(float(d.get('revenue', 0) or 0), 2),
                        "profit": round(float(d.get('profit', 0) or 0), 2)
                    })
                except:
                    pass
        
        return revenue_data
    except Exception as e:
        return []

@router.get("/activity", response_model=List[UserActivity])
async def get_user_activity(
    start_date: str = None,
    end_date: str = None
):
    """Get hourly user activity from Athena"""
    try:
        athena = AthenaService()
        
        # Default to last 7 days if no dates provided
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        query = f"""
        SELECT 
            hour(audit_datetime) as hour,
            COUNT(DISTINCT user_id) as active_users
        FROM {athena.athena_table}
        WHERE audit_datetime >= TIMESTAMP '{start_date} 00:00:00'
          AND audit_datetime <= TIMESTAMP '{end_date} 23:59:59'
          AND user_id IS NOT NULL
        GROUP BY hour(audit_datetime)
        ORDER BY hour ASC
        """
        
        result = athena.execute_query(query)
        data = result.get('results', [])
        
        # Create a map of hours to active users
        hour_map = {int(d.get('hour', 0)): int(d.get('active_users', 0) or 0) for d in data}
        
        # Fill in all 24 hours, using 0 for hours with no data
        activity_data = []
        for hour in range(24):
            activity_data.append({
                "hour": hour,
                "active_users": hour_map.get(hour, 0)
            })
        
        return activity_data
    except Exception as e:
        return []

@router.get("/filter-options")
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

@router.get("/audit-summary", response_model=List[AuditItem])
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
        athena = AthenaService()
        
        # Convert month to date if needed
        if start_month and end_month and not start_date and not end_date:
            start_date = f"{start_month}-01"
            end_date = f"{start_month}-31"
        
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

@router.get("/patient-access", response_model=List[PatientAccessItem])
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

@router.get("/patient-service-usage", response_model=List[ServiceUsageItem])
async def get_patient_service_usage():
    """Get patient service usage data from Athena"""
    try:
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

@router.get("/recommendation-summary", response_model=List[RecommendationItem])
async def get_recommendation_summary(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get recommendation summary from Athena (based on similarity scores)"""
    try:
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

@router.get("/delivery-schedules", response_model=List[DeliveryScheduleItem])
async def get_delivery_schedules():
    """Get report delivery schedules based on actual data patterns from Athena"""
    try:
        athena = AthenaService()
        
        # Get the latest audit date to determine next delivery
        query = f"""
        SELECT 
            MAX(audit_datetime) as last_audit,
            COUNT(*) as total_records,
            COUNT(DISTINCT date(audit_datetime)) as days_with_data
        FROM {athena.athena_table}
        """
        
        result = athena.execute_query(query)
        stats = result.get('results', [{}])[0] if result.get('results') else {}
        
        last_audit = stats.get('last_audit', '')
        total_records = int(stats.get('total_records', 0) or 0)
        days_with_data = int(stats.get('days_with_data', 0) or 0)
        
        # Calculate next delivery dates
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Find next Monday
        days_until_monday = (7 - datetime.now().weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = (datetime.now() + timedelta(days=days_until_monday)).strftime("%Y-%m-%d")
        
        schedules = []
        
        # Audit Summary - Daily if we have daily data
        if days_with_data > 0:
            schedules.append({
                "reportName": "Audit Summary",
                "frequency": "Daily" if days_with_data >= 7 else "Weekly",
                "nextDelivery": tomorrow if days_with_data >= 7 else next_monday,
                "status": "Active" if total_records > 0 else "Inactive"
            })
        
        # Patient Access Report - Based on patient data availability
        patient_query = f"""
        SELECT COUNT(DISTINCT patient_id) as unique_patients
        FROM {athena.athena_table}
        WHERE patient_id IS NOT NULL
        """
        patient_result = athena.execute_query(patient_query)
        patient_stats = patient_result.get('results', [{}])[0] if patient_result.get('results') else {}
        unique_patients = int(patient_stats.get('unique_patients', 0) or 0)
        
        if unique_patients > 0:
            schedules.append({
                "reportName": "Patient Access Report",
                "frequency": "Weekly",
                "nextDelivery": next_monday,
                "status": "Active"
            })
        
        # If no data, return empty list
        if not schedules:
            schedules.append({
                "reportName": "No Reports Available",
                "frequency": "N/A",
                "nextDelivery": "N/A",
                "status": "Inactive"
            })
        
        return schedules
    except Exception as e:
        # Fallback to basic schedule if query fails
        return [
            {
                "reportName": "Audit Summary",
                "frequency": "Daily",
                "nextDelivery": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "status": "Active"
            }
        ]

@router.get("/signed-notes", response_model=List[SignedNoteItem])
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

@router.get("/practitioner-service-usage", response_model=List[PractitionerUsageItem])
async def get_practitioner_service_usage(
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get practitioner service usage from Athena"""
    try:
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

@router.get("/sync-issues", response_model=List[SyncIssueItem])
async def get_sync_issues(
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get sync issues from Athena (sessions with errors or issues)"""
    try:
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

@router.get("/unsigned-notes", response_model=List[UnsignedNoteItem])
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

@router.get("/all-data")
async def get_all_dashboard_data(
    limit: int = None,
    start_date: str = None,
    end_date: str = None,
    status: str = None,
    user_id: str = None
):
    """Get all dashboard data from PostgreSQL"""
    try:
        data = db_service.get_all_data(
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

