"""
Seed data directly into PostgreSQL database
This script will connect to PostgreSQL and seed all tables with one year of data
"""
import os
import sys
from dotenv import load_dotenv

# Force PostgreSQL usage
os.environ["USE_POSTGRES"] = "true"

# Load environment variables
load_dotenv()

# Verify PostgreSQL credentials are set
host = os.getenv("POSTGRES_HOST", "database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com")
port = os.getenv("POSTGRES_PORT", "5432")
database = os.getenv("POSTGRES_DB", "BVSTestDatabase")
username = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "Awesome!1234")

print("=" * 60)
print("PostgreSQL Database Seeding")
print("=" * 60)
print(f"\n📡 Database Configuration:")
print(f"  Host: {host}")
print(f"  Port: {port}")
print(f"  Database: {database}")
print(f"  Username: {username}")

# Test connection first
print("\n🔌 Testing connection...")
try:
    from sqlalchemy import create_engine, text
    postgres_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    engine = create_engine(
        postgres_url,
        connect_args={"connect_timeout": 10},
        pool_pre_ping=True
    )
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ Connection successful!")
        print(f"📊 PostgreSQL Version: {version[:50]}...")
        
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    print("\n🔍 Troubleshooting:")
    print("  1. Verify your IP (223.185.31.191/32) is in RDS Security Group")
    print("  2. Check if database is publicly accessible")
    print("  3. Wait 1-2 minutes after updating security group")
    print("\n💡 See backend/AWS_SECURITY_GROUP_SETUP.md for detailed instructions")
    sys.exit(1)

# Now seed the database
print("\n" + "=" * 60)
print("🌱 Starting database seeding...")
print("=" * 60)
print("\nThis will:")
print("  • Create all tables if they don't exist")
print("  • Clear existing data")
print("  • Seed one year of sample data")
print("  • Include distinct data for each practitioner")
print("\n⏳ This may take a few minutes...\n")

try:
    # Import and run seed function
    from seed_data import seed_database
    
    seed_database()
    
    print("\n" + "=" * 60)
    print("✅ Database Seeding Complete!")
    print("=" * 60)
    print("\n📊 Data Summary:")
    print("  • Metrics: 5 records")
    print("  • Top Users: 8 records")
    print("  • Times Data: 12 months")
    print("  • Audit Items: ~1,800 records (one year)")
    print("  • Patient Access: ~1,200 records (one year)")
    print("  • Signed Notes: ~2,500 records (one year)")
    print("  • Unsigned Notes: ~5,000+ records (one year)")
    print("  • Practitioner Usage: ~1,800 records (one year)")
    print("  • And more...")
    print("\n✨ All data has been seeded to PostgreSQL!")
    print(f"   Database: {database}")
    print(f"   Host: {host}")
    
except Exception as e:
    print(f"\n❌ Error seeding database: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


