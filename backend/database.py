from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - supports both SQLite and PostgreSQL
# Priority: POSTGRES_URL > individual POSTGRES_* vars > SQLite default
def get_database_url():
    """Get database URL from environment or use SQLite default"""
    # Check for full PostgreSQL URL
    postgres_url = os.getenv("POSTGRES_URL")
    if postgres_url:
        return postgres_url
    
    # Check if PostgreSQL should be used
    use_postgres = os.getenv("USE_POSTGRES", "false").lower() == "true"
    if use_postgres:
        # Construct PostgreSQL URL from individual components
        host = os.getenv("POSTGRES_HOST", "database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com")
        port = os.getenv("POSTGRES_PORT", "5432")
        database = os.getenv("POSTGRES_DB", "postgres")
        username = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        
        if username and password:
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    # Default to SQLite
    return "sqlite:///./dashboard.db"

DATABASE_URL = get_database_url()

# Create engine with appropriate connection args
is_postgres = DATABASE_URL.startswith("postgresql://")
connect_args = {} if is_postgres else {"check_same_thread": False}  # SQLite needs this

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True if is_postgres else False  # Verify PostgreSQL connections
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

