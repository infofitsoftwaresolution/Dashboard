"""
Test script to verify project setup
Run this after cloning to ensure everything is configured correctly
"""
import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing Python imports...")
    try:
        import fastapi
        import uvicorn
        import psycopg2
        import pydantic
        from dotenv import load_dotenv
        print("✅ All required modules can be imported")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def test_env_file():
    """Test if .env file exists"""
    print("\nTesting environment file...")
    if os.path.exists('.env'):
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file not found")
        print("   Run: copy env.example .env (Windows) or cp env.example .env (Linux/Mac)")
        print("   Then edit .env with your database credentials")
        return False

def test_env_variables():
    """Test if required environment variables are set"""
    print("\nTesting environment variables...")
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("   Please set these in your .env file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_database_service():
    """Test if DatabaseService can be instantiated"""
    print("\nTesting DatabaseService...")
    try:
        from database_service import DatabaseService
        db = DatabaseService()
        print("✅ DatabaseService can be instantiated")
        return True
    except ValueError as e:
        print(f"❌ DatabaseService error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  DatabaseService error (may be connection issue): {e}")
        print("   This is OK if database is not accessible yet")
        return True  # Not a blocker for setup

def test_database_connection():
    """Test if database connection works"""
    print("\nTesting database connection...")
    try:
        from database_service import DatabaseService
        db = DatabaseService()
        conn = db.get_connection()
        conn.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   Make sure:")
        print("   - Database is running and accessible")
        print("   - Credentials in .env are correct")
        print("   - Network/firewall allows connection")
        return False

def main():
    print("=" * 60)
    print("Project Setup Verification")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Environment File", test_env_file()))
    results.append(("Environment Variables", test_env_variables()))
    results.append(("DatabaseService", test_database_service()))
    results.append(("Database Connection", test_database_connection()))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Project is ready to run.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("   See README.md or SETUP.md for detailed instructions.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

