"""
Quick migration script with interactive prompts for AWS RDS credentials
"""
import os
import sys
from migrate_to_postgres import main

if __name__ == "__main__":
    print("=" * 60)
    print("Quick Migration to AWS RDS PostgreSQL")
    print("=" * 60)
    print("\nThis script will help you migrate data from SQLite to PostgreSQL.")
    print("You'll be prompted for your AWS RDS credentials.\n")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️  No .env file found. You'll be prompted for credentials.")
        print("   After migration, consider creating a .env file for future use.\n")
    
    # Check if SQLite database exists
    if not os.path.exists("dashboard.db"):
        print("❌ SQLite database (dashboard.db) not found!")
        print("   Please run 'python seed_data.py' first to create the database.")
        sys.exit(1)
    
    print("✅ SQLite database found\n")
    
    # Run the main migration
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Migration failed: {str(e)}")
        sys.exit(1)

