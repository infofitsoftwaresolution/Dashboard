# Setup Guide - Athena Data Pipeline Dashboard

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- AWS Account with:
  - S3 bucket with Parquet files
  - Athena access
  - IAM user with appropriate permissions

## 🚀 Quick Setup

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd new_project
```

### Step 2: Configure Backend

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example file
   copy env.example .env  # Windows
   cp env.example .env    # Linux/Mac
   ```

5. **Edit `.env` file with your AWS credentials:**
   ```env
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION=us-east-1
   S3_BUCKET_NAME=your-bucket-name
   S3_PREFIX=audit-trail-data/raw/
   S3_RESULTS_BUCKET=your-bucket-name
   S3_RESULTS_PREFIX=athena-results/
   ATHENA_DATABASE_NAME=audit_trail_db
   ATHENA_TABLE_NAME=audit_trail_data
   ATHENA_WORKGROUP=primary
   ```

### Step 3: Setup Athena Table

1. Go to [AWS Athena Console](https://console.aws.amazon.com/athena/)
2. Run the SQL from `athena/create_table_ACTUAL.sql`
3. Update the S3 location in the SQL to match your bucket
4. Run `MSCK REPAIR TABLE audit_trail_data;` to refresh metadata

### Step 4: Configure Frontend

1. **Navigate to frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

### Step 5: Run the Application

**Option 1: Use the startup scripts**

```bash
# Windows
START_SERVERS.bat

# PowerShell
.\START_SERVERS.ps1
```

**Option 2: Manual startup**

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 6: Access the Dashboard

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## ✅ Verification

1. Check backend is running: http://localhost:8000
2. Check frontend is running: http://localhost:5173
3. Verify Athena connection: http://localhost:8000/api/athena/verify-files
4. View data: Click "☁️ Athena Data View" in the dashboard

## 🔧 Troubleshooting

### Backend won't start
- Check `.env` file exists and has correct AWS credentials
- Verify virtual environment is activated
- Check Python version: `python --version` (should be 3.8+)

### Frontend won't start
- Check Node.js version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again
- Check if port 5173 is available

### No data showing
- Verify AWS credentials are correct
- Check Athena table exists and has data
- Run `MSCK REPAIR TABLE audit_trail_data;` in Athena
- Check S3 bucket permissions

### CORS errors
- Ensure backend is running on port 8000
- Check `backend/main.py` CORS configuration
- Verify frontend is calling correct API URL

## 📚 Additional Resources

- See `QUICK_START.md` for detailed Athena setup
- See `README.md` for project overview

