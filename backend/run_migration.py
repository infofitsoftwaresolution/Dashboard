"""
Migration script that accepts credentials as command-line arguments or environment variables
Usage: python run_migration.py [--username USERNAME] [--password PASSWORD] [--database DATABASE]
"""
import os
import sys
import argparse
from migrate_to_postgres import migrate_table, Base
from database import (
    Metric, TopUser, ActiveUser, StaffSpeaking, TimesData, ConsentsData,
    AuditItem, PatientAccessItem, ServiceUsageItem, RecommendationItem,
    DeliveryScheduleItem, SignedNoteItem, PractitionerUsageItem,
    SyncIssueItem, UnsignedNoteItem
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_postgres_url_from_args():
    """Get PostgreSQL URL from command line arguments or environment"""
    parser = argparse.ArgumentParser(description='Migrate SQLite to PostgreSQL')
    parser.add_argument('--username', help='PostgreSQL username', default=None)
    parser.add_argument('--password', help='PostgreSQL password', default=None)
    parser.add_argument('--database', help='PostgreSQL database name', default='postgres')
    parser.add_argument('--host', help='PostgreSQL host', default='database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com')
    parser.add_argument('--port', help='PostgreSQL port', default='5432')
    
    args = parser.parse_args()
    
    # Get from args or environment
    username = args.username or os.getenv("POSTGRES_USER")
    password = args.password or os.getenv("POSTGRES_PASSWORD")
    database = args.database or os.getenv("POSTGRES_DB", "postgres")
    host = args.host or os.getenv("POSTGRES_HOST", "database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com")
    port = args.port or os.getenv("POSTGRES_PORT", "5432")
    
    # Check for full URL in environment
    postgres_url = os.getenv("POSTGRES_URL")
    if postgres_url:
        return postgres_url
    
    # Prompt if still missing
    if not username:
        username = input("Enter PostgreSQL username: ").strip()
    if not password:
        import getpass
        password = getpass.getpass("Enter PostgreSQL password: ").strip()
    
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"

def main():
    print("=" * 60)
    print("SQLite to PostgreSQL Migration")
    print("=" * 60)
    
    # Get PostgreSQL connection URL
    print("\n📡 Setting up database connections...")
    postgres_url = get_postgres_url_from_args()
    
    # SQLite source
    SQLITE_DB = "sqlite:///./dashboard.db"
    print("  Connecting to SQLite (source)...")
    sqlite_engine = create_engine(
        SQLITE_DB,
        connect_args={"check_same_thread": False},
        echo=False
    )
    
    # PostgreSQL destination
    print("  Connecting to PostgreSQL (destination)...")
    try:
        postgres_engine = create_engine(
            postgres_url,
            echo=False,
            pool_pre_ping=True
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
        
        # Check for existing data
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
        
        # Migrate data
        print("\n📦 Starting data migration...")
        print("-" * 60)
        
        migration_stats = {}
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

