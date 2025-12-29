# Dashboard - AWS Athena Data Pipeline

A modern dashboard application that queries Parquet files from AWS S3 using Athena and displays real-time analytics through a FastAPI backend and React frontend.

---

## ✨ Features

- 📊 **Real-time Dashboard Metrics** - Key numbers at a glance with trend indicators
- 📈 **Interactive Charts** - Line, Bar, Pie, and Area charts powered by Recharts
- 🔍 **Smart Filters** - Date range, Practitioner, Program, and Location filters
- ☁️ **AWS Athena Integration** - Direct querying of S3 Parquet files, no local database
- 📑 **Multiple Reports** - Audit Summary, Patient Access, Signed/Unsigned Notes, and more
- 📱 **Responsive UI** - Works smoothly on desktop and mobile

---

## 🧰 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **AWS Athena** - Query S3 Parquet files with SQL
- **Boto3** - AWS SDK for Python
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Recharts** - Chart library
- **Axios** - HTTP client

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
copy env.example .env  # Windows
cp env.example .env  # Linux/Mac
```

Edit `.env` with your AWS credentials (see `SETUP.md` for details).

### 3. Setup Frontend

```bash
cd frontend
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access Dashboard

Open browser: `http://localhost:5173`

---

## 📚 Documentation

- **SETUP.md** - Complete setup guide including:
  - AWS S3 configuration
  - AWS Athena setup
  - All SQL queries used in the application
  - API endpoints documentation
  - Troubleshooting guide

---

## 📊 Data Source

- ☁️ **S3 Parquet Files** - All data comes from S3
- 🔍 **Athena Queries** - Direct SQL queries on Parquet files
- 📈 **Real-time** - No database, direct from S3
- 🔄 **Auto-sync** - Always shows latest data from S3

Upload your Parquet files to S3 and they'll automatically appear in the dashboard!

---

## 🔌 API Overview

### Health Check
- `GET /` - API health check

### Dashboard Metrics
- `GET /api/metrics` - Dashboard metrics
- `GET /api/top-users` - Top users by session count
- `GET /api/active-users` - Active user statistics
- `GET /api/staff-speaking` - Staff speaking statistics
- `GET /api/times` - Time-related data
- `GET /api/consents` - Consent data

### Reports (All support filters)
- `GET /api/audit-summary`
- `GET /api/patient-access`
- `GET /api/signed-notes`
- `GET /api/unsigned-notes`
- `GET /api/practitioner-service-usage`
- `GET /api/sync-issues`

### Athena Endpoints
- `GET /api/athena/data` - Query Athena data with filters
- `GET /api/athena/summary` - Summary statistics
- `GET /api/athena/dashboard` - Optimized dashboard data
- `GET /api/athena/verify-files` - List Parquet files in S3
- `GET /api/athena/repair-table` - Refresh Athena metadata
- `POST /api/athena/query` - Execute custom queries

**Interactive API Docs:** `http://localhost:8000/docs`

---

## 🏗️ Project Structure

```
Dashboard/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI application
│   ├── athena_service.py # Athena query service
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # React components
│       └── App.jsx      # Main app
├── athena/              # SQL queries
│   ├── create_table_ACTUAL.sql
│   ├── create_view.sql
│   └── ...
├── README.md            # This file
└── SETUP.md             # Complete setup guide
```

---

## 🐞 Common Issues

### Backend not starting?
- Check Python version (need 3.8+)
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Configure `.env` file with AWS credentials

### No data showing?
- Verify AWS credentials in `.env` file
- Check Athena table exists and has data
- Run `MSCK REPAIR TABLE audit_trail_data;` in Athena
- Verify S3 bucket permissions

### Frontend not connecting?
- Ensure backend is running on `localhost:8000`
- Check browser console for errors

See `SETUP.md` for detailed troubleshooting.

---

## 📜 License

Open-source and free to use.

---

## 👤 Author

**infofitsoftware**

---

Happy coding! 🚀
