"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from typing import List, Union

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

