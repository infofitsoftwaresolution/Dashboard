"""
Test script to verify the project can be set up and run after cloning
This simulates what a new user would experience
"""
import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a required directory exists"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} MISSING: {dirpath}")
        return False

def check_env_example():
    """Check if env.example exists and has required variables"""
    env_example = Path("backend/env.example")
    if not env_example.exists():
        print("❌ backend/env.example MISSING")
        return False
    
    print("✅ backend/env.example exists")
    
    # Check for required variables
    required_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
        "S3_BUCKET_NAME",
        "ATHENA_DATABASE_NAME",
        "ATHENA_TABLE_NAME"
    ]
    
    content = env_example.read_text()
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing variables in env.example: {', '.join(missing_vars)}")
        return False
    
    print("✅ env.example contains all required variables")
    return True

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version too old: {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False

def check_node_version():
    """Check Node.js version"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_str = result.stdout.strip()
            print(f"✅ Node.js version: {version_str}")
            return True
        else:
            print("⚠️  Node.js not found (frontend won't work)")
            return False
    except FileNotFoundError:
        print("⚠️  Node.js not found (frontend won't work)")
        return False

def test_backend_imports():
    """Test if backend can import required modules"""
    print("\n📦 Testing backend imports...")
    try:
        # Test if we can import main modules
        sys.path.insert(0, "backend")
        
        # Check if athena_service can be imported (without AWS credentials)
        try:
            import athena_service
            print("✅ athena_service.py can be imported")
        except Exception as e:
            if "AWS credentials" in str(e) or "environment variables" in str(e):
                print("✅ athena_service.py structure is correct (needs .env for full test)")
            else:
                print(f"❌ athena_service.py import error: {e}")
                return False
        
        # Check if main.py can be imported
        try:
            import main
            print("✅ main.py can be imported")
        except Exception as e:
            print(f"❌ main.py import error: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Backend import test failed: {e}")
        return False
    finally:
        if "backend" in sys.path:
            sys.path.remove("backend")

def main():
    print("=" * 60)
    print("PROJECT SETUP VERIFICATION TEST")
    print("=" * 60)
    print("\nThis test verifies that the project can be set up after cloning")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Check project structure
    print("\n📁 Checking project structure...")
    checks = [
        ("README.md", "README file"),
        ("QUICK_START.md", "Quick start guide"),
        ("SETUP.md", "Setup guide"),
        ("backend/main.py", "Backend main file"),
        ("backend/athena_service.py", "Athena service"),
        ("backend/requirements.txt", "Python requirements"),
        ("backend/env.example", "Environment template"),
        ("frontend/package.json", "Frontend package file"),
        ("frontend/src/App.jsx", "Frontend app"),
        ("athena/create_table_ACTUAL.sql", "Athena table SQL"),
    ]
    
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    # Check directories
    print("\n📂 Checking directories...")
    dirs = [
        ("backend", "Backend directory"),
        ("frontend", "Frontend directory"),
        ("athena", "Athena SQL directory"),
        ("frontend/src", "Frontend source"),
        ("frontend/src/components", "Frontend components"),
    ]
    
    for dirpath, description in dirs:
        if not check_directory_exists(dirpath, description):
            all_checks_passed = False
    
    # Check env.example
    print("\n⚙️  Checking configuration...")
    if not check_env_example():
        all_checks_passed = False
    
    # Check .gitignore
    if check_file_exists(".gitignore", ".gitignore file"):
        content = Path(".gitignore").read_text()
        if ".env" in content:
            print("✅ .gitignore excludes .env (good for security)")
        else:
            print("⚠️  .gitignore should exclude .env")
    
    # Check versions
    print("\n🔧 Checking system requirements...")
    if not check_python_version():
        all_checks_passed = False
    
    check_node_version()  # Warning only, not critical
    
    # Test imports
    print("\n🧪 Testing code structure...")
    if not test_backend_imports():
        all_checks_passed = False
    
    # Final summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nThe project structure is correct and ready for cloning.")
        print("Users can:")
        print("  1. Clone the repository")
        print("  2. Copy backend/env.example to backend/.env")
        print("  3. Fill in AWS credentials")
        print("  4. Install dependencies and run")
    else:
        print("❌ SOME CHECKS FAILED")
        print("Please fix the issues above before pushing to GitHub.")
    print("=" * 60)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
