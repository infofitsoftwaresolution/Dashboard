# 📊 AWS Athena Analytics Dashboard

A modern, high-performance analytics dashboard that directly queries Parquet data stored in AWS S3 using Athena, processes it through a FastAPI backend, and presents real-time insights via a React-based dashboard.

No traditional database. No sync delays. Just fresh data straight from S3.

---

## ✨ Features

- 📊 Real-time dashboard metrics with trend indicators  
- 📈 Interactive charts (Line, Bar, Pie, Area) using Recharts  
- 🔍 Advanced filters: Date range, Practitioner, Program, Location  
- ☁️ Direct AWS Athena queries on S3 Parquet files  
- 📑 Multiple reports: Audit Summary, Patient Access, Signed / Unsigned Notes  
- 📱 Fully responsive UI (desktop & mobile)

---

## 🧰 Tech Stack

### Backend
- FastAPI  
- AWS Athena  
- Boto3  
- Pydantic  
- Uvicorn  

### Frontend
- React 18  
- Vite  
- Recharts  
- Axios  

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
````

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
```

For Linux / Mac:

```bash
source venv/bin/activate
cp env.example .env
```

Update `.env` with your AWS credentials (see SETUP.md).

---

### 3. Frontend Setup

```bash
cd frontend
npm install
```

---

### 4. Run the Application

Backend:

```bash
cd backend
python main.py
```

Frontend:

```bash
cd frontend
npm run dev
```

---

### 5. Open Dashboard

```text
http://localhost:5173
```

---

## 📚 Documentation

SETUP.md includes:

* AWS S3 configuration
* Athena setup
* SQL queries used
* API documentation
* Troubleshooting guide

---

## 📊 Data Source & Flow

* Source: S3 Parquet files
* Query Engine: AWS Athena
* Database: None
* Sync: Real-time, always latest data

Upload Parquet files to S3 and they appear automatically in the dashboard.

---

## 🔌 API Overview

### Health

* GET /

### Dashboard Metrics

* GET /api/metrics
* GET /api/top-users
* GET /api/active-users
* GET /api/staff-speaking
* GET /api/times
* GET /api/consents

### Reports (Filter Supported)

* GET /api/audit-summary
* GET /api/patient-access
* GET /api/signed-notes
* GET /api/unsigned-notes
* GET /api/practitioner-service-usage
* GET /api/sync-issues

### Athena APIs

* GET /api/athena/data
* GET /api/athena/summary
* GET /api/athena/dashboard
* GET /api/athena/verify-files
* GET /api/athena/repair-table
* POST /api/athena/query

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## 🏗️ Project Structure

```
Dashboard/
├── backend/
│   ├── api/                        # All API code organized here
│   │   ├── models.py               # Pydantic models
│   │   └── routes/
│   │       ├── dashboard.py         # Dashboard endpoints
│   │       └── athena.py           # Athena endpoints
│   ├── main.py                     # FastAPI app entry point
│   ├── athena_service.py           # Athena service layer
│   ├── requirements.txt
│   └── env.example
├── frontend/
│   └── src/
│       ├── components/
│       └── App.jsx
├── athena/
│   ├── create_table_ACTUAL.sql
│   ├── create_view.sql
│   └── ...
├── README.md
└── SETUP.md
```

---

## 🐞 Common Issues

### Backend not starting

* Python 3.8+
* Virtual environment activated
* Dependencies installed
* `.env` configured correctly

### No data showing

* AWS credentials are valid
* Athena table exists
* Run:

```sql
MSCK REPAIR TABLE audit_trail_data;
```

* Check S3 permissions

### Frontend not connecting

* Backend running on localhost:8000
* Check browser console

---

## 📜 License

Open-source and free to use.

---

## 👤 Author

infofitsoftware

---

Happy coding 🚀
