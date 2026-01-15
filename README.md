# 📊 Dashboard Analytics Application

A modern analytics dashboard that connects to PostgreSQL database, processes data through a FastAPI backend, and presents real-time insights via a React-based dashboard.

---

## ✨ Features

- 📊 Real-time dashboard metrics with trend indicators  
- 📈 Interactive charts (Line, Bar, Pie, Area) using Recharts  
- 🔍 Advanced filters: Date range, Practitioner, Program, Location  
- 🗄️ PostgreSQL database integration  
- 📑 Multiple reports: Audit Summary, Patient Access, Signed / Unsigned Notes  
- 📱 Fully responsive UI (desktop & mobile)
- ⚡ AWS Lambda function to process Parquet files from S3 and save to PostgreSQL

---

## 🧰 Tech Stack

### Backend
- FastAPI  
- PostgreSQL (RDS)  
- psycopg2  
- Pydantic  
- Uvicorn  

### Frontend
- React 18  
- Vite  
- Recharts  
- Axios  

### Infrastructure
- AWS Lambda (for processing Parquet files)
- AWS S3 (for storing Parquet files)
- AWS RDS PostgreSQL (for data storage)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- PostgreSQL database (or AWS RDS PostgreSQL)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
# On Windows:
copy env.example .env
# On Linux/Mac:
cp env.example .env
```

**Configure `.env` file:**

Edit `backend/.env` and add your PostgreSQL database credentials:

```env
DB_HOST=your-database-host.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
TABLE_NAME=audittrail_firehose
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
```

---

### 4. Run the Application

**Backend:**

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Frontend:**

Open a new terminal:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

---

### 5. Open Dashboard

Open your browser and navigate to:

```
http://localhost:5173
```

API Documentation (Swagger UI):

```
http://localhost:8000/docs
```

---

## 📚 Project Structure

```
Dashboard/
├── backend/
│   ├── api/
│   │   ├── models.py               # Pydantic models
│   │   └── routes/
│   │       ├── dashboard.py         # Dashboard endpoints
│   │       └── data.py              # Data endpoints
│   ├── main.py                     # FastAPI app entry point
│   ├── database_service.py         # PostgreSQL service layer
│   ├── requirements.txt
│   └── env.example                 # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   └── App.jsx                 # Main app component
│   └── package.json
├── lambda/
│   └── parquet_to_rds/             # Lambda function for S3 to PostgreSQL
│       ├── lambda_function.py
│       ├── template.yaml
│       └── requirements.txt
└── README.md
```

---

## 🔌 API Overview

### Health Check
- `GET /` - API health check

### Dashboard Metrics
- `GET /api/metrics` - Get dashboard metrics
- `GET /api/top-users` - Get top users
- `GET /api/active-users` - Get active users statistics
- `GET /api/staff-speaking` - Get staff speaking statistics
- `GET /api/times` - Get time-based data
- `GET /api/consents` - Get consents data

### Data Endpoints
- `GET /api/data/all-data` - Get all data from database
- `GET /api/data/count` - Get total record count

### Reports (Filter Supported)
- `GET /api/audit-summary` - Audit trail summary
- `GET /api/patient-access` - Patient access logs
- `GET /api/signed-notes` - Finalized notes
- `GET /api/unsigned-notes` - Pending notes
- `GET /api/practitioner-service-usage` - Practitioner activity
- `GET /api/sync-issues` - Session sync issues

**Swagger Documentation:**
```
http://localhost:8000/docs
```

---

## ✅ Verification After Cloning

After cloning and setting up, verify everything works:

1. **Backend starts without errors:**
   ```bash
   cd backend
   python main.py
   # Should see: "Application startup complete" and "Uvicorn running on http://0.0.0.0:8000"
   ```

2. **Frontend starts without errors:**
   ```bash
   cd frontend
   npm run dev
   # Should see: "Local: http://localhost:5173"
   ```

3. **API is accessible:**
   - Visit: http://localhost:8000/docs (Swagger UI)
   - Visit: http://localhost:8000/ (Should return: `{"message":"Dashboard API is running"}`)

4. **Database connection works:**
   - Visit: http://localhost:8000/api/data/count
   - Should return: `{"success":true,"count":0}` (or actual count if data exists)

5. **Frontend connects to backend:**
   - Open: http://localhost:5173
   - Check browser console for any errors
   - Dashboard should load (may show empty data if database is empty)

---

## 🐞 Common Issues

### Backend not starting

- ✅ Python 3.8+ installed
- ✅ Virtual environment activated (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on Linux/Mac)
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ `.env` file exists and configured correctly (copy from `env.example`)
- ✅ PostgreSQL database is accessible and credentials are correct

### Import errors after cloning

If you see `ModuleNotFoundError`:
- Make sure you're running from the `backend/` directory
- The `backend/api/` folder should exist with all files
- Try: `pip install -r requirements.txt` again
- Make sure virtual environment is activated

### Database connection errors

- ✅ PostgreSQL database is running and accessible
- ✅ Database credentials in `.env` are correct
- ✅ Database table `audittrail_firehose` exists (or update `TABLE_NAME` in `.env`)
- ✅ Network/firewall allows connection to database
- ✅ For AWS RDS: Security group allows your IP address

### No data showing

- ✅ Database table exists and has data
- ✅ Table name in `.env` matches your database table
- ✅ Check database connection: http://localhost:8000/api/data/count

### Frontend not connecting

- ✅ Backend running on http://localhost:8000
- ✅ Check browser console for CORS errors
- ✅ Verify `API_BASE_URL` in frontend code points to `http://localhost:8000`
- ✅ Check that backend CORS allows your frontend origin

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
# PostgreSQL Database Configuration
DB_HOST=your-database-host.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
TABLE_NAME=audittrail_firehose

# Optional: Logging
LOG_LEVEL=INFO
```

**⚠️ Important:** Never commit `.env` file to Git. It contains sensitive credentials.

---

## 📊 Database Setup

The application expects a PostgreSQL table named `audittrail_firehose` (or the name specified in `TABLE_NAME`).

If you need to create the table, use the SQL script in:
```
lambda/parquet_to_rds/create_rds_table.sql
```

---

## 🚀 Deployment

### Lambda Function (S3 to PostgreSQL)

The Lambda function processes Parquet files from S3 and saves them to PostgreSQL.

See `lambda/parquet_to_rds/` directory for:
- Lambda function code
- SAM template for deployment
- IAM policy requirements

---

## 📜 License

Open-source and free to use.

---

## 👤 Author

infofitsoftware

---

Happy coding 🚀
