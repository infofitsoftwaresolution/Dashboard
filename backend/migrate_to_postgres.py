"""
Migration script to transfer data from SQLite to PostgreSQL (AWS RDS)
"""
import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all models from database.py
from database import (
    Base,
    Metric, TopUser, ActiveUser, StaffSpeaking, TimesData, ConsentsData,
    AuditItem, PatientAccessItem, ServiceUsageItem, RecommendationItem,
    DeliveryScheduleItem, SignedNoteItem, PractitionerUsageItem,
    SyncIssueItem, UnsignedNoteItem
)

# SQLite source database
SQLITE_DB = "sqlite:///./dashboard.db"

# PostgreSQL destination database (AWS RDS)
# Format: postgresql://username:password@host:port/database
# Get from environment variables or prompt user
def get_postgres_url():
    """Get PostgreSQL connection URL"""
    # Try environment variables first
    postgres_url = os.getenv("POSTGRES_URL")
    
    if postgres_url:
        return postgres_url
    
    # If not in env, construct from individual components
    host = os.getenv("POSTGRES_HOST", "database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "postgres")
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    
    # Prompt for credentials if not provided
    if not username:
        username = input("Enter PostgreSQL username: ").strip()
    if not password:
        password = input("Enter PostgreSQL password: ").strip()
    
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"

def migrate_table(sqlite_session, postgres_session, model_class, table_name):
    """Migrate data from SQLite to PostgreSQL for a specific table"""
    try:
        # Get all records from SQLite
        records = sqlite_session.query(model_class).all()
        
        if not records:
            print(f"  ⚠️  No data in {table_name}")
            return 0
        
        # Convert to dictionaries and insert into PostgreSQL
        count = 0
        batch_size = 1000
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            records_dict = []
            
            for record in batch:
                record_dict = {}
                for column in model_class.__table__.columns:
                    value = getattr(record, column.name)
                    record_dict[column.name] = value
                records_dict.append(record_dict)
            
            # Insert batch into PostgreSQL
            postgres_session.bulk_insert_mappings(model_class, records_dict)
            count += len(batch)
            print(f"  ✓ Migrated {count}/{len(records)} records from {table_name}", end='\r')
        
        postgres_session.commit()
        print(f"  ✅ Migrated {count} records from {table_name}")
        return count
        
    except Exception as e:
        postgres_session.rollback()
        print(f"  ❌ Error migrating {table_name}: {str(e)}")
        raise

def main():
    print("=" * 60)
    print("SQLite to PostgreSQL Migration Script")
    print("=" * 60)
    
    # Get PostgreSQL connection URL
    print("\n📡 Setting up database connections...")
    postgres_url = get_postgres_url()
    
    # Create engines
    print("  Connecting to SQLite (source)...")
    sqlite_engine = create_engine(
        SQLITE_DB,
        connect_args={"check_same_thread": False},
        echo=False
    )
    
    print("  Connecting to PostgreSQL (destination)...")
    try:
        postgres_engine = create_engine(
            postgres_url,
            echo=False,
            pool_pre_ping=True  # Verify connections before using
        )
        # Test connection
        with postgres_engine.connect() as conn:
            conn.execute("SELECT 1")
        print("  ✅ Connected to PostgreSQL successfully")
    except Exception as e:
        print(f"  ❌ Failed to connect to PostgreSQL: {str(e)}")
        print("\nPlease check:")
        print("  - Database credentials are correct")
        print("  - Database exists and is accessible")
        print("  - Security groups allow your IP address")
        sys.exit(1)
    
    # Create sessions
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    PostgresSession = sessionmaker(bind=postgres_engine)
    
    sqlite_session = SQLiteSession()
    postgres_session = PostgresSession()
    
    try:
        # Create all tables in PostgreSQL
        print("\n📋 Creating tables in PostgreSQL...")
        Base.metadata.create_all(bind=postgres_engine)
        print("  ✅ All tables created")
        
        # Check if tables already have data
        print("\n🔍 Checking existing data in PostgreSQL...")
        existing_data = {}
        for model_class in [Metric, TopUser, ActiveUser, StaffSpeaking, TimesData, ConsentsData,
                           AuditItem, PatientAccessItem, ServiceUsageItem, RecommendationItem,
                           DeliveryScheduleItem, SignedNoteItem, PractitionerUsageItem,
                           SyncIssueItem, UnsignedNoteItem]:
            count = postgres_session.query(model_class).count()
            if count > 0:
                existing_data[model_class.__tablename__] = count
        
        if existing_data:
            print("  ⚠️  Found existing data in PostgreSQL:")
            for table, count in existing_data.items():
                print(f"     - {table}: {count} records")
            response = input("\n  Do you want to clear existing data and migrate? (yes/no): ").strip().lower()
            if response != 'yes':
                print("  Migration cancelled.")
                return
            
            # Clear existing data
            print("\n🗑️  Clearing existing data...")
            for model_class in [Metric, TopUser, ActiveUser, StaffSpeaking, TimesData, ConsentsData,
                               AuditItem, PatientAccessItem, ServiceUsageItem, RecommendationItem,
                               DeliveryScheduleItem, SignedNoteItem, PractitionerUsageItem,
                               SyncIssueItem, UnsignedNoteItem]:
                postgres_session.query(model_class).delete()
            postgres_session.commit()
            print("  ✅ Existing data cleared")
        
        # Migrate data table by table
        print("\n📦 Starting data migration...")
        print("-" * 60)
        
        migration_stats = {}
        
        # Define all tables to migrate
        tables_to_migrate = [
            (Metric, "metrics"),
            (TopUser, "top_users"),
            (ActiveUser, "active_users"),
            (StaffSpeaking, "staff_speaking"),
            (TimesData, "times_data"),
            (ConsentsData, "consents_data"),
            (AuditItem, "audit_items"),
            (PatientAccessItem, "patient_access_items"),
            (ServiceUsageItem, "service_usage_items"),
            (RecommendationItem, "recommendation_items"),
            (DeliveryScheduleItem, "delivery_schedule_items"),
            (SignedNoteItem, "signed_note_items"),
            (PractitionerUsageItem, "practitioner_usage_items"),
            (SyncIssueItem, "sync_issue_items"),
            (UnsignedNoteItem, "unsigned_note_items"),
        ]
        
        for model_class, table_name in tables_to_migrate:
            print(f"\n📊 Migrating {table_name}...")
            try:
                count = migrate_table(sqlite_session, postgres_session, model_class, table_name)
                migration_stats[table_name] = count
            except Exception as e:
                print(f"  ❌ Failed to migrate {table_name}: {str(e)}")
                migration_stats[table_name] = 0
        
        # Print summary
        print("\n" + "=" * 60)
        print("✅ Migration Complete!")
        print("=" * 60)
        print("\n📊 Migration Summary:")
        total_records = 0
        for table_name, count in migration_stats.items():
            print(f"  {table_name}: {count:,} records")
            total_records += count
        print(f"\n  Total: {total_records:,} records migrated")
        
        print("\n💡 Next Steps:")
        print("  1. Update your .env file with POSTGRES_URL")
        print("  2. Update database.py to use PostgreSQL")
        print("  3. Test the application with the new database")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        sqlite_session.close()
        postgres_session.close()
        print("\n🔌 Database connections closed")

if __name__ == "__main__":
    main()

