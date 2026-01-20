"""
Dashboard API routes - Updated to use PostgreSQL instead of Athena
All endpoints now connect to PostgreSQL database
"""
from fastapi import APIRouter
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

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
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get dashboard metrics from PostgreSQL database"""
    try:
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
        
        data = db_service.get_all_data(start_date=start_date, end_date=end_date)
        total_count = len(data)
        completed = len([d for d in data if d.get('status') in ['completed', 'FINALIZED']])
        unique_patients = len(set([d.get('patient_id') for d in data if d.get('patient_id')]))
        
        return [
            {"label": "Total Records", "value": total_count, "change": 0.0, "trend": "neutral"},
            {"label": "Completed Notes", "value": completed, "change": 0.0, "trend": "neutral"},
            {"label": "Pending Notes", "value": total_count - completed, "change": 0.0, "trend": "neutral"},
            {"label": "Unique Patients", "value": unique_patients, "change": 0.0, "trend": "neutral"},
            {"label": "Total Users", "value": len(set([d.get('user_id') for d in data if d.get('user_id')])), "change": 0.0, "trend": "neutral"}
        ]
    except Exception as e:
        print(f"Error in get_metrics: {e}")
        return [
            {"label": "Total Records", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Completed Notes", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Pending Notes", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Unique Patients", "value": 0, "change": 0.0, "trend": "neutral"},
            {"label": "Total Users", "value": 0, "change": 0.0, "trend": "neutral"}
        ]

@router.get("/top-users", response_model=List[TopUser])
async def get_top_users(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get top users data from PostgreSQL"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        # Group by user_id and count visits
        user_counts = {}
        for record in data:
            user_id = record.get('user_id', 'Unknown')
            if user_id and user_id != 'Unknown':
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
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get active vs enabled users from PostgreSQL"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        unique_users = len(set([d.get('user_id') for d in data if d.get('user_id')]))
        total_records = len(data)
        return {"active": unique_users, "enabled": total_records}
    except Exception as e:
        print(f"Error in get_active_users: {e}")
        return {"active": 0, "enabled": 0}

@router.get("/staff-speaking", response_model=StaffSpeakingData)
async def get_staff_speaking(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get staff speaking data from PostgreSQL"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        # Simple logic: count records with user_id as staff, others as non-staff
        staff_count = len([d for d in data if d.get('user_id')])
        non_staff_count = len([d for d in data if not d.get('user_id')])
        return {"staff": staff_count, "nonStaff": non_staff_count}
    except Exception as e:
        print(f"Error in get_staff_speaking: {e}")
        return {"staff": 0, "nonStaff": 0}

@router.get("/times", response_model=List[TimesData])
async def get_times(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get times data from PostgreSQL"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        # Group by month
        monthly_data = defaultdict(lambda: {'count': 0})
        
        for record in data:
            if record.get('audit_datetime'):
                try:
                    dt_str = str(record.get('audit_datetime'))
                    if 'T' in dt_str:
                        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                    month_key = dt.strftime('%Y-%m')
                    monthly_data[month_key]['count'] += 1
                except:
                    pass
        
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        times_data = []
        for month_key, values in sorted(monthly_data.items()):
            try:
                year, month = month_key.split('-')
                month_name = month_names[int(month) - 1]
                times_data.append({
                    "month": f"{month_name} {year}",
                    "recording": 0.0,
                    "processing": 0.0,
                    "createdToSign": 0.0
                })
            except:
                pass
        
        return times_data[-12:]  # Return last 12 months
    except Exception as e:
        print(f"Error in get_times: {e}")
        return []

@router.get("/consents", response_model=ConsentsData)
async def get_consents(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get consents data from PostgreSQL"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        # Count based on event types or status
        listening = len([d for d in data if 'listening' in str(d.get('event_name', '')).lower()])
        dictation = len([d for d in data if 'dictation' in str(d.get('event_name', '')).lower()])
        return {"listening": listening, "dictation": dictation}
    except Exception as e:
        print(f"Error in get_consents: {e}")
        return {"listening": 0, "dictation": 0}

@router.get("/sales", response_model=List[SalesData])
async def get_sales_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get sales data from PostgreSQL (daily session counts and orders)"""
    try:
        # Default to last 30 days if no dates provided
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=100000)
        
        # Group by date
        daily_data = defaultdict(lambda: {'orders': 0, 'sales': 0.0})
        
        for record in data:
            if record.get('audit_datetime'):
                try:
                    dt_str = str(record.get('audit_datetime'))
                    if 'T' in dt_str:
                        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                    date_key = dt.strftime('%Y-%m-%d')
                    daily_data[date_key]['orders'] += 1
                    # Add audio duration if available
                    audio_dur = record.get('audio_duration')
                    if audio_dur:
                        try:
                            daily_data[date_key]['sales'] += float(audio_dur) / 60.0
                        except:
                            pass
                except:
                    pass
        
        return [
            {
                "date": date_key,
                "sales": round(values['sales'], 2),
                "orders": values['orders']
            }
            for date_key, values in sorted(daily_data.items())
        ]
    except Exception as e:
        print(f"Error in get_sales_data: {e}")
        return []

