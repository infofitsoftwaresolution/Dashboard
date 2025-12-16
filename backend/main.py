from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union
from sqlalchemy.orm import Session
from database import get_db, init_db
import random
from datetime import datetime, timedelta

app = FastAPI(title="Dashboard API", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
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
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get dashboard metrics with optional date/month filtering"""
    from database import PatientAccessItem, SignedNoteItem, TimesData as TimesDataModel
    
    # Calculate visits from patient access data if date filter is provided
    visits = 80
    if start_date and end_date:
        try:
            from datetime import datetime
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            access_count = db.query(PatientAccessItem).filter(
                PatientAccessItem.access_date >= start_date,
                PatientAccessItem.access_date <= end_date
            ).count()
            if access_count > 0:
                visits = access_count
        except:
            pass
    
    # Calculate notes from signed notes if date filter is provided
    notes_from_scribe = 13
    notes_without_scribe = 8
    if start_date and end_date:
        try:
            signed_count = db.query(SignedNoteItem).filter(
                SignedNoteItem.signed_date >= start_date,
                SignedNoteItem.signed_date <= end_date
            ).count()
            if signed_count > 0:
                notes_from_scribe = signed_count
                notes_without_scribe = max(1, signed_count // 2)
        except:
            pass
    
    # Calculate total time from times data if month filter is provided
    total_time = "5 hr 9 min"
    if start_month and end_month:
        try:
            from datetime import datetime
            # Convert "YYYY-MM" format to short month names if needed
            def convert_to_short_month(month_str):
                if len(month_str) == 3:  # Already short name like "Jan"
                    return month_str
                try:
                    year, month = month_str.split('-')
                    date = datetime(int(year), int(month), 1)
                    return date.strftime("%b")
                except:
                    return month_str
            
            start_month_short = convert_to_short_month(start_month)
            end_month_short = convert_to_short_month(end_month)
            
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            start_idx = month_order.index(start_month_short) if start_month_short in month_order else 0
            end_idx = month_order.index(end_month_short) if end_month_short in month_order else 11
            months_to_include = month_order[start_idx:end_idx+1]
            times_data = db.query(TimesDataModel).filter(
                TimesDataModel.month.in_(months_to_include)
            ).all()
            if times_data:
                total_recording = sum(t.recording for t in times_data)
                total_processing = sum(t.processing for t in times_data)
                total_hours = int((total_recording + total_processing) / 60)
                total_mins = int((total_recording + total_processing) % 60)
                total_time = f"{total_hours} hr {total_mins} min"
        except:
            pass
    
    return [
        {
            "label": "Visits",
            "value": visits,
            "change": 300.0,
            "trend": "up"
        },
        {
            "label": "Notes from Scribe",
            "value": notes_from_scribe,
            "change": 160.0,
            "trend": "up"
        },
        {
            "label": "Notes without Scribe",
            "value": notes_without_scribe,
            "change": 700.0,
            "trend": "up"
        },
        {
            "label": "Note Content from Scribe",
            "value": 0.0,  # This will display as 0.0%
            "change": -10.2,
            "trend": "down"
        },
        {
            "label": "Total Time",
            "value": total_time,
            "change": 618.6,
            "trend": "up"
        }
    ]

@app.get("/api/top-users", response_model=List[TopUser])
async def get_top_users(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get top users data with optional date/month filtering"""
    from database import TopUser as TopUserModel
    # Note: TopUser model doesn't have date fields, so filtering is not applied
    # In a real app, you'd calculate from PatientAccessItem or add date fields
    users = db.query(TopUserModel).order_by(TopUserModel.visits.desc()).limit(8).all()
    if not users:
        return []
    return [
        {"name": u.name, "visits": u.visits, "totalTime": u.total_time or ""}
        for u in users
    ]

@app.get("/api/active-users", response_model=ActiveUsersData)
async def get_active_users(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get active vs enabled users with optional date/month filtering"""
    from database import ActiveUser as ActiveUserModel
    # Note: ActiveUser is snapshot data, filtering not applicable
    active_user = db.query(ActiveUserModel).first()
    if not active_user:
        enabled = random.randint(150, 200)
        active = random.randint(int(enabled * 0.6), int(enabled * 0.85))
        return {"active": active, "enabled": enabled}
    return {
        "active": active_user.active,
        "enabled": active_user.enabled
    }

@app.get("/api/staff-speaking", response_model=StaffSpeakingData)
async def get_staff_speaking(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get staff speaking data with optional date/month filtering"""
    from database import StaffSpeaking as StaffSpeakingModel
    # Note: StaffSpeaking is snapshot data, filtering not applicable
    staff_data = db.query(StaffSpeakingModel).first()
    if not staff_data:
        non_staff = random.randint(65, 85)
        staff = random.randint(15, 35)
        return {"staff": staff, "nonStaff": non_staff}
    return {
        "staff": staff_data.staff,
        "nonStaff": staff_data.non_staff
    }

@app.get("/api/times", response_model=List[TimesData])
async def get_times(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get times data with month filtering"""
    from database import TimesData as TimesDataModel
    from datetime import datetime
    
    query = db.query(TimesDataModel)
    
    # Apply month range filter
    if start_month and end_month:
        # Convert "YYYY-MM" format to short month names if needed
        def convert_to_short_month(month_str):
            if len(month_str) == 3:  # Already short name like "Jan"
                return month_str
            try:
                # Convert "YYYY-MM" to "Jan", "Feb", etc.
                year, month = month_str.split('-')
                date = datetime(int(year), int(month), 1)
                return date.strftime("%b")
            except:
                return month_str
        
        start_month_short = convert_to_short_month(start_month)
        end_month_short = convert_to_short_month(end_month)
        
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        try:
            start_idx = month_order.index(start_month_short) if start_month_short in month_order else 0
            end_idx = month_order.index(end_month_short) if end_month_short in month_order else 11
            months_to_include = month_order[start_idx:end_idx+1]
            query = query.filter(TimesDataModel.month.in_(months_to_include))
        except:
            pass
    
    times = query.order_by(TimesDataModel.id).all()
    if not times:
        return []
    return [
        {
            "month": t.month,
            "recording": t.recording,
            "processing": t.processing,
            "createdToSign": t.created_to_sign
        }
        for t in times
    ]

@app.get("/api/consents", response_model=ConsentsData)
async def get_consents(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get consents data with optional date/month filtering"""
    from database import ConsentsData as ConsentsDataModel
    # Note: ConsentsData is snapshot data, filtering not applicable
    consents = db.query(ConsentsDataModel).first()
    if not consents:
        listening = random.randint(82, 92)
        dictation = random.randint(8, 18)
        return {"listening": listening, "dictation": dictation}
    return {
        "listening": consents.listening,
        "dictation": consents.dictation
    }

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
async def get_filter_options(db: Session = Depends(get_db)):
    """Get unique values for practitioner, program, and location filters"""
    from database import (
        SignedNoteItem, UnsignedNoteItem, PatientAccessItem, 
        AuditItem, PractitionerUsageItem
    )
    from sqlalchemy import distinct
    
    # Get unique practitioners
    practitioners = set()
    for model in [SignedNoteItem, UnsignedNoteItem, PatientAccessItem, AuditItem, PractitionerUsageItem]:
        if hasattr(model, 'practitioner'):
            results = db.query(distinct(model.practitioner)).filter(model.practitioner.isnot(None)).all()
            practitioners.update([r[0] for r in results if r[0]])
        if hasattr(model, 'practitioner_name'):
            results = db.query(distinct(model.practitioner_name)).filter(model.practitioner_name.isnot(None)).all()
            practitioners.update([r[0] for r in results if r[0]])
    
    # Get unique programs
    programs = set()
    for model in [SignedNoteItem, UnsignedNoteItem, PatientAccessItem, AuditItem, PractitionerUsageItem]:
        if hasattr(model, 'program'):
            results = db.query(distinct(model.program)).filter(model.program.isnot(None)).all()
            programs.update([r[0] for r in results if r[0]])
    
    # Get unique locations
    locations = set()
    for model in [SignedNoteItem, UnsignedNoteItem, PatientAccessItem, AuditItem, PractitionerUsageItem]:
        if hasattr(model, 'location'):
            results = db.query(distinct(model.location)).filter(model.location.isnot(None)).all()
            locations.update([r[0] for r in results if r[0]])
    
    return {
        "practitioners": sorted(list(practitioners)),
        "programs": sorted(list(programs)),
        "locations": sorted(list(locations))
    }

@app.get("/api/audit-summary", response_model=List[AuditItem])
async def get_audit_summary(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get audit summary data with date/month and filter filtering"""
    from database import AuditItem as AuditItemModel
    from datetime import datetime
    
    query = db.query(AuditItemModel)
    
    # Apply date range filter
    if start_date and end_date:
        query = query.filter(AuditItemModel.date >= start_date, AuditItemModel.date <= end_date)
    elif start_month and end_month:
        # Filter by month range (YYYY-MM format)
        query = query.filter(
            AuditItemModel.date >= f"{start_month}-01 00:00:00",
            AuditItemModel.date <= f"{end_month}-31 23:59:59"
        )
    
    # Apply practitioner, program, location filters
    if practitioner:
        query = query.filter(AuditItemModel.practitioner == practitioner)
    if program:
        query = query.filter(AuditItemModel.program == program)
    if location:
        query = query.filter(AuditItemModel.location == location)
    
    audits = query.order_by(AuditItemModel.date.desc()).limit(100).all()
    if not audits:
        return []
    return [
        {
            "date": a.date,
            "action": a.action,
            "user": a.user,
            "status": a.status,
            "details": a.details
        }
        for a in audits
    ]

@app.get("/api/patient-access", response_model=List[PatientAccessItem])
async def get_patient_access(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get patient access data with date/month and filter filtering"""
    from database import PatientAccessItem as PatientAccessItemModel
    
    query = db.query(PatientAccessItemModel)
    
    # Apply date range filter
    if start_date and end_date:
        query = query.filter(PatientAccessItemModel.access_date >= start_date, PatientAccessItemModel.access_date <= end_date)
    elif start_month and end_month:
        query = query.filter(
            PatientAccessItemModel.access_date >= f"{start_month}-01 00:00:00",
            PatientAccessItemModel.access_date <= f"{end_month}-31 23:59:59"
        )
    
    # Apply practitioner, program, location filters
    if practitioner:
        query = query.filter(PatientAccessItemModel.practitioner == practitioner)
    if program:
        query = query.filter(PatientAccessItemModel.program == program)
    if location:
        query = query.filter(PatientAccessItemModel.location == location)
    
    accesses = query.order_by(PatientAccessItemModel.access_date.desc()).limit(100).all()
    if not accesses:
        return []
    return [
        {
            "patientId": a.patient_id,
            "patientName": a.patient_name,
            "accessDate": a.access_date,
            "accessType": a.access_type,
            "duration": a.duration
        }
        for a in accesses
    ]

@app.get("/api/patient-service-usage", response_model=List[ServiceUsageItem])
async def get_patient_service_usage(db: Session = Depends(get_db)):
    """Get patient service usage data"""
    from database import ServiceUsageItem as ServiceUsageItemModel
    services = db.query(ServiceUsageItemModel).all()
    if not services:
        return []
    return [
        {
            "serviceName": s.service_name,
            "usageCount": s.usage_count,
            "totalTime": s.total_time,
            "lastUsed": s.last_used
        }
        for s in services
    ]

@app.get("/api/recommendation-summary", response_model=List[RecommendationItem])
async def get_recommendation_summary(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get recommendation summary data with date/month filtering"""
    from database import RecommendationItem as RecommendationItemModel
    
    query = db.query(RecommendationItemModel)
    
    # Apply date range filter
    if start_date and end_date:
        query = query.filter(RecommendationItemModel.created_date >= start_date, RecommendationItemModel.created_date <= end_date)
    elif start_month and end_month:
        query = query.filter(
            RecommendationItemModel.created_date >= f"{start_month}-01",
            RecommendationItemModel.created_date <= f"{end_month}-31"
        )
    
    recommendations = query.order_by(RecommendationItemModel.created_date.desc()).limit(100).all()
    if not recommendations:
        return []
    return [
        {
            "id": r.rec_id,
            "type": r.type,
            "priority": r.priority,
            "status": r.status,
            "createdDate": r.created_date
        }
        for r in recommendations
    ]

@app.get("/api/delivery-schedules", response_model=List[DeliveryScheduleItem])
async def get_delivery_schedules(db: Session = Depends(get_db)):
    """Get report delivery schedules"""
    from database import DeliveryScheduleItem as DeliveryScheduleItemModel
    schedules = db.query(DeliveryScheduleItemModel).all()
    if not schedules:
        return []
    return [
        {
            "reportName": s.report_name,
            "frequency": s.frequency,
            "nextDelivery": s.next_delivery,
            "status": s.status
        }
        for s in schedules
    ]

@app.get("/api/signed-notes", response_model=List[SignedNoteItem])
async def get_signed_notes(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get signed notes data with date/month and filter filtering"""
    from database import SignedNoteItem as SignedNoteItemModel
    
    query = db.query(SignedNoteItemModel)
    
    # Apply date range filter
    if start_date and end_date:
        query = query.filter(SignedNoteItemModel.signed_date >= start_date, SignedNoteItemModel.signed_date <= end_date)
    elif start_month and end_month:
        query = query.filter(
            SignedNoteItemModel.signed_date >= f"{start_month}-01",
            SignedNoteItemModel.signed_date <= f"{end_month}-31"
        )
    
    # Apply practitioner, program, location filters
    if practitioner:
        query = query.filter(SignedNoteItemModel.practitioner == practitioner)
    if program:
        query = query.filter(SignedNoteItemModel.program == program)
    if location:
        query = query.filter(SignedNoteItemModel.location == location)
    
    notes = query.order_by(SignedNoteItemModel.signed_date.desc()).limit(100).all()
    if not notes:
        return []
    return [
        {
            "noteId": n.note_id,
            "patientName": n.patient_name,
            "practitioner": n.practitioner,
            "signedDate": n.signed_date,
            "status": n.status
        }
        for n in notes
    ]

@app.get("/api/practitioner-service-usage", response_model=List[PractitionerUsageItem])
async def get_practitioner_service_usage(
    db: Session = Depends(get_db),
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get practitioner service usage with filtering"""
    from database import PractitionerUsageItem as PractitionerUsageItemModel
    query = db.query(PractitionerUsageItemModel)
    
    # Apply filters
    if practitioner:
        query = query.filter(PractitionerUsageItemModel.practitioner_name == practitioner)
    if program:
        query = query.filter(PractitionerUsageItemModel.program == program)
    if location:
        query = query.filter(PractitionerUsageItemModel.location == location)
    
    practitioners = query.order_by(PractitionerUsageItemModel.visits.desc()).all()
    if not practitioners:
        return []
    return [
        {
            "practitionerName": p.practitioner_name,
            "visits": p.visits,
            "totalTime": p.total_time,
            "lastActive": p.last_active
        }
        for p in practitioners
    ]

@app.get("/api/sync-issues", response_model=List[SyncIssueItem])
async def get_sync_issues(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None
):
    """Get sync issues data with date/month filtering"""
    from database import SyncIssueItem as SyncIssueItemModel
    
    query = db.query(SyncIssueItemModel)
    
    # Apply date range filter
    if start_date and end_date:
        query = query.filter(SyncIssueItemModel.reported_date >= start_date, SyncIssueItemModel.reported_date <= end_date)
    elif start_month and end_month:
        query = query.filter(
            SyncIssueItemModel.reported_date >= f"{start_month}-01 00:00:00",
            SyncIssueItemModel.reported_date <= f"{end_month}-31 23:59:59"
        )
    
    issues = query.order_by(SyncIssueItemModel.reported_date.desc()).limit(100).all()
    if not issues:
        return []
    return [
        {
            "id": i.issue_id,
            "type": i.type,
            "severity": i.severity,
            "status": i.status,
            "reportedDate": i.reported_date
        }
        for i in issues
    ]

@app.get("/api/unsigned-notes", response_model=List[UnsignedNoteItem])
async def get_unsigned_notes(
    db: Session = Depends(get_db),
    start_date: str = None,
    end_date: str = None,
    start_month: str = None,
    end_month: str = None,
    practitioner: str = None,
    program: str = None,
    location: str = None
):
    """Get unsigned notes data with date/month and filter filtering"""
    from database import UnsignedNoteItem as UnsignedNoteItemModel
    
    query = db.query(UnsignedNoteItemModel)
    
    # Apply date range filter
    if start_date and end_date:
        query = query.filter(UnsignedNoteItemModel.created_date >= start_date, UnsignedNoteItemModel.created_date <= end_date)
    elif start_month and end_month:
        query = query.filter(
            UnsignedNoteItemModel.created_date >= f"{start_month}-01",
            UnsignedNoteItemModel.created_date <= f"{end_month}-31"
        )
    
    # Apply practitioner, program, location filters
    if practitioner:
        query = query.filter(UnsignedNoteItemModel.practitioner == practitioner)
    if program:
        query = query.filter(UnsignedNoteItemModel.program == program)
    if location:
        query = query.filter(UnsignedNoteItemModel.location == location)
    
    notes = query.order_by(UnsignedNoteItemModel.days_pending.desc()).limit(100).all()
    if not notes:
        return []
    return [
        {
            "noteId": n.note_id,
            "patientName": n.patient_name,
            "practitioner": n.practitioner,
            "createdDate": n.created_date,
            "daysPending": n.days_pending
        }
        for n in notes
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

