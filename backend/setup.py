"""
Setup script to initialize the database and verify installation
"""
import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def seed_database():
    """Seed the database with initial data"""
    print("\n🌱 Seeding database...")
    try:
        from seed_data import seed_database
        seed_database()
        print("✅ Database seeded successfully")
        return True
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        return False

def verify_database():
    """Verify database was created and has data"""
    print("\n🔍 Verifying database...")
    if not os.path.exists("dashboard.db"):
        print("❌ Database file not found")
        return False
    
    try:
        from database import SessionLocal, SignedNoteItem
        db = SessionLocal()
        count = db.query(SignedNoteItem).count()
        db.close()
        
        if count > 0:
            print(f"✅ Database verified: {count} signed notes found")
            return True
        else:
            print("⚠️  Database exists but is empty. Run seed_data.py manually.")
            return False
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    print("=" * 50)
    print("Dashboard Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  You may need to install dependencies manually:")
        print("   pip install -r requirements.txt")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Seed database
    if not seed_database():
        print("\n⚠️  Database seeding failed. You can run it manually:")
        print("   python seed_data.py")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Verify database
    verify_database()
    
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\nTo start the server, run:")
    print("   python main.py")
    print("\nThe API will be available at: http://localhost:8000")

if __name__ == "__main__":
    main()