@router.get("/revenue", response_model=List[RevenueData])
async def get_revenue_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get monthly revenue data from PostgreSQL"""
    try:
        # Default to last 12 months if no dates provided
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=100000)
        
        # Group by month
        monthly_data = defaultdict(lambda: {'revenue': 0, 'profit': 0})
        
        for record in data:
            if record.get('audit_datetime'):
                try:
                    dt_str = str(record.get('audit_datetime'))
                    if 'T' in dt_str:
                        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                    month_key = dt.strftime('%Y-%m')
                    monthly_data[month_key]['revenue'] += 1
                    if record.get('status') in ['FINALIZED', 'completed']:
                        monthly_data[month_key]['profit'] += 1
                except:
                    pass
        
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        revenue_data = []
        for month_key, values in sorted(monthly_data.items()):
            try:
                year, month = month_key.split('-')
                month_name = month_names[int(month) - 1]
                revenue_data.append({
                    "month": f"{month_name} {year}",
                    "revenue": round(float(values['revenue']), 2),
                    "profit": round(float(values['profit']), 2)
                })
            except:
                pass
        
        return revenue_data
    except Exception as e:
        print(f"Error in get_revenue_data: {e}")
        return []

@router.get("/activity", response_model=List[UserActivity])
async def get_user_activity(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get hourly user activity from PostgreSQL"""
    try:
        # Default to last 7 days if no dates provided
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=100000)
        
        # Group by hour
        hour_users = defaultdict(set)
        
        for record in data:
            user_id = record.get('user_id')
            if user_id and record.get('audit_datetime'):
                try:
                    dt_str = str(record.get('audit_datetime'))
                    if 'T' in dt_str:
                        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                    hour = dt.hour
                    hour_users[hour].add(user_id)
                except:
                    pass
        
        # Fill in all 24 hours
        activity_data = []
        for hour in range(24):
            activity_data.append({
                "hour": hour,
                "active_users": len(hour_users.get(hour, set()))
            })
        
        return activity_data
    except Exception as e:
        print(f"Error in get_user_activity: {e}")
        return []

@router.get("/filter-options")
async def get_filter_options():
    """Get unique values for filters from PostgreSQL data"""
    try:
        data = db_service.get_all_data(limit=10000)
        practitioners = sorted(set([d.get('user_id') for d in data if d.get('user_id')]))
        programs = sorted(set([d.get('tenant_id') for d in data if d.get('tenant_id')]))
        locations = sorted(set([d.get('tenant_id') for d in data if d.get('tenant_id')]))
        
        return {
            "practitioners": practitioners,
            "programs": programs,
            "locations": locations
        }
    except Exception as e:
        print(f"Error in get_filter_options: {e}")
        return {
            "practitioners": [],
            "programs": [],
            "locations": []
        }

