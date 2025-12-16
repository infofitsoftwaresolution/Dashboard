from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL
DATABASE_URL = "sqlite:///./dashboard.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database Models
class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    value = Column(String, nullable=False)  # Store as string to handle both numbers and strings
    change = Column(Float, nullable=False)
    trend = Column(String, nullable=False)

class TopUser(Base):
    __tablename__ = "top_users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    visits = Column(Integer, nullable=False)
    total_time = Column(String, nullable=True)

class ActiveUser(Base):
    __tablename__ = "active_users"
    
    id = Column(Integer, primary_key=True, index=True)
    active = Column(Integer, nullable=False)
    enabled = Column(Integer, nullable=False)

class StaffSpeaking(Base):
    __tablename__ = "staff_speaking"
    
    id = Column(Integer, primary_key=True, index=True)
    staff = Column(Integer, nullable=False)
    non_staff = Column(Integer, nullable=False)

class TimesData(Base):
    __tablename__ = "times_data"
    
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    recording = Column(Float, nullable=False)
    processing = Column(Float, nullable=False)
    created_to_sign = Column(Float, nullable=False)

class ConsentsData(Base):
    __tablename__ = "consents_data"
    
    id = Column(Integer, primary_key=True, index=True)
    listening = Column(Integer, nullable=False)
    dictation = Column(Integer, nullable=False)

class AuditItem(Base):
    __tablename__ = "audit_items"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    action = Column(String, nullable=False)
    user = Column(String, nullable=False)
    practitioner = Column(String, nullable=True)
    program = Column(String, nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, nullable=False)
    details = Column(Text, nullable=False)

class PatientAccessItem(Base):
    __tablename__ = "patient_access_items"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    practitioner = Column(String, nullable=True)
    program = Column(String, nullable=True)
    location = Column(String, nullable=True)
    access_date = Column(String, nullable=False)
    access_type = Column(String, nullable=False)
    duration = Column(String, nullable=False)

class ServiceUsageItem(Base):
    __tablename__ = "service_usage_items"
    
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)
    usage_count = Column(Integer, nullable=False)
    total_time = Column(String, nullable=False)
    last_used = Column(String, nullable=False)

class RecommendationItem(Base):
    __tablename__ = "recommendation_items"
    
    id = Column(Integer, primary_key=True, index=True)
    rec_id = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_date = Column(String, nullable=False)

class DeliveryScheduleItem(Base):
    __tablename__ = "delivery_schedule_items"
    
    id = Column(Integer, primary_key=True, index=True)
    report_name = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    next_delivery = Column(String, nullable=False)
    status = Column(String, nullable=False)

class SignedNoteItem(Base):
    __tablename__ = "signed_note_items"
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    practitioner = Column(String, nullable=False)
    program = Column(String, nullable=True)
    location = Column(String, nullable=True)
    signed_date = Column(String, nullable=False)
    status = Column(String, nullable=False)

class PractitionerUsageItem(Base):
    __tablename__ = "practitioner_usage_items"
    
    id = Column(Integer, primary_key=True, index=True)
    practitioner_name = Column(String, nullable=False)
    program = Column(String, nullable=True)
    location = Column(String, nullable=True)
    visits = Column(Integer, nullable=False)
    total_time = Column(String, nullable=False)
    last_active = Column(String, nullable=False)

class SyncIssueItem(Base):
    __tablename__ = "sync_issue_items"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False)
    reported_date = Column(String, nullable=False)

class UnsignedNoteItem(Base):
    __tablename__ = "unsigned_note_items"
    
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    practitioner = Column(String, nullable=False)
    program = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_date = Column(String, nullable=False)
    days_pending = Column(Integer, nullable=False)

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