@router.get("/audit-summary", response_model=List[AuditItem])
async def get_audit_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None,
    practitioner: Optional[str] = None,
    program: Optional[str] = None,
    location: Optional[str] = None
):
    """Get audit summary data from PostgreSQL"""
    try:
        data = db_service.get_all_data(
            start_date=start_date,
            end_date=end_date,
            status=None,
            user_id=practitioner,
            limit=100
        )
        
        # Apply additional filters
        if program:
            data = [d for d in data if d.get('tenant_id') == program]
        if location:
            data = [d for d in data if d.get('tenant_id') == location]
        
        # Remove duplicates based on unique identifier
        # Use care_record_id as the unique identifier (it's unique per record)
        # If care_record_id is not available, use audit_datetime + user_id + patient_id combination
        seen = set()
        unique_data = []
        for d in data:
            # Use care_record_id as unique identifier (it's unique per session/record)
            care_record_id = d.get('care_record_id')
            if care_record_id and care_record_id.strip():
                unique_key = care_record_id
            else:
                # Fallback: use combination that includes timestamp to ensure uniqueness
                unique_key = f"{d.get('audit_datetime')}_{d.get('user_id')}_{d.get('patient_id')}_{d.get('event_name')}"
            
            if unique_key and unique_key not in seen:
                seen.add(unique_key)
                unique_data.append({
                    "date": str(d.get('audit_datetime', '')),
                    "action": str(d.get('event_name', '')),
                    "user": str(d.get('user_id', '')),
                    "status": str(d.get('status', '')),
                    "details": f"Patient: {d.get('patient_name', 'N/A')}"
                })
        
        return unique_data[:100]
    except Exception as e:
        print(f"Error in get_audit_summary: {e}")
        return []

@router.get("/patient-access", response_model=List[PatientAccessItem])
async def get_patient_access(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None,
    practitioner: Optional[str] = None,
    program: Optional[str] = None,
    location: Optional[str] = None
):
    """Get patient access data from PostgreSQL"""
    try:
        data = db_service.get_all_data(
            start_date=start_date,
            end_date=end_date,
            user_id=practitioner,
            limit=10000
        )
        
        # Filter for patient records
        patient_data = [d for d in data if d.get('patient_id')]
        
        # Apply additional filters
        if program:
            patient_data = [d for d in patient_data if d.get('tenant_id') == program]
        if location:
            patient_data = [d for d in patient_data if d.get('tenant_id') == location]
        
        return [
            {
                "patientId": str(d.get('patient_id', '')),
                "patientName": str(d.get('patient_name', '')),
                "accessDate": str(d.get('audit_datetime', '')),
                "accessType": str(d.get('event_name', 'Access')),
                "duration": f"{float(d.get('audio_duration', 0) or 0) / 60:.1f} min"
            }
            for d in patient_data[:100]
        ]
    except Exception as e:
        print(f"Error in get_patient_access: {e}")
        return []

@router.get("/patient-service-usage", response_model=List[ServiceUsageItem])
async def get_patient_service_usage():
    """Get patient service usage data from PostgreSQL"""
    try:
        data = db_service.get_all_data(limit=10000)
        
        # Group by note_format
        service_counts = defaultdict(lambda: {'count': 0, 'duration': 0.0, 'last_used': None})
        
        for record in data:
            service = record.get('note_format', 'Unknown')
            service_counts[service]['count'] += 1
            audio_dur = record.get('audio_duration')
            if audio_dur:
                try:
                    service_counts[service]['duration'] += float(audio_dur)
                except:
                    pass
            audit_dt = record.get('audit_datetime')
            if audit_dt:
                service_counts[service]['last_used'] = str(audit_dt)
        
        services = []
        for service, values in sorted(service_counts.items(), key=lambda x: x[1]['count'], reverse=True):
            duration_sec = values['duration']
            hours = int(duration_sec / 3600)
            mins = int((duration_sec % 3600) / 60)
            total_time = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
            
            services.append({
                "serviceName": service,
                "usageCount": values['count'],
                "totalTime": total_time,
                "lastUsed": values['last_used'] or ''
            })
        
        return services
    except Exception as e:
        print(f"Error in get_patient_service_usage: {e}")
        return []

@router.get("/recommendation-summary", response_model=List[RecommendationItem])
async def get_recommendation_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get recommendation summary from PostgreSQL (based on similarity scores)"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        
        # Filter records with similarity data
        recommendations = []
        for record in data:
            similarity = record.get('similarity')
            if similarity:
                try:
                    sim_value = float(similarity)
                    priority = 'high' if sim_value < 0.1 else ('medium' if sim_value < 0.3 else 'low')
                    recommendations.append({
                        "id": str(record.get('care_record_id', record.get('pk', ''))),
                        "type": "Low Similarity",
                        "priority": priority,
                        "status": str(record.get('status', 'pending')),
                        "createdDate": str(record.get('creation_datetime', ''))
                    })
                except:
                    pass
        
        return sorted(recommendations, key=lambda x: x.get('priority', 'low'))[:100]
    except Exception as e:
        print(f"Error in get_recommendation_summary: {e}")
        return []

@router.get("/delivery-schedules", response_model=List[DeliveryScheduleItem])
async def get_delivery_schedules():
    """Get report delivery schedules based on actual data patterns from PostgreSQL"""
    try:
        data = db_service.get_all_data(limit=10000)
        
        if not data:
            return [{
                "reportName": "No Reports Available",
                "frequency": "N/A",
                "nextDelivery": "N/A",
                "status": "Inactive"
            }]
        
        # Calculate next delivery dates
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        days_until_monday = (7 - datetime.now().weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = (datetime.now() + timedelta(days=days_until_monday)).strftime("%Y-%m-%d")
        
        schedules = []
        
        # Check if we have daily data
        unique_dates = len(set([str(d.get('audit_datetime', ''))[:10] for d in data if d.get('audit_datetime')]))
        
        if unique_dates > 0:
            schedules.append({
                "reportName": "Audit Summary",
                "frequency": "Daily" if unique_dates >= 7 else "Weekly",
                "nextDelivery": tomorrow if unique_dates >= 7 else next_monday,
                "status": "Active"
            })
        
        # Check for patient data
        unique_patients = len(set([d.get('patient_id') for d in data if d.get('patient_id')]))
        if unique_patients > 0:
            schedules.append({
                "reportName": "Patient Access Report",
                "frequency": "Weekly",
                "nextDelivery": next_monday,
                "status": "Active"
            })
        
        return schedules if schedules else [{
            "reportName": "No Reports Available",
            "frequency": "N/A",
            "nextDelivery": "N/A",
            "status": "Inactive"
        }]
    except Exception as e:
        print(f"Error in get_delivery_schedules: {e}")
        return [{
            "reportName": "Audit Summary",
            "frequency": "Daily",
            "nextDelivery": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": "Active"
        }]

@router.get("/signed-notes", response_model=List[SignedNoteItem])
async def get_signed_notes(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None,
    practitioner: Optional[str] = None,
    program: Optional[str] = None,
    location: Optional[str] = None
):
    """Get signed notes data from PostgreSQL (FINALIZED status)"""
    try:
        data = db_service.get_all_data(
            start_date=start_date,
            end_date=end_date,
            status='FINALIZED',
            user_id=practitioner,
            limit=100
        )
        
        # Apply additional filters
        if program:
            data = [d for d in data if d.get('tenant_id') == program]
        if location:
            data = [d for d in data if d.get('tenant_id') == location]
        
        return [
            {
                "noteId": str(d.get('care_record_id', '')),
                "patientName": str(d.get('patient_name', '')),
                "practitioner": str(d.get('user_id', '')),
                "signedDate": str(d.get('completed_datetime', '')),
                "status": str(d.get('status', 'FINALIZED'))
            }
            for d in data[:100]
        ]
    except Exception as e:
        print(f"Error in get_signed_notes: {e}")
        return []

@router.get("/practitioner-service-usage", response_model=List[PractitionerUsageItem])
async def get_practitioner_service_usage(
    practitioner: Optional[str] = None,
    program: Optional[str] = None,
    location: Optional[str] = None
):
    """Get practitioner service usage from PostgreSQL"""
    try:
        data = db_service.get_all_data(user_id=practitioner, limit=10000)
        
        # Apply filters
        if program:
            data = [d for d in data if d.get('tenant_id') == program]
        if location:
            data = [d for d in data if d.get('tenant_id') == location]
        
        # Group by user_id
        practitioner_data = defaultdict(lambda: {'visits': 0, 'duration': 0.0, 'last_active': None})
        
        for record in data:
            user_id = record.get('user_id')
            if user_id:
                practitioner_data[user_id]['visits'] += 1
                audio_dur = record.get('audio_duration')
                if audio_dur:
                    try:
                        practitioner_data[user_id]['duration'] += float(audio_dur)
                    except:
                        pass
                audit_dt = record.get('audit_datetime')
                if audit_dt:
                    practitioner_data[user_id]['last_active'] = str(audit_dt)
        
        practitioners = []
        for user_id, values in sorted(practitioner_data.items(), key=lambda x: x[1]['visits'], reverse=True)[:50]:
            duration_sec = values['duration']
            hours = int(duration_sec / 3600)
            mins = int((duration_sec % 3600) / 60)
            total_time = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
            
            practitioners.append({
                "practitionerName": f"User {user_id}",
                "visits": values['visits'],
                "totalTime": total_time,
                "lastActive": values['last_active'] or ''
            })
        
        return practitioners
    except Exception as e:
        print(f"Error in get_practitioner_service_usage: {e}")
        return []

@router.get("/sync-issues", response_model=List[SyncIssueItem])
async def get_sync_issues(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None
):
    """Get sync issues from PostgreSQL (sessions with errors or issues)"""
    try:
        data = db_service.get_all_data(start_date=start_date, end_date=end_date, limit=10000)
        
        # Find records with potential issues
        issues = []
        for record in data:
            if (not record.get('completed_datetime') or 
                record.get('status') not in ['FINALIZED', 'completed'] or
                not record.get('audio_duration')):
                issues.append({
                    "id": str(record.get('care_record_id', record.get('pk', ''))),
                    "type": str(record.get('event_name', 'Sync Issue')),
                    "severity": "medium",
                    "status": str(record.get('status', 'pending')),
                    "reportedDate": str(record.get('audit_datetime', ''))
                })
        
        return issues[:100]
    except Exception as e:
        print(f"Error in get_sync_issues: {e}")
        return []

@router.get("/unsigned-notes", response_model=List[UnsignedNoteItem])
async def get_unsigned_notes(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    start_month: Optional[str] = None,
    end_month: Optional[str] = None,
    practitioner: Optional[str] = None,
    program: Optional[str] = None,
    location: Optional[str] = None
):
    """Get unsigned notes data from PostgreSQL (non-FINALIZED status)"""
    try:
        data = db_service.get_all_data(
            start_date=start_date,
            end_date=end_date,
            user_id=practitioner,
            limit=10000
        )
        
        # Filter non-FINALIZED records
        unsigned = [d for d in data if d.get('status') not in ['FINALIZED', 'completed']]
        
        # Apply additional filters
        if program:
            unsigned = [d for d in unsigned if d.get('tenant_id') == program]
        if location:
            unsigned = [d for d in unsigned if d.get('tenant_id') == location]
        
        # Calculate days pending
        unsigned_notes = []
        for d in unsigned:
            created = d.get('creation_datetime')
            days_pending = 0
            if created:
                try:
                    created_str = str(created)
                    if 'T' in created_str:
                        created_dt = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                    else:
                        created_dt = datetime.strptime(created_str, '%Y-%m-%d %H:%M:%S')
                    days_pending = (datetime.now(created_dt.tzinfo) - created_dt).days
                except:
                    pass
            
            unsigned_notes.append({
                "noteId": str(d.get('care_record_id', '')),
                "patientName": str(d.get('patient_name', '')),
                "practitioner": str(d.get('user_id', '')),
                "createdDate": str(created),
                "daysPending": days_pending
            })
        
        return sorted(unsigned_notes, key=lambda x: x['daysPending'], reverse=True)[:100]
    except Exception as e:
        print(f"Error in get_unsigned_notes: {e}")
        return []

@router.get("/all-data")
async def get_all_dashboard_data(
    limit: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    user_id: Optional[str] = None
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

